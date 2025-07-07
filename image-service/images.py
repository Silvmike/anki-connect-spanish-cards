from fastapi import FastAPI, HTTPException, Response, Query
from diffusers import StableDiffusionPipeline
import torch
from pydantic import BaseModel
import io
import base64
import uvicorn

app = FastAPI()

model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    safety_checker=None,
    requires_safety_checker=False
)
pipe = pipe.to("cuda")

class ImageRequest(BaseModel):
    prompt: str
    height: int = 512
    width: int = 512

@app.post("/generate")
def generate_image_json(request: ImageRequest):
    buffered = generate_image(request)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return { "image": img_str }

@app.get("/generate.png")
def generate_image_get(
    prompt: str = Query(..., description="The text prompt to generate the image"),
    height: int = Query(512, description="Height of the generated image (must be divisible by 8)"),
    width: int = Query(512, description="Width of the generated image (must be divisible by 8)")
):
    return generate_image_post(ImageRequest(prompt=prompt, height=height, width=width))

@app.post("/generate.png")
def generate_image_post(request: ImageRequest):
    buffered = generate_image(request)
    return Response(content=buffered.getvalue(), media_type="image/png")


def generate_image(request):
    if request.height % 8 != 0 or request.width % 8 != 0:
        raise HTTPException(status_code=400, detail="Height and width must be divisible by 8.")

    with torch.autocast("cuda"):
        image = pipe(
            prompt=request.prompt,
            height=request.height,
            width=request.width,
            num_inference_steps=150,
            guidance_scale=7.5
        ).images[0]
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return buffered

@app.get("/health")
def get_health():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)