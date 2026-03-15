"""
🦅 EagleEye v2.0 — 메인 실행 스크립트
수집 → 분석 → 대시보드 데이터 생성 파이프라인
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="🦅 EagleEye v2.0 — 텔레그램 인사이트 엔진"
    )
    parser.add_argument(
        "command",
        choices=["collect", "analyze", "pipeline", "serve"],
        help="실행 명령: collect(수집), analyze(분석), pipeline(수집+분석), serve(대시보드 로컬 서버)",
    )
    parser.add_argument(
        "--days", type=int, default=7,
        help="수집 기간 (기본: 7일)",
    )
    parser.add_argument(
        "--port", type=int, default=8080,
        help="로컬 서버 포트 (기본: 8080)",
    )

    args = parser.parse_args()

    if args.command == "collect":
        from collector import run
        run()

    elif args.command == "analyze":
        from analyzer import run_all_analyses
        run_all_analyses()

    elif args.command == "pipeline":
        print("=" * 50)
        print("🦅 EagleEye 전체 파이프라인 실행")
        print("=" * 50)

        print("\n📡 Step 1: 텔레그램 메시지 수집")
        from collector import run
        run()

        print("\n🧠 Step 2: Gemini 분석 엔진")
        from analyzer import run_all_analyses
        run_all_analyses()

        print("\n" + "=" * 50)
        print("✅ 파이프라인 완료! 대시보드를 열어보세요:")
        print("   python run.py serve")
        print("=" * 50)

    elif args.command == "serve":
        import http.server
        import functools
        import os

        dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=dashboard_dir,
        )
        server = http.server.HTTPServer(("localhost", args.port), handler)
        print(f"🦅 EagleEye 대시보드: http://localhost:{args.port}")
        print("   종료: Ctrl+C")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 서버 종료")
            server.shutdown()


if __name__ == "__main__":
    main()
