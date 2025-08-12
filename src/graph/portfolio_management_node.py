import os
from typing import Dict, Any, List, Optional
import json
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from .base_node import BaseNode, AgentState
from graph import show_agent_reasoning
from llm import get_llm, json_parser, cached_llm_invoke

# 添加决策缓存机制
_previous_signals = {}
_previous_decisions = {}

def signals_changed_significantly(current_signals: Dict, previous_signals: Dict, threshold: float = 0.1) -> bool:
    """检查信号是否发生显著变化"""
    if not previous_signals:
        return True
    
    for ticker in current_signals:
        if ticker not in previous_signals:
            return True
        
        current_ticker_signals = current_signals[ticker]
        previous_ticker_signals = previous_signals[ticker]
        
        for agent in current_ticker_signals:
            if agent not in previous_ticker_signals:
                return True
            
            for interval in current_ticker_signals[agent]:
                if interval not in previous_ticker_signals[agent]:
                    return True
                
                current_confidence = current_ticker_signals[agent][interval].get("confidence", 0)
                previous_confidence = previous_ticker_signals[agent][interval].get("confidence", 0)
                
                # 如果置信度变化超过阈值，认为信号发生显著变化
                if abs(current_confidence - previous_confidence) > threshold * 100:
                    return True
                
                current_signal = current_ticker_signals[agent][interval].get("signal", "neutral")
                previous_signal = previous_ticker_signals[agent][interval].get("signal", "neutral")
                
                # 如果信号方向发生变化
                if current_signal != previous_signal:
                    return True
    
    return False


class PortfolioManagementNode(BaseNode):
    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """Makes final trading decisions and generates orders for multiple tickers"""

        data = state.get('data', {})
        data['name'] = "PortfolioManagementNode"
        # Get the portfolio and analyst signals
        portfolio = data.get("portfolio", {})
        analyst_signals = data.get("analyst_signals", {})
        tickers = data.get("tickers", [])

        # Get position limits, current prices, and signals for every ticker
        position_limits = {}
        current_prices = {}
        max_shares = {}
        signals_by_ticker = {}
        for ticker in tickers:

            # Get position limits and current prices for the ticker
            risk_data = analyst_signals.get("risk_management_agent", {}).get(ticker, {})
            position_limits[ticker] = risk_data.get("remaining_position_limit", 0.0)
            current_prices[ticker] = risk_data.get("current_price", 0.0)

            # Calculate maximum shares allowed based on position limit and price
            if current_prices[ticker] > 0.0:
                max_shares[ticker] = float(position_limits[ticker] / current_prices[ticker])
            else:
                max_shares[ticker] = 0.0

            # Get signals for the ticker
            ticker_signals = {}
            for agent, signals in analyst_signals.items():
                if agent == "technical_analyst_agent" and ticker in signals:
                    ticker_signals[agent] = signals[ticker]

            signals_by_ticker[ticker] = ticker_signals

        # 智能决策：检查信号是否发生显著变化
        global _previous_signals, _previous_decisions
        
        # 如果信号没有显著变化且有之前的决策，复用之前的决策
        if not signals_changed_significantly(signals_by_ticker, _previous_signals) and _previous_decisions:
            print("📊 Signals unchanged, reusing previous decisions")
            result = {"decisions": _previous_decisions}
        else:
            # Generate the trading decision
            result = generate_trading_decision(
                tickers=tickers,
                signals_by_ticker=signals_by_ticker,
                current_prices=current_prices,
                max_shares=max_shares,
                portfolio=portfolio,
                model_name=state["metadata"]["model_name"],
                model_provider=state["metadata"]["model_provider"],
                model_base_url=state["metadata"]["model_base_url"],
            )
            
            # 缓存当前的信号和决策
            _previous_signals = signals_by_ticker.copy()
            _previous_decisions = result.get("decisions", {}).copy()

        # Create the portfolio management message
        message = HumanMessage(
            content=json.dumps(result.get("decisions", {})),
            name="portfolio_management",
        )

        # Print the decision if the flag is set
        if state["metadata"]["show_reasoning"]:
            show_agent_reasoning(result.get("decisions"),
                                 "Portfolio Management Agent")

        return {
            "messages": [message],
            "data": state["data"],
        }

        # return state


def generate_trading_decision(
        tickers: List[str],
        signals_by_ticker: Dict[str, Dict[str, Any]],
        current_prices: Dict[str, float],
        max_shares: Dict[str, float],
        portfolio: Dict[str, float],
        model_name: str,
        model_provider: str,
        model_base_url: Optional[str] = None,
        max_retries: int = 3
):
    """Attempts to get a decision from the LLM with retry logic"""
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a portfolio manager making final trading decisions based on multiple tickers.
  
                Trading Rules:
                - For long positions:
                  * Only buy if you have available cash
                  * Only sell if you currently hold long shares of that ticker
                  * Sell quantity must be ≤ current long position shares
                  * Buy quantity must be ≤ max_shares for that ticker
  
                - For short positions:
                  * Only short if you have available margin (position value × margin requirement)
                  * Only cover if you currently have short shares of that ticker
                  * Cover quantity must be ≤ current short position shares
                  * Short quantity must respect margin requirements
  
                - The max_shares values are pre-calculated to respect position limits
                - Consider both long and short opportunities based on signals
                - Maintain appropriate risk management with both long and short exposure
  
                Available Actions:
                - "buy": Open or add to long position
                - "sell": Close or reduce long position
                - "short": Open or add to short position
                - "cover": Close or reduce short position
                - "hold": No action
  
                Inputs:
                - signals_by_ticker: dictionary of ticker → signals
                - max_shares: maximum shares allowed per ticker
                - portfolio_cash: current cash in portfolio
                - portfolio_positions: current positions (both long and short)
                - current_prices: current prices for each ticker
                - margin_requirement: current margin requirement for short positions (e.g., 0.5 means 50%)
                - total_margin_used: total margin currently in use
                """,
            ),
            (
                "human",
                """Based on the team's analysis, make your trading decisions for each ticker.
  
                Here are the signals by ticker:
                {signals_by_ticker}
  
                Current Prices:
                {current_prices}
  
                Maximum Shares Allowed For Purchases:
                {max_shares}
  
                Portfolio Cash: {portfolio_cash}
                Current Positions: {portfolio_positions}
                Current Margin Requirement: {margin_requirement}
                Total Margin Used: {total_margin_used}
  
                Output strictly in JSON with the following structure:
                {{
                  "decisions": {{
                    "TICKER1": {{
                      "action": "buy/sell/short/cover/hold",
                      "quantity": float,
                      "confidence": float between 0 and 100,
                      "reasoning": "string"
                    }},
                    "TICKER2": {{
                      ...
                    }},
                    ...
                  }}
                }}
                """,
            ),
        ]
    )

    llm = get_llm(provider=model_provider, model=model_name, base_url=model_base_url)

    chain = prompt | llm | json_parser
    
    # 使用缓存的LLM调用
    input_data = {
        "signals_by_ticker": json.dumps(signals_by_ticker, indent=2),
        "current_prices": json.dumps(current_prices, indent=2),
        "max_shares": json.dumps(max_shares, indent=2),
        "portfolio_cash": f"{portfolio.get('cash', 0.0):.2f}",
        "portfolio_positions": json.dumps(portfolio.get('positions', {}), indent=2),
        "margin_requirement": f"{portfolio.get('margin_requirement', 0.0):.2f}",
        "total_margin_used": f"{portfolio.get('margin_used', 0.0):.2f}",
    }
    
    # 带重试机制的LLM调用
    for attempt in range(max_retries):
        try:
            result = cached_llm_invoke(llm, chain, input_data)
            
            # 验证返回结果的格式
            if not isinstance(result, dict) or "decisions" not in result:
                raise ValueError("Invalid LLM response format")
            
            # 验证每个ticker都有决策
            decisions = result["decisions"]
            for ticker in tickers:
                if ticker not in decisions:
                    # 如果某个ticker缺少决策，添加默认的hold决策
                    decisions[ticker] = {
                        "action": "hold",
                        "quantity": 0.0,
                        "confidence": 50.0,
                        "reasoning": "Default hold due to missing LLM decision"
                    }
            
            # print("the return result :", result)
            return result
            
        except Exception as e:
            print(f"⚠️ LLM call attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                # 最后一次尝试失败，返回默认的hold决策
                print("🔄 Falling back to default hold decisions")
                default_decisions = {}
                for ticker in tickers:
                    default_decisions[ticker] = {
                        "action": "hold",
                        "quantity": 0.0,
                        "confidence": 50.0,
                        "reasoning": f"LLM failed after {max_retries} attempts, defaulting to hold"
                    }
                return {"decisions": default_decisions}
