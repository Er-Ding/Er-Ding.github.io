# 朱军 · Stephen Zhu 个人主页

无构建步骤的 HTML/CSS 静态网站，可直接在本地修改。

## 页面与来源

- 最初于 2026-10-10 从 https://academic-notes.stephenzhu17.chatgpt.site/ 整理为本地静态版本。
- 2026-10-30 参照 https://keunhong.com/ 的内容布局与排版重新设计，沿用本地个人资料、照片和论文图。
- 页面依次展示个人简介、研究亮点、论文、教育经历与联系方式。
- 补充图示使用浏览器原生折叠面板，无需 JavaScript。
- 英文字体使用 Google Fonts 的 Crimson Pro 与 Source Sans 3；网络不可用时回退到本机字体，中文使用本机宋体类字体。

## 修改哪些文件

| 文件 | 用途 |
| --- | --- |
| `index.html` | 姓名、个人简介、论文、个人经历、邮箱和链接 |
| `styles.css` | 配色、字体、间距、布局和移动端样式 |
| `favicon.svg` | 浏览器标签页图标 |
| `portrait.jpg` | 首页个人照片 |
| `assets/paper-tim-fig15.png` | 从 TIM 2025 论文 PDF 第 13 页提取的 Fig. 15，保留完整图像与红色标注 |
| `assets/` | 论文原图与其他已有素材 |

新增论文时，复制一个 `article.publication`，修改标题、发表信息、介绍、图片和链接，并为条目设置唯一的 `id`。首页亮点链接指向对应条目的 `id`。

## 本地打开

可以直接用浏览器打开 `/Volumes/disk2/CV/index.html`，无需安装依赖或构建。

也可以在终端启动一个仅供本机访问的静态服务器：

```sh
cd /Volumes/disk2/CV
python3 -m http.server 8000 --bind 127.0.0.1
```

然后打开 http://127.0.0.1:8000/ 。修改文件后刷新浏览器；终端按 `Ctrl+C` 停止服务。

## 线上更新

本地修改不会自动同步到现有的 `chatgpt.site` 网址。当前目录可作为静态网站部署；若继续更新现有 Sites 域名，需通过原站点项目重新部署。

本次未启动本地服务器或进行浏览器功能检查，未生成测试文件或测试结果文件。
