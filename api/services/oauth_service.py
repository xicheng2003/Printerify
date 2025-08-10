import requests
import random
import string
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import logging
import time

logger = logging.getLogger(__name__)
User = get_user_model()

class OAuthService:
    """OAuth认证服务类"""
    
    def __init__(self):
        self.github_client_id = getattr(settings, 'GITHUB_CLIENT_ID', None)
        self.github_client_secret = getattr(settings, 'GITHUB_CLIENT_SECRET', None)
        self.google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        self.google_client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        
        # 网络请求配置
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Printerify/1.0 (OAuth Service)'
        })
        
        # 重试配置
        self.max_retries = 3
        self.retry_delay = 1  # 秒
    
    def _make_request_with_retry(self, method, url, **kwargs):
        """带重试机制的HTTP请求"""
        for attempt in range(self.max_retries):
            try:
                if method.lower() == 'get':
                    response = self.session.get(url, timeout=30, **kwargs)
                elif method.lower() == 'post':
                    response = self.session.post(url, timeout=30, **kwargs)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                return response
                
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, 
                    requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))  # 指数退避
                    continue
                else:
                    logger.error(f"All {self.max_retries} attempts failed for {url}")
                    raise e
    
    def get_random_password(self, length=64):
        """生成随机密码"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))
    
    def get_github_user_info(self, code, redirect_uri):
        """获取GitHub用户信息"""
        try:
            # 1. 使用授权码获取访问令牌
            token_url = 'https://github.com/login/oauth/access_token'
            token_data = {
                'client_id': self.github_client_id,
                'client_secret': self.github_client_secret,
                'code': code,
                'redirect_uri': redirect_uri
            }
            
            response = self._make_request_with_retry('POST', token_url, data=token_data, headers={
                'Accept': 'application/json'
            })
            
            if response.status_code != 200:
                logger.error(f"GitHub token request failed: {response.text}")
                return None
            
            token_info = response.json()
            access_token = token_info.get('access_token')
            
            if not access_token:
                logger.error(f"GitHub access token not found: {token_info}")
                return None
            
            # 2. 使用访问令牌获取用户信息
            user_url = 'https://api.github.com/user'
            user_response = self._make_request_with_retry('GET', user_url, headers={
                'Authorization': f'token {access_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
            
            if user_response.status_code != 200:
                logger.error(f"GitHub user info request failed: {user_response.text}")
                return None
            
            user_info = user_response.json()
            
            # 3. 获取用户邮箱（可选，如果失败不影响主要流程）
            email = None
            try:
                emails_url = 'https://api.github.com/user/emails'
                emails_response = self._make_request_with_retry('GET', emails_url, headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/vnd.github.v3+json'
                })
                
                if emails_response.status_code == 200:
                    emails = emails_response.json()
                    # 查找主要邮箱
                    for email_info in emails:
                        if email_info.get('primary') and email_info.get('verified'):
                            email = email_info.get('email')
                            break
            except Exception as email_error:
                logger.warning(f"Failed to get GitHub emails, continuing without email: {str(email_error)}")
            
            return {
                'provider': 'github',
                'id': str(user_info.get('id')),
                'username': user_info.get('login'),
                'email': email,
                'first_name': user_info.get('name', '').split()[0] if user_info.get('name') else '',
                'last_name': ' '.join(user_info.get('name', '').split()[1:]) if user_info.get('name') and len(user_info.get('name', '').split()) > 1 else '',
                'avatar_url': user_info.get('avatar_url'),
                'github_id': str(user_info.get('id')),
                'extra_data': {
                    'login': user_info.get('login'),
                    'name': user_info.get('name'),
                    'company': user_info.get('company'),
                    'location': user_info.get('location'),
                    'bio': user_info.get('bio'),
                    'public_repos': user_info.get('public_repos'),
                    'followers': user_info.get('followers'),
                    'following': user_info.get('following'),
                    'created_at': user_info.get('created_at'),
                    'updated_at': user_info.get('updated_at')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting GitHub user info: {str(e)}")
            return None
    
    def get_google_user_info(self, code, redirect_uri):
        """获取Google用户信息"""
        try:
            # 1. 使用授权码获取访问令牌
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'client_id': self.google_client_id,
                'client_secret': self.google_client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri
            }
            
            response = self._make_request_with_retry('POST', token_url, data=token_data)
            
            if response.status_code != 200:
                logger.error(f"Google token request failed: {response.text}")
                return None
            
            token_info = response.json()
            access_token = token_info.get('access_token')
            
            if not access_token:
                logger.error(f"Google access token not found: {token_info}")
                return None
            
            # 2. 使用访问令牌获取用户信息
            user_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            user_response = self._make_request_with_retry('GET', user_url, headers={
                'Authorization': f'Bearer {access_token}'
            })
            
            if user_response.status_code != 200:
                logger.error(f"Google user info request failed: {user_response.text}")
                return None
            
            user_info = user_response.json()
            
            return {
                'provider': 'google',
                'id': str(user_info.get('id')),
                'username': user_info.get('email', '').split('@')[0] if user_info.get('email') else f"google_{user_info.get('id')}",
                'email': user_info.get('email'),
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'avatar_url': user_info.get('picture'),
                'google_id': str(user_info.get('id')),
                'extra_data': {
                    'locale': user_info.get('locale'),
                    'verified_email': user_info.get('verified_email'),
                    'hd': user_info.get('hd')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting Google user info: {str(e)}")
            return None
    
    def find_or_create_user(self, user_info, request=None):
        """查找或创建用户，支持账户绑定"""
        try:
            # 策略1: 通过OAuth ID查找现有用户
            if user_info.get('github_id'):
                user = User.objects.filter(github_id=user_info['github_id']).first()
                if user:
                    logger.info(f"Found existing user by GitHub ID: {user.username}")
                    return user
            
            if user_info.get('google_id'):
                user = User.objects.filter(google_id=user_info['google_id']).first()
                if user:
                    logger.info(f"Found existing user by Google ID: {user.username}")
                    return user
            
            # 策略2: 如果用户已登录，绑定OAuth账户到当前用户
            if request and request.user.is_authenticated:
                current_user = request.user
                logger.info(f"User already authenticated, binding OAuth to existing user: {current_user.username}")
                
                # 检查是否已经有其他用户使用了这个OAuth ID
                if user_info.get('github_id'):
                    existing_user = User.objects.filter(github_id=user_info['github_id']).first()
                    if existing_user and existing_user != current_user:
                        logger.warning(f"GitHub ID {user_info['github_id']} already used by user {existing_user.username}")
                        raise ValueError(f"此GitHub账户已被用户 {existing_user.username} 使用")
                
                if user_info.get('google_id'):
                    existing_user = User.objects.filter(google_id=user_info['google_id']).first()
                    if existing_user and existing_user != current_user:
                        logger.warning(f"Google ID {user_info['google_id']} already used by user {existing_user.username}")
                        raise ValueError(f"此Google账户已被用户 {existing_user.username} 使用")
                
                # 绑定OAuth账户到当前用户
                self.bind_oauth_to_existing_user(current_user, user_info)
                return current_user
            
            # 策略3: 通过邮箱查找现有用户
            if user_info.get('email'):
                user = User.objects.filter(email=user_info['email']).first()
                if user:
                    logger.info(f"Found existing user by email: {user.username}")
                    # 绑定OAuth账户到现有用户
                    self.bind_oauth_to_existing_user(user, user_info)
                    return user
            
            # 策略4: 创建新用户
            logger.info(f"Creating new user for OAuth: {user_info.get('username')}")
            return self.create_new_user(user_info)
            
        except Exception as e:
            logger.error(f"Error in find_or_create_user: {str(e)}")
            raise
    
    def bind_oauth_to_existing_user(self, user, user_info):
        """将OAuth账户绑定到现有用户"""
        try:
            # 更新用户的OAuth相关字段
            if user_info.get('github_id'):
                user.github_id = user_info['github_id']
            if user_info.get('google_id'):
                user.google_id = user_info['google_id']
            if user_info.get('avatar_url') and not user.avatar_url:
                user.avatar_url = user_info['avatar_url']
            
            user.save()
            
            # 创建或更新SocialAccount关联
            social_account, created = SocialAccount.objects.get_or_create(
                user=user,
                provider=user_info['provider'],
                uid=user_info['id'],
                defaults={
                    'extra_data': user_info.get('extra_data', {})
                }
            )
            
            if not created:
                # 更新现有社交账户的额外数据
                social_account.extra_data = user_info.get('extra_data', {})
                social_account.save()
            
            logger.info(f"Successfully bound OAuth account {user_info['provider']} to user {user.username}")
            
        except Exception as e:
            logger.error(f"Error binding OAuth to existing user: {str(e)}")
            raise
    
    def create_new_user(self, user_info):
        """创建新用户"""
        try:
            # 生成唯一用户名
            base_username = user_info.get('username') or f"{user_info['provider']}_{user_info['id']}"
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            
            # 创建用户
            user = User.objects.create(
                username=username,
                email=user_info.get('email', ''),
                first_name=user_info.get('first_name', ''),
                last_name=user_info.get('last_name', ''),
                github_id=user_info.get('github_id'),
                google_id=user_info.get('google_id'),
                avatar_url=user_info.get('avatar_url'),
                is_active=True
            )
            
            # 设置随机密码（用户不会用到，但Django需要）
            user.set_password(self.get_random_password())
            user.save()
            
            # 创建SocialAccount关联
            SocialAccount.objects.create(
                user=user,
                provider=user_info['provider'],
                uid=user_info['id'],
                extra_data=user_info.get('extra_data', {})
            )
            
            logger.info(f"Successfully created new user: {username}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating new user: {str(e)}")
            raise
    
    def process_oauth_callback(self, code, provider, redirect_uri, request=None):
        """处理OAuth回调"""
        try:
            # 根据提供商获取用户信息
            if provider == 'github':
                user_info = self.get_github_user_info(code, redirect_uri)
            elif provider == 'google':
                user_info = self.get_google_user_info(code, redirect_uri)
            else:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
            
            if not user_info:
                raise ValueError("Failed to get user info from OAuth provider")
            
            # 查找或创建用户，传入request参数以支持账户绑定
            user = self.find_or_create_user(user_info, request)
            
            if not user:
                raise ValueError("Failed to find or create user")
            
            return user, user_info
            
        except Exception as e:
            logger.error(f"Error processing OAuth callback: {str(e)}")
            raise
