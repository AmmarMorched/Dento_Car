from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.prefilter import has_damage
from pipeline.sahi_detector import detect
from pipeline.severity_scorer import score_severity
from pipeline.annotator import annotate
import httpx, base64, numpy as np
from PIL import Image
import io

app = FastAPI(title="CarScanner Inference Service")

class InferenceRequest(BaseModel):
    image_url: str
    image_id: str

@app.post("/detect")
async def run_detection(req: InferenceRequest):
    # fetch image
    async with httpx.AsyncClient() as client:
        resp = await client.get(req.image_url)
    image = np.array(Image.open(io.BytesIO(resp.content)).convert("RGB"))

    # pre-filter
    damaged, damage_prob = has_damage(image)
    if not damaged:
        return {"detections": [], "damage_probability": damage_prob, "annotated_image_b64": None}

    # SAHI + YOLO
    detections = detect(image)

    # severity scoring
    for det in detections:
        det["severity"] = score_severity(det["mask_area_px"], det["confidence"])

    # annotate image
    annotated = annotate(image, detections)
    buffer = io.BytesIO()
    Image.fromarray(annotated).save(buffer, format="JPEG", quality=90)
    b64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "image_id": req.image_id,
        "damage_probability": damage_prob,
        "detections": detections,
        "annotated_image_b64": b64,
    }