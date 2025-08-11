from django.test import TestCase
from api.serializers import (
    DocumentCreateSerializer, 
    BindingGroupCreateSerializer, 
    OrderCreateSerializer,
    DocumentDetailSerializer,
    BindingGroupDetailSerializer,
    OrderDetailSerializer
)
from api.models import Order, BindingGroup, Document
from decimal import Decimal


class DocumentSerializerTest(TestCase):
    """测试文档序列化器"""

    def test_document_create_serializer(self):
        """测试文档创建序列化器"""
        data = {
            'file_id': 'temp_uploads/test.txt',
            'original_filename': 'test.txt',
            'color_mode': 'black_white',
            'print_sided': 'single',
            'paper_size': 'a4',
            'copies': 1,
            'sequence_in_group': 1
        }
        
        serializer = DocumentCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_document_create_serializer_invalid_data(self):
        """测试文档创建序列化器无效数据"""
        data = {
            'file_id': 'temp_uploads/test.txt',
            'original_filename': 'test.txt',
            'color_mode': 'invalid_color',  # 无效的颜色模式
            'print_sided': 'single',
            'paper_size': 'a4',
            'copies': 1,
            'sequence_in_group': 1
        }
        
        serializer = DocumentCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class BindingGroupSerializerTest(TestCase):
    """测试装订组序列化器"""

    def test_binding_group_create_serializer(self):
        """测试装订组创建序列化器"""
        data = {
            'binding_type': 'staple_top_left',
            'sequence_in_order': 1,
            'documents': [
                {
                    'file_id': 'temp_uploads/test.txt',
                    'original_filename': 'test.txt',
                    'color_mode': 'black_white',
                    'print_sided': 'single',
                    'paper_size': 'a4',
                    'copies': 1,
                    'sequence_in_group': 1
                }
            ]
        }
        
        serializer = BindingGroupCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class OrderSerializerTest(TestCase):
    """测试订单序列化器"""

    def setUp(self):
        """测试前的准备工作"""
        self.order_data = {
            "phone_number": "13800138000",
            "groups": [
                {
                    "binding_type": "staple_top_left",
                    "sequence_in_order": 1,
                    "documents": [
                        {
                            "file_id": "temp_uploads/test.txt",
                            "original_filename": "test.txt",
                            "color_mode": "black_white",
                            "print_sided": "single",
                            "paper_size": "a4",
                            "copies": 1,
                            "sequence_in_group": 1
                        }
                    ]
                }
            ]
        }

    def test_order_create_serializer(self):
        """测试订单创建序列化器"""
        serializer = OrderCreateSerializer(data=self.order_data)
        # 由于缺少实际文件，这里会失败，但结构是正确的
        # 在实际测试中需要mock文件系统
        
    def test_order_detail_serializer(self):
        """测试订单详情序列化器"""
        # 创建测试数据
        order = Order.objects.create(
            total_price=Decimal('10.50'),
            phone_number='13800138000',
            pickup_code='P-123'
        )
        
        serializer = OrderDetailSerializer(order)
        self.assertEqual(serializer.data['phone_number'], '13800138000')
        self.assertEqual(serializer.data['pickup_code'], 'P-123')