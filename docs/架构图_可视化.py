import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_architecture_diagram():
    """创建AI Hedge Fund Crypto架构图"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 定义颜色
    colors = {
        'user': '#E3F2FD',
        'app': '#F3E5F5', 
        'workflow': '#E8F5E8',
        'strategy': '#FFF3E0',
        'data': '#F1F8E9',
        'ai': '#FCE4EC',
        'risk': '#FFEBEE',
        'output': '#E0F2F1'
    }
    
    # 用户层
    user_box = FancyBboxPatch((0.5, 8.5), 9, 1, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['user'], 
                             edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(5, 9, '用户层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(2, 8.7, 'config.yaml\n配置文件', ha='center', va='center', fontsize=10)
    ax.text(5, 8.7, '.env\n环境变量', ha='center', va='center', fontsize=10)
    ax.text(8, 8.7, '主程序入口', ha='center', va='center', fontsize=10)
    
    # 应用层
    app_box = FancyBboxPatch((0.5, 7.2), 9, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['app'], 
                            edgecolor='black', linewidth=2)
    ax.add_patch(app_box)
    ax.text(5, 7.7, '应用层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(2.5, 7.4, 'backtest.py\n回测入口', ha='center', va='center', fontsize=10)
    ax.text(5, 7.4, 'main.py\n实时交易', ha='center', va='center', fontsize=10)
    ax.text(7.5, 7.4, 'Agent\n代理系统', ha='center', va='center', fontsize=10)
    
    # 工作流引擎层
    workflow_box = FancyBboxPatch((0.5, 5.5), 9, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['workflow'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(workflow_box)
    ax.text(5, 6.7, '工作流引擎层 (LangGraph)', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # 工作流节点
    nodes = ['StartNode\n起始节点', 'DataNode\n数据节点群', 'StrategyNode\n策略节点群', 
             'RiskNode\n风险管理', 'PortfolioNode\n投资组合管理']
    for i, node in enumerate(nodes):
        x = 1.5 + i * 1.6
        node_patch = FancyBboxPatch((x-0.4, 5.8), 0.8, 0.6, 
                                   boxstyle="round,pad=0.05", 
                                   facecolor='white', 
                                   edgecolor='gray')
        ax.add_patch(node_patch)
        ax.text(x, 6.1, node, ha='center', va='center', fontsize=8)
        
        # 添加箭头
        if i < len(nodes) - 1:
            arrow = patches.FancyArrowPatch((x+0.4, 6.1), (x+1.2, 6.1),
                                          arrowstyle='->', mutation_scale=15,
                                          color='gray')
            ax.add_patch(arrow)
    
    # 策略层
    strategy_box = FancyBboxPatch((0.5, 4), 4, 1.2, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['strategy'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(strategy_box)
    ax.text(2.5, 4.9, '策略层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(1.5, 4.4, 'MACD策略', ha='center', va='center', fontsize=10)
    ax.text(2.5, 4.4, 'RSI策略', ha='center', va='center', fontsize=10)
    ax.text(3.5, 4.4, '自定义策略', ha='center', va='center', fontsize=10)
    ax.text(2.5, 4.1, '技术指标库', ha='center', va='center', fontsize=10)
    
    # 数据层
    data_box = FancyBboxPatch((5.5, 4), 4, 1.2, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['data'], 
                             edgecolor='black', linewidth=2)
    ax.add_patch(data_box)
    ax.text(7.5, 4.9, '数据层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(6.5, 4.4, 'Binance API', ha='center', va='center', fontsize=10)
    ax.text(7.5, 4.4, '数据缓存', ha='center', va='center', fontsize=10)
    ax.text(8.5, 4.4, '多时间框架', ha='center', va='center', fontsize=10)
    
    # AI决策层
    ai_box = FancyBboxPatch((0.5, 2.5), 4.5, 1.2, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['ai'], 
                           edgecolor='black', linewidth=2)
    ax.add_patch(ai_box)
    ax.text(2.75, 3.4, 'AI决策层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(1.5, 2.9, 'OpenAI\nGPT-4', ha='center', va='center', fontsize=9)
    ax.text(2.5, 2.9, 'Anthropic\nClaude', ha='center', va='center', fontsize=9)
    ax.text(3.5, 2.9, 'Google\nGemini', ha='center', va='center', fontsize=9)
    ax.text(4.5, 2.9, '其他LLM\n提供商', ha='center', va='center', fontsize=9)
    
    # 风险管理层
    risk_box = FancyBboxPatch((5.5, 2.5), 4, 1.2, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['risk'], 
                             edgecolor='black', linewidth=2)
    ax.add_patch(risk_box)
    ax.text(7.5, 3.4, '风险管理层', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(6.5, 2.9, '仓位管理', ha='center', va='center', fontsize=10)
    ax.text(7.5, 2.9, '保证金控制', ha='center', va='center', fontsize=10)
    ax.text(8.5, 2.9, '风险评估', ha='center', va='center', fontsize=10)
    
    # 输出层
    output_box = FancyBboxPatch((0.5, 0.5), 9, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['output'], 
                               edgecolor='black', linewidth=2)
    ax.add_patch(output_box)
    ax.text(5, 1.7, '输出层', ha='center', va='center', fontsize=14, fontweight='bold')
    
    outputs = ['交易信号', '性能报告', '可视化图表', '决策推理']
    for i, output in enumerate(outputs):
        x = 1.5 + i * 2
        ax.text(x, 1.2, output, ha='center', va='center', fontsize=11, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # 添加连接箭头
    # 用户层到应用层
    arrow1 = patches.FancyArrowPatch((5, 8.5), (5, 8.2),
                                    arrowstyle='->', mutation_scale=20,
                                    color='blue', linewidth=2)
    ax.add_patch(arrow1)
    
    # 应用层到工作流层
    arrow2 = patches.FancyArrowPatch((5, 7.2), (5, 7),
                                    arrowstyle='->', mutation_scale=20,
                                    color='blue', linewidth=2)
    ax.add_patch(arrow2)
    
    # 工作流层到策略/数据层
    arrow3 = patches.FancyArrowPatch((3, 5.5), (2.5, 5.2),
                                    arrowstyle='->', mutation_scale=20,
                                    color='green', linewidth=2)
    ax.add_patch(arrow3)
    
    arrow4 = patches.FancyArrowPatch((7, 5.5), (7.5, 5.2),
                                    arrowstyle='->', mutation_scale=20,
                                    color='green', linewidth=2)
    ax.add_patch(arrow4)
    
    # 策略/数据层到AI/风险层
    arrow5 = patches.FancyArrowPatch((2.5, 4), (2.75, 3.7),
                                    arrowstyle='->', mutation_scale=20,
                                    color='purple', linewidth=2)
    ax.add_patch(arrow5)
    
    arrow6 = patches.FancyArrowPatch((7.5, 4), (7.5, 3.7),
                                    arrowstyle='->', mutation_scale=20,
                                    color='purple', linewidth=2)
    ax.add_patch(arrow6)
    
    # AI/风险层到输出层
    arrow7 = patches.FancyArrowPatch((5, 2.5), (5, 2),
                                    arrowstyle='->', mutation_scale=20,
                                    color='red', linewidth=2)
    ax.add_patch(arrow7)
    
    plt.title('AI Hedge Fund Crypto 系统架构图', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('AI_Hedge_Fund_Crypto_架构图.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_workflow_diagram():
    """创建工作流程图"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 定义节点位置和信息
    nodes = [
        {'name': 'StartNode\n起始节点', 'pos': (2, 9), 'color': '#E3F2FD'},
        {'name': 'DataNode_30m\n30分钟数据', 'pos': (1, 7.5), 'color': '#F1F8E9'},
        {'name': 'DataNode_1h\n1小时数据', 'pos': (2, 7.5), 'color': '#F1F8E9'},
        {'name': 'DataNode_4h\n4小时数据', 'pos': (3, 7.5), 'color': '#F1F8E9'},
        {'name': 'MergeNode\n数据合并', 'pos': (2, 6), 'color': '#FFF3E0'},
        {'name': 'MacdStrategy\nMACD策略', 'pos': (1, 4.5), 'color': '#FCE4EC'},
        {'name': 'RSIStrategy\nRSI策略', 'pos': (3, 4.5), 'color': '#FCE4EC'},
        {'name': 'RiskManagement\n风险管理', 'pos': (2, 3), 'color': '#FFEBEE'},
        {'name': 'PortfolioManagement\n投资组合管理', 'pos': (2, 1.5), 'color': '#E0F2F1'},
    ]
    
    # 绘制节点
    for node in nodes:
        circle = plt.Circle(node['pos'], 0.4, facecolor=node['color'], 
                           edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(node['pos'][0], node['pos'][1], node['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # 定义连接关系
    connections = [
        ((2, 9), (1, 7.5)),    # Start -> DataNode_30m
        ((2, 9), (2, 7.5)),    # Start -> DataNode_1h
        ((2, 9), (3, 7.5)),    # Start -> DataNode_4h
        ((1, 7.5), (2, 6)),    # DataNode_30m -> Merge
        ((2, 7.5), (2, 6)),    # DataNode_1h -> Merge
        ((3, 7.5), (2, 6)),    # DataNode_4h -> Merge
        ((2, 6), (1, 4.5)),    # Merge -> MacdStrategy
        ((2, 6), (3, 4.5)),    # Merge -> RSIStrategy
        ((1, 4.5), (2, 3)),    # MacdStrategy -> Risk
        ((3, 4.5), (2, 3)),    # RSIStrategy -> Risk
        ((2, 3), (2, 1.5)),    # Risk -> Portfolio
    ]
    
    # 绘制连接线
    for start, end in connections:
        arrow = patches.FancyArrowPatch(start, end,
                                      arrowstyle='->', mutation_scale=15,
                                      color='blue', linewidth=2)
        ax.add_patch(arrow)
    
    # 添加时间轴
    ax.text(5, 9, '数据获取阶段', ha='left', va='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    ax.text(5, 7.5, '多时间框架\n并行处理', ha='left', va='center', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    ax.text(5, 6, '数据合并', ha='left', va='center', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.7))
    ax.text(5, 4.5, '策略分析阶段', ha='left', va='center', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightpink', alpha=0.7))
    ax.text(5, 3, '风险评估', ha='left', va='center', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
    ax.text(5, 1.5, 'AI决策输出', ha='left', va='center', fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightseagreen', alpha=0.7))
    
    plt.title('AI Hedge Fund Crypto 工作流程图', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('AI_Hedge_Fund_Crypto_工作流程图.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_data_flow_diagram():
    """创建数据流图"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 数据源
    sources = [
        {'name': 'Binance\nWebSocket', 'pos': (1, 7), 'color': '#E3F2FD'},
        {'name': 'Binance\nREST API', 'pos': (1, 5.5), 'color': '#E3F2FD'},
    ]
    
    # 处理阶段
    processes = [
        {'name': '实时数据流', 'pos': (3, 7), 'color': '#F1F8E9'},
        {'name': '历史数据', 'pos': (3, 5.5), 'color': '#F1F8E9'},
        {'name': '数据标准化', 'pos': (5, 6.25), 'color': '#FFF3E0'},
        {'name': '多时间框架\n处理', 'pos': (7, 6.25), 'color': '#FCE4EC'},
        {'name': '技术指标\n计算', 'pos': (5, 4), 'color': '#FFEBEE'},
        {'name': '信号生成', 'pos': (7, 4), 'color': '#E0F2F1'},
        {'name': '最终决策', 'pos': (9, 4), 'color': '#F3E5F5'},
    ]
    
    all_nodes = sources + processes
    
    # 绘制所有节点
    for node in all_nodes:
        if 'WebSocket' in node['name'] or 'REST' in node['name']:
            # 数据源用矩形
            rect = FancyBboxPatch((node['pos'][0]-0.5, node['pos'][1]-0.4), 1, 0.8,
                                 boxstyle="round,pad=0.1", 
                                 facecolor=node['color'], 
                                 edgecolor='black', linewidth=2)
            ax.add_patch(rect)
        else:
            # 处理节点用椭圆
            ellipse = patches.Ellipse(node['pos'], 1.2, 0.8, 
                                    facecolor=node['color'], 
                                    edgecolor='black', linewidth=2)
            ax.add_patch(ellipse)
        
        ax.text(node['pos'][0], node['pos'][1], node['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # 数据流连接
    flows = [
        ((1, 7), (3, 7)),        # WebSocket -> 实时数据
        ((1, 5.5), (3, 5.5)),    # REST -> 历史数据
        ((3, 7), (5, 6.25)),     # 实时数据 -> 标准化
        ((3, 5.5), (5, 6.25)),   # 历史数据 -> 标准化
        ((5, 6.25), (7, 6.25)),  # 标准化 -> 多时间框架
        ((7, 6.25), (5, 4)),     # 多时间框架 -> 技术指标
        ((5, 4), (7, 4)),        # 技术指标 -> 信号生成
        ((7, 4), (9, 4)),        # 信号生成 -> 最终决策
    ]
    
    for start, end in flows:
        arrow = patches.FancyArrowPatch(start, end,
                                      arrowstyle='->', mutation_scale=15,
                                      color='darkblue', linewidth=2)
        ax.add_patch(arrow)
    
    # 添加数据类型标签
    ax.text(2, 7.5, 'K线数据\n成交量\n价格变动', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    ax.text(4, 6.8, 'OHLCV\n标准格式', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    ax.text(6, 5.5, '30m, 1h, 4h\n多周期数据', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    ax.text(6, 3.2, 'MACD, RSI\nBB, SMA', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    ax.text(8, 3.2, 'Buy/Sell/Hold\n置信度', ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    plt.title('AI Hedge Fund Crypto 数据流程图', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('AI_Hedge_Fund_Crypto_数据流程图.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_usage_flow_diagram():
    """创建使用流程图"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 定义流程步骤
    steps = [
        {'name': '1. 环境准备\n安装Python 3.12+\n安装依赖包', 'pos': (2, 9), 'color': '#E3F2FD'},
        {'name': '2. 获取API密钥\nBinance API\nLLM API', 'pos': (6, 9), 'color': '#F3E5F5'},
        {'name': '3. 配置系统\n编辑config.yaml\n设置.env', 'pos': (10, 9), 'color': '#E8F5E8'},
        {'name': '4. 选择模式\n回测模式\n实时模式', 'pos': (2, 7), 'color': '#FFF3E0'},
        {'name': '5. 配置策略\n选择时间框架\n选择交易对', 'pos': (6, 7), 'color': '#F1F8E9'},
        {'name': '6. 运行系统\nbacktest.py\nmain.py', 'pos': (10, 7), 'color': '#FCE4EC'},
        {'name': '7. 分析结果\n性能指标\n可视化图表', 'pos': (2, 5), 'color': '#FFEBEE'},
        {'name': '8. 优化策略\n调整参数\n添加新策略', 'pos': (6, 5), 'color': '#E0F2F1'},
        {'name': '9. 部署监控\n实时交易\n风险控制', 'pos': (10, 5), 'color': '#FFF8E1'},
    ]
    
    # 绘制步骤节点
    for i, step in enumerate(steps):
        # 使用不同形状区分不同阶段
        if i < 3:  # 准备阶段 - 矩形
            rect = FancyBboxPatch((step['pos'][0]-0.8, step['pos'][1]-0.6), 1.6, 1.2,
                                 boxstyle="round,pad=0.1", 
                                 facecolor=step['color'], 
                                 edgecolor='black', linewidth=2)
            ax.add_patch(rect)
        elif i < 6:  # 配置阶段 - 六边形
            hexagon = patches.RegularPolygon(step['pos'], 6, radius=0.8,
                                           facecolor=step['color'], 
                                           edgecolor='black', linewidth=2)
            ax.add_patch(hexagon)
        else:  # 执行阶段 - 椭圆
            ellipse = patches.Ellipse(step['pos'], 1.6, 1.2, 
                                    facecolor=step['color'], 
                                    edgecolor='black', linewidth=2)
            ax.add_patch(ellipse)
        
        ax.text(step['pos'][0], step['pos'][1], step['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # 添加流程箭头
    arrows = [
        ((2, 9), (6, 9)),    # 1 -> 2
        ((6, 9), (10, 9)),   # 2 -> 3
        ((10, 9), (2, 7)),   # 3 -> 4 (换行)
        ((2, 7), (6, 7)),    # 4 -> 5
        ((6, 7), (10, 7)),   # 5 -> 6
        ((10, 7), (2, 5)),   # 6 -> 7 (换行)
        ((2, 5), (6, 5)),    # 7 -> 8
        ((6, 5), (10, 5)),   # 8 -> 9
    ]
    
    for start, end in arrows:
        if start[1] != end[1]:  # 换行箭头
            # 创建弯曲箭头
            mid_x = (start[0] + end[0]) / 2
            mid_y = start[1] - 1
            arrow = patches.FancyArrowPatch(start, end,
                                          connectionstyle="arc3,rad=0.3",
                                          arrowstyle='->', mutation_scale=20,
                                          color='red', linewidth=3)
        else:  # 直线箭头
            arrow = patches.FancyArrowPatch(start, end,
                                          arrowstyle='->', mutation_scale=20,
                                          color='blue', linewidth=2)
        ax.add_patch(arrow)
    
    # 添加阶段标签
    ax.text(6, 9.8, '准备阶段', ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    ax.text(6, 7.8, '配置阶段', ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    ax.text(6, 5.8, '执行阶段', ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
    
    # 添加决策分支
    ax.text(2, 6, '回测验证', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.8))
    ax.text(10, 6, '实时交易', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='orange', alpha=0.8))
    
    # 添加反馈循环
    feedback_arrow = patches.FancyArrowPatch((6, 4.5), (6, 6.5),
                                           connectionstyle="arc3,rad=0.5",
                                           arrowstyle='->', mutation_scale=15,
                                           color='green', linewidth=2, linestyle='--')
    ax.add_patch(feedback_arrow)
    ax.text(7.5, 5.5, '策略优化\n反馈循环', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen', alpha=0.8))
    
    plt.title('AI Hedge Fund Crypto 使用流程图', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('AI_Hedge_Fund_Crypto_使用流程图.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("正在生成AI Hedge Fund Crypto架构图...")
    
    # 生成所有图表
    create_architecture_diagram()
    print("✓ 系统架构图已生成")
    
    create_workflow_diagram()
    print("✓ 工作流程图已生成")
    
    create_data_flow_diagram()
    print("✓ 数据流程图已生成")
    
    create_usage_flow_diagram()
    print("✓ 使用流程图已生成")
    
    print("\n所有架构图已生成完成！")
    print("生成的文件：")
    print("- AI_Hedge_Fund_Crypto_架构图.png")
    print("- AI_Hedge_Fund_Crypto_工作流程图.png") 
    print("- AI_Hedge_Fund_Crypto_数据流程图.png")
    print("- AI_Hedge_Fund_Crypto_使用流程图.png")
