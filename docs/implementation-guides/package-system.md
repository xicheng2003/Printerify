# Printerify 打印套餐系统实施文档

## 📋 系统概述

成功为 Printerify 实施了完整的打印套餐功能，用户可以预充值购买页数套餐，享受折扣优惠并在打印时使用余额抵扣。

---

## 💰 套餐定价方案

| 套餐名称 | 包含页数 | 原价 | 折扣率 | 实际售价 | 单页成本 | 节省金额 |
|---------|---------|------|--------|---------|---------|---------|
| **基础版** | 100页 | ¥15.00 | 95折 | **¥14.20** | ¥0.142/页 | ¥0.80 |
| **标准版** | 300页 | ¥45.00 | 90折 | **¥40.50** | ¥0.135/页 | ¥4.50 |
| **超值版** | 500页 | ¥75.00 | 85折 | **¥63.75** | ¥0.128/页 | ¥11.25 |
| **旗舰版** | 1000页 | ¥150.00 | 80折 | **¥120.00** | ¥0.120/页 | ¥30.00 |

### 套餐特点
- ✅ **永久有效**：套餐余额无过期时间
- ✅ **按需扣费**：实际打印多少页扣除多少页
- ✅ **余额累计**：多次购买余额自动累加
- ✅ **折扣递增**：页数越多折扣越大

---

## 🗄️ 数据库变更

### 1. User 模型扩展
```python
# 新增字段
page_balance = IntegerField(default=0)           # 账户页数余额
total_pages_purchased = IntegerField(default=0)  # 累计购买页数
total_pages_used = IntegerField(default=0)       # 累计使用页数
```

### 2. 新增模型

**Package（套餐模板）**
- 定义套餐名称、价格、页数、折扣率、有效期等

**UserPackage（用户已购套餐）**
- 记录用户购买的套餐及使用情况
- 状态：待支付/使用中/已过期/已用完/已取消

**Transaction（交易记录）**
- 记录所有余额变动（充值/消费/退款/管理员调整）
- 保存余额快照用于对账

---

## 🔌 API 端点

### 套餐相关
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/packages/` | 获取所有可用套餐 | 公开 |
| POST | `/api/packages/purchase/` | 购买套餐 | 需登录 |
| GET | `/api/user/packages/` | 获取用户套餐列表 | 需登录 |
| GET | `/api/user/balance/` | 获取用户余额信息 | 需登录 |
| GET | `/api/user/transactions/` | 获取交易记录 | 需登录 |
| POST | `/api/admin/packages/<id>/activate/` | 管理员激活套餐 | 管理员 |

### 订单创建扩展
```json
// POST /api/orders/ 新增字段
{
  "use_balance": true,  // 是否使用余额抵扣
  // ... 其他订单字段
}
```

---

## 🎨 前端页面

### 1. 套餐购买页面 (`/packages`)
- **文件**：`frontend/src/views/PackageView.vue`
- **功能**：
  - 展示所有可用套餐（卡片式布局）
  - 套餐对比（价格、折扣、节省金额）
  - 购买流程（选择支付方式 → 上传凭证 → 提交）
- **路由**：需在 `router/index.js` 中配置

### 2. 用户中心余额展示 (`/profile`)
- **文件**：`frontend/src/views/ProfileView.vue`（已修改）
- **功能**：
  - 显示剩余页数、累计购买、累计使用
  - 展示活跃套餐及进度条
  - 显示最近5条交易记录
  - "购买套餐"按钮跳转到套餐页面

### 3. 订单创建流程（待完善）
- **文件**：`frontend/src/components/order/Step2_Payment.vue`
- **需新增**：
  - 余额抵扣开关（复选框）
  - 显示可用余额和所需页数
  - 计算抵扣后的实际支付金额

---

## 🔄 业务流程

### 套餐购买流程
```
1. 用户浏览套餐页面，选择合适套餐
   ↓
2. 选择支付方式（微信/支付宝）并扫码支付
   ↓
3. 上传支付凭证并提交
   ↓
4. 创建 UserPackage 记录（状态：待支付）
   ↓
5. 管理员在 Django Admin 中审核支付凭证
   ↓
6. 管理员激活套餐
   ↓
7. 系统自动：
   - 更新 User.page_balance（增加页数）
   - 更新 UserPackage.status（使用中）
   - 创建 Transaction 记录（充值类型）
```

### 订单创建扣费流程
```
1. 用户上传文件并配置打印选项
   ↓
2. 用户在支付步骤选择"使用余额抵扣"
   ↓
3. 系统检查余额是否足够
   ↓
4. 创建订单时：
   - 计算总页数消耗
   - 扣除 User.page_balance
   - 增加 User.total_pages_used
   - 创建 Transaction 记录（消费类型）
   ↓
5. 订单创建成功，用户看到更新后的余额
```

---

## ⚙️ 部署步骤

### 1. 运行数据库迁移
```bash
cd c:\Users\lxc52\Desktop\printerify
python manage.py makemigrations
python manage.py migrate
```

### 2. 创建初始套餐（Django Shell）
```python
python manage.py shell

from api.models import Package
from decimal import Decimal

# 创建基础套餐
Package.objects.create(
    name="基础版",
    description="适合轻量用户，偶尔打印",
    pages=100,
    price=Decimal('14.20'),
    original_price=Decimal('15.00'),
    discount_rate=Decimal('95'),
    is_active=True,
    sort_order=1
)

Package.objects.create(
    name="标准版",
    description="适合日常使用，性价比高",
    pages=300,
    price=Decimal('40.50'),
    original_price=Decimal('45.00'),
    discount_rate=Decimal('90'),
    is_active=True,
    is_featured=True,  # 推荐套餐
    sort_order=2
)

Package.objects.create(
    name="超值版",
    description="适合重度用户，大量打印",
    pages=500,
    price=Decimal('63.75'),
    original_price=Decimal('75.00'),
    discount_rate=Decimal('85'),
    is_active=True,
    sort_order=3
)

Package.objects.create(
    name="旗舰版",
    description="适合企业用户，海量打印",
    pages=1000,
    price=Decimal('120.00'),
    original_price=Decimal('150.00'),
    discount_rate=Decimal('80'),
    is_active=True,
    sort_order=4
)
```

### 3. 配置前端路由
在 `frontend/src/router/index.js` 中添加：
```javascript
{
  path: '/packages',
  name: 'packages',
  component: () => import('../views/PackageView.vue'),
  meta: { requiresAuth: false }
}
```

### 4. 更新导航菜单
在主导航中添加"套餐"链接，指向 `/packages`

---

## 🧪 测试要点

### 功能测试
1. **套餐购买**
   - ✅ 浏览套餐列表，信息显示正确
   - ✅ 购买流程完整（支付方式选择、凭证上传、提交）
   - ✅ 管理员激活后余额正确增加

2. **余额使用**
   - ✅ 个人中心余额正确显示
   - ✅ 订单创建时余额抵扣功能正常
   - ✅ 余额不足时提示正确
   - ✅ 交易记录准确记录

3. **管理后台**
   - ✅ 套餐管理（创建、编辑、启用/禁用）
   - ✅ 用户套餐审核（查看凭证、激活）
   - ✅ 交易记录查询和导出

### 边界测试
- 余额为0时无法使用抵扣
- 余额不足时显示清晰提示
- 重复激活套餐的防护
- 并发购买套餐的数据一致性

---

## 📊 后续优化建议

### 第一阶段（当前已完成）
- ✅ 基础套餐功能
- ✅ 余额抵扣
- ✅ 管理后台

### 第二阶段（建议3个月后）
- 🔄 在线支付集成（微信/支付宝 SDK）
- 🔄 自动到账（无需人工审核）
- 🔄 套餐有效期管理
- 🔄 会员等级体系

### 第三阶段（建议6个月后）
- 🔄 优惠券系统
- 🔄 积分系统
- 🔄 推荐奖励
- 🔄 套餐自动续费

---

## 📝 注意事项

1. **安全性**
   - 所有余额操作都有 Transaction 记录，可追溯
   - 套餐激活需要管理员审核，防止刷单
   - 订单创建时使用数据库事务，确保数据一致性

2. **用户体验**
   - 套餐永久有效，降低用户心理负担
   - 折扣直观展示，刺激大额购买
   - 余额抵扣可选，灵活支付

3. **运营策略**
   - 定期推出限时优惠套餐
   - 针对大客户提供定制套餐
   - 通过数据分析优化套餐定价

---

## 🆘 常见问题

**Q: 套餐余额可以退款吗？**
A: 当前版本不支持退款。建议在用户协议中明确说明"套餐余额一经充值不可退款"。

**Q: 如何调整套餐价格？**
A: 在 Django Admin 中修改 Package 模型的价格字段即可。历史购买的套餐价格不受影响。

**Q: 用户删除账号后余额如何处理？**
A: 当前 User 模型与 Transaction 关联使用 CASCADE，删除用户会同时删除交易记录。建议实施软删除或余额转移机制。

**Q: 如何防止恶意刷单？**
A: 
1. 所有套餐购买需上传支付凭证
2. 管理员人工审核后才激活
3. 可在 UserPackage 模型中添加 IP 地址、设备指纹等字段
4. 对同一用户短时间内大量购买套餐设置告警

---

## 📞 技术支持

如有问题，请查看：
1. Django Admin: `/admin/`（管理套餐、审核购买）
2. API文档: `/api/` （查看所有端点）
3. 日志文件: `django.log`（排查错误）

更新时间：2025-12-04
