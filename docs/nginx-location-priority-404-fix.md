# 快速修复指南 - 基于你的实际Nginx配置

## ⚠️ 核心问题

你的Nginx配置中有**location规则冲突**：

```nginx
# 规则1：所有PDF都匹配（正则location，优先级高）
location ~* \.(rar|zip|pdf|gz|7z)$ {
    root /home/xicheng2003/public_downloads;
    add_header Content-Disposition "attachment";
}

# 规则2：media目录（前缀location，优先级低）
location /media/ {
    alias /home/xicheng2003/Printerify/media/;
}
```

**结果**：所有 `.pdf` 结尾的请求都被规则1拦截，去 `public_downloads` 目录找文件，找不到就404！

---

## 🔧 解决方案（三选一）

### 方案A：提高 /media/ 优先级（推荐）

在 `/media/` 前面加 `^~` 前缀：

```nginx
location ^~ /media/ {
    alias /home/xicheng2003/Printerify/media/;
    charset utf-8;  # 处理中文文件名
    
    # 根据URL参数动态设置Content-Disposition
    set $disposition "inline";
    if ($arg_download = "1") {
        set $disposition "attachment";
    }
    add_header Content-Disposition "$disposition; filename*=UTF-8''$uri" always;
    
    try_files $uri =404;
}
```

### 方案B：限制下载规则范围

修改正则规则，只匹配特定路径：

```nginx
# 改为：只匹配/downloads/路径下的文件
location ~* ^/downloads/.*\.(rar|zip|pdf|gz|7z)$ {
    root /home/xicheng2003/public_downloads;
    add_header Content-Disposition "attachment";
}
```

### 方案C：完全移除下载规则

如果不需要公共下载功能，直接删除或注释掉：

```nginx
# location ~* \.(rar|zip|pdf|gz|7z)$ {
#     root /home/xicheng2003/public_downloads;
#     add_header Content-Disposition "attachment";
# }
```

---

## 🚀 立即执行（5分钟完成）

### 步骤1：编辑Nginx配置

```bash
sudo nano /etc/nginx/sites-available/printerify
```

找到这两行：
```nginx
location /media/ {
    alias /home/xicheng2003/Printerify/media/;
}
```

改为：
```nginx
location ^~ /media/ {
    alias /home/xicheng2003/Printerify/media/;
    charset utf-8;
    
    # 动态设置Content-Disposition
    set $disposition "inline";
    if ($arg_download = "1") {
        set $disposition "attachment";
    }
    add_header Content-Disposition "$disposition; filename*=UTF-8''$uri" always;
    
    try_files $uri =404;
}
```

找到这一段：
```nginx
location ~* \.(rar|zip|pdf|gz|7z)$ {
    root /home/xicheng2003/public_downloads;
    add_header Content-Disposition "attachment";
}
```

改为（三选一）：
```nginx
# 选项1：限制范围
location ~* ^/downloads/.*\.(rar|zip|pdf|gz|7z)$ {
    root /home/xicheng2003/public_downloads;
    add_header Content-Disposition "attachment";
}

# 选项2：完全注释掉
# location ~* \.(rar|zip|pdf|gz|7z)$ {
#     root /home/xicheng2003/public_downloads;
#     add_header Content-Disposition "attachment";
# }
```

### 步骤2：测试并重载

```bash
# 测试配置
sudo nginx -t

# 如果显示 "syntax is okay"，重载
sudo systemctl reload nginx
```

### 步骤3：立即测试

访问一个实际的文件链接：
```
https://print.morlight.top/media/order_documents/2025-10-17/P-092/Group_37/01_26%E8%82%96%E7%A7%80%E8%8D%A3%E8%83%8C%E8%AF%B5%E8%B5%A0%E5%93%81.pdf
```

---

## 🔍 如果仍然不行

### 检查1：确认Nginx加载了新配置

```bash
sudo nginx -T | grep -A 5 "location.*media"
```

应该看到 `^~` 前缀。

### 检查2：确认文件确实存在

```bash
ls -la /home/xicheng2003/Printerify/media/order_documents/2025-10-17/P-092/Group_37/
```

### 检查3：查看错误日志

```bash
sudo tail -50 /var/log/nginx/error.log
```

### 检查4：检查权限

```bash
# 文件所有者应该是 xicheng2003 或 www-data
ls -l /home/xicheng2003/Printerify/media/order_documents/2025-10-17/P-092/Group_37/01_26*.pdf

# 如果权限不对，修复：
sudo chown -R xicheng2003:www-data /home/xicheng2003/Printerify/media/
sudo chmod -R 755 /home/xicheng2003/Printerify/media/
```

---

## 📋 完整的优化配置（复制粘贴）

```nginx
server {
    server_name print.morlight.top;
    listen 127.0.0.1:8080;

    # 通用代理设置
    proxy_request_buffering off;
    proxy_buffering off;
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
    proxy_read_timeout 300s;
    
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
    proxy_set_header X-Forwarded-Host $server_name;
    proxy_set_header X-Forwarded-Server $server_name;
    proxy_set_header X-Forwarded-Port $server_port;

    client_max_body_size 200M;

    # ========== 关键修复：提高media优先级 ==========
    location ^~ /media/ {
        alias /home/xicheng2003/Printerify/media/;
        charset utf-8;
        try_files $uri =404;
        
        types {
            application/pdf pdf;
            image/jpeg jpg jpeg;
            image/png png;
        }
        
        expires 7d;
        add_header Cache-Control "public";
        autoindex off;
    }

    location ^~ /static/ {
        alias /home/xicheng2003/Printerify/staticfiles/;
        expires 30d;
        charset utf-8;
    }

    # ========== 限制下载规则范围（或完全注释掉） ==========
    # 选项1：限制到/downloads/路径
    location ~* ^/downloads/.*\.(rar|zip|pdf|gz|7z)$ {
        root /home/xicheng2003/public_downloads;
        add_header Content-Disposition "attachment";
    }
    
    # 选项2：完全禁用
    # location ~* \.(rar|zip|pdf|gz|7z)$ {
    #     root /home/xicheng2003/public_downloads;
    #     add_header Content-Disposition "attachment";
    # }

    # Admin（优先级最高）
    location /admin {
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    # API
    location /api/ {
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    # OAuth
    location ~ ^/(accounts|auth|social)/ {
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    # Vue前端
    location / {
        root /home/xicheng2003/Printerify/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## ✅ 修复前后对比

### 修复前
```
请求: /media/order_documents/.../file.pdf
↓
匹配到: location ~* \.(pdf)$ (正则优先级高)
↓
查找: /home/xicheng2003/public_downloads/media/order_documents/.../file.pdf
↓
结果: 404 Not Found ❌
```

### 修复后
```
请求: /media/order_documents/.../file.pdf
↓
匹配到: location ^~ /media/ (^~提高优先级)
↓
查找: /home/xicheng2003/Printerify/media/order_documents/.../file.pdf
↓
结果: 200 OK ✅
```

---

## 🎯 预期效果

修复后立即生效：
- ✅ 点击文件链接正常下载
- ✅ 中文文件名正确显示
- ✅ 不会再出现404错误
- ✅ 其他功能不受影响

---

**估计修复时间：** 5分钟  
**需要重启服务：** 否（只需 `nginx reload`）  
**是否影响现有功能：** 否
