# {{theme_id}} {{theme_name}}

## 本月核心观点

{{core观点}}

## 信号地图

| 信号 | 强度 | 来源数 | 共识/分歧 |
|------|------|--------|-----------|
{{#each signals}}
| {{name}} | {{strength}} | {{source_count}} | {{consensus}} |
{{/each}}

---

{{#each sub_themes}}
## {{number}}. {{name}}

### 核心观点
{{core_points}}

### 关键数据
{{key_data}}

### 信息源与读后收获

{{#each sources}}
**来源：{{name}} — {{author}}**
- 核心观点：{{point}}
- 读后收获：{{insight}}
- 质量：{{quality}}
- 关联：{{related_to}}

{{/each}}

### 共识与分歧
- 共识：{{consensus}}
- 分歧：{{dissent}}

---

{{/each}}

## 关键变量清单

{{#each key_variables}}
- **{{name}}**：如果{{condition}}，则{{impact}}
{{/each}}

## 跨主题关联

{{#each cross_refs}}
- 与{{other_theme}}的关联：{{description}}
{{/each}}
