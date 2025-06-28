# api/pricing.py

import io
from PyPDF2 import PdfReader
from docx import Document

def calculate_pages(file_object):
    """
    根据文件对象估算页数。
    支持 PDF 和 DOCX 格式。
    """
    try:
        # 确保文件读取指针在开头
        file_object.seek(0)
        file_name = file_object.name.lower()

        if file_name.endswith('.pdf'):
            reader = PdfReader(file_object)
            return len(reader.pages)

        elif file_name.endswith('.docx'):
            # 对于docx，页数是估算的。这里的逻辑是基于段落和图片数量。
            # 您可以根据需要调整这个估算逻辑。
            document = Document(io.BytesIO(file_object.read()))
            paragraphs = len(document.paragraphs)
            images = len(document.inline_shapes)
            # 一个简化的估算：每30个段落或5个图片大约算一页
            page_estimate = max(1, (paragraphs // 30) + (images // 5))
            return page_estimate

        else:
            # 对于不支持的或未知的格式，暂时按1页计算
            return 1
    except Exception as e:
        print(f"Error calculating pages for {file_object.name}: {e}")
        return 1 # 如果处理出错，也按1页计算
    finally:
        # 再次将指针移到开头，以便文件可以被再次读取
        file_object.seek(0)


def calculate_price(specifications, pages):
    """
    根据打印规格和页数计算总价。
    """
    # 定义一个简单的价格规则字典
    price_rules = {
        'A4_黑白': 0.10,
        'A4_彩色': 0.50,
        'A3_黑白': 0.20,
        'A3_彩色': 1.00,
    }

    # 从规格中获取参数
    copies = int(specifications.get('copies', 1))
    paper_size = specifications.get('paper_size', 'A4')
    color = specifications.get('color', '黑白')

    # 构建查询键并获取单价
    rule_key = f"{paper_size}_{color}"
    price_per_page = price_rules.get(rule_key, 0.10) # 如果没有匹配的规则，使用默认价

    # 计算总价并四舍五入到两位小数
    total_price = float(price_per_page) * pages * copies
    return round(total_price, 2)