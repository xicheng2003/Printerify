# Printerify 法律文档软编码方案说明

## 1. 方案目标
- 实现服务条款、隐私协议等法律文档的内容“软编码”，做到一次维护、多处复用。
- 支持内容在不同页面（如关于页、下单页弹窗等）以不同样式展示。
- 便于后期维护和内容更新，支持非技术人员直接编辑。

## 2. 技术实现

### 2.1 Markdown 作为唯一内容源
- 所有法律文档内容均以 Markdown 文件（如 `terms-of-service.md`、`privacy-policy.md`）存放于 `frontend/public/legal/` 目录。
- Markdown 格式便于内容编辑、版本管理和多语言扩展。

### 2.2 运行时动态加载与渲染
- 前端通过 `useMarkdown.js` composable 动态加载并解析 Markdown 文件，自动缓存结果。
- 解析使用 `markdown-it`，支持标题、列表、加粗、链接等常用格式。

### 2.3 复用型渲染组件
- `src/components/legal/LegalDocument.vue` 组件负责渲染法律文档。
- 支持 `type`（文档类型：terms/privacy）、`mode`（展示模式：full/compact）等参数，适配不同页面需求。
- 组件自动从 public 目录加载对应 Markdown 文件，无需重复维护内容。

### 2.4 页面集成
- 在下单页（HomeView.vue）和关于页（TermsView.vue）均已集成 `LegalDocument` 组件。
- 弹窗、整页等不同场景通过 `mode` 参数切换样式。

## 3. 维护指南

### 3.1 如何修改法律文档内容？
1. 直接编辑 `frontend/public/legal/terms-of-service.md` 或 `privacy-policy.md` 文件。
2. 保存后，前端页面会自动加载最新内容，无需重启服务。

### 3.2 如何新增其他法律文档？
1. 在 `public/legal/` 目录下新增 Markdown 文件（如 refund-policy.md）。
2. 在需要展示的页面引入 `LegalDocument` 组件，传入对应 type 或自定义 src 路径。

### 3.3 样式调整
- 可在 `LegalDocument.vue` 组件内调整全局/局部样式，支持响应式和主题切换。
- 支持通过 mode 参数自定义不同场景下的字号、间距等。

### 3.4 依赖说明
- 依赖 `markdown-it` 进行 Markdown 解析。
- 依赖 Vue3 组件机制。

## 4. 典型用法示例

```vue
<!-- 弹窗中展示服务条款 -->
<LegalDocument type="terms" mode="compact" />

<!-- 关于页面整页展示隐私协议 -->
<LegalDocument type="privacy" mode="full" />
```

## 5. 方案优势
- 内容维护极简，支持多人协作和版本管理。
- 复用性强，适配多种展示场景。
- 支持未来多语言和更多法律文档扩展。

---
如需进一步扩展或遇到问题，请联系前端开发维护者。
