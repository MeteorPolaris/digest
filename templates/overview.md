# {{month}} 精华书导览

> 信息来源：{{star_count}}条星球内容 + {{article_count}}篇付费文章 + {{report_count}}份研报
> 覆盖时间：{{date_range}}
> 生成时间：{{generated_at}}

---

## 一句话速览

{{one_line_summary}}

---

## 各主题速览

{{#each themes}}
### {{id}} {{name}} — "{{tagline}}"

{{overview}}

→ 信号强度：{{signal_strength}} | 共识度：{{consensus_level}} | 关键变量：{{key_variable}}

{{/each}}

---

## 本月核心变量

{{#each key_variables}}
{{number}}. **{{name}}**：{{description}}
{{/each}}

## 跨主题共振

{{#each cross_theme_links}}
- **{{theme_a}}×{{theme_b}}**：{{description}}
{{/each}}
