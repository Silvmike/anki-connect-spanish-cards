import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from aiohttp import ClientSession
import logging


class AudioGenerationService:
    SPEAKERS = ["Craig Gutsy", "Maja Ruoho", "Barbora MacLean"]

    def __init__(self, audio_client, audio_upload_client):
        self.audio_client = audio_client
        self.audio_upload_client = audio_upload_client
        self.logger = logging.getLogger(__name__)

    async def _generate_and_upload(self, session: ClientSession, query: str, speaker: str) -> Optional[Dict]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_query = query.replace(' ', '_')[:50]  # Limit length
        sanitized_speaker = speaker.replace(' ', '_')
        file_name = f"{timestamp}_{sanitized_query}_{sanitized_speaker}.wav"

        if audio_content := await self.audio_client.generate_audio(session, query, speaker):
            if upload_result := await self.audio_upload_client.upload_file(session, file_name, audio_content):
                return {
                    "url": f"{upload_result['url']}",
                    "speaker": speaker
                }

        self.logger.warning(f"Failed to process audio for speaker: {speaker}")
        return None

    async def generate_audio_files(self, query: str) -> List[Dict]:
        async with ClientSession() as session:
            tasks = [self._generate_and_upload(session, query, speaker) for speaker in self.SPEAKERS]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            successful_results = []
            for result in results:
                if isinstance(result, Exception):
                    self.logger.error(f"Error processing task: {str(result)}")
                elif result is not None:
                    successful_results.append(result)

            return successful_results