# printerify/api/services/pricing.py

import fitz  # PyMuPDF, 用于读取PDF
import docx  # python-docx, 用于读取DOCX
from decimal import Decimal # 使用 Decimal 来精确计算货币

# --- 价格配置 ---
# 您可以在这里集中管理所有的价格，方便未来调整
# 这是延续您原有项目的计费标准
PRICE_CONFIG = {
    # 【新增】在这里定义基础服务费
    'base_service_fee': Decimal('0.50'),
    'print': {
        'black_white': {
            'single': Decimal('0.15'), # 黑白单面
            'double': Decimal('0.15'), # 黑白双面
        },
        'color': {
            'single': Decimal('0.50'), # 彩色单面
            'double': Decimal('0.80'), # 彩色双面
        }
    },
    'binding': {
        'none': Decimal('0.00'),      # 不装订
        'staple': Decimal('2.00'),    # 骑马钉
        'ring_bound': Decimal('5.00'),# 胶圈装
        # --- 【新增】在这里加上新的装订方式 ---
        'staple_top_left': Decimal('0.10'), # 订书钉（左上角）
        'staple_left_side': Decimal('0.10'),# 订书钉（左侧）
        # 您可以继续添加其他装订方式及其价格
    }
}

# --- 核心计费函数 ---

def _calculate_pages(file_path):
    """
    计算文件页数的核心逻辑。
    【已延续】此函数延续了您项目中对不同文件类型的处理方式。
    """
    try:
        if file_path.lower().endswith('.pdf'):
            with fitz.open(file_path) as doc:
                return doc.page_count
        elif file_path.lower().endswith('.docx'):
            doc = docx.Document(file_path)
            # 这是一个简化的估算逻辑，和您原来的一致
            # 您未来可以根据需要使其更精确
            num_pages = len(doc.sections)
            # 一个更简单的估算：直接基于段落和图片数量
            # paragraphs = len(doc.paragraphs)
            # images = len(doc.inline_shapes)
            # estimated_pages = (paragraphs // 10) + (images // 4) + 1
            return num_pages if num_pages > 0 else 1
        else:
            # 对于不支持的格式，暂时返回1页，避免程序崩溃
            return 1
    except Exception as e:
        print(f"Error calculating pages for {file_path}: {e}")
        # 如果计算出错，返回一个默认值，并打印错误
        return 1

def calculate_document_price(file_path, color_mode, print_sided, copies):
    """
    计算【单个文件】的打印费用。
    这是被 Serializer 调用的主要函数之一。
    返回: (页数, 打印费用) 的元组
    """
    page_count = _calculate_pages(file_path)
    
    # 从价格配置中获取单页价格
    try:
        price_per_page = PRICE_CONFIG['print'][color_mode][print_sided]
    except KeyError:
        # 如果配置不存在，给一个默认值或抛出错误
        price_per_page = Decimal('0.10')

    # 计算总打印费：单价 * 页数 * 份数
    total_print_cost = price_per_page * page_count * copies
    
    return page_count, total_print_cost

def calculate_binding_cost(binding_type, page_count):
    """
    计算【单个装订组】的装订费用。
    这是被 Serializer 调用的主要函数之二。
    """
    # 简单的实现：如果页数大于0且需要装订，则收取装订费
    if page_count > 0 and binding_type != 'none':
        try:
            return PRICE_CONFIG['binding'][binding_type]
        except KeyError:
            return Decimal('0.00') # 如果装订类型不存在，则不收费
    
    # 如果不满足装订条件，则装订费为0
    return Decimal('0.00')