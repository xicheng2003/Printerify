# printerify/api/views.py (最终修复版)

import uuid
from pathlib import Path
from django.conf import settings # <-- 【新增】导入Django的settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .models import Order, User
from .serializers import OrderCreateSerializer, OrderDetailSerializer, UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from .services import pricing

# --- 用户认证视图 ---

class UserRegistrationView(generics.CreateAPIView):
    """
    用户注册视图
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 创建Token
        token, created = Token.objects.get_or_create(user=user)
        
        # 登录用户
        login(request, user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    用户登录视图
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # 登录用户
        login(request, user)
        
        # 获取或创建Token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """
    用户登出视图
    """
    try:
        # 删除用户的Token
        request.user.auth_token.delete()
    except:
        pass
    
    # 登出用户
    logout(request)
    
    return Response({'detail': '成功登出'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    获取用户信息
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    """
    更新用户信息
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 原有视图 ---

class FileUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': '没有提供文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 【关键修复】使用settings.MEDIA_ROOT构建一个绝对、可靠的存储路径
        temp_dir = Path(settings.MEDIA_ROOT) / 'temp_uploads'
        fs = FileSystemStorage(location=temp_dir)
        
        file_extension = Path(file_obj.name).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        filename = fs.save(unique_filename, file_obj)
        
        # 【关键修复】返回给前端的路径，应该是相对于media/的路径，而不是完整路径
        # 这样前端传回来时，我们才能正确地拼接
        relative_path = Path('temp_uploads') / filename
        
        return Response({
            'file_id': str(relative_path), # 返回相对路径作为 file_id
            'original_filename': file_obj.name,
        }, status=status.HTTP_201_CREATED)


class PriceEstimationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        # 注意：这里的 'file_path' 实际上是我们上面返回的 relative_path
        file_path_from_frontend = request.data.get('file_path')
        color_mode = request.data.get('color_mode')
        print_sided = request.data.get('print_sided')
        copies = int(request.data.get('copies', 1))
        # 【核心修正】从请求中获取 paper_size
        paper_size = request.data.get('paper_size') # <-- 【新增】获取纸张尺寸

        if not all([file_path_from_frontend, color_mode, print_sided, copies, paper_size]):
            return Response({'error': '缺少必要的参数 (file_path, color_mode, print_sided, copies, paper_size)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 【关键修复】同样使用settings.MEDIA_ROOT来构建绝对路径，确保与上传时一致
        full_file_path = Path(settings.MEDIA_ROOT) / file_path_from_frontend
        
        if not full_file_path.exists():
             return Response({'error': f'文件在服务器上未找到，路径: {full_file_path}'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # 【核心修正】将 paper_size 传递给计价函数
            page_count, print_cost = pricing.calculate_document_price(
                file_path=str(full_file_path),
                paper_size=paper_size, # <--- 传递新参数
                color_mode=color_mode,
                print_sided=print_sided,
                copies=int(copies)
            )
            
            # 返回成功响应
            return Response({
                "page_count": page_count,
                "print_cost": f"{print_cost:.2f}"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # 捕获其他潜在错误（如计价逻辑内部错误）
            return Response(
                {"error": f"计算价格时发生错误: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# OrderViewSet 的代码保持不变
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        pickup_code = self.request.query_params.get('code')
        phone_number = self.request.query_params.get('phone')
        
        # 如果用户已认证，只返回该用户的订单
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        if pickup_code:
            queryset = queryset.filter(pickup_code=pick_code)
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)
        return queryset
        
    def perform_create(self, serializer):
        # 如果用户已认证，将订单与用户关联
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


# --- 【新增】付款凭证上传视图 ---
class PaymentScreenshotUploadView(generics.CreateAPIView):
    """
    一个专门用于接收付款凭证截图的视图。
    它接收一个图片文件，将其保存到 'payments/' 目录，并返回一个唯一ID。
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        screenshot_file = request.FILES.get('file')
        if not screenshot_file:
            return Response({'error': '没有提供文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 为了安全和区分，我们为支付凭证创建一个独立的存储实例
        # 这会将其保存在 'media/payments/' 目录下
        fs = FileSystemStorage(location=Path(settings.MEDIA_ROOT) / 'payments')
        
        # 使用UUID生成唯一文件名
        file_extension = Path(screenshot_file.name).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # 保存文件
        filename = fs.save(unique_filename, screenshot_file)
        
        # 返回给前端需要的数据
        return Response({
            'screenshot_id': filename, # 返回保存后的文件名作为ID
        }, status=status.HTTP_201_CREATED)