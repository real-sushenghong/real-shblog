# real-shenghong

> Personal technical blog and engineering knowledge base.

一个面向基础设施与 AI 系统工程的个人技术博客。

## 定位

**AI-Native Infrastructure Engineer**

构建生产级 AI 背后的基础设施、运行时与工程系统。

## 技术方向

* Kubernetes
* AI Infrastructure
* Agent Runtime
* GPU / DRA
* Linux
* Go
* Container Runtime
* Cloud Native

## 内容

博客主要记录：

* Kubernetes 与云原生基础设施
* AI Infrastructure 与 GPU 集群
* Agent / Runtime 系统设计
* Linux 与系统工程
* Go 工程实践
* 容器与运行时
* 开源项目与工程实践
* 技术研究与实践记录

## 技术栈

```text
Hugo
Go
Hugo Modules
Markdown
Podman
Ubuntu
Kubernetes
```

博客使用 **Hugo + Hugo Modules** 构建，开发环境基于 **VS Code + Podman + Ubuntu**。

## 项目结构

```text
real-shenghong/
├── .devcontainer/      # VS Code Dev Container
├── archetypes/         # Hugo content templates
├── assets/             # Assets
├── content/            # Blog content
├── data/               # Data files
├── layouts/            # Custom layouts
├── static/             # Static files
├── themes/             # Local theme overrides
├── hugo.toml           # Hugo configuration
├── go.mod              # Hugo Modules
├── go.sum              # Module checksums
└── README.md
```

## 本地开发

进入开发容器：

```bash
hugo server --bind 0.0.0.0
```

访问：

```text
http://localhost:1313
```

GitHub Actions 会在推送到 `main` 或提交 Pull Request 时自动检查 Hugo 配置并构建站点，构建结果会作为 workflow artifact 保存。

构建：

```bash
hugo
```

检查 Hugo Modules：

```bash
hugo mod graph
```

更新依赖：

```bash
hugo mod get -u
hugo mod tidy
```

## 设计原则

### 简洁

保持内容优先，减少不必要的视觉元素和复杂动画。

### 技术

以真实工程实践为核心，记录问题、设计、实现与验证过程。

### 长期

博客不仅用于发布文章，也作为个人长期技术知识库与工程记录。

### 开源

公开可分享的技术实践、工具和开源项目。

## Roadmap

* [x] Hugo 基础环境
* [x] Hugo Modules
* [x] Podman + Ubuntu 开发环境
* [x] VS Code Dev Container
* [ ] 个人主页
* [ ] 技术方向展示
* [ ] 精选项目
* [ ] 博客文章系统
* [ ] About 页面
* [ ] RSS
* [ ] Sitemap
* [ ] SEO
* [ ] 深色 / 浅色模式
* [ ] GitHub Pages / CI 自动部署

## License

Content and code are provided for personal and educational purposes unless otherwise specified.

---

## 神经网络分类关系图

`/categories/` 页面展示一个以 **shenghong** 为核心的三级力导向神经网络图，动态反映博客的分类、系列与文章之间的关联关系。

### 体系架构

```
                    Center (shenghong)
                   /      |      \      \
                  /       |       \      \
          Category   Category   Category  Resources
          /  |  \      / | \       |         \
         /   |   \    /  |  \      |          \
     Title Title Title Title Title Title     Title
       |            |       |
     Post         Post    Post ...
```

**四层节点：**

| 层级 | group 值 | 节点大小 | 颜色 | 说明 |
|------|----------|---------|------|------|
| 中心 | `center` | 28px | 金色 `#f0a040` | 固定画布中央，不可拖拽 |
| 分类 | 数字 `"1"`~`"8"` | 按文章数动态 | 分区色 | 来自 Hugo Taxonomy categories |
| 系列标题 | `title` | 10px | 继承父分类色 | 来自 `data/blog_links.yaml` |
| 文章 | `post` | 6px | 继承父分类色 | 来自 `content/posts/` |

### 数据来源

| 节点类型 | 数据源 | 生成方式 |
|----------|--------|---------|
| 中心 | 硬编码 | `id: "shenghong"`，固定在模板中 |
| 分类 | `.Site.Taxonomies.categories` | 遍历 Hugo 分类 taxonomy，自动生成 |
| Resources | 手动定义 | 不在 taxonomy 中，模板中单独添加（`id: "resources"`） |
| 系列标题 | `data/blog_links.yaml` | 遍历 `hugo.Data.blog_links`，自动生成 |
| 文章 | `.Site.RegularPages` (section `posts`) | 遍历所有已发布文章，自动生成 |

### 连线逻辑

| 连线 | source → target | 生成规则 |
|------|----------------|---------|
| 中心 → 分类 | `shenghong` → 每个 category | 固定，每个分类一条（含 resources） |
| 分类 → 系列标题 | category → title | 按 `blog_links.yaml` 中的 `category` 字段匹配 |
| 系列标题 → 文章 | title → post | 基于文章 front matter 的 `series` 字段精确匹配 |
| 分类共现 | category ↔ category | 分类在同一篇文章中共现的次数（原有逻辑） |

### 文章与系列标题的精确关联（series 字段）

每篇文章的 front matter 需要指定 `series` 字段：

```yaml
# content/posts/your-post.en.md
---
title: "Your Post Title"
categories:
  - cloud-native
series: kubernetes-tutorial   # 关联到 blog_links.yaml 中的对应标题
---
```

**匹配规则：**

1. 从 `blog_links.yaml` 中每个条目的 `url` 或 `title.en` 推导出 `slug`：
   - URL 是 `/series/xxx/` → slug = `xxx`
   - URL 是 `/posts/` → slug = `title.en` 的小写 + 空格转连字符
2. 文章的 `series` 字段与 title 的 `slug` 精确匹配后建立连线

**示例：**

| 文章 series 值 | 匹配到的 blog_links 标题 | 推导方式 |
|---------------|------------------------|---------|
| `ai-agent-building-guide` | AI Agent Building Guide | url `/series/ai-agent-building-guide/` → slug = `ai-agent-building-guide` |
| `kubernetes-tutorial` | Kubernetes Tutorial | url `/posts/` → slug = `"kubernetes tutorial".lower()` → `kubernetes-tutorial` |
| `service-mesh-intro` | Service Mesh Introduction | url `/series/service-mesh-intro/` → slug = `service-mesh-intro` |

### 自动识别机制

**新增系列标题：** 只需在 `data/blog_links.yaml` 中添加条目，无需修改任何模板代码：

```yaml
- title:
    en: "New Series"
    zh: "新系列"
  icon: "cpu"
  url: "/series/new-series/"
  category: "ai-engineering"
```

模板自动遍历 `hugo.Data.blog_links`，新增条目自动生成 title 节点和 category→title 连线。

**新增文章：** 只需在文章 front matter 中添加 `series` 字段：

```yaml
series: new-series   # 对应 blog_links.yaml 中推导出的 slug
```

模板自动遍历 `.Site.RegularPages`，新文章自动生成 post 节点和 title→post 连线。

### 技术实现

**模板文件：** `layouts/categories/list.html`

**可视化库：** D3.js v7（CDN 加载）

**关键 JS 函数：**

| 函数 | 作用 |
|------|------|
| `getNodeGroup(d)` | 获取节点的实际颜色组（title/post 继承父分类） |
| `getNodeColor(d)` | 获取节点颜色（center 返回金色） |
| `nodeRadius(d)` | 根据节点类型返回不同半径 |
| `highlightNode(d)` | 悬停高亮：当前节点+邻居高亮，其余暗淡 |
| `resetHighlight()` | 恢复所有节点和连线到默认状态 |

**力模拟参数（按层级不同）：**

| 层级 | 连线距离 | 电荷斥力 |
|------|---------|---------|
| center → category | 200px | -600 |
| category → title | 120px | -280 |
| title → post | 80px | -150 / -80 |

**交互：**
- 拖拽节点（中心节点除外）
- 点击节点跳转到对应页面
- 悬停高亮关联节点和连线
- 滚轮缩放、拖拽平移
- R 键重置视图

### 维护指南

**新增系列：**
1. 编辑 `data/blog_links.yaml`，在对应 category 下添加条目
2. （可选）创建 `content/series/<slug>/_index.en.md` 和 `_index.zh.md`
3. 更新 `layouts/partials/icon.html` 添加新图标（如需要）

**新增文章并关联到系列：**
1. 在文章 front matter 中设置 `categories`（至少一个）
2. 在文章 front matter 中设置 `series`（对应 blog_links 中某条目的 slug）
3. 文章自动出现在图中，并连线到对应系列标题

**新增图标：**
1. 在 `layouts/partials/icon.html` 中添加 `else if eq $name "新图标名"` 分支
2. 在 `data/blog_links.yaml` 对应条目中设置 `icon: "新图标名"`