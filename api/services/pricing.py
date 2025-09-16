# printerify/api/services/pricing.py

import fitz  # PyMuPDF, 用于读取PDF
import docx  # python-docx, 用于读取DOCX
from decimal import Decimal # 使用 Decimal 来精确计算货币

# --- 价格配置 (已重构) ---
# 价格结构现在以“纸张尺寸”作为顶层key，更具扩展性
PRICE_CONFIG = {
    'base_service_fee': Decimal('0.50'),
    'print': {
        'a4_70g': {
            'black_white': {
                'single': Decimal('0.15'),
                'double': Decimal('0.15'),
                'single_double': None, # 沿用单/双面价格逻辑
            },
            'color': {
                'single': Decimal('0.50'),
                'double': Decimal('0.80'),
                'single_double': None, # 封面单面+内容双面
            }
        },
        'a4_80g': {
            'black_white': {
                'single': Decimal('0.15'),
                'double': Decimal('0.15'),
                'single_double': None,
            },
            'color': {
                'single': Decimal('0.50'),
                'double': Decimal('0.80'),
                'single_double': None,
            }
        },
        'b5_70g': {
            'black_white': {
                'single': Decimal('0.12'), # B5 价格稍低
                'double': Decimal('0.12'),
                'single_double': None,
            },
            'color': {
                'single': Decimal('0.40'),
                'double': Decimal('0.70'),
                'single_double': None,
            }
        }
        # 您未来可以在此添加 'a3': { ... } 等更多规格
    },
    'binding': {
        'none': Decimal('0.00'),
        'staple_top_left': Decimal('0.10'),
        'staple_left_side': Decimal('0.10'),
        'staple': Decimal('2.00'),
        'ring_bound': Decimal('5.00'),
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

# --- ▼▼▼ calculate_document_price 函数已重构 ▼▼▼ ---
def calculate_document_price(file_path, paper_size, color_mode, print_sided, copies):
    """
    计算【单个文件】的打印费用 (已更新以支持纸张尺寸和新的单双面选项)。
    返回: (页数, 打印费用) 的元组
    """
    page_count = _calculate_pages(file_path)
    if page_count == 0:
        return 0, Decimal('0.00')

    total_print_cost = Decimal('0.00')

    try:
        # 1. 根据纸张尺寸和颜色获取价格表
        price_map = PRICE_CONFIG['print'][paper_size][color_mode]
    except KeyError:
        # 如果配置不存在 (例如一个无效的 paper_size)，返回0价
        return page_count, Decimal('0.0')

    # 2. 根据打印方式计算价格
    if print_sided == 'single_double':
        # “封面单面”的特殊逻辑
        if page_count == 1:
            # 只有一页时，按单面计算
            total_print_cost = price_map['single']
        else:
            # 封面按“单面”价，其余 (page_count - 1) 页按“双面”价
            cover_cost = price_map['single']
            content_cost = (page_count - 1) * price_map['double']
            total_print_cost = cover_cost + content_cost
    else:
        # 标准的单面或双面逻辑
        price_per_page = price_map.get(print_sided, Decimal('0.00'))
        total_print_cost = price_per_page * page_count

    # 3. 乘以份数得到最终价格
    final_cost = total_print_cost * copies
    
    return page_count, final_cost
# --- ▲▲▲ 函数重构结束 ▲▲▲ ---

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