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
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Order, User
from .serializers import OrderCreateSerializer, OrderDetailSerializer, UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from .services import pricing

# OAuth认证相关视图
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from .services.oauth_service import OAuthService
import requests
import logging

logger = logging.getLogger(__name__)

# --- 用户认证视图 ---

class UserRegistrationView(generics.CreateAPIView):
    """
    用户注册视图
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # 添加调试日志
        logger.info(f"Registration request received: {request.data}")
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        serializer = self.get_serializer(data=request.data)
        
        # 检查序列化器验证结果
        if not serializer.is_valid():
            logger.error(f"Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info("Serializer validation passed, creating user...")
        user = serializer.save()
        
        # 创建Token
        token, created = Token.objects.get_or_create(user=user)
        
        # 登录用户，指定使用默认的ModelBackend
        from django.contrib.auth import authenticate
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        logger.info(f"User created successfully: {user.username}")
        
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
        
        # 登录用户，指定使用默认的ModelBackend
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
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
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    获取CSRF token的端点
    """
    return Response({'csrfToken': get_token(request)})


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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_orders(request):
    """
    获取当前用户的订单列表
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderDetailSerializer(orders, many=True)
    return Response(serializer.data)


# --- 原有视图 ---

class FileUploadView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  # 允许任何用户上传文件
    
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
    permission_classes = [permissions.AllowAny]  # 允许任何用户获取价格估算
    
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
    
    def get_permissions(self):
        """
        根据不同的操作设置不同的权限
        """
        if self.action == 'create':
            # 创建订单：允许任何人
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'retrieve']:
            # 查询订单：允许任何人（但get_queryset会控制具体可见的订单）
            permission_classes = [permissions.AllowAny]
        else:
            # 其他操作（更新、删除）：需要认证
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        base_queryset = super().get_queryset()
        # 统一使用前端传参的名称
        pickup_code = self.request.query_params.get('pickup_code')
        phone_number = self.request.query_params.get('phone_number')

        # 已登录用户：只能看自己的订单，可再叠加查询条件
        if self.request.user.is_authenticated:
            queryset = base_queryset.filter(user=self.request.user)
            if pickup_code:
                queryset = queryset.filter(pickup_code=pickup_code)
            if phone_number:
                queryset = queryset.filter(phone_number=phone_number)
            return queryset

        # 未登录用户：仅允许通过取件码或手机号查询；否则不返回任何结果
        if pickup_code or phone_number:
            queryset = base_queryset
            if pickup_code:
                queryset = queryset.filter(pickup_code=pickup_code)
            if phone_number:
                queryset = queryset.filter(phone_number=phone_number)
            return queryset

        return base_queryset.none()
        
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
    permission_classes = [permissions.AllowAny]  # 允许任何用户上传付款截图，包括未登录用户
    
    def create(self, request, *args, **kwargs):
        try:
            screenshot_file = request.FILES.get('file')
            if not screenshot_file:
                return Response({'error': '没有提供文件'}, status=status.HTTP_400_BAD_REQUEST)

            # 检查文件类型
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if screenshot_file.content_type not in allowed_types:
                return Response({
                    'error': '不支持的文件类型，请上传JPEG或PNG格式的图片'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 检查文件大小（限制为5MB）
            if screenshot_file.size > 5 * 1024 * 1024:
                return Response({
                    'error': '文件大小不能超过5MB'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 为了安全和区分，我们为支付凭证创建一个独立的存储实例
            # 这会将其保存在 'media/payments/' 目录下
            fs = FileSystemStorage(location=Path(settings.MEDIA_ROOT) / 'payments')
            
            # 使用UUID生成唯一文件名
            file_extension = Path(screenshot_file.name).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # 保存文件
            filename = fs.save(unique_filename, screenshot_file)
            
            # 记录上传日志
            user_info = f"user_{request.user.id}" if request.user.is_authenticated else "anonymous"
            logger.info(f"Payment screenshot uploaded: {filename} by {user_info}")
            
            # 返回给前端需要的数据
            return Response({
                'screenshot_id': filename, # 返回保存后的文件名作为ID
                'message': '付款截图上传成功'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Payment screenshot upload error: {str(e)}")
            return Response({
                'error': '上传过程中发生错误，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GitHubLoginView(View):
    """GitHub OAuth登录视图"""
    
    def get(self, request):
        """重定向到GitHub OAuth授权页面"""
        github_client_id = getattr(settings, 'GITHUB_CLIENT_ID', None)
        if not github_client_id:
            return JsonResponse({'error': 'GitHub OAuth未配置'}, status=500)
        
        # 构建GitHub OAuth授权URL
        redirect_uri = request.build_absolute_uri('/api/oauth/github/callback/')
        scope = 'user:email'
        
        github_auth_url = (
            f'https://github.com/login/oauth/authorize?'
            f'client_id={github_client_id}&'
            f'redirect_uri={redirect_uri}&'
            f'scope={scope}'
        )
        
        return redirect(github_auth_url)

class GoogleLoginView(View):
    """Google OAuth登录视图"""
    
    def get(self, request):
        """重定向到Google OAuth授权页面"""
        google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        if not google_client_id:
            return JsonResponse({'error': 'Google OAuth未配置'}, status=500)
        
        # 构建Google OAuth授权URL
        redirect_uri = request.build_absolute_uri('/api/oauth/google/callback/')
        scope = 'openid email profile'
        
        google_auth_url = (
            f'https://accounts.google.com/o/oauth2/v2/auth?'
            f'client_id={google_client_id}&'
            f'redirect_uri={redirect_uri}&'
            f'scope={scope}&'
            f'response_type=code&'
            f'access_type=offline'
        )
        
        return redirect(google_auth_url)

class GitHubCallbackView(View):
    """GitHub OAuth回调处理视图"""
    
    def get(self, request):
        """处理GitHub OAuth回调"""
        try:
            # 添加详细的日志记录
            logger.info(f"GitHub callback received. GET params: {dict(request.GET)}")
            logger.info(f"Request URL: {request.build_absolute_uri()}")
            
            code = request.GET.get('code')
            state = request.GET.get('state')
            error = request.GET.get('error')
            
            # 检查是否有OAuth错误
            if error:
                logger.error(f"GitHub OAuth error: {error}")
                frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
                frontend_callback_url += f'?provider=github&success=false&error={error}'
                return redirect(frontend_callback_url)
            
            if not code:
                logger.error("GitHub callback: No authorization code received")
                logger.error(f"Available GET parameters: {list(request.GET.keys())}")
                return JsonResponse({'error': '授权码缺失'}, status=400)
            
            logger.info(f"GitHub callback: Authorization code received: {code[:10]}...")
            
            # 使用OAuth服务处理回调，传入request参数以支持账户绑定
            oauth_service = OAuthService()
            redirect_uri = request.build_absolute_uri('/api/oauth/github/callback/')
            logger.info(f"GitHub callback: Using redirect_uri: {redirect_uri}")
            
            user, user_info = oauth_service.process_oauth_callback(code, 'github', redirect_uri, request)
            logger.info(f"GitHub callback: User processed successfully: {user.username}")
            
            # 自动登录用户 - 明确指定认证后端
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.info(f"GitHub callback: User logged in: {user.username}")
            
            # 检查是否为绑定流程
            is_binding = request.GET.get('bind') == 'true'
            
            # 生成认证token（用于前端API调用）
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            
            # 所有OAuth回调都重定向到前端，让前端完成认证
            frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
            frontend_callback_url += f'?provider=github&success=true&username={user.username}'
            
            if is_binding:
                frontend_callback_url += '&bind=true'
            
            # 将token作为临时参数传递（注意：这不是安全的做法，仅用于演示）
            # 在生产环境中，应该使用更安全的方式
            frontend_callback_url += f'&temp_token={token.key}'
            
            logger.info(f"GitHub callback: Redirecting to frontend: {frontend_callback_url}")
            return redirect(frontend_callback_url)
            
        except Exception as e:
            logger.error(f"GitHub OAuth callback error: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # 提供更友好的错误信息
            if "Failed to get user info from OAuth provider" in str(e):
                friendly_error = "网络连接问题，请稍后重试"
            elif "already used by user" in str(e):
                friendly_error = "此OAuth账户已被其他用户使用"
            elif "SSLError" in str(e) or "ConnectionError" in str(e):
                friendly_error = "网络连接不稳定，请检查网络后重试"
            elif "Timeout" in str(e):
                friendly_error = "请求超时，请稍后重试"
            else:
                friendly_error = "GitHub认证过程中发生错误，请重试"
            
            frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
            frontend_callback_url += f'?provider=github&success=false&error={friendly_error}'
            return redirect(frontend_callback_url)

class GoogleCallbackView(View):
    """Google OAuth回调处理视图"""
    
    def get(self, request):
        """处理Google OAuth回调"""
        try:
            # 添加详细的日志记录
            logger.info(f"Google callback received. GET params: {dict(request.GET)}")
            logger.info(f"Request URL: {request.build_absolute_uri()}")
            
            code = request.GET.get('code')
            state = request.GET.get('state')
            error = request.GET.get('error')
            
            # 检查是否有OAuth错误
            if error:
                logger.error(f"Google OAuth error: {error}")
                frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
                frontend_callback_url += f'?provider=google&success=false&error={error}'
                return redirect(frontend_callback_url)
            
            if not code:
                logger.error("Google callback: No authorization code received")
                logger.error(f"Available GET parameters: {list(request.GET.keys())}")
                return JsonResponse({'error': '授权码缺失'}, status=400)
            
            logger.info(f"Google callback: Authorization code received: {code[:10]}...")
            
            # 使用OAuth服务处理回调，传入request参数以支持账户绑定
            oauth_service = OAuthService()
            redirect_uri = request.build_absolute_uri('/api/oauth/google/callback/')
            logger.info(f"Google callback: Using redirect_uri: {redirect_uri}")
            
            user, user_info = oauth_service.process_oauth_callback(code, 'google', redirect_uri, request)
            logger.info(f"Google callback: User processed successfully: {user.username}")
            
            # 自动登录用户 - 明确指定认证后端
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logger.info(f"Google callback: User logged in: {user.username}")
            
            # 检查是否为绑定流程
            is_binding = request.GET.get('bind') == 'true'
            
            # 生成认证token（用于前端API调用）
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            
            # 所有OAuth回调都重定向到前端，让前端完成认证
            frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
            frontend_callback_url += f'?provider=google&success=true&username={user.username}'
            
            if is_binding:
                frontend_callback_url += '&bind=true'
            
            # 将token作为临时参数传递（注意：这不是安全的做法，仅用于演示）
            # 在生产环境中，应该使用更安全的方式
            frontend_callback_url += f'&temp_token={token.key}'
            
            logger.info(f"Google callback: Redirecting to frontend: {frontend_callback_url}")
            return redirect(frontend_callback_url)
            
        except Exception as e:
            logger.error(f"Google OAuth callback error: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # 提供更友好的错误信息
            if "Failed to get user info from OAuth provider" in str(e):
                friendly_error = "网络连接问题，请稍后重试"
            elif "already used by user" in str(e):
                friendly_error = "此OAuth账户已被其他用户使用"
            elif "SSLError" in str(e) or "ConnectionError" in str(e):
                friendly_error = "网络连接不稳定，请检查网络后重试"
            elif "Timeout" in str(e):
                friendly_error = "请求超时，请稍后重试"
            else:
                friendly_error = "Google认证过程中发生错误，请重试"
            
            frontend_callback_url = 'http://127.0.0.1:5173/oauth/callback'
            frontend_callback_url += f'?provider=google&success=false&error={friendly_error}'
            return redirect(frontend_callback_url)

class OAuthTokenValidationView(View):
    """OAuth临时token验证视图"""
    
    def get(self, request):
        """验证临时token并返回用户信息"""
        try:
            temp_token = request.GET.get('token')
            if not temp_token:
                return JsonResponse({'error': '临时token缺失'}, status=400)
            
            # 验证token
            from rest_framework.authtoken.models import Token
            try:
                token = Token.objects.get(key=temp_token)
                user = token.user
                
                # 序列化用户信息
                from .serializers import UserSerializer
                user_serializer = UserSerializer(user)
                
                response_data = {
                    'user': user_serializer.data,
                    'token': temp_token,
                    'message': 'token验证成功'
                }
                
                logger.info(f"临时token验证成功: {user.username}")
                return JsonResponse(response_data)
                
            except Token.DoesNotExist:
                return JsonResponse({'error': '无效的临时token'}, status=401)
                
        except Exception as e:
            logger.error(f"临时token验证错误: {str(e)}")
            return JsonResponse({'error': 'token验证失败'}, status=500)

class OAuthCallbackView(View):
    """通用OAuth回调处理视图（已废弃，保留兼容性）"""
    
    def get(self, request):
        """处理OAuth回调"""
        code = request.GET.get('code')
        state = request.GET.get('state')
        
        if not code:
            return JsonResponse({'error': '授权码缺失'}, status=400)
        
        # 这里可以添加状态验证逻辑
        # 处理OAuth回调，创建或更新用户
        
        return JsonResponse({'message': 'OAuth认证成功'})

class OAuthUserInfoView(View):
    """获取OAuth用户信息"""
    
    def get(self, request):
        """获取当前用户的OAuth信息"""
        try:
            # 检查用户是否已认证（支持session和token认证）
            if not request.user.is_authenticated:
                return JsonResponse({'error': '用户未认证'}, status=401)
            
            # 获取用户信息
            user_data = {
                'username': request.user.username,
                'email': request.user.email,
                'github_id': request.user.github_id,
                'google_id': request.user.google_id,
                'avatar_url': request.user.get_avatar_url() if hasattr(request.user, 'get_avatar_url') else None,
                'display_name': request.user.get_display_name() if hasattr(request.user, 'get_display_name') else request.user.username,
                'is_oauth_user': bool(request.user.github_id or request.user.google_id)
            }
            
            return JsonResponse(user_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class OAuthBindingView(View):
    """OAuth账户绑定管理视图"""
    
    def get(self, request):
        """获取用户的OAuth绑定状态"""
        try:
            # 检查用户是否已认证（支持session和token认证）
            if not request.user.is_authenticated:
                return JsonResponse({'error': '用户未认证'}, status=401)
            
            # 获取绑定状态
            bindings = []
            
            # 检查GitHub绑定
            if request.user.github_id:
                bindings.append({
                    'provider': 'github',
                    'uid': request.user.github_id,
                    'date_joined': request.user.date_joined.isoformat(),
                    'extra_data': {}
                })
            
            # 检查Google绑定
            if request.user.google_id:
                bindings.append({
                    'provider': 'google',
                    'uid': request.user.google_id,
                    'date_joined': request.user.date_joined.isoformat(),
                    'extra_data': {}
                })
            
            return JsonResponse({
                'bindings': bindings,
                'github_id': request.user.github_id,
                'google_id': request.user.google_id,
                'can_bind_github': not request.user.github_id,
                'can_bind_google': not request.user.google_id
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request, provider):
        """绑定OAuth账户到当前用户"""
        try:
            # 检查用户是否已认证（支持session和token认证）
            if not request.user.is_authenticated:
                return JsonResponse({'error': '用户未认证'}, status=401)
            
            if provider not in ['github', 'google']:
                return JsonResponse({'error': '不支持的OAuth提供商'}, status=400)
            
            # 检查是否已经绑定
            if provider == 'github' and request.user.github_id:
                return JsonResponse({'error': 'GitHub账户已绑定'}, status=400)
            elif provider == 'google' and request.user.google_id:
                return JsonResponse({'error': 'Google账户已绑定'}, status=400)
            
            # 重定向到OAuth授权页面
            if provider == 'github':
                oauth_url = '/api/oauth/github/'
            else:
                oauth_url = '/api/oauth/google/'
            
            # 添加绑定标识到state参数
            oauth_url += f'?bind=true&user_id={request.user.id}'
            
            return JsonResponse({
                'redirect_url': oauth_url,
                'message': f'正在跳转到{provider}授权页面...'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, provider):
        """解绑OAuth账户"""
        try:
            # 检查用户是否已认证（支持session和token认证）
            if not request.user.is_authenticated:
                return JsonResponse({'error': '用户未认证'}, status=401)
            
            if provider not in ['github', 'google']:
                return JsonResponse({'error': '不支持的OAuth提供商'}, status=400)
            
            # 检查是否还有其他OAuth账户绑定
            remaining_oauth = 0
            if request.user.github_id and provider != 'github':
                remaining_oauth += 1
            if request.user.google_id and provider != 'google':
                remaining_oauth += 1
            
            if remaining_oauth == 0:
                return JsonResponse({'error': '不能解绑最后一个OAuth账户'}, status=400)
            
            # 解绑账户
            if provider == 'github':
                request.user.github_id = None
            elif provider == 'google':
                request.user.google_id = None
            
            request.user.save()
            
            return JsonResponse({'message': f'{provider}账户已解绑'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)