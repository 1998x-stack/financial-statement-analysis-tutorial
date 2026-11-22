# 财务报表分析 · 从数字到商业事实

[课程首页（GitHub Pages）](https://1998x-stack.github.io/financial-statement-analysis-tutorial/) · [立即开始 01](https://1998x-stack.github.io/financial-statement-analysis-tutorial/chapters/01.html) · [设计规范](AGENTS.md)

28 篇中文财务报表分析教程：从 **资产负债表、利润表、现金流量表、所有者权益变动表及附注** 出发，进一步学习经营质量、风险识别和估值。每章尽可能独立成篇，有图解、可复算教学案例、异常情景与官方来源。

> **版本提示（2026-11）**：01–10 已按图解式长文重写；11–28 从原仓库迁移，正在逐章复核。财政部财会〔2026〕11 号新列报准则分批于 **2027（境内外两地上市等）/2029（其他境内上市）/2030（非上市）** 实施（允许提前执行），IFRS 18 自 2027 年开始适用，不要把新版利润表列报误用于未经调整的旧数据。

## 本轮改造
- 重新组织为 `docs/` 页面源、统一的 `assets/` 和独立 SVG。
- 首页采用静态章节目录 + 渐进增强搜索，可直接打开 HTML。
- 每篇新文章沿“问题→概念→全局/局部 SVG→计算→风险→练习→官方来源”叙事。
- 旧 `01.html`…`28.html` 地址保留自动跳转，以降低外链迁移破坏。
- GitHub Actions：静态质量检查 + Chromium 多视口检查 + Docs 部署。

## 课程结构

| 模块 | 章节 | 学习目标 |
|---|---|---|
| 一 · 理解报表 | 01–05 | 三表关系、资产结构、利润形成、现金桥接和附注 |
| 二 · 经营质量 | 06–14 | 盈余管理、盈利、偿债、周转、成长与杜邦分析 |
| 三 · 风险估值 | 15–22 | 财务粉饰、审计、案例、估值和并购 |
| 四 · 分析工程 | 23–28 | Excel、Python、BI、AI 和综合模型 |

完整标题和主题见 [docs/courses.json](docs/courses.json)。

## 仓库结构

```text
.
├── docs/
│   ├── index.html                 # GitHub Pages 首页
│   ├── courses.json
│   ├── chapters/
│   │   ├── 01.html .. 05.html    # 首批独立重写文章
│   │   ├── 06.html .. 28.html    # 迁移兼容，待进一步深审
│   │   ├── theme.css             # 旧文章样式兼容
│   │   └── index.html            # 返回课程首页
│   └── assets/
│       ├── css/site.css
│       ├── js/site.js
│       └── figures/*.svg
├── scripts/
│   ├── site_check.py
│   └── browser_smoke.py
├── .github/workflows/
│   ├── quality.yml
│   └── pages.yml
├── AGENTS.md
└── index.html, 01.html..28.html  # 旧地址兼容跳转
```

## 本地预览

无需编译，在仓库目录执行：

```bash
python -m http.server 8000
# 打开 http://localhost:8000/docs/
```

质量检查：

```bash
python scripts/site_check.py
python -m pip install playwright
python -m playwright install chromium
python scripts/browser_smoke.py
```

## 部署说明

工作流 [pages.yml](.github/workflows/pages.yml) 在 `main` 更新后打包 `docs/` 部署 GitHub Pages。首次使用可能需在 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**；若仓库此前已配置为 `main/docs` 分支发布，也可以使用现有配置，但不要同时把两种发布方式混用。部署状态以 Actions 与实际 URL 检查为准。

## 依据与边界
- [财政部：2026 修订企业会计准则第30号](https://kjs.mof.gov.cn/zt/kjzzss/kuaijizhunzeshishi/202608/t20260806_3995008.htm)
- [中国证监会：上市公司信息披露管理办法](https://www.csrc.gov.cn/c106256/c1653948/content.shtml)
- [SEC：Beginners’ Guide to Financial Statements](https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements)
- [IFRS Foundation：IFRS 18](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/)

**所有未明确标注实际上市公司/报告期的数据均为教学虚构，不构成证券投资建议。**
