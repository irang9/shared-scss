# RexBox

여러 프로젝트에서 공통으로 사용하는 SCSS 변수, mixins, 유틸리티 클래스 라이브러리입니다.

## 📚 온라인 문서

**👉 [온라인 문서 보기](https://irang9.github.io/rexbox/)** (GitHub Pages)

문서에서 모든 변수, mixins, 유틸리티 클래스를 확인할 수 있습니다.

## 📁 프로젝트 구조

이 저장소는 다음과 같은 구조로 구성되어 있습니다:

```
rexbox/
├── rexbox/           # SCSS 라이브러리 (메인)
│   ├── variables/    # 변수 (colors, typo, spacing)
│   ├── breakpoints/  # Breakpoint 변수와 mixins
│   ├── theme/        # 의미 색상 (semantic colors)
│   ├── mixins/       # Mixins
│   ├── fonts/        # 기본 폰트 파일 (Spoqa, Material Icons)
│   ├── base/         # 기본 스타일 (reset)
│   ├── utilities/    # 유틸리티 클래스
│   ├── _index.scss   # 메인 진입점
│   └── README.md     # 상세 문서
├── docs/             # 문서 (HTML)
│   ├── index.html
│   ├── colors.html
│   ├── typography.html
│   ├── breakpoints.html
│   ├── spacing.html
│   ├── borders.html
│   ├── stacks.html
│   ├── vertical-rule.html
│   ├── mixins.html
│   ├── scripts/          # 문서 생성 스크립트
│   └── assets/           # 정적 파일 (favicon 등)
└── README.md         # 이 파일
```

## 📂 디렉토리 설명

### `rexbox/` - SCSS 라이브러리

실제 SCSS 라이브러리 코드가 들어있는 디렉토리입니다. 다른 프로젝트에서 이 디렉토리를 참조하여 사용합니다.

**주요 내용:**
- **variables/**: 색상, 타이포그래피, spacing 등 변수 정의
- **breakpoints/**: 반응형 디자인을 위한 breakpoint 변수와 mixins
- **theme/**: 의미 색상 (primary, secondary, success 등)
- **mixins/**: 재사용 가능한 SCSS mixins
- **fonts/**: 기본 폰트 파일 (Spoqa, Material Icons) - 선택적 폰트는 프로젝트별로 관리
- **base/**: 기본 스타일 (reset, forms 등)
- **utilities/**: 유틸리티 클래스 (Bootstrap 스타일)

**사용 방법:**
```scss
// 프로젝트의 SCSS 파일에서
@use '../rexbox/rexbox' as *;

// 또는 필요한 것만 선택적으로
@use '../rexbox/rexbox/variables' as *;
@use '../rexbox/rexbox/breakpoints' as *;
@use '../rexbox/rexbox/theme' as *;
@use '../rexbox/rexbox/mixins' as *;
```

자세한 사용 방법은 [`rexbox/README.md`](./rexbox/README.md)를 참고하세요.

### `docs/` - 문서

HTML 형식의 문서가 들어있는 디렉토리입니다. GitHub Pages를 통해 온라인으로 제공됩니다.

**주요 내용:**
- **index.html**: 문서 홈페이지
- **colors.html**: 색상 변수 문서
- **typography.html**: 타이포그래피 문서
- **breakpoints.html**: Breakpoint 문서
- **spacing.html**: Spacing 문서
- **borders.html**: Border 유틸리티 문서
- **stacks.html**: Stacks 유틸리티 문서
- **vertical-rule.html**: Vertical Rule 유틸리티 문서
- **mixins.html**: Mixins 문서
- **scripts/**: 문서 생성 스크립트 디렉토리

**문서 업데이트:**
`rexbox/` 디렉토리의 SCSS 파일을 수정한 후, 다음 명령어로 문서를 자동 생성할 수 있습니다:

```bash
cd docs
python3 scripts/generate-docs.py
```

문서는 `rexbox/` 디렉토리의 SCSS 파일을 파싱하여 자동으로 생성되므로, SCSS 코드를 수정하면 문서도 함께 업데이트됩니다.

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/irang9/rexbox.git
cd rexbox
```

### 2. 다른 프로젝트에서 사용

#### 방법 A: Git 서브모듈로 추가 (권장)

```bash
# 프로젝트 디렉토리에서
git submodule add https://github.com/irang9/rexbox.git rexbox
```

#### 방법 B: 직접 복사

```bash
# rexbox/rexbox 디렉토리를 프로젝트에 복사
cp -r rexbox/rexbox /path/to/your/project/
```

### 3. SCSS 파일에서 사용

```scss
// 프로젝트의 SCSS 파일에서
@use '../rexbox/rexbox' as *;

// 또는 필요한 것만 선택적으로
@use '../rexbox/rexbox/variables' as *;
@use '../rexbox/rexbox/breakpoints' as *;
@use '../rexbox/rexbox/theme' as *;
@use '../rexbox/rexbox/mixins' as *;
```

### 4. 프로젝트별 커스터마이징

프로젝트별 설정 파일(`_config.scss`)을 만들어 색상 등을 오버라이드할 수 있습니다.

#### 폰트 커스터마이징

프로젝트별 선택적 폰트는 프로젝트의 `fonts/` 디렉토리에서 관리합니다:

```scss
// 프로젝트의 fonts/_gmarket.scss
@font-face {
    font-family: 'GmarketSans';
    src: url('...') format('woff');
}

// _config.scss
$font-gmarket: "GmarketSans", "Spoqa Han Sans Neo", ...;

// main.scss
@use 'fonts/gmarket' as *;
```

**참고:** RexBox는 기본 폰트(`$font-basic`, `$font-monospace`)와 Material Icons만 제공합니다. 선택적 폰트는 프로젝트별로 다를 수 있으므로 각 프로젝트에서 관리합니다.

## 📖 더 알아보기

- **[온라인 문서](https://irang9.github.io/rexbox/)** - 모든 변수와 설정값 확인
- **[RexBox 상세 문서](./rexbox/README.md)** - 라이브러리 상세 설명

## 🔧 문서 업데이트

`rexbox/` 디렉토리의 SCSS 파일을 수정한 후, 문서를 업데이트하려면:

```bash
cd docs
python3 scripts/generate-docs.py
```

문서는 자동으로 `rexbox/` 디렉토리의 SCSS 파일을 파싱하여 생성되므로, SCSS 코드를 수정하면 문서도 함께 업데이트됩니다.

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

