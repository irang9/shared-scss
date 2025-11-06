#!/usr/bin/env python3
"""
RexBox Documentation File Watcher
SCSS 파일이 변경될 때마다 자동으로 모든 문서 페이지를 생성합니다.
"""

import sys
import time
import subprocess
from pathlib import Path

# macOS/Linux용 (watchdog 패키지 필요)
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️  watchdog 패키지가 설치되지 않았습니다.")
    print("   설치: pip3 install watchdog")
    print("   또는 Git pre-commit hook을 사용하세요.")
    sys.exit(1)


class DocsHandler(FileSystemEventHandler):
    """SCSS 파일 변경 감지 핸들러"""
    
    def __init__(self, script_path):
        self.script_path = script_path
        self.last_modified = 0
        self.debounce_time = 0.5  # 0.5초 debounce
    
    def on_modified(self, event):
        """파일 수정 이벤트 처리"""
        if event.is_directory:
            return
        
        # 관련 SCSS 파일만 처리
        if not event.src_path.endswith(('.scss')):
            return
        
        # docs 디렉토리 내 파일은 무시 (생성된 HTML 파일)
        if 'docs' in event.src_path:
            return
        
        # Debounce: 너무 빠른 연속 수정 방지
        current_time = time.time()
        if current_time - self.last_modified < self.debounce_time:
            return
        self.last_modified = current_time
        
        # 상대 경로 계산 (프로젝트 루트 기준)
        try:
            project_root = self.script_path.parent.parent.parent
            rel_path = Path(event.src_path).relative_to(project_root)
        except ValueError:
            rel_path = Path(event.src_path)
        print(f"\n📝 변경 감지: {rel_path}")
        print("   문서 페이지 생성 중...")
        
        try:
            # 스크립트 실행 (docs/ 디렉토리에서 실행)
            result = subprocess.run(
                [sys.executable, str(self.script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.script_path.parent.parent)  # docs/ 디렉토리
            )
            
            if result.returncode == 0:
                print("   ✓ 모든 문서 페이지가 업데이트되었습니다.\n")
            else:
                print(f"   ✗ 오류 발생:\n{result.stderr}\n")
        except Exception as e:
            print(f"   ✗ 오류: {e}\n")


def main():
    """메인 함수"""
    root_dir = Path(__file__).parent.parent.parent / "rexbox"
    script_path = Path(__file__).parent / "generate-docs.py"
    
    # 감시할 디렉토리 (SCSS 파일이 있는 모든 디렉토리)
    watch_dirs = [
        root_dir / "variables",
        root_dir / "theme",
        root_dir / "breakpoints",
        root_dir / "mixins",
        root_dir / "fonts",
        root_dir / "utilities",
    ]
    
    print("👀 SCSS 파일 감시 시작...")
    print("   감시 디렉토리:")
    for watch_dir in watch_dirs:
        if watch_dir.exists():
            print(f"   - {watch_dir.relative_to(root_dir)}")
    print("\n   Ctrl+C를 눌러 종료하세요.\n")
    
    # 이벤트 핸들러 생성
    event_handler = DocsHandler(script_path)
    
    # Observer 생성 및 시작
    observer = Observer()
    for watch_dir in watch_dirs:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 감시를 종료합니다.")
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    main()

