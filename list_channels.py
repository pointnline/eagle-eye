"""
🦅 EagleEye — 구독 중인 텔레그램 채널 목록 조회
첫 실행 시 전화번호 + 인증코드 입력 필요 (이후 세션 저장됨)
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH

SESSION_PATH = "eagleeye_session"


async def list_channels():
    client = TelegramClient(SESSION_PATH, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()

    print("=" * 60)
    print("  구독 중인 텔레그램 채널 목록")
    print("=" * 60)

    channels = []
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Channel) and dialog.entity.broadcast:
            channels.append({
                "title": dialog.entity.title,
                "username": dialog.entity.username or "(비공개)",
                "id": dialog.entity.id,
                "participants": getattr(dialog.entity, 'participants_count', None),
            })

    channels.sort(key=lambda c: c["title"])

    for i, ch in enumerate(channels, 1):
        uname = f"@{ch['username']}" if ch['username'] != "(비공개)" else "(비공개)"
        members = f" | {ch['participants']}명" if ch['participants'] else ""
        print(f"  {i:3d}. {ch['title'][:40]:<40s} {uname}{members}")

    print(f"\n  총 {len(channels)}개 채널")
    print("=" * 60)

    await client.disconnect()
    return channels


if __name__ == "__main__":
    asyncio.run(list_channels())
