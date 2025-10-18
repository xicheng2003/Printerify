# 文件查看与下载功能说明

## 功能概述

订单查询页面现在提供两种文件操作方式：
1. **在线预览** - 在浏览器中直接打开PDF文件
2. **下载文件** - 将文件下载到本地

---

## 实现方案

### 方案1：前端双按钮（已实施）✅

在前端为每个文件提供两个独立的按钮：

#### 前端实现 (QueryView.vue)

```vue
<!-- 文件操作按钮组 -->
<div class="file-actions">
  <!-- 在线预览按钮 -->
  <a :href="doc.file_path" target="_blank" class="file-action-btn preview-btn">
    <svg>眼睛图标</svg>
    在线预览
  </a>
  
  <!-- 下载按钮 -->
  <a :href="doc.file_path" :download="doc.original_filename" class="file-action-btn download-btn">
    <svg>下载图标</svg>
    下载文件
  </a>
</div>
```

**工作原理：**
- **在线预览**：使用 `target="_blank"` 在新标签页打开文件，浏览器会根据文件类型决定是否可以预览
- **下载文件**：使用 `download` 属性强制触发下载，保留原始文件名

**优点：**
- ✅ 用户体验好，操作直观
- ✅ 不需要后端改动
- ✅ 支持所有现代浏览器
- ✅ 移动端友好

---

### 方案2：Nginx响应头控制（可选）

通过Nginx配置控制浏览器行为。

#### 修改 Nginx 配置

```nginx
location ^~ /media/ {
    alias /home/xicheng2003/Printerify/media/;
    charset utf-8;
    
    # 默认：允许浏览器内联显示（在线预览）
    # 如果URL带有 ?download=1 参数，则触发下载
    set $disposition "inline";
    if ($arg_download = "1") {
        set $disposition "attachment";
    }
    
    add_header Content-Disposition "$disposition; filename*=UTF-8''$uri" always;
    
    types {
        application/pdf pdf;
        image/jpeg jpg jpeg;
        image/png png;
    }
    
    expires 7d;
    add_header Cache-Control "public";
    autoindex off;
}
```

#### 前端配合使用

```vue
<!-- 在线预览 -->
<a :href="doc.file_path" target="_blank">在线预览</a>

<!-- 下载文件 -->
<a :href="doc.file_path + '?download=1'">下载文件</a>
```

**优点：**
- ✅ 更精确控制浏览器行为
- ✅ 支持中文文件名下载

**缺点：**
- ❌ 需要修改Nginx配置
- ❌ 需要重载Nginx服务

---

### 方案3：Django后端API端点（备选）

创建专门的下载API端点。

#### 后端实现 (api/views.py)

```python
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def download_document(request, document_id):
    """
    下载文档端点
    ?preview=1 : 在线预览
    ?preview=0 : 强制下载
    """
    try:
        doc = Document.objects.get(id=document_id)
        
        if not doc.file_path:
            return Response({'error': '文件不存在'}, status=404)
        
        # 判断是预览还是下载
        preview = request.GET.get('preview', '0') == '1'
        
        response = FileResponse(
            doc.file_path.open('rb'),
            content_type='application/pdf'
        )
        
        # 设置Content-Disposition头
        if preview:
            # 在线预览
            response['Content-Disposition'] = f'inline; filename="{doc.original_filename}"'
        else:
            # 强制下载
            response['Content-Disposition'] = f'attachment; filename="{doc.original_filename}"'
        
        return response
        
    except Document.DoesNotExist:
        return Response({'error': '文档不存在'}, status=404)
```

#### URL配置 (api/urls.py)

```python
urlpatterns = [
    # ...其他路由
    path('documents/<int:document_id>/download/', download_document, name='download_document'),
]
```

#### 前端使用

```vue
<!-- 在线预览 -->
<a :href="`/api/documents/${doc.id}/download/?preview=1`" target="_blank">在线预览</a>

<!-- 下载文件 -->
<a :href="`/api/documents/${doc.id}/download/?preview=0`">下载文件</a>
```

**优点：**
- ✅ 更好的权限控制
- ✅ 可以记录下载日志
- ✅ 支持大文件流式传输

**缺点：**
- ❌ 需要后端开发工作
- ❌ 增加服务器负载

---

## 浏览器兼容性

### HTML5 `download` 属性

| 浏览器 | 支持版本 |
|--------|---------|
| Chrome | 14+ ✅ |
| Firefox | 20+ ✅ |
| Safari | 10.1+ ✅ |
| Edge | 13+ ✅ |
| Mobile Safari | 13+ ✅ |
| Chrome Android | ✅ |

**注意事项：**
- ⚠️ `download` 属性只对**同源URL**有效
- ⚠️ 跨域URL会忽略 `download` 属性，直接导航到文件
- ⚠️ 由于我们的文件在同一域名下（`/media/`），`download` 属性完全有效

---

## 推荐配置

### 当前已实施：方案1（前端双按钮）

**优点总结：**
1. ✅ 实现简单，无需后端改动
2. ✅ 用户体验好，操作明确
3. ✅ 浏览器兼容性好
4. ✅ 同时支持预览和下载

### 如果需要更精确控制

可以结合方案2，在Nginx中添加响应头控制：

```nginx
location ^~ /media/ {
    # ... 其他配置 ...
    
    # 默认允许内联显示（预览）
    add_header Content-Disposition "inline" always;
}
```

然后前端使用 `download` 属性即可触发下载。

---

## 测试方法

### 测试在线预览
1. 访问订单查询页面
2. 点击"在线预览"按钮
3. 应该在新标签页打开PDF文件
4. 浏览器内置PDF查看器应该显示文件内容

### 测试下载功能
1. 访问订单查询页面
2. 点击"下载文件"按钮
3. 浏览器应该弹出下载对话框
4. 文件名应该是原始文件名（中文正常显示）
5. 下载完成后可以打开查看

### 测试中文文件名
1. 上传一个中文文件名的PDF
2. 测试预览和下载
3. 下载后的文件名应该正确显示中文

---

## 移动端体验

在移动设备上：
- **在线预览**：在系统浏览器或PDF阅读器中打开
- **下载文件**：保存到设备下载目录

iOS Safari 特殊行为：
- 点击下载可能会在Safari中预览
- 用户可以通过"分享"按钮选择"存储到文件"

---

## 故障排查

### 问题1：点击"下载"仍然在浏览器中预览

**原因：** 浏览器认为文件可以内联显示

**解决方案：**
- 方案A：使用方案2，在Nginx中添加 `Content-Disposition: attachment`
- 方案B：接受这个行为，用户可以通过浏览器菜单下载

### 问题2：中文文件名下载后乱码

**原因：** Nginx未正确设置字符编码

**解决方案：**
```nginx
location ^~ /media/ {
    charset utf-8;  # 确保添加这一行
    # ...
}
```

### 问题3：跨域文件无法下载

**原因：** `download` 属性不支持跨域URL

**解决方案：**
- 确保文件URL与网站在同一域名下
- 或使用方案3通过后端代理文件

---

## 未来优化方向

1. **下载进度显示** - 对于大文件显示下载进度条
2. **批量下载** - 支持一次性下载多个文件（打包成ZIP）
3. **下载统计** - 记录文件下载次数和日志
4. **权限控制** - 限制文件访问权限和下载次数
5. **防盗链** - 添加token验证防止文件被盗链

---

**更新日期：** 2025-10-18  
**实施状态：** ✅ 已实施方案1（前端双按钮）  
**测试状态：** ⏳ 待测试
