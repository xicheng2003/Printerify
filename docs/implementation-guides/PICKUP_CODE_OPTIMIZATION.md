# 取件码生成逻辑优化与并发安全实施方案

## 1. 背景与问题

在原有的系统中，取件码（Pickup Code）的生成逻辑是基于“当前最大值递增”的策略（例如：P-066 -> P-067）。在实际生产环境和高并发场景下，这种方案暴露出了两个主要问题：

1.  **业务误导性 (Business Logic Issue)**:
    *   如果最新的订单（如 P-100）被删除，下一个生成的订单会回退使用 P-100。
    *   这会导致用户或操作员困惑，误以为是旧订单，或者在打印店场景中导致取件混乱。
    *   顺序号容易暴露每日单量，存在隐私泄露风险。

2.  **并发安全隐患 (Concurrency Issue)**:
    *   在高并发下，两个请求可能同时读取到相同的“最大值”，从而生成完全相同的取件码。
    *   虽然数据库字段可能有唯一性约束，但这会导致其中一个请求直接报错（500 Internal Server Error），用户体验极差。

## 2. 解决方案概述

我们实施了一套全新的 **“随机生成 + 乐观锁重试 + 数据库约束”** 方案。

### 2.1 核心策略变更

| 特性 | 旧方案 | 新方案 |
| :--- | :--- | :--- |
| **生成算法** | 顺序递增 (Max + 1) | **随机生成 (Random)** |
| **取值范围** | 066 - 666 | **010 - 999** |
| **冲突处理** | 无 (依赖应用层检查) | **自动重试 (Retry Loop)** |
| **唯一性保证** | 应用层 `exists()` 查询 | **数据库级 UniqueConstraint** |

## 3. 技术实现细节

### 3.1 随机生成策略 (`api/models.py`)

不再依赖数据库的历史状态，而是生成纯随机数。

```python
def generate_pickup_code():
    """
    生成一个在有效订单中唯一的取件码 (P-010 to P-999)。
    采用随机生成策略，避免因历史订单删除导致号码回退或重复的误导。
    """
    # ... 省略部分代码 ...
    
    # 尝试生成次数上限
    MAX_RETRIES = 50
    
    for _ in range(MAX_RETRIES):
        # 随机生成 10 - 999 之间的数字
        next_code_num = random.randint(10, 999)
        # ...
```

### 3.2 数据库级约束

为了防止应用层检查（`exists()`）在高并发下的“竞态条件”（Race Condition），我们在数据库层面添加了强制约束。

```python
class Order(models.Model):
    # ...
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pickup_code'],
                # 仅在订单处于活跃状态时要求唯一
                condition=models.Q(status__in=['pending', 'processing', 'completed']),
                name='unique_active_pickup_code'
            )
        ]
```

### 3.3 乐观锁重试机制 (`Order.save`)

我们将生成逻辑下沉到 Model 的 `save` 方法中，并利用 Django 的事务原子性实现自动重试。

**工作流程：**
1.  尝试生成一个随机码。
2.  尝试保存到数据库。
3.  如果数据库抛出 `IntegrityError`（说明运气不好，号码刚被别人抢了）：
    *   捕获异常。
    *   回滚当前保存点的事务。
    *   重新生成一个新的随机码。
    *   再次尝试保存。
4.  如果连续 5 次都失败（概率极低），才抛出异常。

```python
    def save(self, *args, **kwargs):
        if not self.pickup_code:
            max_retries = 5
            for attempt in range(max_retries):
                code_str, code_num = generate_pickup_code()
                self.pickup_code = code_str
                self.pickup_code_num = code_num
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return 
                except IntegrityError:
                    if attempt == max_retries - 1:
                        raise
                    continue
        else:
            super().save(*args, **kwargs)
```

## 4. 优势总结

1.  **用户体验提升**: 随机码消除了顺序误导，且范围扩大降低了重复感。
2.  **系统健壮性**: 即使在高并发下，系统也能自动处理冲突，不会直接报错给用户。
3.  **数据一致性**: 数据库级的约束是最后一道防线，确保绝对不会出现重复的有效取件码。
4.  **代码解耦**: 序列化器（Serializer）不再关心取件码的生成细节，只需调用 `create`，由模型层自动处理。

## 5. 部署说明

由于修改了 `Meta` 中的 `constraints`，部署时必须执行数据库迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```
