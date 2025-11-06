#!/bin/bash
# 색상 파일 변경 감시 시작 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

# Python 가상환경 확인 (선택사항)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# watchdog 패키지 확인 및 설치 안내
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  watchdog 패키지가 필요합니다."
    echo ""
    echo "설치 방법:"
    echo "  pip3 install watchdog"
    echo ""
    echo "또는:"
    echo "  python3 -m pip install watchdog"
    echo ""
    read -p "지금 설치하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install watchdog
    else
        echo "설치를 건너뜁니다. Git pre-commit hook을 사용하세요."
        exit 1
    fi
fi

# watcher 시작
python3 "$SCRIPT_DIR/watch-theme-colors.py"

