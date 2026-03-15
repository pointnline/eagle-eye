"""
🦅 EagleEye v2.0 — 텔레그램 채널 수집기
Telethon (MTProto) 기반으로 모든 구독 채널 메시지 수집
"""

import json
import os
import sys
import asyncio

# Windows cp949 인코딩 문제 해결
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from config import (
    TELEGRAM_API_ID, TELEGRAM_API_HASH,
    CHANNELS, COLLECT_LIMIT, COLLECT_DAYS, DATA_DIR,
)


# 세션 파일 경로
SESSION_PATH = os.path.join(os.path.dirname(__file__), "eagleeye_session")


async def collect_channel(client: TelegramClient, channel: str, days: int = COLLECT_DAYS) -> list[dict]:
    """단일 채널에서 메시지 수집"""
    messages = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    try:
        entity = await client.get_entity(channel)
        async for msg in client.iter_messages(entity, limit=COLLECT_LIMIT):
            if msg.date < cutoff:
                break
            if not msg.text:
                continue

            messages.append({
                "id": msg.id,
                "channel": channel,
                "text": msg.text,
                "date": msg.date.isoformat(),
                "views": msg.views or 0,
                "forwards": msg.forwards or 0,
            })

        print(f"  ✅ {channel}: {len(messages)}개 수집")
    except Exception as e:
        print(f"  ❌ {channel}: {e}")

    return messages


async def collect_all() -> dict:
    """모든 채널에서 메시지 수집"""
    print("🦅 EagleEye 수집 시작...")
    print(f"   수집 기간: 최근 {COLLECT_DAYS}일")

    client = TelegramClient(SESSION_PATH, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()

    all_messages = {}
    total = 0

    for category, channels in CHANNELS.items():
        if not channels:
            continue
        print(f"\n📂 [{category}] — {len(channels)}개 채널")
        category_msgs = []

        for ch in channels:
            msgs = await collect_channel(client, ch)
            category_msgs.extend(msgs)

        all_messages[category] = category_msgs
        total += len(category_msgs)

    await client.disconnect()

    # 수집 결과 저장
    result = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "total_messages": total,
        "categories": all_messages,
    }

    output_path = os.path.join(DATA_DIR, "raw_messages.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n🎯 수집 완료: 총 {total}개 메시지 → {output_path}")
    return result


def run():
    """수집기 실행"""
    asyncio.run(collect_all())


if __name__ == "__main__":
    run()
