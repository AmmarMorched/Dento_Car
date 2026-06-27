from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from sahi.utils.cv import read_image_as_pil
from PIL import Image
import numpy as np

MODEL_PATH = "models/yolov8x-seg-carscanner.pt"

detection_model = AutoDetectionModel.from_pretrained(
    model_type="yolov8",
    model_path=MODEL_PATH,
    confidence_threshold=0.25,
    device="cuda",
)

def detect(image: np.ndarray) -> list[dict]:
    pil_image = Image.fromarray(image)

    result = get_sliced_prediction(
        pil_image,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2,
    )

    detections = []
    for obj in result.object_prediction_list:
        detections.append({
            "type":       obj.category.name,
            "confidence": round(obj.score.value, 4),
            "bbox":       obj.bbox.to_xyxy(),
            "mask_polygon": obj.mask.segmentation if obj.mask else None,
            "mask_area_px": int(obj.mask.bool_mask.sum()) if obj.mask else None,
        })

    return detections