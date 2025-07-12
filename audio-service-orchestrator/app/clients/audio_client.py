from aiohttp import ClientSession
from typing import Optional
import logging

class AudioClient:
    def __init__(self, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    async def generate_audio(self, session: ClientSession, query: str, speaker: str) -> Optional[bytes]:
        url = f"{self.base_url}generate"
        try:
            async with session.post(
                url,
                json={"query": query, "speaker": speaker},
                timeout=30
            ) as response:
                response.raise_for_status()
                if response.content_type == 'audio/wav':
                    return await response.read()
                self.logger.error(f"Unexpected content type: {response.content_type}")
                return None
        except Exception as e:
            self.logger.error(f"Error generating audio: {str(e)}")
            return None