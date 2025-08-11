from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from api.models import Order, BindingGroup, Document


class OrderModelTest(TestCase):
    """测试订单模型"""

    def setUp(self):
        """测试前的准备工作"""
        self.order = Order.objects.create(
            total_price=Decimal('10.50'),
            phone_number='13800138000',
            pickup_code='P-123',
            pickup_code_num=123
        )

    def test_order_creation(self):
        """测试订单创建"""
        self.assertEqual(self.order.total_price, Decimal('10.50'))
        self.assertEqual(self.order.phone_number, '13800138000')
        self.assertEqual(self.order.pickup_code, 'P-123')
        self.assertEqual(self.order.status, 'pending')
        self.assertIsNotNone(self.order.order_number)

    def test_order_string_representation(self):
        """测试订单字符串表示"""
        expected = f"Order {self.order.order_number} ({self.order.pickup_code})"
        self.assertEqual(str(self.order), expected)


class BindingGroupModelTest(TestCase):
    """测试装订组模型"""

    def setUp(self):
        """测试前的准备工作"""
        self.order = Order.objects.create(
            total_price=Decimal('10.50'),
            phone_number='13800138000'
        )
        self.binding_group = BindingGroup.objects.create(
            order=self.order,
            binding_type='staple_top_left',
            binding_cost=Decimal('0.10'),
            sequence_in_order=1
        )

    def test_binding_group_creation(self):
        """测试装订组创建"""
        self.assertEqual(self.binding_group.order, self.order)
        self.assertEqual(self.binding_group.binding_type, 'staple_top_left')
        self.assertEqual(self.binding_group.binding_cost, Decimal('0.10'))
        self.assertEqual(self.binding_group.sequence_in_order, 1)

    def test_binding_type_display(self):
        """测试装订类型显示"""
        self.assertEqual(self.binding_group.binding_type_display, '订书钉 (左上角)')
        
        # 测试其他装订类型
        self.binding_group.binding_type = 'none'
        self.assertEqual(self.binding_group.binding_type_display, '不装订')
        
        self.binding_group.binding_type = 'staple'
        self.assertEqual(self.binding_group.binding_type_display, '骑马钉')


class DocumentModelTest(TestCase):
    """测试文档模型"""

    def setUp(self):
        """测试前的准备工作"""
        self.order = Order.objects.create(
            total_price=Decimal('10.50'),
            phone_number='13800138000'
        )
        self.binding_group = BindingGroup.objects.create(
            order=self.order,
            binding_type='staple_top_left'
        )
        self.document = Document.objects.create(
            group=self.binding_group,
            original_filename='test.pdf',
            file_path='test_path/test.pdf',
            color_mode='black_white',
            print_sided='single',
            paper_size='a4',
            copies=1,
            page_count=5,
            print_cost=Decimal('0.75'),
            sequence_in_group=1
        )

    def test_document_creation(self):
        """测试文档创建"""
        self.assertEqual(self.document.group, self.binding_group)
        self.assertEqual(self.document.original_filename, 'test.pdf')
        self.assertEqual(self.document.color_mode, 'black_white')
        self.assertEqual(self.document.print_sided, 'single')
        self.assertEqual(self.document.paper_size, 'a4')
        self.assertEqual(self.document.copies, 1)
        self.assertEqual(self.document.page_count, 5)
        self.assertEqual(self.document.print_cost, Decimal('0.75'))
        self.assertEqual(self.document.sequence_in_group, 1)

    def test_document_display_properties(self):
        """测试文档显示属性"""
        self.assertEqual(self.document.print_sided_display, '单面打印')
        self.assertEqual(self.document.paper_size_display, 'A4')