"""
run_app.py – SalesAssist 실행 런처
===================================
윈도우에서 이 파일을 더블클릭하거나
터미널에서 `python run_app.py`를 실행하면:
  1. FastAPI 서버를 백그라운드에서 시작합니다.
  2. 2초 후 기본 브라우저를 http://localhost:8000 으로 자동으로 엽니다.
  3. Ctrl+C 를 누르거나 창을 닫으면 서버가 종료됩니다.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

URL = "http://localhost:8000"
WAIT_SECONDS = 2


def main():
    root = Path(__file__).parent
    main_py = root / "main.py"

    print("=" * 50)
    print("  SalesAssist 시작 중...")
    print("=" * 50)
    print(f"  서버 준비 후 브라우저가 자동으로 열립니다.")
    print(f"  주소: {URL}")
    print(f"  종료하려면 이 창에서 Ctrl+C 를 누르세요.")
    print("=" * 50)

    # Start the FastAPI server as a subprocess
    proc = subprocess.Popen(
        [sys.executable, str(main_py)],
        cwd=str(root),
    )

    # Wait for the server to be ready, then open the browser
    time.sleep(WAIT_SECONDS)
    webbrowser.open(URL)

    # Keep running until the user closes the window or presses Ctrl+C
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("종료되었습니다.")


if __name__ == "__main__":
    main()
