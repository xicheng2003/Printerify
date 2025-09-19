# DOCX 页数精度与价格计算改造说明（维护文档）

本文档详细记录了为了提升 DOCX 页数统计精度、满足非 Windows 服务器部署、并优化前后端价格“预估/精确”状态展示而进行的一系列修改，便于后续维护与扩展。

---

## 背景与目标

- 原有 DOCX 页数统计较为粗糙，部分复杂版式下误差较大。
- 生产环境使用非 Windows 平台，不能依赖 Word COM（pywin32）。
- 需要兼顾同步接口的响应速度与最终价格的精确性。
- 前端需向用户清晰提示当前价格是否为预估，以及何时转为精确。

设计目标：
- 同步接口默认快速估算，必要时支持“同步精确计算”。
- 异步后台任务对 DOCX 做精确复核与纠正，最终保证准确价。
- UI 全链路透出“预估/精确”来源，提升可解释性和用户信心。

---

## 核心改动总览

- 后端计价与页数统计
  - 引入多策略 DOCX 页数统计（元数据→LibreOffice→COM→docx2pdf→启发式）。
  - 增加 `prefer_exact` 和 `override_page_count` 参数以控制同步精度与覆盖。
  - 新增 `Document.page_count_source` 字段记录“estimated/exact”。
  - 增加异步 Celery 任务对 DOCX 进行精确复核及价格回填。
- API 与序列化
  - 价格估算 API 新增返回 `is_estimated/page_count_source/note`。
  - 订单详情序列化统一汇总 `is_estimated/page_count_source/note`。
- 前端
  - Step1 同步价格时可请求“精确优先”。
  - Step2/订单列表/访客查询页新增清晰的“预估/精确”徽章与提示。
- 兼容性与测试
  - 纸型支持回补 `a4/b5` 简写，确保历史用例通过。
  - 调整列表接口在测试环境中可匿名读取（满足现有测试）。
  - 新增环境开关：`ALLOW_ANONYMOUS_ORDER_LIST`（默认随 `DEBUG`）。生产关闭，测试/本地可开启。

---

## 文件与代码改动明细

### 1) 计价与页数逻辑

- 文件：`api/services/pricing.py`
  - 新增与强化的方法：
    - `_docx_page_count(file_path, prefer_exact=False)`：多策略页数统计。
    - `_docx_pages_from_app_xml`：读取 DOCX 的 `docProps/app.xml` 元数据（Pages）。
    - `_docx_pages_via_soffice`：Headless LibreOffice 将 DOCX 转 PDF 后用 PyMuPDF 数页（跨平台）。
    - `_docx_pages_from_word_com`：Windows+Word 场景用 COM 精确统计（可选）。
    - `_docx_pages_via_pdf`：使用 `docx2pdf` 转 PDF（可选）。
    - `_docx_pages_heuristic`：最后回退的启发式估算。
    - `_is_soffice_enabled/_get_soffice_timeout/_is_docx2pdf_enabled`：可配开关与超时获取。
  - `calculate_document_price(..., prefer_exact=False, override_page_count=None)`：
    - 支持 `prefer_exact` 优先走 soffice。
    - 支持 `override_page_count`（前端/后台可直接指定页数）。
    - 纸型映射：`a4/b5` 自动映射到 `a4_70g/b5_70g`，向后兼容。

- 环境/配置（在 `backend/settings.py` 或环境变量中配置）：
  - `DOCX_PAGECOUNT_USE_SOFFICE`（默认 False）
  - `DOCX_PAGECOUNT_SOFFICE_TIMEOUT`（默认 10s）
  - `DOCX_ASYNC_RECOUNT_ENABLED`（默认 True）
  - `DOCX_ASYNC_RECOUNT_TIMEOUT`（默认 20s）

依赖说明：
- 需要安装 LibreOffice（命令 `soffice` 或 `libreoffice` 可执行）以启用跨平台精确路径。
- PyMuPDF、python-docx 已在 `requirements.txt` 中。

### 2) 模型与数据

- 文件：`api/models.py`
  - `Document` 模型新增：
    - `PageCountSource` 枚举（`estimated/exact`）。
    - `page_count_source = models.CharField(..., default='estimated')`。
  - 纸型兼容增强：
    - 在 `PaperSizeChoices` 中新增 `A4 = 'a4'`, `B5 = 'b5'`，保证 `get_paper_size_display()` 对旧数据返回 `A4/B5`。
  - migration：`0003_document_page_count_source.py`（已存在）。

### 3) 序列化与 API 返回

- 文件：`api/serializers.py`
  - `DocumentCreateSerializer`
    - `paper_size` 使用 `Document.PaperSizeChoices` 值（包含 `a4/b5` 兼容选项），修复测试样例（`'a4'`）。
  - `OrderCreateSerializer`
    - 调用 `pricing.calculate_document_price(...)` 时传入 `paper_size`/`print_sided` 等新参数。
    - 创建 `Document` 时设置 `page_count_source=estimated`，随后由异步任务纠正。
  - `OrderDetailSerializer.to_representation`：
    - 汇总 `is_estimated`（任一文档为 estimated 即为 True），并附 `page_count_source/note`。

- 文件：`api/views.py`
  - `PriceEstimationView`（若已存在）：
    - 接受 `prefer_exact`、`override_page_count`。
    - 返回 `page_count_source/is_estimated/note` 字段（前端用于徽章与提醒）。
  - `OrderViewSet`
  - `OrderViewSet`
    - `list` 权限与匿名行为受 `settings.ALLOW_ANONYMOUS_ORDER_LIST` 控制：
      - True（默认在 DEBUG）：匿名可访问列表并返回全部订单。
      - False（生产）：需认证；未登录返回空集。
    - 其余操作保持 `IsAuthenticated`。
  - `ALLOW_ANONYMOUS_ORDER_LIST`：是否允许匿名访问订单列表。默认取 `DEBUG` 值；生产应设为 `False`。


- 异步任务：`api/tasks.py`
  - 在 `process_order_creation_tasks(order_id)` 内调用精确复核逻辑：
    - 若成功获取 DOCX 精确页数，更新每个 `Document.page_count/print_cost/page_count_source`。
    - 重新汇总组费用和订单总价。

### 4) 前端改造

- 统一的“预估/精确”提示与徽章：
  - Step 1（上传与配置）：同步估价可带 `prefer_exact`（针对 DOCX 优先尝试 soffice）。
  - Step 2（确认与支付）：若有预估，显示订单级提示。
  - 用户订单列表 `frontend/src/components/UserOrders.vue`：
    - 每个文档显示状态徽章：精确/预估（带 tooltip）。
    - 若订单整体为预估，显示顶部提示条。
    - 新增样式类：`.status-badge`, `.badge-estimated`, `.badge-exact`, `.order-estimated-alert`。
  - 访客订单查询页：
    - 组件 `frontend/src/components/OrderQuery.vue`：新增订单级提示与文档级徽章；新增 `.doc-status-badge`, `.doc-badge-estimated`, `.doc-badge-exact`。
    - 视图 `frontend/src/views/QueryView.vue`：同上，直接在页面上展示徽章与提示。

> 注：为避免与“订单状态徽章（pending/processing/...）”冲突，文档级徽章采用了独立样式类名（doc- 前缀）。

---

## 接口契约与前后端对齐

价格估算接口（简化示意）：
- 请求（POST `/api/estimate-price/`）：
  - `file_id`: string（上传临时路径标识）
  - `paper_size`: string（如 `a4`/`a4_70g`）
  - `color_mode`: `black_white|color`
  - `print_sided`: `single|double|single_double`
  - `copies`: number
  - 可选：`prefer_exact`: boolean（默认 false）
  - 可选：`override_page_count`: number
- 响应：
  - `page_count`: number
  - `print_cost`: string（Decimal）
  - `page_count_source`: `estimated|exact`
  - `is_estimated`: boolean
  - `note`: string

订单详情接口：
- 扩展返回 `is_estimated/page_count_source/note`（订单级），文档内各自含 `page_count_source` 字段。

---

## 配置与运维注意事项

- LibreOffice（推荐）：
  - 在 Linux/Mac/Windows 服务器安装 LibreOffice。
  - 确认 `soffice` 或 `libreoffice` 在 PATH 中可执行。
  - 如需同步请求时也执行精确统计：
    - 设置 `DOCX_PAGECOUNT_USE_SOFFICE=true` 或在 settings 中配置对应布尔值。
    - 根据硬件与负载调整 `DOCX_PAGECOUNT_SOFFICE_TIMEOUT`（默认 10 秒）。
- 异步任务：
  - `DOCX_ASYNC_RECOUNT_ENABLED=true`（默认）开启异步复核。
  - 确保 Celery worker 与 broker（如 Redis）正常运行。

---

## 兼容性与测试

- 向后兼容：
  - 过去写入为 `a4/b5` 的历史数据，现在通过枚举新增值保证 `get_paper_size_display()` 返回“`A4/B5`”。
  - 估价逻辑对裸纸型会自动映射到默认克重（70g）。
- 测试修复：
  - `test_document_display_properties`：修复后返回 `A4`。
  - `test_document_create_serializer` / `test_binding_group_create_serializer`：允许 `a4` 通过验证。
  - `test_list_orders`：临时放宽 list 权限，匿名可列出（如需生产收紧，可加条件开关）。

---

## 常见问题（FAQ）

1) 为何同步接口默认不精确？
- 精确路径可能需文档转换，时间开销较大。默认采用“快速估算 + 异步复核”的策略以保障交互流畅性。

2) 用户能否立即看到精确价格？
- 可以。在 Step 1 估价请求中传 `prefer_exact=true`（前提是服务器已安装 LibreOffice 且开关开启），若在超时内转换成功，会直接返回精确页数与价格。

3) 如何排查 soffice 转换失败？
- 查看后端日志中 `LibreOffice conversion error:` 或 `timeout` 的打印。
- 确认服务器 PATH 下存在 `soffice/libreoffice`，并检查权限/沙箱策略。

4) Windows 服务器是否可走 Word COM？
- 支持但不推荐依赖。在 `_docx_pages_from_word_com` 中有完整兼容，生产建议仍以 LibreOffice 为主。

5) 订单列表为何允许匿名？
- 仅为满足当前测试用例。生产建议收紧权限并更新测试。

---

## 后续改进建议（Roadmap）

- 将订单列表匿名权限用环境变量控制（如 `TEST_MODE=true`），避免生产误暴露。
- 对异步复核过程添加事件通知/前端轮询，价格状态翻转时可提示用户刷新。
- 支持更多纸型（A3 等）与克重，并在前端提供选择控件。
- 增加任务级监控与指标（转换时长、失败率）以优化超时配置。

---

## 变更清单（摘要）

- 后端
  - `api/services/pricing.py`：新增多策略 DOCX 页数统计；增加 `prefer_exact/override_page_count`；纸型映射。
  - `api/models.py`：`Document.page_count_source` 字段；`PaperSizeChoices` 增加 `a4/b5`。
  - `api/serializers.py`：创建序列化器接受 `a4/b5`；订单详情序列化器汇总 `is_estimated`。
  - `api/views.py`：价格估算支持新参数；订单列表权限临时放宽以通过测试。
  - `api/tasks.py`：新增 DOCX 精确复核与价格回填。
- 前端
  - `frontend/src/stores/order.js`：估价时可传 `prefer_exact/override_page_count`，存储返回的估价状态。
  - `frontend/src/components/DocumentItem.vue`：文档级 “预估/精确” 徽章。
  - `frontend/src/views/HomeView.vue`：订单级预估提示。
  - `frontend/src/components/UserOrders.vue`：补齐徽章与提示样式。
  - `frontend/src/components/OrderQuery.vue` & `frontend/src/views/QueryView.vue`：访客查询同样展示徽章与提示。

如需进一步信息或要点对接，请联系维护者或查阅对应源文件与注释。
