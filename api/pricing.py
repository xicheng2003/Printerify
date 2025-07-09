from PyPDF2 import PdfReader
from docx import Document
import io

def calculate_pages(file_object):
    """根据文件对象估算页数，支持 PDF 和 DOCX。"""
    try:
        file_object.seek(0)
        file_name = file_object.name.lower()

        if file_name.endswith('.pdf'):
            reader = PdfReader(file_object)
            return len(reader.pages)
        elif file_name.endswith('.docx'):
            document = Document(io.BytesIO(file_object.read()))
            # 这是一个简化的估算逻辑，您可以根据需要调整
            paragraphs = len(document.paragraphs)
            images = len(document.inline_shapes)
            return max(1, (paragraphs // 10) + (images // 4))
        else:
            return 1
    except Exception as e:
        print(f"计价时计算页数出错: {e}")
        return 1
    finally:
        file_object.seek(0)

def get_price(specifications, total_pages):
    """
    唯一的计价中心：根据规格和页数计算总价。
    """
    # 1. 从规格中获取参数
    copies = int(specifications.get('copies', 1))
    sided_mode = specifications.get('sided', '单面')
    binding_method = specifications.get('binding_method', '无装订')
    
    # 2. 定义价格规则
    # 基础打印单价 (A4, 黑白, 单面)
    price_per_page = 0.15
    # 双面打印附加费
    if sided_mode in ['双面', '单双']:
        price_per_page = 0.15
    
    # 3. 计算基础打印费用
    printing_cost = price_per_page * total_pages

    # 4. 计算装订费用
    binding_cost = 0.0
    if binding_method == '订书钉装订':
        binding_cost = 0.1  # 每次装订固定收费1元

    # 5. 计算最终总价
    total_price = (printing_cost + binding_cost) * copies + 0.5 # 每个打印订单有0.5元的基础服务费用
    
    return round(total_price, 2)
