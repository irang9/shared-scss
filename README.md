# Shared SCSS

여러 프로젝트에서 공통으로 사용하는 SCSS 변수, mixins, typography 파일 모음입니다.

## 구조

```
shared-scss/
├── variables/          # 변수 파일들
│   ├── _colors.scss
│   ├── _breakpoints.scss
│   ├── _typo.scss
│   ├── _border-radius.scss
│   └── _index.scss
├── mixins/            # Mixin 파일들
│   ├── _backdrop.scss
│   ├── _bootstrap.scss
│   ├── _border-radius.scss
│   ├── _breakpoints.scss
│   ├── _button-hover.scss
│   ├── _clearfix.scss
│   ├── _ellipsis.scss
│   ├── _transform.scss
│   ├── _transition.scss
│   └── _index.scss
├── typo/              # Typography 파일들
│   ├── _spoqa.scss
│   ├── _google.scss
│   ├── _gmarket.scss
│   ├── _scoredream.scss
│   └── _index.scss
└── README.md
```

## 사용 방법

### 프로젝트에서 사용하기

각 프로젝트의 SCSS 파일에서 다음과 같이 import 합니다:

```scss
// Variables 사용
@use '../../shared-scss/variables' as *;

// Mixins 사용
@use '../../shared-scss/mixins' as *;

// Typography 사용
@use '../../shared-scss/typo' as *;
```

또는 전체를 한 번에:

```scss
@use '../../shared-scss/variables' as *;
@use '../../shared-scss/mixins' as *;
@use '../../shared-scss/typo' as *;
```

### 예시

```scss
@charset "utf-8";
@use '../../shared-scss/variables' as *;
@use '../../shared-scss/mixins' as *;

.my-component {
    color: $primary;
    padding: $spacer;
    
    @include mobile {
        padding: $spacer / 2;
    }
}
```

## 파일 설명

### Variables

- `_colors.scss`: 색상 변수 (primary, secondary, slate, gray 등)
- `_breakpoints.scss`: 반응형 브레이크포인트 변수
- `_typo.scss`: 폰트 관련 변수 (font-family, font-size, font-weight)
- `_border-radius.scss`: border-radius 관련 변수

### Mixins

- `_breakpoints.scss`: 반응형 미디어쿼리 mixins
- `_border-radius.scss`: border-radius 관련 mixins
- `_backdrop.scss`: backdrop-filter 관련 mixins
- `_button-hover.scss`: 버튼 호버 효과 mixin
- `_clearfix.scss`: clearfix mixin
- `_ellipsis.scss`: 텍스트 말줄임 mixin
- `_transform.scss`: transform 관련 mixins
- `_transition.scss`: transition 관련 mixins

### Typo

- `_spoqa.scss`: Spoqa Han Sans Neo 폰트 import
- `_google.scss`: Google Fonts (Material Icons, Outfit) import
- `_gmarket.scss`: Gmarket Sans 폰트
- `_scoredream.scss`: SCoreDream 폰트

## 주의사항

- 이 폴더의 파일들은 직접 CSS로 컴파일되지 않습니다 (부분 파일)
- 각 프로젝트에서 `@use`로 import하여 사용합니다
- 경로는 프로젝트의 위치에 따라 조정해야 합니다

