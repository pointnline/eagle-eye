"""
🦅 EagleEye v2.0 — 설정 파일
텔레그램 채널 목록 및 분석 설정
"""

import os
from dotenv import load_dotenv

load_dotenv()

# === API Keys ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_api_id = os.getenv("TELEGRAM_API_ID", "0")
TELEGRAM_API_ID = int(_api_id) if _api_id.isdigit() else 0
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")

# === 모니터링 채널 목록 ===
# 채널 username 또는 ID (@ 없이)
# 카테고리별로 정리
CHANNELS = {
    "crypto": [
        # 예시 — 실제 채널로 교체
        # "channel_username_1",
        # "channel_username_2",
    ],
    "macro": [
        # 매크로/금리/환율 채널
    ],
    "realestate": [
        # 부동산 관련 채널
    ],
    "stocks": [
        # 주식/증권 채널
    ],
    "general": [
        # 기타 시황/뉴스 채널
    ],
}

# === 수집 설정 ===
COLLECT_LIMIT = 100          # 채널당 최근 N개 메시지
COLLECT_DAYS = 7             # 최근 N일 메시지만 수집
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# === 분석 설정 ===
ANALYSIS_MODEL = "gemini-2.0-flash"  # 대량 분류/요약용 (무료)
DEEP_MODEL = "gemini-2.0-pro"       # 심층 시나리오 분석용

# === 분석 프롬프트 카테고리 ===
ANALYSIS_TYPES = [
    "signal_chain",      # 시그널 체인
    "narrative_shift",   # 내러티브 전이
    "correlation",       # 상관관계
    "risk_radar",        # 리스크 레이더
    "scenario",          # 시나리오
]

# === 대시보드 설정 ===
DASHBOARD_TITLE = "EagleEye v2.0"
REFRESH_INTERVAL_SEC = 300   # 프론트엔드 데이터 갱신 주기 (5분)
