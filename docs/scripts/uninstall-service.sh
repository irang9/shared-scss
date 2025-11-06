#!/bin/bash
# macOS launchd 서비스 제거 스크립트

LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.rexbox.docs-watcher.plist"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "🛑 RexBox 문서 자동화 서비스 제거"
echo ""

if [ ! -f "$PLIST_PATH" ]; then
    echo "⚠️  서비스가 설치되어 있지 않습니다."
    exit 0
fi

# 서비스 중지
echo "서비스 중지 중..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true

# 파일 제거
echo "서비스 파일 제거 중..."
rm -f "$PLIST_PATH"

echo "✅ 서비스 제거 완료!"

