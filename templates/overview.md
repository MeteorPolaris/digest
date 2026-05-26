# {{month}} 知识摘要总览

> 本期共覆盖 {{source_count}} 个信息源，提炼 {{theme_count}} 个核心主题。

---

## 信息来源统计

| 来源类别 | 数量 | 覆盖主题 | 可信度评级 |
|---------|------|---------|-----------|
{{source_stats_rows}}
| **合计** | **{{source_count}}** | - | - |

### 来源分布

- 专业期刊/论文：{{journal_count}} 篇
- 行业报告：{{report_count}} 份
- 权威媒体：{{media_count}} 篇
- 深度访谈/播客：{{interview_count}} 期
- 社区讨论/论坛：{{community_count}} 条

---

## 各主题速览

{{#each themes}}
### {{@index}}. {{title}}

{{summary}}

**关键信号**: {{key_signal}}

---
{{/each}}

## 本月核心变量

> 以下变量在多个主题中反复出现，是理解本月信息格局的关键锚点。

| 变量 | 出现频次 | 影响方向 | 关联主题 |
|-----|---------|---------|---------|
{{core_variables_rows}}

### 变量解读

{{#each core_variables}}
**{{name}}**: {{interpretation}}

{{/each}}

---

## 跨主题共振

> 不同主题之间的信号交叉点，往往预示着结构性变化。

{{#each resonances}}
### {{title}}

- **涉及主题**: {{themes}}
- **共振信号**: {{signal}}
- **潜在影响**: {{impact}}

{{/each}}

---

## 阅读建议

{{reading_suggestions}}

---

*生成时间: {{generated_at}}*
*数据截止: {{data_cutoff}}*
