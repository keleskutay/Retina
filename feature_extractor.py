import torch
from torch.nn.functional import normalize
from PIL import Image
import timm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from torchvision import transforms
import io

class FeatureExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the pre-trained model
        self.model = torch.hub.load("facebookresearch/dinov2","dinov2_vitb14").to(self.device)

        self.model.eval()

        self.transform = transforms.Compose([
                    transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=(0.485, 0.456, 0.406),
                         std=(0.229, 0.224, 0.225)),
                ])

    def __call__(self, image):
        # Preprocess the input image
        if isinstance(image, (bytes, bytearray)):
            stream = io.BytesIO(image)
            input_image = Image.open(stream).convert("RGB")  # Convert to RGB if needed
        else:
            input_image = Image.open(image).convert("RGB")
        
        input_image = self.transform(input_image)

        # Convert the image to a PyTorch tensor and add a batch dimension
        input_tensor = input_image.unsqueeze(0).to(self.device)

        # Perform inference
        with torch.no_grad():
            output = self.model(input_tensor)

        # Extract the feature vector
        feature_vector = output.squeeze()

        #return feature_vector
        return normalize(input=feature_vector.reshape(1, -1), p=2.0, dim=1).flatten().cpu().numpy()

