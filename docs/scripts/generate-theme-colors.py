#!/usr/bin/env python3
"""
RexBox Theme Colors HTML Generator
SCSS 파일에서 색상 변수를 추출하여 index.html 파일을 자동 생성합니다.
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple

# 프로젝트 루트 디렉토리
# scripts 디렉토리에서 rexbox 디렉토리로의 경로
ROOT_DIR = Path(__file__).parent.parent.parent / "rexbox"
DOCS_DIR = Path(__file__).parent.parent
VARIABLES_COLORS_FILE = ROOT_DIR / "variables" / "_colors.scss"
THEME_FILE = ROOT_DIR / "theme" / "_index.scss"
OUTPUT_FILE = DOCS_DIR / "index.html"


def extract_color_variables(scss_file: Path) -> Dict[str, str]:
    """SCSS 파일에서 색상 변수를 추출합니다."""
    colors = {}
    
    if not scss_file.exists():
        print(f"Warning: {scss_file} 파일이 없습니다.")
        return colors
    
    with open(scss_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # $variable-name: #hex; 또는 $variable-name: #hex; // comment 패턴 매칭
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
        print(f"Warning: {theme_file} 파일이 없습니다.")
        return mappings
    
    with open(theme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # $semantic-name: $base-color; 패턴 매칭
    pattern = r'\$([a-z0-9-]+):\s*\$([a-z0-9-]+)\s*;'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        semantic_name = match.group(1)
        base_color_var = match.group(2)
        
        # base_color_var에서 실제 색상 값 찾기
        if base_color_var in color_vars:
            mappings[semantic_name] = (base_color_var, color_vars[base_color_var])
    
    return mappings


def sort_color_by_brightness(color_list: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """색상을 밝은 순서대로 정렬합니다. 숫자가 없는 것 먼저, 그 다음 50, 100, 200... 순서"""
    def get_sort_key(item):
        var_name = item[0]
        # 숫자 추출
        match = re.search(r'-(\d+)$', var_name)
        if match:
            num = int(match.group(1))
            # 50이 있으면 50이 100보다 앞에 오도록 (50이 더 밝음)
            # 숫자가 작을수록 밝음 (50 < 100 < 200...)
            return (1, num)  # 숫자가 있으면 (1, 숫자)
        else:
            return (0, 0)  # 숫자가 없으면 (0, 0) - 가장 앞에
    
    return sorted(color_list, key=get_sort_key)


def get_category_order_from_file(color_vars: Dict[str, str]) -> Dict[str, int]:
    """variables/_colors.scss 파일에서 카테고리가 나타나는 순서를 추적합니다."""
    category_order = {}
    order = 0
    seen_categories = set()
    
    # 파일에서 변수 정의 순서대로 읽기
    with open(VARIABLES_COLORS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 변수 추출 패턴
    pattern = r'\$([a-z0-9-]+):\s*#[0-9a-fA-F]{3,8}\s*;'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        var_name = match.group(1)
        
        # 카테고리 추출
        if var_name in ['white', 'white-real', 'black', 'black-real']:
            category = 'Global'
        else:
            parts = var_name.split('-')
            if len(parts) > 1:
                category = parts[0].capitalize()
            else:
                continue
        
        # 카테고리가 처음 나타날 때만 순서 기록
        if category not in seen_categories:
            seen_categories.add(category)
            category_order[category] = order
            order += 1
    
    return category_order


def generate_html(color_vars: Dict[str, str], theme_mappings: Dict[str, Tuple[str, str]]) -> str:
    """HTML 파일 내용을 생성합니다."""
    
    # 카테고리 순서 가져오기
    category_order_map = get_category_order_from_file(color_vars)
    
    # 색상 카테고리별로 분류
    categories = {
        'Global': [],
        'Slate': [],
        'Gray': [],
        'Zinc': [],
        'Neutral': [],
        'Stone': [],
        'Lime': [],
        'Green': [],
        'Emerald': [],
        'Teal': [],
        'Cyan': [],
        'Sky': [],
        'Blue': [],
        'Indigo': [],
        'Violet': [],
        'Purple': [],
        'Fuchsia': [],
        'Pink': [],
        'Rose': [],
        'Red': [],
        'Orange': [],
        'Amber': [],
        'Yellow': [],
    }
    
    # 색상 변수 분류
    for var_name, color_value in sorted(color_vars.items()):
        # 카테고리 추출
        category = None
        for cat in categories.keys():
            if var_name.startswith(cat.lower()):
                category = cat
                break
        
        if not category:
            # 특수 케이스
            if var_name in ['white', 'white-real', 'black', 'black-real']:
                category = 'Global'
            else:
                # 기본 카테고리 추측
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
            # 숫자가 붙은 primary-*는 제외 (primary-100, primary-200 등)
            brand_colors.append(item)
        elif semantic_name in ['success', 'warning', 'error', 'info', 'valid', 'invalid']:
            state_colors.append(item)
        elif semantic_name in ['positive', 'negative', 'neutral', 'stock-up', 'stock-down', 'stock-neutral', 'stock-positive', 'stock-negative', 'value-red', 'value-blue', 'gapup', 'gapdown']:
            stock_colors.append(item)
        elif semantic_name.startswith('link'):
            link_colors.append(item)
    
    # HTML 생성
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RexBox Theme Colors</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            color: #212121;
            margin-bottom: 10px;
            font-size: 32px;
        }}
        .subtitle {{
            color: #64748b;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .section {{
            background: white;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .color-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }}
        .color-item {{
            display: flex;
            flex-direction: column;
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            background: white;
        }}
        .color-swatch {{
            width: 100%;
            height: 80px;
            position: relative;
        }}
        .color-info {{
            padding: 8px;
            font-size: 11px;
        }}
        .color-name {{
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
        }}
        .color-value {{
            color: #64748b;
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        .semantic-colors {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }}
        .semantic-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f8fafc;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        .semantic-item.bg-example {{
            padding: 16px;
        }}
        .semantic-item.text-example {{
            padding: 16px;
        }}
        .semantic-item.border-example {{
            padding: 16px;
        }}
        .semantic-swatch {{
            width: 48px;
            height: 48px;
            border-radius: 4px;
            flex-shrink: 0;
            border: 1px solid #e2e8f0;
        }}
        .semantic-info {{
            flex: 1;
        }}
        .semantic-name {{
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 4px;
            font-size: 13px;
        }}
        .semantic-value {{
            color: #64748b;
            font-size: 11px;
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        .category-group {{
            margin-bottom: 32px;
        }}
        .category-title {{
            font-size: 18px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 16px;
            margin-top: 32px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .category-title:first-child {{
            margin-top: 0;
        }}
        .example-text {{
            font-size: 14px;
            font-weight: 500;
        }}
        .palette-group {{
            margin-bottom: 32px;
        }}
        .palette-title {{
            font-size: 16px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 12px;
            margin-top: 24px;
        }}
        .palette-title:first-child {{
            margin-top: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>RexBox Theme Colors</h1>
        <p class="subtitle">RexBox의 theme과 variables 색상 팔레트</p>
"""

    # Semantic Colors 섹션
    html += """
        <!-- Semantic Colors (Theme) -->
        <div class="section">
            <h2 class="section-title">Semantic Colors (Theme)</h2>
"""
    
    # Background Colors
    if bg_colors:
        html += """
            <!-- Background Colors -->
            <div class="category-group">
                <div class="category-title">Background Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(bg_colors):
            text_color = "#1e293b" if not name.startswith('bg-dark') else "#ffffff"
            border_style = 'border: 1px solid #e2e8f0;' if color.upper() in ['#FCFCFC', '#FFFFFF'] else ''
            html += f"""
                    <div class="semantic-item bg-example" style="background: {color}; {border_style}">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {text_color};">background-color: ${name};</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # Text Colors
    if text_colors:
        html += """
            <!-- Text Colors -->
            <div class="category-group">
                <div class="category-title">Text Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(text_colors):
            bg_color = "#111827" if name == 'text-inverse' else "#ffffff"
            border_style = 'border: 1px solid #e2e8f0;' if bg_color == '#ffffff' else ''
            html += f"""
                    <div class="semantic-item text-example" style="background: {bg_color}; {border_style}">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {color};">color: ${name};</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # Border Colors
    if border_colors:
        html += """
            <!-- Border Colors -->
            <div class="category-group">
                <div class="category-title">Border Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(border_colors):
            html += f"""
                    <div class="semantic-item border-example" style="background: #ffffff; border: 2px solid {color};">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: #1e293b;">border: 1px solid ${name};</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # Brand Colors
    if brand_colors:
        html += """
            <!-- Brand Colors -->
            <div class="category-group">
                <div class="category-title">Brand Colors</div>
                <div class="semantic-colors">
"""
        # brand_colors는 primary가 가장 앞에 오도록 정렬
        brand_colors_sorted = sorted(brand_colors, key=lambda x: (0 if x[0] == 'primary' else 1, x[0]))
        for name, color, base_var in brand_colors_sorted:
            html += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # State Colors
    if state_colors:
        html += """
            <!-- State Colors -->
            <div class="category-group">
                <div class="category-title">State Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(state_colors):
            html += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # Stock Colors
    if stock_colors:
        html += """
            <!-- Stock Colors -->
            <div class="category-group">
                <div class="category-title">Stock/Finance State Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(stock_colors):
            html += f"""
                    <div class="semantic-item">
                        <div class="semantic-swatch" style="background: {color};"></div>
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    # Link Colors
    if link_colors:
        html += """
            <!-- Link Colors -->
            <div class="category-group">
                <div class="category-title">Link Colors</div>
                <div class="semantic-colors">
"""
        for name, color, base_var in sort_color_by_brightness(link_colors):
            html += f"""
                    <div class="semantic-item text-example" style="background: #ffffff; border: 1px solid #e2e8f0;">
                        <div class="semantic-info">
                            <div class="semantic-name">${name}</div>
                            <div class="semantic-value">{color}</div>
                            <div class="example-text" style="margin-top: 8px; color: {color}; text-decoration: underline;">color: ${name};</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    html += """
        </div>
"""
    
    # Primary Color Scale (theme에서 정의된 primary-* 색상들)
    primary_mappings = {name: (base_var, color) for name, (base_var, color) in theme_mappings.items() if name.startswith('primary-') or name == 'primary'}
    primary_colors = []
    
    # primary를 먼저 추가
    if 'primary' in primary_mappings:
        _, color = primary_mappings['primary']
        primary_colors.append(('primary', color))
    
    # primary-50, primary-100, primary-200... 순서대로 추가 (50이 있으면 50이 가장 앞)
    # 먼저 50이 있는지 확인
    if 'primary-50' in primary_mappings:
        _, color = primary_mappings['primary-50']
        primary_colors.append(('primary-50', color))
    
    # primary-100부터 primary-900까지 순서대로 추가
    for num in range(100, 1000, 100):
        name = f'primary-{num}'
        if name in primary_mappings:
            _, color = primary_mappings[name]
            primary_colors.append((name, color))
    
    if primary_colors:
        html += """
        <!-- Primary Color Scale -->
        <div class="section">
            <h2 class="section-title">Primary Color Scale</h2>
            <div class="color-grid">
"""
        for name, color_value in primary_colors:
            
            html += f"""
                <div class="color-item">
                    <div class="color-swatch" style="background: {color_value};"></div>
                    <div class="color-info">
                        <div class="color-name">${name}</div>
                        <div class="color-value">{color_value}</div>
                    </div>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    # Color Palettes 섹션
    html += """
        <!-- Color Palettes -->
        <div class="section">
            <h2 class="section-title">Color Palettes</h2>
"""
    
    # 카테고리를 variables/_colors.scss 파일의 순서대로 정렬
    # Global이 가장 먼저, 그 다음은 파일에서 나타나는 순서대로
    def get_category_sort_key(item):
        category, color_list = item
        if category == 'Global':
            return (-1, category)  # Global이 가장 앞
        order = category_order_map.get(category, 999)  # 순서가 없으면 뒤로
        return (order, category)
    
    sorted_categories = sorted(categories.items(), key=get_category_sort_key)
    
    for category, color_list in sorted_categories:
        if not color_list:
            continue
        
        html += f"""
            <div class="palette-group">
                <div class="palette-title">{category}</div>
                <div class="color-grid">
"""
        # 밝은 색상 순서대로 정렬
        sorted_color_list = sort_color_by_brightness(color_list)
        for var_name, color_value in sorted_color_list:
            border_style = 'border: 1px solid #e2e8f0;' if color_value.upper() in ['#FCFCFC', '#FFFFFF'] else ''
            html += f"""
                    <div class="color-item">
                        <div class="color-swatch" style="background: {color_value}; {border_style}"></div>
                        <div class="color-info">
                            <div class="color-name">${var_name}</div>
                            <div class="color-value">{color_value}</div>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """메인 함수"""
    print("RexBox Theme Colors HTML 생성 중...")
    
    # 색상 변수 추출
    print(f"  - {VARIABLES_COLORS_FILE} 파일 읽는 중...")
    color_vars = extract_color_variables(VARIABLES_COLORS_FILE)
    print(f"  - {len(color_vars)}개의 색상 변수 발견")
    
    # Theme 매핑 추출
    print(f"  - {THEME_FILE} 파일 읽는 중...")
    theme_mappings = extract_theme_mappings(THEME_FILE, color_vars)
    print(f"  - {len(theme_mappings)}개의 semantic color 매핑 발견")
    
    # HTML 생성
    print("  - HTML 생성 중...")
    html_content = generate_html(color_vars, theme_mappings)
    
    # 파일 저장
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ {OUTPUT_FILE} 파일이 생성되었습니다!")


if __name__ == "__main__":
    main()

