#!/bin/bash
# macOS launchd 서비스 설치 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.rexbox.docs-watcher.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.rexbox.docs-watcher.plist"

echo "🚀 RexBox 문서 자동화 서비스 설치"
echo ""

# launchd 디렉토리 확인 및 생성
if [ ! -d "$LAUNCH_AGENTS_DIR" ]; then
    mkdir -p "$LAUNCH_AGENTS_DIR"
    echo "✓ LaunchAgents 디렉토리 생성: $LAUNCH_AGENTS_DIR"
fi

# 기존 서비스 중지 및 제거 (새로운 이름)
if [ -f "$LAUNCH_AGENTS_DIR/$PLIST_NAME" ]; then
    echo "⚠️  기존 서비스 발견. 중지 중..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true
    rm -f "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
    echo "✓ 기존 서비스 제거 완료"
fi

# 이전 버전 서비스 제거 (com.irang.shared-scss.color-guide)
OLD_PLIST_NAME="com.irang.shared-scss.color-guide.plist"
if [ -f "$LAUNCH_AGENTS_DIR/$OLD_PLIST_NAME" ]; then
    echo "⚠️  이전 버전 서비스 발견. 중지 중..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$OLD_PLIST_NAME" 2>/dev/null || true
    rm -f "$LAUNCH_AGENTS_DIR/$OLD_PLIST_NAME"
    echo "✓ 이전 버전 서비스 제거 완료"
fi

# Python 경로 확인
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "❌ python3를 찾을 수 없습니다."
    exit 1
fi

# PLIST 파일의 Python 경로 업데이트
echo "📝 서비스 파일 생성 중..."
sed "s|/usr/bin/python3|$PYTHON_PATH|g" "$PLIST_FILE" > "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# 스크립트 경로 업데이트
SCRIPT_PATH="$SCRIPT_DIR/watch-theme-colors.py"
sed -i '' "s|REPLACE_WITH_SCRIPT_PATH|$SCRIPT_PATH|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
sed -i '' "s|REPLACE_WITH_WORKING_DIR|$SCRIPT_DIR/../..|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# 서비스 시작
echo "🔄 서비스 시작 중..."
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 서비스 설치 완료!"
    echo ""
    echo "📋 서비스 상태 확인:"
    echo "   launchctl list | grep com.rexbox.docs-watcher"
    echo ""
    echo "📋 로그 확인:"
    echo "   tail -f /tmp/rexbox-docs-watcher.log"
    echo ""
    echo "🛑 서비스 중지:"
    echo "   launchctl unload $LAUNCH_AGENTS_DIR/$PLIST_NAME"
    echo ""
    echo "🗑️  서비스 제거:"
    echo "   ./docs/scripts/uninstall-service.sh"
    echo ""
    echo "이제 컴퓨터를 재부팅해도 자동으로 실행됩니다! 🎉"
else
    echo "❌ 서비스 시작 실패"
    exit 1
fi

