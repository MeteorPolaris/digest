# {{theme_name}} — {{month}} 主题分册

> {{theme_tagline}}

---

## 本月核心观点

{{#each core_views}}
{{@index}}. **{{title}}**: {{description}}
{{/each}}

---

## 信号地图

| 信号强度 | 信号内容 | 来源 | 出现频次 | 趋势方向 |
|---------|---------|------|---------|---------|
{{signal_map_rows}}

> 信号强度说明: ★★★ 高频多源确认 | ★★ 中频交叉验证 | ★ 单源但可信

---

## 子主题结构

{{#each subtopics}}
### {{@index}}. {{title}}

#### 核心观点

{{core_point}}

#### 关键数据

| 指标 | 数值 | 环比变化 | 数据来源 |
|-----|------|---------|---------|
{{data_rows}}

#### 信息源与读后收获

**主要信息源**:

{{#each sources}}
- [{{title}}]({{url}}) — {{relevance}}
{{/each}}

**读后收获**:

{{takeaway}}

#### 共识与分歧

**共识点**:

{{#each consensus}}
- {{this}}
{{/each}}

**分歧点**:

{{#each disagreements}}
- **{{perspective}}**: {{position}} — *来源: {{source}}*
{{/each}}

---

{{/each}}

## 关键变量清单

> 本主题内需要持续跟踪的核心变量。

| 变量名 | 当前状态 | 监测指标 | 下次评估 | 风险等级 |
|-------|---------|---------|---------|---------|
{{variable_checklist_rows}}

### 变量详细说明

{{#each variables}}
**{{name}}**
- 定义: {{definition}}
- 当前值/状态: {{current_status}}
- 变化触发条件: {{trigger_conditions}}
- 预期影响: {{expected_impact}}

{{/each}}

---

## 跨主题关联

> 本主题与其他主题的交叉影响分析。

{{#each cross_links}}
### 与「{{related_theme}}」的关联

- **关联强度**: {{strength}}
- **关联类型**: {{type}}
- **具体表现**: {{manifestation}}
- **协同效应**: {{synergy}}

{{/each}}

---

## 信息源索引

| 序号 | 来源标题 | 类型 | 可信度 | 核心贡献 |
|-----|---------|------|-------|---------|
{{source_index_rows}}

---

## 附录

### 术语表

{{#each glossary}}
- **{{term}}**: {{definition}}
{{/each}}

### 延伸阅读

{{#each further_reading}}
- [{{title}}]({{url}}) — {{reason}}
{{/each}}

---

*主题负责人: {{author}}*
*最后更新: {{updated_at}}*
*下次评估: {{next_review}}*
