from aiohttp import ClientSession, FormData
from typing import Optional, Dict
import logging
import traceback

class AudioUploadClient:
    def __init__(self, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    async def upload_file(self, session: ClientSession, file_name: str, file_content: bytes) -> Optional[Dict]:
        url = f"{self.base_url}upload"
        try:
            data = FormData()
            data.add_field(
                'file',
                file_content,
                filename=file_name,
                content_type='audio/wav'
            )

            async with session.post(
                url,
                data=data,
                timeout=60
            ) as response:

                response.raise_for_status()

                return await response.json()
        except Exception as e:
            stack_trace_string = traceback.format_exc()
            self.logger.error(f"Error uploading file: {str(e)} {stack_trace_string}")
            return None