#!/usr/bin/env python3
"""
Shared SCSS Documentation Generator
SCSS 파일들을 파싱하여 다중 페이지 사양서를 자동 생성합니다.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 프로젝트 루트 디렉토리
ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
VARIABLES_COLORS_FILE = ROOT_DIR / "variables" / "_colors.scss"
THEME_FILE = ROOT_DIR / "theme" / "_index.scss"
BREAKPOINTS_FILE = ROOT_DIR / "breakpoints" / "_index.scss"
TYPOGRAPHY_FILE = ROOT_DIR / "variables" / "_typo.scss"
SPACING_FILE = ROOT_DIR / "variables" / "_spacing.scss"
FONTS_VARIABLES_FILE = ROOT_DIR / "fonts" / "_variables.scss"

# 네비게이션 메뉴
NAV_ITEMS = [
    {"title": "홈", "url": "index.html"},
    {"title": "Colors", "url": "colors.html"},
    {"title": "Breakpoints", "url": "breakpoints.html"},
    {"title": "Typography", "url": "typography.html"},
    {"title": "Spacing", "url": "spacing.html"},
    {"title": "Google Icons", "url": "fonts.html"},
    {"title": "Mixins", "url": "mixins.html"},
]


def get_common_styles() -> str:
    """공통 CSS 스타일"""
    return """
    <style>
        @import url(//spoqa.github.io/spoqa-han-sans/css/SpoqaHanSansNeo.css);
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: "Spoqa Han Sans Neo", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", sans-serif;
            background: #f5f5f5;
            line-height: 1.6;
        }
        .nav {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .nav-content {
            display: flex;
            align-items: center;
            gap: 32px;
        }
        .nav-title {
            font-size: 20px;
            font-weight: 700;
            color: #1e293b;
            text-decoration: none;
        }
        .nav-menu {
            display: flex;
            gap: 24px;
            list-style: none;
        }
        .nav-menu a {
            color: #64748b;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }
        .nav-menu a:hover,
        .nav-menu a.active {
            color: #2563eb;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px 20px;
        }
        h1 {
            color: #212121;
            margin-bottom: 10px;
            font-size: 32px;
        }
        .subtitle {
            color: #64748b;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .section {
            background: white;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        .grid {
            display: grid;
            gap: 16px;
        }
        .card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card-title {
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
            font-size: 14px;
        }
        .card-value {
            color: #64748b;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
        }
        .code {
            font-family: 'Monaco', 'Menlo', monospace;
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
        }
        .semantic-colors {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }
        .semantic-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }
        .semantic-item.bg-example {
            padding: 16px;
        }
        .semantic-item.text-example {
            padding: 16px;
        }
        .semantic-item.border-example {
            padding: 16px;
        }
        .semantic-swatch {
            width: 48px;
            height: 48px;
            border-radius: 4px;
            flex-shrink: 0;
            border: 1px solid #e2e8f0;
        }
        .semantic-info {
            flex: 1;
        }
        .semantic-name {
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
            font-size: 13px;
        }
        .semantic-value {
            color: #64748b;
            font-size: 11px;
            font-family: 'Monaco', 'Menlo', monospace;
        }
        .category-group {
            margin-bottom: 32px;
        }
        .category-title {
            font-size: 18px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 16px;
            margin-top: 32px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        .category-title:first-child {
            margin-top: 0;
        }
        .example-text {
            font-size: 14px;
            font-weight: 500;
        }
        .palette-group {
            margin-bottom: 32px;
        }
        .palette-title {
            font-size: 16px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 12px;
            margin-top: 24px;
        }
        .palette-title:first-child {
            margin-top: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        table th,
        table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        table th {
            background: #f8fafc;
            font-weight: 600;
            color: #1e293b;
            font-size: 13px;
        }
        table td {
            color: #334155;
            font-size: 14px;
        }
        .color-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 12px;
        }
        .color-item {
            display: flex;
            flex-direction: column;
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            background: white;
        }
        .color-swatch {
            width: 100%;
            height: 80px;
        }
        .color-info {
            padding: 8px;
            font-size: 11px;
        }
        .color-name {
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
        }
        .color-value {
            color: #64748b;
            font-family: 'Monaco', 'Menlo', monospace;
        }
    </style>
    """


def get_navigation(current_page: str = "") -> str:
    """네비게이션 HTML 생성"""
    nav_html = """
    <nav class="nav">
        <div class="nav-container">
            <div class="nav-content">
                <a href="index.html" class="nav-title">Shared SCSS</a>
                <ul class="nav-menu">
    """
    for item in NAV_ITEMS:
        active = ' class="active"' if item["url"] == current_page else ""
        nav_html += f'                    <li><a href="{item["url"]}"{active}>{item["title"]}</a></li>\n'
    
    nav_html += """
                </ul>
            </div>
        </div>
    </nav>
    """
    return nav_html


def generate_html_page(title: str, content: str, current_page: str = "") -> str:
    """HTML 페이지 생성 (공통 헤더/푸터 포함)"""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Shared SCSS</title>
    {get_common_styles()}
</head>
<body>
    {get_navigation(current_page)}
    <div class="container">
        {content}
    </div>
</body>
</html>
"""


# ============================================
# Colors 페이지 (기존 코드 활용)
# ============================================

def extract_color_variables(scss_file: Path) -> Dict[str, str]:
    """SCSS 파일에서 색상 변수를 추출합니다."""
    colors = {}
    if not scss_file.exists():
        return colors
    
    with open(scss_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\$([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,6}|#[0-9a-fA-F]{8})\s*;'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        var_name = match.group(1)
        color_value = match.group(2).upper()
        colors[var_name] = color_value
    
    return colors


def extract_theme_mappings(theme_file: Path, color_vars: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
    """Theme 파일에서 semantic color 매핑을 추출합니다."""
    mappings = {}
    if not theme_file.exists():
        return mappings
    
    with open(theme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\$([a-z0-9-]+):\s*\$([a-z0-9-]+)\s*;'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        semantic_name = match.group(1)
        base_color_var = match.group(2)
        if base_color_var in color_vars:
            mappings[semantic_name] = (base_color_var, color_vars[base_color_var])
    
    return mappings


def sort_color_by_brightness(color_list: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """색상을 밝은 순서대로 정렬합니다."""
    def get_sort_key(item):
        var_name = item[0]
        match = re.search(r'-(\d+)$', var_name)
        if match:
            num = int(match.group(1))
            return (1, num)
        else:
            return (0, 0)
    return sorted(color_list, key=get_sort_key)


def get_category_order_from_file(color_vars: Dict[str, str]) -> Dict[str, int]:
    """variables/_colors.scss 파일에서 카테고리가 나타나는 순서를 추적합니다."""
    category_order = {}
    order = 0
    seen_categories = set()
    
    with open(VARIABLES_COLORS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\$([a-z0-9-]+):\s*#[0-9a-fA-F]{3,8}\s*;'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        var_name = match.group(1)
        if var_name in ['white', 'white-real', 'black', 'black-real']:
            category = 'Global'
        else:
            parts = var_name.split('-')
            if len(parts) > 1:
                category = parts[0].capitalize()
            else:
                continue
        
        if category not in seen_categories:
            seen_categories.add(category)
            category_order[category] = order
            order += 1
    
    return category_order


def generate_colors_page() -> str:
    """Colors 페이지 생성"""
    # 색상 변수 추출
    color_vars = extract_color_variables(VARIABLES_COLORS_FILE)
    theme_mappings = extract_theme_mappings(THEME_FILE, color_vars)
    
    # 카테고리 순서 가져오기
    category_order_map = get_category_order_from_file(color_vars)
    
    # 색상 카테고리별로 분류
    categories = {
        'Global': [],
        'Slate': [], 'Gray': [], 'Zinc': [], 'Neutral': [], 'Stone': [],
        'Lime': [], 'Green': [], 'Emerald': [], 'Teal': [], 'Cyan': [],
        'Sky': [], 'Blue': [], 'Indigo': [], 'Violet': [], 'Purple': [],
        'Fuchsia': [], 'Pink': [], 'Rose': [], 'Red': [], 'Orange': [],
        'Amber': [], 'Yellow': [],
    }
    
    # 색상 변수 분류
    for var_name, color_value in sorted(color_vars.items()):
        category = None
        for cat in categories.keys():
            if var_name.startswith(cat.lower()):
                category = cat
                break
        
        if not category:
            if var_name in ['white', 'white-real', 'black', 'black-real']:
                category = 'Global'
            else:
                parts = var_name.split('-')
                if len(parts) > 1:
                    potential_cat = parts[0].capitalize()
                    if potential_cat in categories:
                        category = potential_cat
        
        if category:
            categories[category].append((var_name, color_value))
        else:
            categories['Global'].append((var_name, color_value))
    
    # Theme 색상 분류
    bg_colors = []
    text_colors = []
    border_colors = []
    brand_colors = []
    state_colors = []
    stock_colors = []
    link_colors = []
    
    for semantic_name, (base_var, color_value) in theme_mappings.items():
        item = (semantic_name, color_value, base_var)
        
        if semantic_name.startswith('bg-'):
            bg_colors.append(item)
        elif semantic_name.startswith('text-'):
            text_colors.append(item)
        elif semantic_name.startswith('border-'):
            border_colors.append(item)
        elif semantic_name in ['primary', 'secondary', 'point']:
            brand_colors.append(item)
        elif semantic_name in ['success', 'warning', 'error', 'info', 'valid', 'invalid']:
            state_colors.append(item)
        elif semantic_name in ['positive', 'negative', 'neutral', 'stock-up', 'stock-down', 'stock-neutral', 'stock-positive', 'stock-negative', 'value-red', 'value-blue', 'gapup', 'gapdown']:
            stock_colors.append(item)
        elif semantic_name.startswith('link'):
            link_colors.append(item)
    
    # HTML 생성
    content = """
        <h1>Colors</h1>
        <p class="subtitle">shared-scss의 theme과 variables 색상 팔레트</p>
        
        <!-- Semantic Colors (Theme) -->
        <div class="section">
            <h2 class="section-title">Semantic Colors (Theme)</h2>
    """
    
    # Background Colors
    if bg_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Background Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(bg_colors):
            text_color = "#1e293b" if not name.startswith('bg-dark') else "#ffffff"
            border_style = 'border: 1px solid #e2e8f0;' if color.upper() in ['#FCFCFC', '#FFFFFF'] else ''
            content += f"""
                    <div class="semantic-item bg-example" style="background: {color}; {border_style}">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {text_color};">background-color: ${name};</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # Text Colors
    if text_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Text Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(text_colors):
            bg_color = "#111827" if name == 'text-inverse' else "#ffffff"
            border_style = 'border: 1px solid #e2e8f0;' if bg_color == '#ffffff' else ''
            content += f"""
                    <div class="semantic-item text-example" style="background: {bg_color}; {border_style}">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {color};">color: ${name};</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # Border Colors
    if border_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Border Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(border_colors):
            content += f"""
                    <div class="semantic-item border-example" style="background: #ffffff; border: 2px solid {color};">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: #1e293b;">border: 1px solid ${name};</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # Brand Colors
    if brand_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Brand Colors</div>
                <div class="semantic-colors">
        """
        brand_colors_sorted = sorted(brand_colors, key=lambda x: (0 if x[0] == 'primary' else 1, x[0]))
        for name, color, base_var in brand_colors_sorted:
            content += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # State Colors
    if state_colors:
        content += """
            <div class="category-group">
                <div class="category-title">State Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(state_colors):
            content += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # Stock Colors
    if stock_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Stock/Finance State Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(stock_colors):
            content += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    # Link Colors
    if link_colors:
        content += """
            <div class="category-group">
                <div class="category-title">Link Colors</div>
                <div class="semantic-colors">
        """
        for name, color, base_var in sort_color_by_brightness(link_colors):
            content += f"""
                    <div class="semantic-item text-example" style="background: #ffffff; border: 1px solid #e2e8f0;">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {color}; text-decoration: underline;">color: ${name};</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    content += """
        </div>
    """
    
    # Primary Color Scale
    primary_mappings = {name: (base_var, color) for name, (base_var, color) in theme_mappings.items() if name.startswith('primary-') or name == 'primary'}
    primary_colors = []
    
    if 'primary' in primary_mappings:
        _, color = primary_mappings['primary']
        primary_colors.append(('primary', color))
    
    if 'primary-50' in primary_mappings:
        _, color = primary_mappings['primary-50']
        primary_colors.append(('primary-50', color))
    
    for num in range(100, 1000, 100):
        name = f'primary-{num}'
        if name in primary_mappings:
            _, color = primary_mappings[name]
            primary_colors.append((name, color))
    
    if primary_colors:
        content += """
        <div class="section">
            <h2 class="section-title">Primary Color Scale</h2>
            <div class="color-grid">
        """
        for name, color_value in primary_colors:
            content += f"""
                <div class="color-item">
                    <div class="color-swatch" style="background: {color_value};"></div>
                    <div class="color-info">
                        <div class="color-name">${name}</div>
                        <div class="color-value">{color_value}</div>
                    </div>
                </div>
            """
        content += """
            </div>
        </div>
        """
    
    # Color Palettes
    content += """
        <div class="section">
            <h2 class="section-title">Color Palettes</h2>
    """
    
    def get_category_sort_key(item):
        category, color_list = item
        if category == 'Global':
            return (-1, category)
        order = category_order_map.get(category, 999)
        return (order, category)
    
    sorted_categories = sorted(categories.items(), key=get_category_sort_key)
    
    for category, color_list in sorted_categories:
        if not color_list:
            continue
        
        content += f"""
            <div class="palette-group">
                <div class="palette-title">{category}</div>
                <div class="color-grid">
        """
        sorted_color_list = sort_color_by_brightness(color_list)
        for var_name, color_value in sorted_color_list:
            border_style = 'border: 1px solid #e2e8f0;' if color_value.upper() in ['#FCFCFC', '#FFFFFF'] else ''
            content += f"""
                    <div class="color-item">
                        <div class="color-swatch" style="background: {color_value}; {border_style}"></div>
                        <div class="color-info">
                            <div class="color-name">${var_name}</div>
                            <div class="color-value">{color_value}</div>
                        </div>
                    </div>
            """
        content += """
                </div>
            </div>
        """
    
    content += """
        </div>
    """
    
    return content


# ============================================
# Breakpoints 페이지
# ============================================

def extract_breakpoints() -> Dict[str, str]:
    """Breakpoints 파일에서 breakpoint 값을 추출합니다."""
    breakpoints = {}
    if not BREAKPOINTS_FILE.exists():
        return breakpoints
    
    with open(BREAKPOINTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Map 정의 찾기
    pattern = r'"([^"]+)":\s*(\d+px)'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        key = match.group(1)
        value = match.group(2)
        breakpoints[key] = value
    
    return breakpoints


def generate_breakpoints_page() -> str:
    """Breakpoints 페이지 생성"""
    breakpoints = extract_breakpoints()
    
    content = """
        <h1>Breakpoints</h1>
        <p class="subtitle">반응형 디자인을 위한 breakpoint 값들</p>
        
        <div class="section">
            <h2 class="section-title">Breakpoint Map</h2>
            <table>
                <thead>
                    <tr>
                        <th>이름</th>
                        <th>값</th>
                        <th>용도</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Breakpoint 용도 설명
    descriptions = {
        "xxs": "초소형 모바일",
        "xs": "소형 모바일",
        "sm": "중형 모바일",
        "md": "대형 모바일",
        "lg": "태블릿",
        "xl": "소형 데스크톱",
        "2xl": "데스크톱",
        "3xl": "대형 데스크톱",
        "4xl": "초대형 데스크톱",
    }
    
    # 정렬된 breakpoints (값 순서대로)
    sorted_bps = sorted(breakpoints.items(), key=lambda x: int(x[1].replace('px', '')))
    
    for key, value in sorted_bps:
        desc = descriptions.get(key, "")
        content += f"""
                    <tr>
                        <td><code class="code">{key}</code></td>
                        <td><code class="code">{value}</code></td>
                        <td>{desc}</td>
                        <td><code class="code">@include up("{key}")</code></td>
                    </tr>
        """
    
    content += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2 class="section-title">Core Mixins</h2>
            <p>Map 기반 breakpoint mixin 사용법:</p>
            <table style="margin-top: 16px;">
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                        <th>적용 범위 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include up("xs")</code></td>
                        <td>위로 (min-width) - Mobile First</td>
                        <td><code class="code">@include up("xs") { ... }</code></td>
                        <td>360px 이상 (소형 모바일 이상)</td>
                    </tr>
                    <tr>
                        <td><code class="code">@include down("md")</code></td>
                        <td>아래로 (max-width) - Desktop First</td>
                        <td><code class="code">@include down("md") { ... }</code></td>
                        <td>575.98px 이하 (대형 모바일 이하)</td>
                    </tr>
                    <tr>
                        <td><code class="code">@include between("xs", "lg")</code></td>
                        <td>범위 (between) - 특정 범위 지정</td>
                        <td><code class="code">@include between("xs", "lg") { ... }</code></td>
                        <td>360px ~ 767.98px (소형 모바일 ~ 태블릿)</td>
                    </tr>
                </tbody>
            </table>
            
            <div style="margin-top: 24px; padding: 16px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 12px; color: #1e293b;">사용 예시</h3>
                <pre style="background: #1e293b; color: #f8fafc; padding: 16px; border-radius: 4px; overflow-x: auto; font-size: 13px; line-height: 1.6;"><code>.container {
    padding: 16px;
    
    @include up("md") {
        padding: 24px;  // 576px 이상에서 적용
    }
    
    @include down("sm") {
        padding: 12px;  // 479.98px 이하에서 적용
    }
    
    @include between("md", "xl") {
        max-width: 1200px;  // 576px ~ 991.98px 범위에서 적용
    }
}</code></pre>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">기존 변수 (하위 호환성)</h2>
            <p>다음 변수들은 Map 기반 breakpoint에서 자동으로 생성됩니다:</p>
            <ul style="margin-top: 16px; padding-left: 24px;">
                <li><code class="code">$mobile-xxs</code> = <code class="code">$bp["xxs"]</code></li>
                <li><code class="code">$mobile-xs</code> = <code class="code">$bp["xs"]</code></li>
                <li><code class="code">$mobile-sm</code> = <code class="code">$bp["sm"]</code></li>
                <li><code class="code">$mobile</code> = <code class="code">$bp["md"]</code></li>
                <li><code class="code">$desktop-xs</code> = <code class="code">$bp["lg"]</code></li>
                <li><code class="code">$desktop-sm</code> = <code class="code">$bp["xl"]</code></li>
                <li><code class="code">$desktop</code> = <code class="code">$bp["2xl"]</code></li>
                <li><code class="code">$desktop-lg</code> = <code class="code">$bp["3xl"]</code></li>
                <li><code class="code">$desktop-xl</code> = <code class="code">$bp["4xl"]</code></li>
            </ul>
        </div>
    """
    
    return content


# ============================================
# Typography 페이지
# ============================================

def extract_typography() -> Dict[str, Dict[str, str]]:
    """Typography 파일에서 font size와 weight 값을 추출합니다."""
    typo = {"sizes": {}, "weights": {}}
    if not TYPOGRAPHY_FILE.exists():
        return typo
    
    with open(TYPOGRAPHY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Font sizes 추출
    size_pattern = r'\$font-size-([a-z0-9-]+):\s*rem\((\d+)\);'
    size_matches = re.finditer(size_pattern, content)
    for match in size_matches:
        key = match.group(1)
        px_value = match.group(2)
        rem_value = f"{int(px_value) / 16}rem"
        typo["sizes"][key] = {"px": px_value, "rem": rem_value}
    
    # Font weights 추출
    weight_pattern = r'\$font-weight-([a-z]+):\s*(\d+);'
    weight_matches = re.finditer(weight_pattern, content)
    for match in weight_matches:
        key = match.group(1)
        value = match.group(2)
        typo["weights"][key] = value
    
    return typo


def generate_typography_page() -> str:
    """Typography 페이지 생성"""
    typo = extract_typography()
    
    content = """
        <h1>Typography</h1>
        <p class="subtitle">폰트 크기 및 굵기 설정값</p>
        
        <div class="section">
            <h2 class="section-title">Font Sizes</h2>
            <table>
                <thead>
                    <tr>
                        <th>변수명</th>
                        <th>rem 값</th>
                        <th>px 값</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Font sizes 정렬 (3xs부터 9xl까지)
    size_order = ["3xs", "2xs", "xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl", "9xl"]
    for size_key in size_order:
        if size_key in typo["sizes"]:
            size_info = typo["sizes"][size_key]
            content += f"""
                    <tr>
                        <td><code class="code">$font-size-{size_key}</code></td>
                        <td><code class="code">{size_info["rem"]}</code></td>
                        <td><code class="code">{size_info["px"]}px</code></td>
                        <td style="font-size: {size_info["rem"]};">예시 텍스트</td>
                    </tr>
            """
    
    content += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2 class="section-title">Font Weights</h2>
            <table>
                <thead>
                    <tr>
                        <th>변수명</th>
                        <th>값</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    weight_order = ["light", "normal", "medium", "semibold", "bold", "black"]
    for weight_key in weight_order:
        if weight_key in typo["weights"]:
            value = typo["weights"][weight_key]
            font_weight = int(value)
            content += f"""
                    <tr>
                        <td><code class="code">$font-weight-{weight_key}</code></td>
                        <td><code class="code">{value}</code></td>
                        <td style="font-weight: {font_weight};">예시 텍스트</td>
                    </tr>
            """
    
    content += """
                </tbody>
            </table>
        </div>
    """
    
    return content


# ============================================
# Spacing 페이지
# ============================================

def extract_spacing() -> Dict[str, str]:
    """Spacing 파일에서 spacing 값을 추출합니다."""
    spacing = {}
    if not SPACING_FILE.exists():
        return spacing
    
    with open(SPACING_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\$([a-z]+):\s*(\d+px);'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        key = match.group(1)
        value = match.group(2)
        spacing[key] = value
    
    return spacing


def generate_spacing_page() -> str:
    """Spacing 페이지 생성"""
    spacing = extract_spacing()
    
    content = """
        <h1>Spacing</h1>
        <p class="subtitle">간격 관련 변수 및 Utility Classes</p>
        
        <div class="section">
            <h2 class="section-title">Spacing Variables</h2>
            <table>
                <thead>
                    <tr>
                        <th>변수명</th>
                        <th>값</th>
                        <th>설명</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for key, value in spacing.items():
        desc = "기본 간격 단위 (margin, padding 기본값)" if key == "spacer" else ""
        content += f"""
                    <tr>
                        <td><code class="code">${key}</code></td>
                        <td><code class="code">{value}</code></td>
                        <td>{desc}</td>
                    </tr>
        """
    
    content += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2 class="section-title">Spacing Utility Classes</h2>
            <p>다음 utility classes를 사용하여 간격을 빠르게 적용할 수 있습니다:</p>
            
            <h3 style="font-size: 16px; font-weight: 600; margin-top: 24px; margin-bottom: 12px; color: #1e293b;">Margin Utilities</h3>
            <table>
                <thead>
                    <tr>
                        <th>클래스</th>
                        <th>설명</th>
                        <th>값</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code class="code">m-0</code></td><td>margin: 0</td><td>0</td></tr>
                    <tr><td><code class="code">m-1</code></td><td>margin: 0.25rem</td><td>4px</td></tr>
                    <tr><td><code class="code">m-2</code></td><td>margin: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">m-3</code></td><td>margin: 1rem</td><td>16px</td></tr>
                    <tr><td><code class="code">m-4</code></td><td>margin: 1.5rem</td><td>24px</td></tr>
                    <tr><td><code class="code">m-5</code></td><td>margin: 3rem</td><td>48px</td></tr>
                    <tr><td><code class="code">mt-2</code></td><td>margin-top: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">mb-2</code></td><td>margin-bottom: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">ms-2</code></td><td>margin-left: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">me-2</code></td><td>margin-right: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">m-auto</code></td><td>margin: auto</td><td>auto</td></tr>
                </tbody>
            </table>
            
            <h3 style="font-size: 16px; font-weight: 600; margin-top: 24px; margin-bottom: 12px; color: #1e293b;">Padding Utilities</h3>
            <table>
                <thead>
                    <tr>
                        <th>클래스</th>
                        <th>설명</th>
                        <th>값</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code class="code">p-0</code></td><td>padding: 0</td><td>0</td></tr>
                    <tr><td><code class="code">p-1</code></td><td>padding: 0.25rem</td><td>4px</td></tr>
                    <tr><td><code class="code">p-2</code></td><td>padding: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">p-3</code></td><td>padding: 1rem</td><td>16px</td></tr>
                    <tr><td><code class="code">p-4</code></td><td>padding: 1.5rem</td><td>24px</td></tr>
                    <tr><td><code class="code">p-5</code></td><td>padding: 3rem</td><td>48px</td></tr>
                    <tr><td><code class="code">pt-2</code></td><td>padding-top: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">pb-2</code></td><td>padding-bottom: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">ps-2</code></td><td>padding-left: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">pe-2</code></td><td>padding-right: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">px-2</code></td><td>padding-left + padding-right: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">py-2</code></td><td>padding-top + padding-bottom: 0.5rem</td><td>8px</td></tr>
                </tbody>
            </table>
            
            <h3 style="font-size: 16px; font-weight: 600; margin-top: 24px; margin-bottom: 12px; color: #1e293b;">Gap Utilities</h3>
            <table>
                <thead>
                    <tr>
                        <th>클래스</th>
                        <th>설명</th>
                        <th>값</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code class="code">gap-1</code></td><td>gap: 0.25rem</td><td>4px</td></tr>
                    <tr><td><code class="code">gap-2</code></td><td>gap: 0.5rem</td><td>8px</td></tr>
                    <tr><td><code class="code">gap-3</code></td><td>gap: 1rem</td><td>16px</td></tr>
                    <tr><td><code class="code">gap-4</code></td><td>gap: 1.5rem</td><td>24px</td></tr>
                    <tr><td><code class="code">gap-5</code></td><td>gap: 3rem</td><td>48px</td></tr>
                </tbody>
            </table>
            
            <div style="margin-top: 24px; padding: 16px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0;">
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 12px; color: #1e293b;">사용 방법</h3>
                <p style="margin-bottom: 12px; color: #64748b;">SCSS 파일에서 <code class="code">@include spacing-utils;</code>를 사용하여 utility classes를 생성합니다:</p>
                <pre style="background: #1e293b; color: #f8fafc; padding: 16px; border-radius: 4px; overflow-x: auto; font-size: 13px; line-height: 1.6;"><code>// 모든 utility classes 생성
@include spacing-utils;

// prefix를 사용한 경우 (예: "u")
@include spacing-utils("u");
// → .u-m-2, .u-p-2 등으로 생성됨</code></pre>
            </div>
        </div>
    """
    
    return content


# ============================================
# Fonts 페이지
# ============================================

def extract_fonts() -> Dict[str, str]:
    """Fonts 파일에서 font family 값을 추출합니다."""
    fonts = {}
    if not FONTS_VARIABLES_FILE.exists():
        return fonts
    
    with open(FONTS_VARIABLES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 전체 폰트 스택을 추출 (인용부호와 쉼표 포함)
    pattern = r'\$font-([a-z0-9-]+):\s*([^;]+);'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        key = match.group(1)
        value = match.group(2).strip()
        fonts[key] = value
    
    return fonts


def generate_fonts_page() -> str:
    """Fonts 페이지 생성"""
    fonts = extract_fonts()
    
    content = """
        <h1>Google Icons</h1>
        <p class="subtitle">폰트 패밀리 변수 및 Google Material Icons</p>
        
        <div class="section">
            <h2 class="section-title">Font Family Variables</h2>
            <table>
                <thead>
                    <tr>
                        <th>변수명</th>
                        <th>폰트 패밀리</th>
                        <th>설명</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    descriptions = {
        "basic": "기본 폰트",
        "monospace": "Monospace 폰트",
        "popup": "팝업용 폰트",
        "title": "타이틀 폰트",
        "title-2": "타이틀 폰트 2",
    }
    
    for key, value in fonts.items():
        desc = descriptions.get(key, "")
        content += f"""
                    <tr>
                        <td><code class="code">$font-{key}</code></td>
                        <td style="font-family: {value};"><code class="code">{value}</code></td>
                        <td>{desc}</td>
                    </tr>
        """
    
    content += """
                </tbody>
            </table>
        </div>
    """
    
    return content


# ============================================
# Mixins 페이지
# ============================================

def extract_mixins() -> Dict[str, Dict[str, str]]:
    """Mixins 파일들에서 mixin 정보를 추출합니다."""
    mixins = {}
    mixins_dir = ROOT_DIR / "mixins"
    
    mixin_files = {
        "border-radius": mixins_dir / "_border-radius.scss",
        "backdrop": mixins_dir / "_backdrop.scss",
        "button-hover": mixins_dir / "_button-hover.scss",
        "clearfix": mixins_dir / "_clearfix.scss",
        "ellipsis": mixins_dir / "_ellipsis.scss",
        "transform": mixins_dir / "_transform.scss",
        "transition": mixins_dir / "_transition.scss",
    }
    
    for name, file_path in mixin_files.items():
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Mixin 정의 찾기
            pattern = r'@mixin\s+([a-z0-9-]+)\s*(?:\(([^)]*)\))?\s*{'
            matches = re.finditer(pattern, content)
            
            mixin_list = []
            for match in matches:
                mixin_name = match.group(1)
                params = match.group(2) if match.group(2) else ""
                mixin_list.append({"name": mixin_name, "params": params})
            
            if mixin_list:
                mixins[name] = mixin_list
    
    return mixins


def generate_mixins_page() -> str:
    """Mixins 페이지 생성"""
    mixins = extract_mixins()
    
    content = """
        <h1>Mixins</h1>
        <p class="subtitle">사용 가능한 SCSS mixins</p>
    """
    
    # Border Radius Mixins
    if "border-radius" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Border Radius Mixins</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include border-radius</code></td>
                        <td>Generic border-radius (4개 코너 각각 지정 가능)</td>
                        <td><code class="code">@include border-radius(8px);</code><br><code class="code">@include border-radius(8px, 4px, 8px, 4px);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-none</code></td>
                        <td>border-radius: 0</td>
                        <td><code class="code">@include border-radius-none;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-xs</code></td>
                        <td>border-radius: 2px</td>
                        <td><code class="code">@include border-radius-xs;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-sm</code></td>
                        <td>border-radius: 4px</td>
                        <td><code class="code">@include border-radius-sm;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-md</code></td>
                        <td>border-radius: 6px</td>
                        <td><code class="code">@include border-radius-md;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-lg</code></td>
                        <td>border-radius: 8px</td>
                        <td><code class="code">@include border-radius-lg;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-xl</code></td>
                        <td>border-radius: 12px</td>
                        <td><code class="code">@include border-radius-xl;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-2xl</code></td>
                        <td>border-radius: 16px</td>
                        <td><code class="code">@include border-radius-2xl;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-3xl</code></td>
                        <td>border-radius: 24px</td>
                        <td><code class="code">@include border-radius-3xl;</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include border-radius-full</code></td>
                        <td>border-radius: 999px</td>
                        <td><code class="code">@include border-radius-full;</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Backdrop Mixins
    if "backdrop" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Backdrop Mixins</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include backdrop</code></td>
                        <td>backdrop-filter 적용</td>
                        <td><code class="code">@include backdrop(blur(10px));</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include blur</code></td>
                        <td>backdrop blur 효과</td>
                        <td><code class="code">@include blur(10px);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include filter</code></td>
                        <td>CSS filter 적용</td>
                        <td><code class="code">@include filter(brightness, 80%);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include drop-shadow</code></td>
                        <td>drop-shadow 효과</td>
                        <td><code class="code">@include drop-shadow(4px 5px 7px rgba(0, 0, 0, .6));</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Button Hover Mixin
    if "button-hover" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Button Hover Mixin</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include button-hover</code></td>
                        <td>버튼 hover 시 brightness 조절</td>
                        <td><code class="code">@include button-hover(120%);</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Clearfix Mixin
    if "clearfix" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Clearfix Mixin</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include clearfix</code></td>
                        <td>float 요소 정리</td>
                        <td><code class="code">@include clearfix;</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Ellipsis Mixin
    if "ellipsis" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Ellipsis Mixin</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include ellipsis</code></td>
                        <td>한 줄 말줄임</td>
                        <td><code class="code">@include ellipsis;</code> 또는 <code class="code">@include ellipsis(1);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include ellipsis(2)</code></td>
                        <td>두 줄 말줄임</td>
                        <td><code class="code">@include ellipsis(2);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include ellipsis(3)</code></td>
                        <td>세 줄 말줄임</td>
                        <td><code class="code">@include ellipsis(3);</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Transform Mixins
    if "transform" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Transform Mixins</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include transform</code></td>
                        <td>CSS transform 적용</td>
                        <td><code class="code">@include transform(rotate(45deg));</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include rotate</code></td>
                        <td>회전</td>
                        <td><code class="code">@include rotate(45);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include scale</code></td>
                        <td>크기 조절</td>
                        <td><code class="code">@include scale(1.2);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include translate</code></td>
                        <td>이동</td>
                        <td><code class="code">@include translate(10px, 20px);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include skew</code></td>
                        <td>기울임</td>
                        <td><code class="code">@include skew(10, 20);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include transform-origin</code></td>
                        <td>transform 기준점 설정</td>
                        <td><code class="code">@include transform-origin(center);</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    # Transition Mixins
    if "transition" in mixins:
        content += """
        <div class="section">
            <h2 class="section-title">Transition Mixins</h2>
            <table>
                <thead>
                    <tr>
                        <th>Mixin</th>
                        <th>설명</th>
                        <th>사용 예시</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code class="code">@include transition</code></td>
                        <td>CSS transition 적용</td>
                        <td><code class="code">@include transition(background-color 1s 2s, color 2s);</code><br><code class="code">@include transition(0.3s);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include transition-property</code></td>
                        <td>transition 속성 지정</td>
                        <td><code class="code">@include transition-property(background-color, color);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include transition-duration</code></td>
                        <td>transition 지속 시간</td>
                        <td><code class="code">@include transition-duration(0.3s);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include transition-timing-function</code></td>
                        <td>transition 타이밍 함수</td>
                        <td><code class="code">@include transition-timing-function(ease-in-out);</code></td>
                    </tr>
                    <tr>
                        <td><code class="code">@include transition-delay</code></td>
                        <td>transition 지연 시간</td>
                        <td><code class="code">@include transition-delay(0.2s);</code></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    return content


# ============================================
# Index 페이지 (홈)
# ============================================

def generate_index_page() -> str:
    """Index 페이지 (홈/목차) 생성"""
    content = """
        <h1>Shared SCSS Documentation</h1>
        <p class="subtitle">shared-scss의 모든 변수와 설정값을 확인할 수 있는 사양서</p>
        
        <div class="section">
            <h2 class="section-title">카테고리</h2>
            <div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px;">
    """
    
    for item in NAV_ITEMS[1:]:  # 홈 제외
        content += f"""
                <a href="{item["url"]}" style="text-decoration: none; color: inherit;">
                    <div class="card" style="cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;">
                        <div class="card-title" style="font-size: 18px; margin-bottom: 8px;">{item["title"]}</div>
                        <div class="card-value" style="color: #64748b; font-size: 14px;">
                            {item["title"]} 관련 변수와 설정값을 확인할 수 있습니다.
                        </div>
                    </div>
                </a>
        """
    
    content += """
            </div>
        </div>
    """
    
    return content


# ============================================
# Main
# ============================================

def main():
    """메인 함수 - 모든 페이지 생성"""
    print("Shared SCSS Documentation 생성 중...")
    
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Index 페이지
    print("  - index.html 생성 중...")
    index_content = generate_index_page()
    with open(DOCS_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("홈", index_content, "index.html"))
    
    # Breakpoints 페이지
    print("  - breakpoints.html 생성 중...")
    breakpoints_content = generate_breakpoints_page()
    with open(DOCS_DIR / "breakpoints.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Breakpoints", breakpoints_content, "breakpoints.html"))
    
    # Typography 페이지
    print("  - typography.html 생성 중...")
    typography_content = generate_typography_page()
    with open(DOCS_DIR / "typography.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Typography", typography_content, "typography.html"))
    
    # Spacing 페이지
    print("  - spacing.html 생성 중...")
    spacing_content = generate_spacing_page()
    with open(DOCS_DIR / "spacing.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Spacing", spacing_content, "spacing.html"))
    
    # Fonts 페이지 (Google Icons)
    print("  - fonts.html 생성 중...")
    fonts_content = generate_fonts_page()
    with open(DOCS_DIR / "fonts.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Google Icons", fonts_content, "fonts.html"))
    
    # Colors 페이지 (기존 코드 활용 필요)
    print("  - colors.html 생성 중...")
    colors_content = generate_colors_page()
    with open(DOCS_DIR / "colors.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Colors", colors_content, "colors.html"))
    
    # Mixins 페이지
    print("  - mixins.html 생성 중...")
    mixins_content = generate_mixins_page()
    with open(DOCS_DIR / "mixins.html", 'w', encoding='utf-8') as f:
        f.write(generate_html_page("Mixins", mixins_content, "mixins.html"))
    
    print(f"✓ 모든 문서가 {DOCS_DIR} 디렉토리에 생성되었습니다!")


if __name__ == "__main__":
    main()

