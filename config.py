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
    # 리서치/분석 전문 채널
    "research": [
        "hedgehara",               # Pluto Research
        "rafikiresearch",          # Rafiki research
        "ym_research",             # YM리서치
        "HS_academy",              # HS아카데미 이효석
        "Yeouido_Lab",             # 여의도 톺아보기
        "umbrellaresearch",        # 엄브렐라 리서치
        "aetherjapanresearch",     # 에테르 일본&미국 리서치
        "fundeasy_choi",           # Fund Easy
        "EMchina",                 # 한투증권 중국/신흥국
        "pharmbiohana",            # 제약/바이오 원리버
        "hogniel",                 # 호그니엘
        "bbanjil",                 # 뺀지뤼의 SKLab
    ],
    # 매크로/경제/시황
    "macro": [
        "slsyphus",                # Macrotrader 금융치료
        "bumgore",                 # 시장 이야기 by 제이슨
        "hankyung_fin",            # 한국경제
        "TRENDSETTERVERSION2",     # TRENDSETTER GLOBAL
        "investment_puzzle",       # 투자의 빅 픽처
        "koreancapitalist",        # Korean Capitalist Magazine
        "getfeed",                 # 전문가들의 마켓 인사이트
        "jghjfdgfh",               # 세사모
        "YeouidoStory2",           # 여의도스토리 Ver2.0
    ],
    # 주식 트레이딩/종목분석
    "stocks": [
        "corevalue",               # 가치투자클럽
        "bornlupin",               # 루팡
        "easobi",                  # 서화백의 그림놀이
        "athletes_village",        # 선수촌
        "tazastock",               # 타점 읽어주는 여자
        "quantum_ALGO",            # 퀀텀 알고리즘
        "stocktrip",               # Stock Trip
        "bufkr",                   # Buff
        "yaza_stock",              # 야자반 Y.Z. stock
        "Onionfarmer",             # 양파농장
        "allbareun",               # 올바른
        "WoosanXNNN",              # 우산 X NNN의 아이디어
        "gaoshoukorea",            # 재야의 고수들
        "guroguru",                # 최선생네 반지하
        "Ten_level",               # 텐렙
        "fourgachi",               # 피폭된 뚱땡이 4가투
        "daegurr",                 # 똥밭에 굴러도 주식판
        "hermitcrab41",            # 기술적 분석으로 보는 주식시장
        "Desperatestudycafe",      # 간절한 투자스터디카페
        "bbong_tta",               # 돼지바
        "REDZONEMONEY",            # 레드존
    ],
    # 뉴스/속보/모니터링
    "news": [
        "dada_news2",              # 단독 & 속보 뉴스 콜렉터
        "GoUpstock",               # 오를주식
        "awake_realtimeCheck",     # AWAKE 52주 신고가 모니터링
        "darthacking",             # AWAKE 실시간 공시 정리
        "mbngoldkty",              # 매일경제TV 김태윤
        "mbngoldcsi",              # 매일경제TV 조선일
        "blockmedia",              # 블록미디어
        "cyber_rangers",           # 상장기업 수사대
        "knowledge_to_wealth",     # 지식 책꽂이 이대호 기자
    ],
    # 부동산
    "realestate": [
        "mootda",                  # 묻따방
        # "조르바의 기승전부동산" — 비공개 채널 (ID 필요)
    ],
    # 인사이트/라이프/기타
    "general": [
        "Brain_And_Body_Research", # Brain and Body Research
        "habit4117",               # 습관이 부자를 만든다
        "kimcharger",              # 김찰저의 관심과 생각
        "moneybottle",             # 머니보틀
        "anysong_Technon",         # 아무자료 아무노래
        "talkative_pikachu",       # 수다스러운 피카츄 아저씨
        "pikachu_aje",             # 피카츄 아저씨
    ],
}

# 비공개 채널 (username 없음, 채널 ID로 수집)
# list_channels.py로 ID 확인 후 추가 가능
PRIVATE_CHANNELS = [
    # {"id": 채널ID, "name": "돈파민 하이퍼패스", "category": "stocks"},
    # {"id": 채널ID, "name": "조르바의 기승전부동산", "category": "realestate"},
    # {"id": 채널ID, "name": "주식 급등일보", "category": "stocks"},
    # {"id": 채널ID, "name": "투자자윤의 투자일지", "category": "stocks"},
    # {"id": 채널ID, "name": "신한 리서치본부 IT", "category": "research"},
]

# === 수집 설정 ===
COLLECT_LIMIT = 100          # 채널당 최근 N개 메시지
COLLECT_DAYS = 7             # 최근 N일 메시지만 수집
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# === 분석 설정 ===
ANALYSIS_MODEL = "gemini-2.5-flash"  # 대량 분류/요약용
DEEP_MODEL = "gemini-2.5-pro"       # 심층 시나리오 분석용

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
