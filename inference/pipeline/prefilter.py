import torch
from torchvision import transforms, models
from PIL import Image
import numpy as np

# EfficientNetV2-S fine-tuned binary classifier: damage / clean
WEIGHTS_PATH = "models/efficientnet_prefilter.pt"

model = models.efficientnet_v2_s()
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 2)
model.load_state_dict(torch.load(WEIGHTS_PATH, map_location="cuda"))
model.eval().cuda()

transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

def has_damage(image: np.ndarray) -> tuple[bool, float]:
    pil = Image.fromarray(image)
    tensor = transform(pil).unsqueeze(0).cuda()
    with torch.no_grad():
        logits = model(tensor)
        probs  = torch.softmax(logits, dim=1)
        damage_prob = probs[0][1].item()
    return damage_prob > 0.4, round(damage_prob, 4)