# api/views.py
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pricing import calculate_pages, calculate_price
from rest_framework import viewsets, parsers # 导入parsers
from .models import Order, PrintFile # 确保PrintFile已导入
from .serializers import OrderSerializer, PrintFileUploadSerializer # 导入新的Serializer
from django_filters.rest_framework import DjangoFilterBackend # 导入DjangoFilterBackend


# OrderViewSet 定义了一套完整的、针对Order模型的增删改查(CRUD)操作
class OrderViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑订单的ViewSet。
    """
    # queryset 定义了这个视图集要操作的数据范围，这里是所有的Order对象
    queryset = Order.objects.all().order_by('-created_at') # 默认按创建时间倒序排列
    
    # serializer_class 指定了这个视图集在进行数据转换时应该使用的“翻译官”
    serializer_class = OrderSerializer
    # --- 添加以下开启过滤 ---
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_number', 'phone_number']

class PrintFileViewSet(viewsets.ModelViewSet):
    """
    一个用于上传和管理文件的ViewSet。
    """
    queryset = PrintFile.objects.all()
    serializer_class = PrintFileUploadSerializer
    # 指定这个ViewSet使用文件解析器，以支持multipart/form-data类型的请求
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

# 创建一个新的视图来处理报价请求
class PriceQuoteView(APIView):
    """
    接收文件和规格，返回预估价格的API视图。
    """
    # 确保视图能处理文件上传
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        specs_str = request.data.get('specifications', '{}')

        if not file_obj:
            return Response({'error': '必须提供一个文件。'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            specifications = json.loads(specs_str)
        except json.JSONDecodeError:
            return Response({'error': '规格参数必须是合法的JSON字符串。'}, status=status.HTTP_400_BAD_REQUEST)

        # 调用我们的计价逻辑
        pages = calculate_pages(file_obj)
        price = calculate_price(specifications, pages)

        # 返回结果
        return Response({
            'estimated_pages': pages,
            'estimated_price': price
        }, status=status.HTTP_200_OK)