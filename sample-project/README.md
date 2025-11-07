sample-project/
sass --watch scss/main.scss css/main.css
# Sample Project

샘플 프로젝트는 RexBox SCSS 라이브러리를 **프로젝트 맞춤형으로 통합·오버라이드하는 패턴**을 보여줍니다. 이 README는 디렉터리 구조, 빌드 플로우, 커스터마이징 지점을 한눈에 정리합니다.

## 1. 디렉터리 구조

```
sample-project/
├── scss/
│   ├── _config.scss         # 프로젝트 설정(색상·spacing·폰트 변수)
│   ├── _rexbox-base.scss    # RexBox 공통 리소스 forward 묶음
│   ├── _project-fonts.scss  # 프로젝트 전용 폰트 forward 묶음
│   ├── _global.scss         # 전역 스타일 (본문, 유틸리티 클래스 등)
│   ├── main.scss            # 엔트리 포인트 (컴파일 대상)
│   └── components/          # 개별 컴포넌트 스타일
│       ├── _header.scss
│       ├── _hero.scss
│       ├── _cards.scss
│       └── _footer.scss
├── css/
│   └── main.css             # 컴파일 결과물 (자동 생성)
├── index.html               # 샘플 마크업 (스타일 미리보기)
└── README.md                # 이 문서
```

## 2. 빌드 & 프리뷰

### 2-1. SCSS → CSS 컴파일

#### 옵션 A · VS Code Live Sass Compiler (권장)
1. VS Code에서 **Live Sass Compiler** 설치
2. `scss/main.scss` 열기 → 하단 상태바의 **Watch Sass** 클릭
3. 변경 사항이 저장될 때마다 `css/main.css`가 자동 갱신

#### 옵션 B · 명령줄에서 Dart Sass 사용

```bash
# 필요 시 Dart Sass 설치
npm install -g sass

# 1회 컴파일
sass scss/main.scss css/main.css

# Watch 모드 (파일 변경 시 자동 컴파일)
sass --watch scss/main.scss css/main.css
```

### 2-2. HTML 확인

```bash
open index.html      # macOS
# or
start index.html     # Windows
```

브라우저를 열어 UI, 반응형 동작, 유틸리티 클래스를 바로 확인할 수 있습니다.

## 3. 스타일 구성 흐름

1. **`_config.scss`** – RexBox 기본값을 덮어쓰고 프로젝트 전용 변수를 선언합니다.
2. **`_rexbox-base.scss`** – RexBox theme/variables/breakpoints/mixins/fonts를 한 번에 forward 합니다.
3. **`_project-fonts.scss`** – 프로젝트에서 사용하는 선택 폰트를 forward 합니다.
4. **`_global.scss`** – 공통 전역 스타일과 간단한 유틸리티 클래스를 정의합니다.
5. **`components/*.scss`** – 실제 UI 컴포넌트별 스타일을 모듈화합니다.
6. **`main.scss`** – 위 모듈들을 import 후, 컴포넌트와 전역 스타일을 묶어 최종 CSS를 생성합니다.

이 구조 덕분에 RexBox에서 가져온 자원과 프로젝트 전용 리소스를 명확히 구분할 수 있습니다.

## 4. 커스터마이징 포인트

### 4-1. 색상 & 테마 값 오버라이드

`_config.scss`에서 RexBox 변수(map)를 재정의한 뒤, `main.scss`에서 theme을 `with` 옵션으로 불러옵니다.

```scss
// _config.scss (발췌)
@use '../../rexbox/variables' as *;
@use '../../rexbox/breakpoints' as *;

$primary: #ff6b6b;
$secondary: #4ecdc4;
$point: #ffd93d;

$section-padding: 60px;
$card-gap: 24px;
```

```scss
// main.scss (발췌)
@use '../../rexbox/theme' as * with (
  $primary: config.$primary,
  $secondary: config.$secondary,
  $point: config.$point,
  ...
);
```

### 4-2. 프로젝트 전용 폰트 묶기

`fonts/_gmarket.scss` 같은 개별 폰트 정의를 `_project-fonts.scss`에서 forward 하면, 컴포넌트는 `@use '../project-fonts'` 한 줄로 모든 폰트에 접근할 수 있습니다.

```scss
// _project-fonts.scss
@forward 'fonts/gmarket';
// @forward 'fonts/google';
// @forward 'fonts/scoredream';

// components/_hero.scss
@use '../project-fonts' as *;
```

### 4-3. 공통 리소스 공용화

`_rexbox-base.scss`는 theme, mixin, breakpoints 등 RexBox 핵심 리소스를 forward 하고 있으므로, 컴포넌트는 다음과 같이 간단하게 import 합니다.

```scss
@use '../config' as config;
@use '../rexbox-base' as *;
@use '../project-fonts' as *;

.hero {
  background: linear-gradient(135deg, $primary 0%, $secondary 100%);
  @include rounded-lg;
  @include down('md') { ... }
}
```

## 5. 포함된 UI 요소

- **Hero**: 브랜드 그라디언트 배경과 CTA 버튼
- **Cards**: Grid + 카드 호버 효과, Breakpoint 기반 1열 전환
- **Header/Footer**: 반응형 네비게이션, 다단 Footer
- **Utility 활용**: `.border-*`, `.rounded-*`, `.hstack`, `.vstack`, spacing 유틸리티 등

각 컴포넌트는 RexBox에 없는 프로젝트 전용 변수(`config.$section-padding`)와 RexBox mixin(`@include transition`)을 함께 사용하는 예시로 작성되어 있습니다.

## 6. 팁 & 참고

- `_config.scss`에서 선언한 뒤 theme을 import해야 `!default` 변수가 올바르게 덮어집니다.
- `sass --watch`를 실행한 터미널은 SCSS 구조를 바꿀 때마다 자동으로 CSS를 다시 생성합니다.
- 유틸리티 클래스는 이미 CSS로 컴파일되므로, SCSS에서 mixin처럼 호출할 필요 없이 HTML에서 바로 사용하면 됩니다.
- 필요 없는 컴포넌트는 `main.scss`에서 `@use 'components/...'` 라인을 주석 처리하거나 제거하면 됩니다.

## 7. 추가 자료

- [RexBox README](../README.md) – 저장소 전반 개요
- [RexBox 라이브러리 상세](../rexbox/README.md)
- [온라인 문서](../docs/index.html) – 색상·타입스케일·유틸리티 전체 목록

---

의도에 맞게 더 단순화하거나 컴포넌트를 교체하고 싶다면, `_rexbox-base.scss`와 `_project-fonts.scss`를 수정해 자신만의 “기본 진입점”으로 활용하세요.

