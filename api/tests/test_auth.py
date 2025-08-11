from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status


User = get_user_model()


class AuthenticationTest(TestCase):
    """测试用户认证功能"""

    def setUp(self):
        """测试前的准备工作"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }

    def test_user_registration(self):
        """测试用户注册"""
        response = self.client.post('/api/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_user_login(self):
        """测试用户登录"""
        # 先创建用户
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # 测试登录
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)

    def test_user_profile(self):
        """测试获取用户信息"""
        # 创建用户并获取token
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        token = Token.objects.create(user=user)
        
        # 使用token进行认证
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # 获取用户信息
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')