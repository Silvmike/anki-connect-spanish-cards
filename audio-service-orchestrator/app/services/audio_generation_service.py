import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from aiohttp import ClientSession
import logging
import os

GEN_MODE_COQUI_TTS = "coqui-tts"
GEN_MODE_GTTS = "gtts"
GEN_MODE = os.getenv("GEN_MODE", GEN_MODE_COQUI_TTS)

GEN_MODE_EXTS = {
    GEN_MODE_COQUI_TTS: "wav",
    GEN_MODE_GTTS: "mp3"
}

GEN_MODE_SPEAKERS = {
    GEN_MODE_COQUI_TTS: ["Craig Gutsy", "Maja Ruoho", "Barbora MacLean"],
    GEN_MODE_GTTS: ["Google Translate Text-to-Speech"],
}

class AudioGenerationService:
    SPEAKERS = GEN_MODE_SPEAKERS[GEN_MODE]

    def __init__(self, audio_client, audio_upload_client):
        self.audio_client = audio_client
        self.audio_upload_client = audio_upload_client
        self.logger = logging.getLogger(__name__)

    async def _generate_and_upload(self, session: ClientSession, query: str, speaker: str) -> Optional[Dict]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_query = query.replace(' ', '_')[:50]  # Limit length
        sanitized_speaker = speaker.replace(' ', '_')
        file_name = f"{timestamp}_{sanitized_query}_{sanitized_speaker}.{GEN_MODE_EXTS[GEN_MODE]}"

        if audio_pair := await self.audio_client.generate_audio(session, query, speaker):
            content_type, audio_content = audio_pair
            if upload_result := await self.audio_upload_client.upload_file(session, file_name, audio_content, content_type):
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