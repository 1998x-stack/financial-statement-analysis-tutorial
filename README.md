# 财务报表分析 · 从数字到商业事实

[课程首页（GitHub Pages）](https://1998x-stack.github.io/financial-statement-analysis-tutorial/) · [立即开始 01](https://1998x-stack.github.io/financial-statement-analysis-tutorial/chapters/01.html) · [设计规范](AGENTS.md)

28 篇中文财务报表分析教程：从 **资产负债表、利润表、现金流量表、所有者权益变动表及附注** 出发，进一步学习经营质量、风险识别和估值。每章尽可能独立成篇，有图解、可复算教学案例、异常情景与官方来源。

> **版本提示（2026-11）**：01–10 已按图解式长文重写，11–18 已完成第二批技术审校；19–28 从原仓库迁移，仍待逐章复核。财政部财会〔2026〕11 号新列报准则分批于 **2027（境内外两地上市等）/2029（其他境内上市）/2030（非上市）** 实施（允许提前执行），IFRS 18 自 2027 年开始适用，不要把新版利润表列报误用于未经调整的旧数据。

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
│   │   ├── 01.html .. 18.html    # 已完成审校批次（01–10、11–18）
│   │   ├── 19.html .. 28.html    # 迁移兼容，待逐章深审
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

## 第二轮：06–10 深度分析（2026-11-22）
- 06 [会计政策与估计](docs/chapters/06.html) · 会计政策/估计/差错分类、折旧敏感性与预期信用损失
- 07 [财报分析框架](docs/chapters/07.html) · Palepu–Healy 四视角、CFA 六阶段及现金兑现反证
- 08 [盈利能力](docs/chapters/08.html) · 毛利、净利、ROA、ROE 及正确的杜邦分解
- 09 [偿债能力](docs/chapters/09.html) · 短期流动性、受限资金、偿债到期日、租赁负债
- 10 [营运能力](docs/chapters/10.html) · DSO/DIO/DPO 与 CCC 天数、成本口径

10 张新的无外链 SVG、5 组交互数据实验，来源集中在财政部/CFA Institute/SEC/Palepu 教材。2027/2029/2030 的列报准则执行分层提示已同步回修至01–05、README和AGENTS。完整核查记录见 [第二批审校记录](reviews/2026-11-22-foundations-06-10.md)。

## 第三轮：11–18 审校（2026-11-22）
- 11 [成长能力](docs/chapters/11.html) · 有机增长与并表拆解、SGR、PEG 边界
- 12 [现金流质量](docs/chapters/12.html) · 净利润到经营现金流的桥接、净现比与收现比口径
- 13 [杜邦与综合评分](docs/chapters/13.html) · 三因子复算、经营/金融拆分、F-Score 适用边界
- 14 [同业比较](docs/chapters/14.html) · 可比公司四道筛选、中位数与分位数对标
- 15 [财务粉饰手法](docs/chapters/15.html) · 盈余管理/差错/造假三分，修正“经营租赁在表外”
- 16 [红旗信号](docs/chapters/16.html) · 红旗的反面解释、M-Score 八变量与误报边界
- 18 [审计意见与治理](docs/chapters/18.html) · 四类意见与强调事项段、关键审计事项、治理线索

14 张新的无外链 SVG、7 组可复算工作台（`growth`/`cashq`/`dupont`/`peer`/`revenueq`/`misindex`/`gov`），并在 1440/768/390/360 四视口完成浏览器回归。17（暴雷案例）需按监管公开处罚决定书原文重写，未在本批处理；19–28 仍为迁移版本。核查细节与未完成项见 [第三批审校记录](reviews/2026-11-22-risk-and-framework-11-18.md)。
