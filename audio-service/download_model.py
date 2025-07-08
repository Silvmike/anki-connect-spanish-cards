import os
import io

import torch
from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

audio_data = io.BytesIO()
tts.tts_to_file(
    text="Hi!",
    file_path=audio_data,
    language="en",
    speaker=tts.speakers[0]
)
