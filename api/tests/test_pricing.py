from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from api.models import Order, BindingGroup, Document
from api.services.pricing import calculate_document_price, calculate_binding_cost


class PricingServiceTest(TestCase):
    """测试定价服务"""

    def test_calculate_document_price_black_white_single_a4(self):
        """测试黑白单面A4文档价格计算"""
        # 创建一个简单的文本文件用于测试
        test_file = SimpleUploadedFile(
            "test.txt", 
            b"Test content for pricing calculation",
            content_type="text/plain"
        )
        
        # 保存文件到临时位置以进行测试
        temp_file_path = f"temp_test_file.txt"
        with open(temp_file_path, 'wb') as f:
            f.write(test_file.read())
        
        # 测试1页黑白单面A4文档，1份
        page_count, cost = calculate_document_price(
            file_path=temp_file_path,
            paper_size='a4',
            color_mode='black_white',
            print_sided='single',
            copies=1
        )
        
        # 验证页数和价格计算
        self.assertEqual(page_count, 1)
        expected_cost = Decimal('0.15')  # 根据定价配置
        self.assertEqual(cost, expected_cost)
        
        # 清理临时文件
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    def test_calculate_document_price_color_double_b5(self):
        """测试彩色双面B5文档价格计算"""
        # 创建一个简单的文本文件用于测试
        test_file = SimpleUploadedFile(
            "test.txt", 
            b"Test content for pricing calculation",
            content_type="text/plain"
        )
        
        # 保存文件到临时位置以进行测试
        temp_file_path = f"temp_test_file.txt"
        with open(temp_file_path, 'wb') as f:
            f.write(test_file.read())
        
        # 测试1页彩色双面B5文档，2份
        page_count, cost = calculate_document_price(
            file_path=temp_file_path,
            paper_size='b5',
            color_mode='color',
            print_sided='double',
            copies=2
        )
        
        # 验证页数和价格计算
        self.assertEqual(page_count, 1)
        expected_cost = Decimal('0.70') * 2  # 根据定价配置
        self.assertEqual(cost, expected_cost)
        
        # 清理临时文件
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    def test_calculate_binding_cost(self):
        """测试装订费用计算"""
        # 测试不装订
        cost = calculate_binding_cost('none', 10)
        self.assertEqual(cost, Decimal('0.00'))
        
        # 测试订书钉装订
        cost = calculate_binding_cost('staple_top_left', 10)
        self.assertEqual(cost, Decimal('0.10'))
        
        # 测试骑马钉装订
        cost = calculate_binding_cost('staple', 10)
        self.assertEqual(cost, Decimal('2.00'))
        
        # 测试胶圈装订
        cost = calculate_binding_cost('ring_bound', 10)
        self.assertEqual(cost, Decimal('5.00'))