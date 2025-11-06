# Sample Project - RexBox 사용 예제

이 프로젝트는 `RexBox`를 사용하여 프로젝트별 커스터마이징을 하는 방법을 보여주는 예제입니다.

## 파일 구조

```
sample-project/
├── scss/
│   ├── _config.scss          # 프로젝트별 설정 (오버라이드)
│   ├── main.scss             # 메인 스타일 파일
│   └── components/           # 컴포넌트 스타일들
│       ├── _header.scss
│       ├── _hero.scss
│       ├── _cards.scss
│       └── _footer.scss
├── css/
│   └── main.css              # 컴파일된 CSS 파일 (자동 생성)
├── index.html                # 예제 HTML 파일
└── README.md                 # 이 파일
```

## 사용 방법

### 1. SCSS 컴파일

#### 방법 A: VS Code Live Sass Compiler 사용 (권장)

1. VS Code에서 `Live Sass Compiler` 확장 설치
2. `scss/main.scss` 파일 열기
3. 하단 상태바에서 "Watch Sass" 클릭
4. 자동으로 `css/main.css` 파일이 생성됩니다

#### 방법 B: 명령줄 사용

```bash
# Dart Sass 설치 (필요시)
npm install -g sass

# 컴파일
sass scss/main.scss css/main.css

# Watch 모드 (파일 변경 시 자동 컴파일)
sass --watch scss/main.scss css/main.css
```

**참고:** sample-project는 rexbox 디렉토리 안에 있습니다:
```
rexbox/
├── rexbox/         # SCSS 라이브러리
├── docs/           # 문서
└── sample-project/ # 예제 프로젝트
```

### 2. HTML에서 사용

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Sample Project</title>
    <!-- 컴파일된 CSS 파일 링크 -->
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <!-- 내용 -->
</body>
</html>
```

## 커스터마이징 방법

### 1. 색상 오버라이드

`scss/_config.scss` 파일에서 RexBox의 기본 색상을 오버라이드할 수 있습니다:

```scss
// RexBox 기본값 import
@use '../../rexbox/variables' as *;
@use '../../rexbox/breakpoints' as *;

// Primary 색상 오버라이드 (theme import 전에 정의)
$primary: #ff6b6b;
$primary-light: #ff8787;
$primary-dark: #ee5a6f;

// Secondary 색상 오버라이드
$secondary: #4ecdc4;

// Theme import (위에서 정의한 변수가 !default를 덮어씁니다)
@use '../../rexbox/theme' as *;
```

**주의사항:**
- `_config.scss`에서 변수를 정의한 후 `theme`을 import하면, 정의한 변수가 theme의 기본값을 덮어씁니다.
- theme 파일의 변수들이 `!default`를 사용하므로, config에서 정의한 값이 우선됩니다.

### 2. 프로젝트별 선택적 폰트 추가

프로젝트별 선택적 폰트는 프로젝트의 `fonts/` 디렉토리에서 관리합니다:

```scss
// 1. fonts/_gmarket.scss 파일 생성 (폰트 정의)
@font-face {
    font-family: 'GmarketSans';
    src: url('...') format('woff');
    font-weight: 300;
}

// 2. _config.scss에서 폰트 변수 정의
$font-gmarket: "GmarketSans", "Spoqa Han Sans Neo", ...;

// 3. main.scss에서 폰트 import
@use 'fonts/gmarket' as *;

// 4. 사용
.title {
    font-family: config.$font-gmarket;
}
```

**주의사항:**
- RexBox는 기본 폰트(spoqa, icons)만 제공합니다.
- 선택적 폰트는 프로젝트별로 다를 수 있으므로 각 프로젝트에서 관리합니다.

### 3. 프로젝트 전용 변수 추가

RexBox에 없는 프로젝트 전용 변수를 추가할 수 있습니다:

```scss
// 프로젝트 전용 색상
$brand-accent: #ffd93d;
$brand-gradient-start: #ff6b6b;
$brand-gradient-end: #4ecdc4;

// 프로젝트 전용 spacing
$section-padding: 60px;
$card-gap: 24px;
```

### 4. 컴포넌트에서 사용

컴포넌트 파일에서 오버라이드된 변수와 mixins를 사용할 수 있습니다:

```scss
// scss/components/_header.scss
// 프로젝트 설정과 RexBox import
// 주의: config와 theme 모두 변수를 정의하므로,
// config는 namespace로, theme은 *로 import
@use '../config' as config;
@use '../../../rexbox/theme' as *;
@use '../../../rexbox/variables' as *;
@use '../../../rexbox/breakpoints' as *;

.header {
    background: white;
    border-bottom: 1px solid $border-default;  // theme 변수
    padding: 16px 0;
    
    &__logo {
        color: $primary;  // theme에서 오버라이드된 primary 색상 사용
        @include rounded-lg;  // RexBox mixin 사용
    }
    
    @include down("md") {  // RexBox breakpoint mixin
        // 모바일 스타일
    }
    
    // 프로젝트 전용 변수 사용
    &__custom {
        padding: config.$section-padding;  // config의 프로젝트 전용 변수
    }
}
```

## 주요 기능

### 1. 색상 시스템
- RexBox의 semantic 색상 변수 사용
- 프로젝트별 브랜드 색상 오버라이드
- 프로젝트 전용 색상 추가

### 2. Mixins 활용
- `@include rounded-lg` - border-radius
- `@include down("md")` - 반응형 미디어쿼리
- `@include transition` - transition 효과

### 3. Utility Classes
- `.border`, `.border-primary` - Border 유틸리티
- `.rounded`, `.rounded-lg` - Border radius 유틸리티
- `.hstack`, `.vstack` - Stacks 유틸리티
- `.gap-*`, `.p-*`, `.m-*` - Spacing 유틸리티

### 4. 반응형 디자인
- Breakpoint mixins를 사용한 모바일/태블릿/데스크톱 대응
- `@include up("md")` - Mobile First
- `@include down("md")` - Desktop First

## 참고사항

- `_config.scss`는 프로젝트별 설정 파일로, RexBox의 기본값을 오버라이드합니다.
- `main.scss`는 모든 스타일을 통합하는 메인 파일입니다.
- 컴포넌트 스타일은 `components/` 디렉토리에 모듈화하여 관리합니다.
- HTML에서는 컴파일된 CSS 파일만 링크하면 됩니다.

## 더 알아보기

- [RexBox README](../README.md)
- [RexBox 문서](../docs/index.html)

