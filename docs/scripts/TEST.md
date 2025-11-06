# RexBox 문서 자동화 서비스 테스트 가이드

## 📋 테스트 체크리스트

### 1. 기본 설정 확인

```bash
# 프로젝트 루트로 이동
cd /Users/irang/Github/rexbox

# Python3 설치 확인
python3 --version

# watchdog 모듈 설치 확인 (필요시 설치)
python3 -c "import watchdog" || pip3 install watchdog

# 스크립트 파일 존재 확인
ls -la docs/scripts/
```

### 2. 문서 생성 스크립트 테스트

```bash
# 수동으로 문서 생성 테스트
cd docs
python3 scripts/generate-docs.py

# 생성된 HTML 파일 확인
ls -la *.html
```

### 3. 파일 감시 스크립트 테스트 (수동 실행)

```bash
# 파일 감시 스크립트 직접 실행
cd /Users/irang/Github/rexbox
python3 docs/scripts/watch-theme-colors.py

# 다른 터미널에서 SCSS 파일 수정하여 자동 생성 확인
# 예: rexbox/theme/_index.scss 파일을 수정하고 저장
```

### 4. macOS 서비스 설치 테스트

```bash
# 서비스 설치
cd /Users/irang/Github/rexbox
./docs/scripts/install-service.sh

# 서비스 상태 확인
launchctl list | grep com.rexbox.docs-watcher

# 로그 확인
tail -f /tmp/rexbox-docs-watcher.log

# 에러 로그 확인 (필요시)
tail -f /tmp/rexbox-docs-watcher-error.log
```

### 5. 자동 문서 생성 테스트

```bash
# SCSS 파일 수정하여 자동 생성 확인
# 예: rexbox/theme/_index.scss 파일을 수정하고 저장

# 로그에서 변경 감지 확인
tail -f /tmp/rexbox-docs-watcher.log

# 생성된 HTML 파일의 수정 시간 확인
ls -lt docs/*.html | head -5
```

### 6. 서비스 제거 테스트

```bash
# 서비스 제거
./docs/scripts/uninstall-service.sh

# 서비스 제거 확인
launchctl list | grep com.rexbox.docs-watcher
# (출력이 없어야 함)

# plist 파일 제거 확인
ls -la ~/Library/LaunchAgents/com.rexbox.docs-watcher.plist
# (파일이 없어야 함)
```

## 🔍 문제 해결

### 서비스가 시작되지 않는 경우

1. **로그 확인:**
   ```bash
   tail -20 /tmp/rexbox-docs-watcher-error.log
   ```

2. **plist 파일 확인:**
   ```bash
   cat ~/Library/LaunchAgents/com.rexbox.docs-watcher.plist
   ```

3. **수동 실행 테스트:**
   ```bash
   cd /Users/irang/Github/rexbox
   python3 docs/scripts/watch-theme-colors.py
   ```

### 문서가 자동 생성되지 않는 경우

1. **파일 감시 대상 확인:**
   - `rexbox/theme/_index.scss`
   - `rexbox/variables/_colors.scss`
   - 기타 SCSS 파일

2. **로그에서 변경 감지 확인:**
   ```bash
   tail -f /tmp/rexbox-docs-watcher.log
   ```

3. **수동 문서 생성 테스트:**
   ```bash
   cd docs
   python3 scripts/generate-docs.py
   ```

## ✅ 완료 조건

- [ ] 문서 생성 스크립트가 정상 작동
- [ ] 파일 감시 스크립트가 정상 작동
- [ ] macOS 서비스가 정상 설치됨
- [ ] SCSS 파일 수정 시 자동으로 문서가 생성됨
- [ ] 서비스 제거가 정상 작동함

