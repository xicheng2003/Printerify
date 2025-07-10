# 文件路径: api/views.py

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, parsers
from .models import Order, PrintFile
from .serializers import OrderSerializer, PrintFileUploadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pricing import calculate_pages, get_price
from .pdf_generator import generate_order_pdf # 引入PDF生成器

class OrderViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑订单的ViewSet。
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_number', 'phone_number', 'pickup_code']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 首先，正常创建订单实例
        order = serializer.save()

        # 然后，为这个新订单生成并保存PDF
        try:
            pdf_file = generate_order_pdf(order)
            order.order_summary_pdf.save(pdf_file.name, pdf_file, save=True)
        except Exception as e:
            # 即使PDF生成失败，也不应该让整个下单流程失败
            # 这里可以替换为更完善的日志记录
            print(f"!!! PDF生成失败，订单ID: {order.order_number}, 错误: {e}")

        # 使用序列化器生成最终的响应数据
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PrintFileViewSet(viewsets.ModelViewSet):
    """
    一个用于上传和管理文件的ViewSet。
    """
    queryset = PrintFile.objects.all()
    serializer_class = PrintFileUploadSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

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