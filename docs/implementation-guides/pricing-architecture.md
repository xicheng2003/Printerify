# 计费逻辑架构与维护指南

## 1. 概述

本项目采用**“后端主导，前端渲染”**的计费架构。所有的价格配置（基础服务费、打印单价、装订费）均由后端统一管理，前端在初始化时动态获取配置并进行渲染和计算。

这种架构解决了“双重维护”的问题，确保了价格调整的灵活性和一致性。

## 2. 架构设计

### 2.1 后端 (Source of Truth)

*   **配置文件**: `api/services/pricing.py`
    *   定义了 `PRICE_CONFIG` 字典，包含所有价格信息。
    *   这是整个系统价格的**唯一数据源**。
*   **API 接口**: `GET /api/config/pricing/`
    *   由 `api/views.py` 中的 `get_pricing_config` 视图提供。
    *   直接返回 `PRICE_CONFIG` 的 JSON 数据。

### 2.2 前端 (Consumer)

*   **API 服务**: `frontend/src/services/apiService.js`
    *   `getPricingConfig()` 方法负责调用后端接口。
*   **状态管理**: `frontend/src/stores/order.js`
    *   `pricingConfig` state: 存储从后端获取的配置。
    *   `fetchPricingConfig()` action: 初始化时调用 API 并更新 state。
    *   `totalCost` getter: 使用 `pricingConfig` 中的数据动态计算订单总价。
*   **UI 展示**: `frontend/src/views/HomeView.vue`
    *   在 `onMounted` 生命周期钩子中调用 `orderStore.fetchPricingConfig()`。
    *   “计费规则说明”模态框使用 `v-for` 动态渲染价格表，不再硬编码 HTML。

## 3. 维护指南

### 3.1 如何修改价格？

**只需修改后端一个文件即可。**

1.  打开 `api/services/pricing.py`。
2.  找到 `PRICE_CONFIG` 字典。
3.  修改对应的数值。
    *   例如，将 A4 黑白单面价格从 `0.15` 改为 `0.20`：
        ```python
        'a4_70g': {
            'black_white': {
                'single': Decimal('0.20'), # 修改这里
                ...
            }
        }
        ```
4.  重启后端服务（如果是开发环境，通常会自动重载）。
5.  前端刷新页面后，会自动获取并显示新价格，计算逻辑也会立即生效。

### 3.2 如何添加新的纸张规格？

1.  **后端**: 在 `api/services/pricing.py` 的 `PRICE_CONFIG['print']` 中添加新的键值对（例如 `a3_80g`）。
2.  **前端**:
    *   在 `frontend/src/views/HomeView.vue` 的 `formatPaperSize` 函数中添加新规格的中文映射。
    *   在 `frontend/src/components/OrderConfiguration.vue` (或相关组件) 的下拉菜单中添加新选项（如果下拉菜单也是动态生成的则无需此步，目前下拉菜单可能还需要手动添加选项）。

### 3.3 如何添加新的装订方式？

1.  **后端**: 在 `api/services/pricing.py` 的 `PRICE_CONFIG['binding']` 中添加新的键值对。
2.  **前端**:
    *   在 `frontend/src/views/HomeView.vue` 的 `formatBindingType` 函数中添加中文映射。
    *   确保 `OrderConfiguration` 组件能支持选择新类型。

## 4. 故障排查

*   **前端显示“正在加载计费规则...”且不消失**:
    *   检查网络请求 `GET /api/config/pricing/` 是否成功。
    *   检查后端服务是否运行正常。
*   **价格计算显示为 NaN 或错误**:
    *   检查 `api/services/pricing.py` 中的数值是否为有效的 `Decimal` 或数字类型。
    *   检查前端 `order.js` 中的 `totalCost` 计算逻辑是否正确处理了空值或缺失的配置键。

## 5. 代码索引

*   **后端配置**: `api/services/pricing.py`
*   **后端视图**: `api/views.py` (`get_pricing_config`)
*   **前端 Store**: `frontend/src/stores/order.js`
*   **前端 View**: `frontend/src/views/HomeView.vue`
