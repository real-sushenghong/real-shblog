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
