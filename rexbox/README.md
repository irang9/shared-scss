# RexBox

여러 프로젝트에서 공통으로 사용하는 SCSS 변수, mixins, 유틸리티 클래스 라이브러리입니다.

## 📚 문서

**👉 [온라인 문서 보기](https://irang9.github.io/rexbox/)** (GitHub Pages)

문서에서 모든 변수, mixins, 유틸리티 클래스를 확인할 수 있습니다.

## 📁 프로젝트 구조

이 README는 `rexbox/` 라이브러리 디렉토리 내에 있습니다. 전체 프로젝트 구조:

```
rexbox/                    # 프로젝트 루트
├── rexbox/                # SCSS 라이브러리 (메인) - 이 디렉토리
│   ├── variables/         # 변수 (colors, typo, spacing)
│   ├── breakpoints/       # Breakpoint 변수와 mixins
│   ├── theme/             # 의미 색상 (semantic colors)
│   ├── mixins/            # Mixins
│   ├── fonts/             # 기본 폰트 파일 (Spoqa, Material Icons)
│   ├── base/              # 기본 스타일 (reset)
│   ├── utilities/         # 유틸리티 클래스
│   ├── _index.scss        # 메인 진입점
│   └── README.md          # 이 파일
├── docs/                  # 문서 (HTML)
│   ├── scripts/           # 문서 생성 스크립트
│   ├── assets/            # 정적 파일 (favicon 등)
│   ├── index.html
│   ├── colors.html
│   └── ...
├── sample-project/        # 사용 예제
│   ├── scss/
│   ├── css/
│   └── index.html
└── README.md              # 프로젝트 루트 README
```

## 🚀 빠른 시작

### 1. 설치

```bash
# Git 서브모듈로 추가 (권장)
git submodule add https://github.com/irang9/rexbox.git rexbox

# 또는 직접 클론
git clone https://github.com/irang9/rexbox.git
cd rexbox
```

### 2. 사용

```scss
// 프로젝트의 SCSS 파일에서
// rexbox 디렉토리를 프로젝트에 복사하거나 서브모듈로 추가한 경우
@use '../rexbox/rexbox' as *;

// 또는 필요한 것만 선택적으로
@use '../rexbox/rexbox/variables' as *;
@use '../rexbox/rexbox/breakpoints' as *;
@use '../rexbox/rexbox/theme' as *;
@use '../rexbox/rexbox/mixins' as *;
```

### 3. 커스터마이징

프로젝트별 설정 파일(`_config.scss`)을 만들어 색상 등을 오버라이드할 수 있습니다:

```scss
// _config.scss
@use '../rexbox/rexbox/variables' as *;
@use '../rexbox/rexbox/breakpoints' as *;

// Primary 색상 오버라이드
$primary: #ff6b6b;
$secondary: #4ecdc4;

// Theme import (위에서 정의한 변수가 기본값을 덮어씁니다)
@use '../rexbox/rexbox/theme' as *;
```

자세한 사용 방법은 [sample-project](../sample-project/)를 참고하세요.

## ✨ 주요 기능

### Variables (변수)
- **Colors**: Tailwind 기반 색상 팔레트
- **Typography**: Font-size, font-weight, rem 함수
- **Spacing**: Margin, padding, gap 변수

### Breakpoints
- Bootstrap 5 표준과 일치하는 breakpoint
- Mobile First / Desktop First mixins
- `@include up("md")`, `@include down("md")`, `@include between("xs", "lg")`

### Theme (의미 색상)
- Semantic color variables (`$primary`, `$secondary`, `$success` 등)
- Background, text, border 색상
- 프로젝트별 오버라이드 가능

### Mixins
- `rounded`: Border-radius mixins (Bootstrap 스타일)
- `transition`: Transition 효과
- `transform`: Transform 효과
- `ellipsis`: 텍스트 말줄임
- 기타 유용한 mixins

### Fonts (폰트)
- **기본 폰트**: `$font-basic`, `$font-monospace` (Spoqa Han Sans Neo 기반)
- **Material Icons**: Google Material Icons 자동 포함
- **선택적 폰트**: 프로젝트별 `fonts/` 디렉토리에서 관리 (Gmarket, Google Fonts 등)

### Utilities (유틸리티 클래스)
- **Borders**: Border 추가/제거, width, color, radius, opacity
- **Colors**: 색상 유틸리티
- **Display**: Display 유틸리티
- **Flex**: Flexbox 유틸리티
- **Spacing**: Margin, padding, gap
- **Stacks**: `.vstack`, `.hstack` (Bootstrap 스타일)
- **Vertical Rule**: `.vr` (수직 구분선)
- **Text**: Typography 유틸리티

## 📖 문서

- [온라인 문서](https://irang9.github.io/rexbox/) - 모든 변수와 설정값 확인
- [Sample Project](../sample-project/) - 사용 예제

## 🎯 사용 예시

### 색상 사용
```scss
.button {
    background-color: $primary;
    color: white;
    border: 1px solid $border-default;
}
```

### Breakpoint 사용
```scss
.container {
    padding: 16px;
    
    @include up("md") {
        padding: 24px;  // 768px 이상
    }
    
    @include down("sm") {
        padding: 12px;  // 575.98px 이하
    }
}
```

### Mixin 사용
```scss
.card {
    @include rounded-lg;
    @include transition(transform 0.2s);
    
    &:hover {
        transform: translateY(-4px);
    }
}
```

### Utility Classes 사용
```html
<div class="border border-primary rounded-lg p-4">
    <div class="hstack gap-3">
        <span>Item 1</span>
        <div class="vr"></div>
        <span>Item 2</span>
    </div>
</div>
```

## 🔧 커스터마이징

프로젝트별로 색상, spacing 등을 커스터마이징할 수 있습니다. 자세한 방법은 [sample-project](../sample-project/README.md)를 참고하세요.

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

