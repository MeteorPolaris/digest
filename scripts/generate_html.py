#!/usr/bin/env python3
"""
generate_html.py - 读取目录下所有 .md 文件，生成暗色主题交互式 HTML 单页应用。

用法:
    python generate_html.py ./output-dir

输出:
    在指定目录下生成 index.html
"""

import os
import re
import sys
import html
from pathlib import Path
from typing import List, Tuple


# ─── Markdown 解析 ────────────────────────────────────────────────────────────

def parse_markdown(text: str) -> str:
    """将 Markdown 文本转换为 HTML，支持标题、粗体、斜体、代码、表格、列表、引用、分隔线。"""
    lines = text.split('\n')
    result = []
    i = 0
    in_code_block = False
    code_block_content = []
    code_block_lang = ''

    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith('```'):
            if in_code_block:
                # 结束代码块
                escaped = html.escape('\n'.join(code_block_content))
                result.append(f'<pre><code class="language-{code_block_lang}">{escaped}</code></pre>')
                code_block_content = []
                code_block_lang = ''
                in_code_block = False
            else:
                # 开始代码块
                in_code_block = True
                code_block_lang = line.strip()[3:].strip()
            i += 1
            continue

        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue

        stripped = line.strip()

        # 空行
        if not stripped:
            result.append('')
            i += 1
            continue

        # 分隔线
        if re.match(r'^[-*_]{3,}\s*$', stripped):
            result.append('<hr>')
            i += 1
            continue

        # 标题
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            content = inline_format(heading_match.group(2))
            result.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue

        # 引用块
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(re.sub(r'^>\s?', '', lines[i].strip()))
                i += 1
            quote_content = parse_markdown('\n'.join(quote_lines))
            result.append(f'<blockquote>{quote_content}</blockquote>')
            continue

        # 表格
        if '|' in stripped and i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i + 1].strip()):
            table_lines = []
            while i < len(lines) and '|' in lines[i].strip():
                table_lines.append(lines[i].strip())
                i += 1
            result.append(parse_table(table_lines))
            continue

        # 无序列表
        if re.match(r'^[-*+]\s+', stripped):
            items = []
            while i < len(lines) and re.match(r'^[-*+]\s+', lines[i].strip()):
                item_text = re.sub(r'^[-*+]\s+', '', lines[i].strip())
                items.append(f'<li>{inline_format(item_text)}</li>')
                i += 1
            result.append('<ul>' + '\n'.join(items) + '</ul>')
            continue

        # 有序列表
        if re.match(r'^\d+\.\s+', stripped):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                items.append(f'<li>{inline_format(item_text)}</li>')
                i += 1
            result.append('<ol>' + '\n'.join(items) + '</ol>')
            continue

        # 普通段落
        result.append(f'<p>{inline_format(stripped)}</p>')
        i += 1

    return '\n'.join(result)


def inline_format(text: str) -> str:
    """处理行内格式：粗体、斜体、行内代码、链接。"""
    # 行内代码（先处理，避免被其他规则干扰）
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    return text


def parse_table(table_lines: List[str]) -> str:
    """将 Markdown 表格行转换为 HTML 表格。"""
    if len(table_lines) < 2:
        return ''

    def split_cells(row: str) -> List[str]:
        cells = row.strip('|').split('|')
        return [c.strip() for c in cells]

    headers = split_cells(table_lines[0])
    rows = [split_cells(line) for line in table_lines[2:]]  # 跳过分隔行

    thead = '<thead><tr>' + ''.join(f'<th>{inline_format(h)}</th>' for h in headers) + '</tr></thead>'
    tbody_rows = []
    for row in rows:
        cells = ''.join(f'<td>{inline_format(c)}</td>' for c in row)
        tbody_rows.append(f'<tr>{cells}</tr>')
    tbody = '<tbody>' + '\n'.join(tbody_rows) + '</tbody>'

    return f'<table>{thead}{tbody}</table>'


# ─── 文件扫描 ──────────────────────────────────────────────────────────────────

def scan_md_files(directory: str) -> List[Tuple[str, str]]:
    """扫描目录下所有 .md 文件，返回 [(文件名, 内容), ...] 列表。"""
    md_files = []
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"错误: 目录 '{directory}' 不存在")
        sys.exit(1)

    for file_path in sorted(dir_path.glob('*.md')):
        try:
            content = file_path.read_text(encoding='utf-8')
            md_files.append((file_path.stem, content))
        except Exception as e:
            print(f"警告: 无法读取 {file_path}: {e}")

    return md_files


# ─── HTML 模板 ─────────────────────────────────────────────────────────────────

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Digest - 知识摘要</title>
<style>
  :root {{
    --bg-primary: #0f1117;
    --bg-surface: #1a1d27;
    --bg-surface-hover: #242736;
    --accent: #6366f1;
    --accent-hover: #818cf8;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #2d3041;
    --search-bg: #1e2130;
    --sidebar-width: 280px;
  }}

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Microsoft YaHei', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.7;
    display: flex;
    min-height: 100vh;
  }}

  /* ─── 侧边栏 ─── */
  .sidebar {{
    width: var(--sidebar-width);
    background: var(--bg-surface);
    border-right: 1px solid var(--border);
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    overflow-y: auto;
    z-index: 100;
    transition: transform 0.3s ease;
  }}

  .sidebar-header {{
    padding: 24px 20px 16px;
    border-bottom: 1px solid var(--border);
  }}

  .sidebar-header h1 {{
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
  }}

  .sidebar-header p {{
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
  }}

  .search-box {{
    padding: 12px 16px;
  }}

  .search-box input {{
    width: 100%;
    padding: 10px 14px;
    background: var(--search-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
  }}

  .search-box input:focus {{
    border-color: var(--accent);
  }}

  .search-box input::placeholder {{
    color: var(--text-muted);
  }}

  .nav-list {{
    list-style: none;
    padding: 8px 12px;
  }}

  .nav-item {{
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    color: var(--text-secondary);
    transition: all 0.2s;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .nav-item:hover {{
    background: var(--bg-surface-hover);
    color: var(--text-primary);
  }}

  .nav-item.active {{
    background: var(--accent);
    color: white;
    font-weight: 500;
  }}

  .nav-item.hidden {{
    display: none;
  }}

  .nav-icon {{
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    opacity: 0.7;
  }}

  /* ─── 主内容区 ─── */
  .main {{
    margin-left: var(--sidebar-width);
    flex: 1;
    min-height: 100vh;
  }}

  .content {{
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 40px;
  }}

  .article {{
    display: none;
  }}

  .article.active {{
    display: block;
  }}

  .article h1 {{
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--accent);
  }}

  .article h2 {{
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 40px;
    margin-bottom: 16px;
    padding-left: 12px;
    border-left: 3px solid var(--accent);
  }}

  .article h3 {{
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 32px;
    margin-bottom: 12px;
  }}

  .article h4, .article h5, .article h6 {{
    font-size: 16px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 24px;
    margin-bottom: 8px;
  }}

  .article p {{
    margin-bottom: 16px;
    color: var(--text-primary);
  }}

  .article a {{
    color: var(--accent-hover);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
  }}

  .article a:hover {{
    border-bottom-color: var(--accent-hover);
  }}

  .article strong {{
    color: var(--text-primary);
    font-weight: 600;
  }}

  .article em {{
    color: var(--text-secondary);
    font-style: italic;
  }}

  .article code {{
    background: var(--bg-surface);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 0.9em;
    color: var(--accent-hover);
  }}

  .article pre {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    overflow-x: auto;
    margin-bottom: 16px;
  }}

  .article pre code {{
    background: none;
    padding: 0;
    color: var(--text-primary);
    font-size: 13px;
    line-height: 1.6;
  }}

  .article blockquote {{
    border-left: 3px solid var(--accent);
    background: var(--bg-surface);
    padding: 12px 20px;
    margin-bottom: 16px;
    border-radius: 0 8px 8px 0;
    color: var(--text-secondary);
  }}

  .article blockquote p {{
    margin-bottom: 0;
    color: var(--text-secondary);
  }}

  .article table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
    font-size: 14px;
  }}

  .article th, .article td {{
    padding: 10px 14px;
    border: 1px solid var(--border);
    text-align: left;
  }}

  .article th {{
    background: var(--bg-surface);
    font-weight: 600;
    color: var(--text-primary);
  }}

  .article td {{
    color: var(--text-secondary);
  }}

  .article tr:hover td {{
    background: var(--bg-surface-hover);
  }}

  .article ul, .article ol {{
    padding-left: 24px;
    margin-bottom: 16px;
  }}

  .article li {{
    margin-bottom: 6px;
    color: var(--text-primary);
  }}

  .article hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
  }}

  /* ─── 搜索高亮 ─── */
  mark {{
    background: rgba(99, 102, 241, 0.3);
    color: var(--text-primary);
    padding: 1px 2px;
    border-radius: 2px;
  }}

  /* ─── 移动端菜单按钮 ─── */
  .menu-btn {{
    display: none;
    position: fixed;
    top: 16px;
    left: 16px;
    z-index: 200;
    width: 40px;
    height: 40px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 20px;
    cursor: pointer;
    align-items: center;
    justify-content: center;
  }}

  /* ─── 响应式 ─── */
  @media (max-width: 768px) {{
    .sidebar {{
      transform: translateX(-100%);
    }}

    .sidebar.open {{
      transform: translateX(0);
    }}

    .main {{
      margin-left: 0;
    }}

    .content {{
      padding: 60px 20px 40px;
    }}

    .menu-btn {{
      display: flex;
    }}

    .overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      z-index: 99;
    }}

    .overlay.active {{
      display: block;
    }}
  }}
</style>
</head>
<body>

<button class="menu-btn" onclick="toggleSidebar()">&#9776;</button>
<div class="overlay" onclick="toggleSidebar()"></div>

<aside class="sidebar">
  <div class="sidebar-header">
    <h1>Digest</h1>
    <p>知识摘要导航</p>
  </div>
  <div class="search-box">
    <input type="text" id="searchInput" placeholder="搜索内容..." oninput="onSearch(this.value)">
  </div>
  <ul class="nav-list" id="navList">
    {nav_items}
  </ul>
</aside>

<main class="main">
  <div class="content">
    {articles}
  </div>
</main>

<script>
  const navItems = document.querySelectorAll('.nav-item');
  const articles = document.querySelectorAll('.article');
  const searchInput = document.getElementById('searchInput');

  // 文章内容索引（用于搜索）
  const articleTexts = {{}};
  articles.forEach(a => {{
    articleTexts[a.id] = a.textContent.toLowerCase();
  }});

  // 切换文章
  function showArticle(id) {{
    navItems.forEach(item => item.classList.remove('active'));
    articles.forEach(article => article.classList.remove('active'));

    const navItem = document.querySelector(`.nav-item[data-id="${{id}}"]`);
    const article = document.getElementById(id);

    if (navItem) navItem.classList.add('active');
    if (article) article.classList.add('active');

    // 移动端关闭侧边栏
    if (window.innerWidth <= 768) {{
      toggleSidebar();
    }}

    // 滚动到顶部
    window.scrollTo(0, 0);
  }}

  // 搜索
  function onSearch(query) {{
    query = query.toLowerCase().trim();

    navItems.forEach(item => {{
      const id = item.dataset.id;
      const name = item.dataset.name.toLowerCase();

      if (!query || name.includes(query) || articleTexts[id]?.includes(query)) {{
        item.classList.remove('hidden');
      }} else {{
        item.classList.add('hidden');
      }}
    }});
  }}

  // 移动端侧边栏切换
  function toggleSidebar() {{
    document.querySelector('.sidebar').classList.toggle('open');
    document.querySelector('.overlay').classList.toggle('active');
  }}

  // 默认显示第一篇文章
  if (navItems.length > 0) {{
    showArticle(navItems[0].dataset.id);
  }}

  // 键盘快捷键：Ctrl+K 聚焦搜索
  document.addEventListener('keydown', (e) => {{
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
      e.preventDefault();
      searchInput.focus();
    }}
  }});
</script>

</body>
</html>'''


# ─── 生成逻辑 ──────────────────────────────────────────────────────────────────

def generate_nav_item(name: str, index: int) -> str:
    """生成导航项 HTML。"""
    display_name = name.replace('-', ' ').replace('_', ' ')
    return (
        f'<li class="nav-item" data-id="article-{index}" data-name="{html.escape(display_name)}" '
        f'onclick="showArticle(\'article-{index}\')">'
        f'<span class="nav-icon">&#9679;</span>{html.escape(display_name)}</li>'
    )


def generate_article(name: str, content: str, index: int) -> str:
    """生成文章区 HTML。"""
    body = parse_markdown(content)
    return f'<div class="article" id="article-{index}">{body}</div>'


def generate_html(md_files: List[Tuple[str, str]]) -> str:
    """生成完整 HTML。"""
    nav_items = '\n    '.join(
        generate_nav_item(name, i) for i, (name, _) in enumerate(md_files)
    )
    articles = '\n    '.join(
        generate_article(name, content, i) for i, (name, content) in enumerate(md_files)
    )
    return HTML_TEMPLATE.format(nav_items=nav_items, articles=articles)


# ─── 入口 ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_html.py <目录路径>")
        print("示例: python generate_html.py ./output-dir")
        sys.exit(1)

    directory = sys.argv[1]
    md_files = scan_md_files(directory)

    if not md_files:
        print(f"错误: 在 '{directory}' 中未找到 .md 文件")
        sys.exit(1)

    print(f"找到 {len(md_files)} 个 Markdown 文件:")
    for name, _ in md_files:
        print(f"  - {name}.md")

    html_content = generate_html(md_files)

    output_path = Path(directory) / 'index.html'
    output_path.write_text(html_content, encoding='utf-8')

    print(f"\n已生成: {output_path}")
    print(f"文件大小: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
