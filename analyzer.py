"""
🦅 EagleEye v2.0 — Gemini 분석 엔진
수집된 메시지를 5개 핵심 분석 카테고리로 처리
"""

import json
import os
import sys
from datetime import datetime, timezone

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import google.generativeai as genai
from config import GEMINI_API_KEY, ANALYSIS_MODEL, DEEP_MODEL, DATA_DIR

genai.configure(api_key=GEMINI_API_KEY)


# === 분석 프롬프트 ===

PROMPTS = {
    "signal_chain": """당신은 금융 시그널 분석 전문가입니다.
아래 텔레그램 채널 메시지들을 분석하여 **시그널 체인**을 추출하세요.

시그널 체인이란: 하나의 이벤트가 연쇄적으로 다른 자산/시장에 영향을 미치는 경로
예: 미국 CPI 상승 → 금리 인상 기대 → 달러 강세 → 원화 약세 → 한국 수출주 압박

출력 형식 (JSON):
{
  "chains": [
    {
      "trigger": "촉발 이벤트",
      "path": ["이벤트1 → 이벤트2 → 이벤트3"],
      "confidence": 0.0-1.0,
      "sources": ["채널명"],
      "timestamp": "최초 감지 시간"
    }
  ],
  "summary": "전체 시그널 체인 요약 (2-3문장)"
}

메시지 데이터:
{messages}""",

    "narrative_shift": """당신은 시장 내러티브 분석 전문가입니다.
아래 텔레그램 채널 메시지들에서 **내러티브 전이**를 감지하세요.

내러티브 전이란: 시장 참여자들의 주요 관심사/테마가 바뀌는 현상
예: "인플레이션 우려" → "경기침체 우려"로 주요 화제 전환

출력 형식 (JSON):
{
  "shifts": [
    {
      "from_narrative": "이전 내러티브",
      "to_narrative": "새 내러티브",
      "evidence": ["근거 메시지 요약"],
      "strength": 0.0-1.0,
      "first_detected": "최초 감지 시간"
    }
  ],
  "dominant_narrative": "현재 지배적 내러티브",
  "emerging_narratives": ["떠오르는 내러티브들"]
}

메시지 데이터:
{messages}""",

    "correlation": """당신은 자산 상관관계 분석 전문가입니다.
아래 텔레그램 채널 메시지들에서 **자산/이벤트 간 상관관계**를 분석하세요.

출력 형식 (JSON):
{
  "correlations": [
    {
      "asset_a": "자산/이벤트 A",
      "asset_b": "자산/이벤트 B",
      "direction": "positive|negative|decoupling",
      "strength": 0.0-1.0,
      "evidence": "근거 요약"
    }
  ],
  "anomalies": ["기존 상관관계에서 벗어난 이상 징후"],
  "summary": "상관관계 전체 요약"
}

메시지 데이터:
{messages}""",

    "risk_radar": """당신은 리스크 분석 전문가입니다.
아래 텔레그램 채널 메시지들에서 **리스크 요인**을 식별하고 레이더 차트용 데이터를 생성하세요.

리스크 카테고리: 시장리스크, 신용리스크, 유동성리스크, 지정학리스크, 규제리스크, 시스템리스크

출력 형식 (JSON):
{
  "risk_scores": {
    "market": 0-10,
    "credit": 0-10,
    "liquidity": 0-10,
    "geopolitical": 0-10,
    "regulatory": 0-10,
    "systemic": 0-10
  },
  "overall_level": 1-5,
  "top_risks": [
    {
      "risk": "리스크 설명",
      "category": "카테고리",
      "severity": 0-10,
      "probability": 0.0-1.0,
      "evidence": "근거"
    }
  ],
  "risk_trend": "increasing|stable|decreasing"
}

메시지 데이터:
{messages}""",

    "scenario": """당신은 시나리오 분석 전문가입니다.
아래 텔레그램 채널 메시지들을 종합하여 **향후 시나리오**를 생성하세요.

출력 형식 (JSON):
{
  "scenarios": [
    {
      "name": "시나리오명",
      "type": "bull|base|bear|black_swan",
      "probability": 0.0-1.0,
      "description": "시나리오 설명 (3-5문장)",
      "triggers": ["촉발 조건들"],
      "implications": ["시사점/영향"],
      "timeline": "예상 기간"
    }
  ],
  "base_case": "기본 시나리오 요약",
  "key_variables": ["핵심 변수들 (이것에 따라 시나리오가 갈림)"]
}

메시지 데이터:
{messages}""",

    "smart_money": """당신은 스마트머니 추적 전문가입니다.
아래 텔레그램 채널 메시지들을 분석하여 어떤 채널이 정확한 시장 예측을 했는지 추적하세요.

출력 형식 (JSON):
{
  "channels": [
    {
      "name": "채널명",
      "category": "crypto|stocks|macro",
      "calls": [
        {"message": "메시지 요약", "date": "날짜", "asset": "자산", "direction": "long|short", "result": "win|loss|pending", "return_pct": 0.0}
      ],
      "hit_rate": 0.0,
      "total_calls": 0,
      "avg_return": 0.0
    }
  ],
  "top_performers": ["상위 채널들"],
  "summary": "스마트머니 전체 요약"
}

메시지 데이터:
{messages}""",

    "hidden_pattern": """당신은 데이터 패턴 분석 전문가입니다.
아래 텔레그램 채널 메시지들에서 명확하지 않은 **히든 패턴** 5개를 찾아내세요.

출력 형식 (JSON):
{
  "patterns": [
    {
      "id": 1,
      "title": "패턴 제목",
      "description": "패턴 설명 (3-5문장)",
      "evidence": "근거 데이터",
      "significance": 0.0,
      "category": "volume|timing|sentiment|divergence|structural"
    }
  ],
  "volume_vs_volatility": {"insight": "볼륨과 변동성 관계 인사이트"},
  "information_spread": {"insight": "채널간 정보 확산 패턴"}
}

메시지 데이터:
{messages}""",

    "action_signal": """당신은 투자 액션 시그널 전문가입니다.
아래 텔레그램 채널 메시지들을 종합하여 실행 가능한 트레이딩/모니터링 시그널을 생성하세요.

출력 형식 (JSON):
{
  "actions": [
    {
      "priority": 1,
      "action": "액션 설명",
      "asset": "관련 자산",
      "direction": "buy|sell|watch|hedge",
      "confidence": 0.0,
      "timeframe": "기간",
      "reasoning": "근거"
    }
  ],
  "monitoring_checklist": ["다음 주 핵심 모니터링 포인트들"],
  "top_3_insights": ["가장 중요한 인사이트 3줄"]
}

메시지 데이터:
{messages}""",
}


def load_messages() -> dict | None:
    """수집된 메시지 로드"""
    path = os.path.join(DATA_DIR, "raw_messages.json")
    if not os.path.exists(path):
        print("❌ 수집 데이터 없음. collector.py를 먼저 실행하세요.")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


MAX_CHARS = 180_000  # Gemini 안정적 처리 범위

def flatten_messages(data: dict) -> str:
    """전체 메시지를 분석용 텍스트로 변환 (MAX_CHARS 이내로 제한)"""
    lines = []
    for category, msgs in data.get("categories", {}).items():
        # 최신 메시지 우선, 채널당 최대 200자로 압축
        sorted_msgs = sorted(msgs, key=lambda m: m["date"], reverse=True)
        for m in sorted_msgs:
            lines.append(f"[{category}/{m['channel']}] {m['date'][:10]} | {m['text'][:200]}")

    result = "\n".join(lines)
    if len(result) > MAX_CHARS:
        result = result[:MAX_CHARS]
        print(f"  ⚠️ 텍스트 {len('\n'.join(lines)):,}자 → {MAX_CHARS:,}자로 축소")
    return result


def analyze(analysis_type: str, messages_text: str, use_deep: bool = False) -> dict:
    """단일 분석 타입 실행"""
    model_name = DEEP_MODEL if use_deep else ANALYSIS_MODEL
    model = genai.GenerativeModel(model_name)

    prompt = PROMPTS[analysis_type].replace("{messages}", messages_text)

    try:
        response = model.generate_content(prompt)
        text = response.text

        # JSON 블록 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text.strip())
    except json.JSONDecodeError:
        print(f"  ⚠️ {analysis_type}: JSON 파싱 실패, 원본 텍스트 저장")
        return {"raw_response": response.text, "parse_error": True}
    except Exception as e:
        print(f"  ❌ {analysis_type}: {e}")
        return {"error": str(e)}


def run_all_analyses() -> dict:
    """전체 분석 파이프라인 실행"""
    print("🦅 EagleEye 분석 엔진 시작...")

    data = load_messages()
    if not data:
        return {}

    messages_text = flatten_messages(data)
    print(f"   총 메시지: {data['total_messages']}개")
    print(f"   분석 텍스트: {len(messages_text):,}자")

    results = {
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "source_collected_at": data["collected_at"],
        "total_messages": data["total_messages"],
    }

    # 8개 분석 순차 실행
    for atype in PROMPTS:
        print(f"\n🔍 분석 중: {atype}...")
        # 시나리오, 액션시그널은 Deep 모델 사용
        use_deep = (atype in ("scenario", "action_signal"))
        result = analyze(atype, messages_text, use_deep=use_deep)
        results[atype] = result
        print(f"  ✅ {atype} 완료")

    # 개별 JSON 파일로 저장 (대시보드 연동용)
    for atype in PROMPTS:
        output_path = os.path.join(DATA_DIR, f"{atype}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": results["analyzed_at"],
                "data": results[atype],
            }, f, ensure_ascii=False, indent=2)

    # 라이브 피드용 메타 데이터
    meta = {
        "last_updated": results["analyzed_at"],
        "total_messages": data["total_messages"],
        "analysis_types": list(PROMPTS.keys()),
        "status": "live",
    }
    with open(os.path.join(DATA_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n🎯 전체 분석 완료 → {DATA_DIR}/")
    return results


if __name__ == "__main__":
    run_all_analyses()
