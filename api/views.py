# 文件路径: api/views.py

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, parsers
from .models import Order, PrintFile
from .serializers import OrderSerializer, PrintFileUploadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pricing import calculate_pages, get_price
# --- 移除 PDF 生成器的导入 ---
# from .pdf_generator import generate_order_pdf
# +++ 导入新增的异步任务 +++
from .tasks import process_order_creation_tasks, calculate_file_pages_task

class OrderViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑订单的ViewSet。
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_number', 'phone_number', 'pickup_code']

    # +++ 修改 create 方法 +++
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save() # 调用 serializer.save()

        # --- 将耗时任务交给Celery ---
        process_order_creation_tasks.delay(order.id)

        headers = self.get_success_headers(serializer.data)
        # API会立即返回，用户无需等待
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PrintFileViewSet(viewsets.ModelViewSet):
    """
    一个用于上传和管理文件的ViewSet。
    """
    queryset = PrintFile.objects.all()
    serializer_class = PrintFileUploadSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    # +++ 新增 perform_create 方法以触发异步计算 +++
    def perform_create(self, serializer):
        print_file = serializer.save()
        # 如果上传的是打印文件，则触发异步页数计算
        if print_file.purpose == 'PRINT':
            calculate_file_pages_task.delay(print_file.id)

class PriceQuoteView(APIView):
    """实时报价接口"""
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

        pages = calculate_pages(file_obj)
        price = get_price(specifications, pages)

        return Response({
            'estimated_pages': pages,
            'estimated_price': price
        }, status=status.HTTP_200_OK)