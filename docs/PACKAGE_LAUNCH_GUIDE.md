# 打印套餐系统上线指南

## ✅ 系统已完成

所有开发工作已完成！数据库迁移也已成功执行。

---

## 🚀 快速上线步骤

### 1. 创建初始套餐数据（3分钟）

在项目根目录打开 Django Shell：

```bash
python manage.py shell
```

复制粘贴以下代码创建4个套餐：

```python
from api.models import Package
from decimal import Decimal

# 基础版
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

# 标准版（推荐）
Package.objects.create(
    name="标准版",
    description="适合日常使用，性价比高",
    pages=300,
    price=Decimal('40.50'),
    original_price=Decimal('45.00'),
    discount_rate=Decimal('90'),
    is_active=True,
    is_featured=True,  # 标记为推荐
    sort_order=2
)

# 超值版
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

# 旗舰版
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

print("✅ 套餐创建成功！")
exit()
```

### 2. 启动开发服务器（2分钟）

**后端（Django）：**
```bash
# Terminal 1
cd c:\Users\lxc52\Desktop\printerify
python manage.py runserver
```

**前端（Vue）：**
```bash
# Terminal 2
cd c:\Users\lxc52\Desktop\printerify\frontend
npm run dev
```

**Celery（异步任务）：**
```bash
# Terminal 3 (Windows)
cd c:\Users\lxc52\Desktop\printerify
celery -A backend worker -l info -P eventlet
```

### 3. 测试完整流程（5分钟）

#### 测试1：浏览套餐页面
1. 访问：http://localhost:5173/packages
2. 检查4个套餐是否正确显示
3. 查看折扣、价格计算是否正确

#### 测试2：购买套餐
1. 登录用户账号
2. 点击"立即购买"按钮
3. 选择支付方式（微信/支付宝）
4. 上传支付凭证
5. 提交订单

#### 测试3：管理员审核
1. 访问：http://localhost:8000/admin/
2. 进入"用户套餐"管理页面
3. 找到刚才创建的套餐购买记录
4. 查看支付凭证
5. 点击"激活选中的待审核套餐"按钮

#### 测试4：查看余额
1. 返回前端，访问：http://localhost:5173/profile
2. 查看"账户余额"卡片
3. 确认页数余额是否正确增加

#### 测试5：使用余额下单
1. 访问：http://localhost:5173/order
2. 上传文件并配置打印选项
3. 进入支付步骤
4. 勾选"使用余额抵扣"
5. 确认创建订单
6. 返回个人中心查看余额是否正确扣除

---

## 📋 功能清单

### 用户端功能
- ✅ 浏览套餐列表（`/packages`）
- ✅ 购买套餐（支付凭证上传）
- ✅ 查看余额信息（个人中心）
- ✅ 查看活跃套餐和剩余页数
- ✅ 查看交易记录（最近10条）
- ✅ 下单时使用余额抵扣
- ✅ 余额不足提示和引导充值

### 管理端功能
- ✅ 套餐管理（创建/编辑/启用/禁用）
- ✅ 用户套餐审核（查看凭证/激活）
- ✅ 交易记录查询
- ✅ 用户余额管理

---

## 🎨 页面路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/packages` | 套餐购买页面 | 展示所有可用套餐 |
| `/profile` | 个人中心 | 显示余额和交易记录 |
| `/order` | 订单创建 | 支持余额抵扣 |
| `/admin/api/package/` | 套餐管理 | Django Admin |
| `/admin/api/userpackage/` | 套餐审核 | Django Admin |
| `/admin/api/transaction/` | 交易记录 | Django Admin |

---

## 💰 套餐定价

| 套餐 | 页数 | 原价 | 售价 | 折扣 | 单页成本 |
|------|------|------|------|------|---------|
| 基础版 | 100页 | ¥15.00 | ¥14.20 | 95折 | ¥0.142/页 |
| 标准版 | 300页 | ¥45.00 | ¥40.50 | 90折 | ¥0.135/页 |
| 超值版 | 500页 | ¥75.00 | ¥63.75 | 85折 | ¥0.128/页 |
| 旗舰版 | 1000页 | ¥150.00 | ¥120.00 | 80折 | ¥0.120/页 |

---

## 🔍 常见问题

### Q1: 套餐购买后用户看不到余额？
**A:** 确保管理员在 Django Admin 中激活了套餐。只有激活后余额才会充值到用户账户。

### Q2: 下单时无法使用余额抵扣？
**A:** 检查：
1. 用户是否已登录
2. 用户余额是否大于订单所需页数
3. 是否勾选了"使用余额抵扣"复选框

### Q3: 如何修改套餐价格？
**A:** 在 Django Admin 的"打印套餐"管理页面中直接编辑。历史购买不受影响。

### Q4: 余额可以退款吗？
**A:** 当前版本不支持退款。建议在服务条款中明确说明。

### Q5: 如何查看某个用户的余额变动历史？
**A:** 在 Django Admin 的"交易记录"页面，使用用户名或邮箱搜索即可。

---

## 📊 运营建议

### 初期推广（第1-2个月）
- 🎁 新用户首次购买享9折优惠码
- 📢 在首页显著位置推广套餐
- 💡 对高频用户推送套餐购买提醒

### 中期优化（第3-6个月）
- 📈 根据销售数据调整套餐配置
- 🎯 针对不同用户群体推出定制套餐
- 🏆 推出限时优惠套餐（如双11特惠）

### 长期发展（6个月后）
- 💳 接入在线支付（微信/支付宝SDK）
- 🤖 自动到账，无需人工审核
- 👥 推出推荐奖励计划
- 🎖️ 会员等级体系

---

## 🛡️ 安全提示

1. **生产环境部署前：**
   - 修改 `SECRET_KEY`
   - 设置 `DEBUG = False`
   - 配置 ALLOWED_HOSTS
   - 启用 HTTPS

2. **数据备份：**
   - 定期备份数据库
   - 备份支付凭证图片
   - 导出交易记录留存

3. **监控告警：**
   - 监控异常购买行为（如短时间大量购买）
   - 监控余额异常变动
   - 设置管理员邮件通知

---

## 📞 技术支持

如遇到问题，请检查：
1. **后端日志**：查看 `django.log` 文件
2. **浏览器控制台**：查看前端错误信息
3. **Django Admin**：`/admin/` 查看数据状态

详细文档：`docs/implementation-guides/package-system.md`

---

## 🎉 恭喜！

打印套餐系统已完成开发并可以上线使用！

**最后检查清单：**
- [x] 数据库迁移完成
- [x] 套餐数据已创建
- [x] 前后端服务正常运行
- [x] 测试流程通过
- [ ] 生产环境部署（如需要）

祝运营顺利！ 🚀
