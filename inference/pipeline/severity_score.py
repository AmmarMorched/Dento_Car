def score_severity(mask_area_px: int, confidence: float) -> str:
    """
    Simple heuristic — tune thresholds after collecting real data.
    mask_area_px: number of pixels covered by the detection mask.
    """
    if mask_area_px is None:
        return "minor"
    if mask_area_px < 500:
        return "minor"
    elif mask_area_px < 5000:
        return "moderate"
    else:
        return "severe"