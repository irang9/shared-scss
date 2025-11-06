# Shared SCSS

여러 프로젝트에서 공통으로 사용하는 SCSS 변수, mixins, typography 파일 모음입니다.

## 구조

```
shared-scss/
├── _index.scss        # 통합 파일 (모든 것을 한 번에 가져오기)
├── variables/          # 변수 파일들 (원시 데이터)
│   ├── _colors.scss   # 원시 색상 팔레트
│   ├── _typo.scss     # Typography 변수 (font-size, font-weight, rem 함수)
│   ├── _spacing.scss  # Spacing 변수
│   └── _index.scss
├── breakpoints/       # Breakpoints (도메인 중심)
│   └── _index.scss    # breakpoint 변수와 mixin 모두 포함
├── theme/             # 테마 설정 (의미 색상)
│   └── _index.scss    # 의미 색상 (bg-light, text-primary 등)
├── mixins/            # Mixin 파일들
│   ├── _backdrop.scss
│   ├── _bootstrap.scss
│   ├── _border-radius.scss
│   ├── _button-hover.scss
│   ├── _clearfix.scss
│   ├── _ellipsis.scss
│   ├── _transform.scss
│   ├── _transition.scss
│   └── _index.scss
├── fonts/             # 폰트 파일들
│   ├── _variables.scss # 폰트 패밀리 변수 (프로젝트별 오버라이드 가능)
│   ├── _spoqa.scss   # Spoqa Han Sans Neo
│   ├── _google.scss  # Google Fonts (Material Icons, Outfit)
│   ├── _gmarket.scss # Gmarket Sans
│   ├── _scoredream.scss # SCoreDream
│   └── _index.scss   # 모든 폰트와 변수 통합
├── base/              # 기본 스타일
│   └── _reset.scss    # CSS Reset 스타일
├── utilities/         # 유틸리티 클래스
│   ├── _colors.scss   # 색상 유틸리티 클래스
│   ├── _display.scss  # Display 유틸리티 클래스
│   ├── _flex.scss     # Flexbox 유틸리티 클래스
│   ├── _position.scss # Position 유틸리티 클래스
│   ├── _spacing.scss  # Spacing 유틸리티 클래스 (margin, padding, gap)
│   ├── _text.scss     # Typography 유틸리티 클래스
│   └── _index.scss
└── README.md
```

## 사용 방법

### 방법 1: 통합 파일 사용 (권장 - 간편함)

변수, breakpoints, theme, mixins, fonts, base, utilities를 한 번에 가져오려면:

```scss
@use '../../shared-scss' as *;
```

**포함 내용:**
- `variables`: 모든 변수 (colors, typo, spacing)
- `breakpoints`: breakpoint 변수와 mixin
- `theme`: 의미 색상
- `mixins`: 모든 mixin
- `fonts`: 필수 폰트만 (spoqa, google) - 폰트 변수 포함
- `base/reset`: CSS Reset 스타일
- `utilities`: 모든 유틸리티 클래스

**참고:**
- fonts는 필수 폰트(spoqa, google)만 자동으로 포함됩니다
- 선택적 폰트(gmarket, scoredream)는 프로젝트에서 직접 import하세요:
  ```scss
  @use '../../shared-scss' as *;
  @use '../../shared-scss/fonts/gmarket' as *;  // 필요 시 추가
  ```

**장점:**
- 한 줄로 모든 모듈을 가져올 수 있어 간편함
- 실수로 일부만 가져오는 것을 방지
- 필수 폰트만 포함되어 CSS 파일 크기 최적화

**단점:**
- 모든 유틸리티 클래스가 포함되어 CSS 파일 크기가 커질 수 있음

### 방법 2: 개별 파일 사용 (권장 - 최적화)

필요한 것만 선택적으로 가져오려면:

```scss
// Variables만 사용
@use '../../shared-scss/variables' as *;

// Mixins만 사용
@use '../../shared-scss/mixins' as *;

// Fonts만 사용
@use '../../shared-scss/fonts' as *;
```

또는 조합해서 사용:

```scss
// Variables, Breakpoints, Theme, Mixins만 사용 (typo 제외)
@use '../../shared-scss/variables' as *;
@use '../../shared-scss/breakpoints' as *;
@use '../../shared-scss/theme' as *;
@use '../../shared-scss/mixins' as *;
```

**장점:**
- 필요한 것만 선택적으로 가져와 CSS 파일 크기 최적화
- fonts가 필요 없는 경우 폰트 import를 제외할 수 있음
- 개별 폰트만 선택적으로 import 가능 (예: `@use '../../shared-scss/fonts/spoqa'`)

**단점:**
- 여러 줄 작성 필요

### 예시

**방법 1: 통합 파일 사용**
```scss
@charset "utf-8";
@use '../../shared-scss' as *;

.my-component {
    color: $primary;
    padding: $spacer;
    
    @include mobile {
        padding: $spacer / 2;
    }
}
```

**방법 2: 개별 파일 사용 (typo 제외)**
```scss
@charset "utf-8";
@use '../../shared-scss/variables' as *;
@use '../../shared-scss/breakpoints' as *;
@use '../../shared-scss/theme' as *;
@use '../../shared-scss/mixins' as *;

.my-component {
    background-color: $bg-light;   // theme에서 정의
    color: $text-primary;          // theme에서 정의
    padding: $spacer;
    width: $mobile;                // breakpoints 변수 사용
    
    @include mobile {              // breakpoints mixin 사용
        padding: $spacer / 2;
    }
}
```

## 파일 설명

### Variables (변수 파일들)

- `_colors.scss`: 원시 색상 팔레트 (yellow-50, gray-500, blue-600 등 기본 색상 값)
- `_typo.scss`: Typography 변수 (font-size, font-weight, rem 함수)
  - **폰트 패밀리 변수는 `fonts/_variables.scss`로 이동되었습니다**
- `_spacing.scss`: Spacing 변수 (기본 간격 단위)

### Breakpoints (도메인 중심)

- `_index.scss`: breakpoint 변수와 mixin을 함께 관리
  - **변수**: `$mobile`, `$desktop` 등 breakpoint 값
  - **Mixin**: `@mixin mobile`, `@include from-mobile` 등 미디어쿼리 mixin
  
**구조 설계 이유:**
- breakpoints는 변수와 mixin이 강하게 결합되어 있어 도메인 중심으로 관리
- 관련 코드가 한 파일에 모여 있어 유지보수가 쉬움
- 변수와 mixin을 함께 사용할 때 파일 이동 없이 한 곳에서 확인 가능

### Theme (테마 설정)

- `_index.scss`: 의미 색상 (bg-light, text-primary 등 실제 사용 목적별 매핑)

#### 색상 구조 설명

색상은 두 단계로 구성됩니다:

1. **원시 색상 (`variables/_colors.scss`)**: 기본 색상 팔레트
   ```scss
   $yellow-200: #fef08a;
   $gray-900: #111827;
   $blue-600: #2563eb;
   ```

2. **의미 색상 (`theme/_index.scss`)**: 사용 목적별 매핑
   ```scss
   $bg-light: $yellow-200;      // 배경에 사용할 밝은 색
   $text-primary: $gray-900;    // 주요 텍스트 색상
   $primary: $blue-600;         // 브랜드 주요 색상
   ```

이렇게 분리하면:
- **명확한 구조**: `variables/`는 순수 변수, `theme/`는 테마 설정으로 역할이 명확함
- **테마 변경 용이**: 원시 색상만 변경하면 자동 반영
- **유지보수 편의**: 색상 팔레트와 사용 목적이 명확히 분리됨
- **프로젝트별 커스터마이징**: 프로젝트별로 다른 의미 색상을 쉽게 정의 가능

### Mixins

모든 mixin 파일은 독립적으로 동작하며, 필요한 경우에만 다른 모듈을 참조합니다.

- `_border-radius.scss`: border-radius 관련 mixins (값이 mixin 내부에 하드코딩됨)
- `_backdrop.scss`: backdrop-filter 관련 mixins
- `_bootstrap.scss`: Bootstrap 관련 mixins (현재 비어있음)
- `_button-hover.scss`: 버튼 호버 효과 mixin
- `_clearfix.scss`: clearfix mixin
- `_ellipsis.scss`: 텍스트 말줄임 mixin (한 줄/여러 줄 지원)
- `_transform.scss`: transform 관련 mixins (rotate, scale, translate, skew 등)
- `_transition.scss`: transition 관련 mixins

### Fonts (폰트 파일들)

- `_index.scss`: 필수 폰트(spoqa, google)와 폰트 변수를 포함
- `_variables.scss`: 폰트 패밀리 변수 (`$font-basic`, `$font-title` 등) - **프로젝트별 오버라이드 가능**
- `_spoqa.scss`: Spoqa Han Sans Neo 폰트 import (필수)
- `_google.scss`: Google Fonts (Material Icons, Outfit) import (필수)
- `_gmarket.scss`: Gmarket Sans 폰트 (@font-face 정의) - 선택적
- `_scoredream.scss`: SCoreDream 폰트 (@font-face 정의) - 선택적

**구조 설계 이유:**
- 필수 폰트와 선택적 폰트를 분리하여 CSS 파일 크기 최적화
- 각 폰트를 개별 파일로 분리하여 선택적 import 가능
- 프로젝트별로 다른 폰트 조합 사용 가능
- 폰트 패밀리 변수를 fonts에 통합하여 폰트 관련 설정을 한 곳에서 관리

**사용 예시:**

```scss
// 방법 1: 통합 파일 사용 (필수 폰트만 포함)
@use '../../shared-scss' as *;
// 결과: spoqa, google만 자동 포함

// 방법 2: fonts만 사용 (필수 폰트 포함)
@use '../../shared-scss/fonts' as *;
// 결과: spoqa, google만 포함

// 방법 3: 선택적 폰트 추가
@use '../../shared-scss' as *;
@use '../../shared-scss/fonts/gmarket' as *;      // Gmarket 추가
@use '../../shared-scss/fonts/scoredream' as *;   // SCoreDream 추가

// 방법 4: 특정 폰트만 사용
@use '../../shared-scss/fonts/spoqa' as *;
@use '../../shared-scss/fonts/google' as *;
```

**프로젝트별 폰트 변수 커스터마이징:**
프로젝트에서 다른 폰트 패밀리를 사용하려면:
```scss
// 프로젝트의 _typo.scss 또는 별도 파일에서
@use '../../shared-scss/fonts/variables' as * with (
  $font-basic: "CustomFont", "Spoqa Han Sans Neo", sans-serif,
  $font-title: "TitleFont", "Spoqa Han Sans Neo", sans-serif
);
```

### Base (기본 스타일)

- `_reset.scss`: CSS Reset 스타일
  - 브라우저 기본 스타일 초기화
  - `variables`, `fonts`, `breakpoints`를 사용하여 스타일 정의
  - 사용 예시:
    ```scss
    @use '../../shared-scss/base/reset' as *;
    ```

### Utilities (유틸리티 클래스)

유틸리티 클래스는 프로젝트에서 바로 사용할 수 있는 CSS 클래스들을 제공합니다.

- `_colors.scss`: 색상 유틸리티 클래스 (`.red`, `.positive`, `.negative`, `.neutral` 등)
- `_display.scss`: Display 유틸리티 클래스 (`.d-flex`, `.d-none`, `.d-block` 등)
- `_flex.scss`: Flexbox 유틸리티 클래스 (`.flex-row`, `.justify-center`, `.items-center` 등)
- `_position.scss`: Position 유틸리티 클래스 (`.position-relative`, `.position-absolute` 등)
- `_spacing.scss`: Spacing 유틸리티 클래스 (`.m-1`, `.p-2`, `.gap-3` 등)
- `_text.scss`: Typography 유틸리티 클래스 (`.fs-sm`, `.fw-bold`, `.text-center` 등)

**사용 예시:**
```scss
// 모든 유틸리티 클래스 사용
@use '../../shared-scss/utilities' as *;

// 특정 유틸리티만 사용
@use '../../shared-scss/utilities/colors' as *;
@use '../../shared-scss/utilities/spacing' as *;
```

## 사용 시나리오별 권장 방법

- **대부분의 경우**: 통합 파일 사용 (`@use '../../shared-scss' as *`)
  - 필수 폰트(spoqa, google)만 포함되어 최적화됨
  - base, utilities도 자동 포함

- **CSS 파일 크기 최적화가 중요한 경우**: 개별 파일 사용
  ```scss
  @use '../../shared-scss/variables' as *;
  @use '../../shared-scss/breakpoints' as *;
  @use '../../shared-scss/theme' as *;
  @use '../../shared-scss/mixins' as *;
  // utilities, base, fonts 제외
  ```

- **폰트가 이미 다른 방식으로 로드되는 경우**: 통합 파일 사용 후 fonts 제외
  ```scss
  @use '../../shared-scss/variables' as *;
  @use '../../shared-scss/breakpoints' as *;
  @use '../../shared-scss/theme' as *;
  @use '../../shared-scss/mixins' as *;
  @use '../../shared-scss/base/reset' as *;
  @use '../../shared-scss/utilities' as *;
  ```

- **선택적 폰트가 필요한 경우**: 통합 파일 + 선택적 폰트 추가
  ```scss
  @use '../../shared-scss' as *;
  @use '../../shared-scss/fonts/gmarket' as *;  // 필요 시 추가
  ```

- **유틸리티 클래스가 필요 없는 경우**: utilities 제외
  ```scss
  @use '../../shared-scss/variables' as *;
  @use '../../shared-scss/breakpoints' as *;
  @use '../../shared-scss/theme' as *;
  @use '../../shared-scss/mixins' as *;
  @use '../../shared-scss/fonts' as *;
  @use '../../shared-scss/base/reset' as *;
  ```

- **CSS Reset이 필요 없는 경우**: base/reset 제외
  ```scss
  @use '../../shared-scss/variables' as *;
  @use '../../shared-scss/breakpoints' as *;
  @use '../../shared-scss/theme' as *;
  @use '../../shared-scss/mixins' as *;
  @use '../../shared-scss/fonts' as *;
  @use '../../shared-scss/utilities' as *;
  ```

- **특정 폰트만 필요한 경우**: fonts의 개별 파일만 import
  ```scss
  @use '../../shared-scss/fonts/spoqa' as *;
  @use '../../shared-scss/fonts/google' as *;
  ```

- **테마 없이 원시 색상만 필요한 경우**: variables만 사용
- **breakpoint 변수만 필요한 경우**: breakpoints만 사용 (mixin도 함께 포함됨)

## 주의사항

- 이 폴더의 파일들은 직접 CSS로 컴파일되지 않습니다 (부분 파일)
- 각 프로젝트에서 `@use`로 import하여 사용합니다
- 경로는 프로젝트의 위치에 따라 조정해야 합니다
- `fonts`는 폰트를 외부에서 import하므로, 필요 없는 경우 제외하는 것을 권장합니다
- 개별 폰트 파일을 선택적으로 import하여 필요한 폰트만 사용할 수 있습니다
- `utilities`는 CSS 클래스를 생성하므로, 필요한 경우에만 사용하는 것을 권장합니다
- `base/_reset.scss`는 전역 스타일을 초기화하므로, 프로젝트의 최상단에서 한 번만 import해야 합니다

## Import 구조 최적화

모든 파일은 필요한 의존성만 import하도록 최적화되어 있습니다:

- **Mixins**: 대부분의 mixin 파일은 독립적으로 동작하며 불필요한 dependency가 없습니다
- **Variables**: `variables/_colors.scss`는 순수 변수만 정의하며 다른 모듈을 참조하지 않습니다
- **Theme**: `theme/_index.scss`는 `variables/_colors.scss`만 참조합니다
- **Utilities**: `utilities/_colors.scss`는 `variables`와 `theme`를 참조하며, 나머지 유틸리티 파일들은 필요한 경우에만 `variables`나 `fonts`를 참조합니다
- **Base**: `base/_reset.scss`는 `variables`, `fonts`, `breakpoints`를 참조합니다

이 구조를 통해 순환 참조를 방지하고, 필요한 것만 선택적으로 import할 수 있습니다.

