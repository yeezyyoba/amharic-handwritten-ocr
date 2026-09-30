"""Load the trained CRNN and transcribe single text-line images."""

import argparse

import numpy as np
import torch
from PIL import Image

from .dataset import IMG_HEIGHT, IMG_WIDTH
from .decode import greedy_decode
from .model import CRNN


def preprocess(image):
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    image = image.convert("L").resize((IMG_WIDTH, IMG_HEIGHT))
    array = np.array(image).astype(np.float32) / 255.0
    return torch.tensor(array).unsqueeze(0)


def load_model(weights_path, device="cpu"):
    checkpoint = torch.load(weights_path, map_location=device, weights_only=True)
    idx_to_char = {int(k): v for k, v in checkpoint["idx_to_char"].items()}
    model = CRNN(len(idx_to_char) + 1).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, idx_to_char


@torch.no_grad()
def recognize(model, idx_to_char, images, device="cpu", batch_size=16):
    texts = []
    for start in range(0, len(images), batch_size):
        batch = torch.stack([preprocess(x) for x in images[start:start + batch_size]])
        texts.extend(greedy_decode(model(batch.to(device)), idx_to_char))
    return texts


def main():
    parser = argparse.ArgumentParser(description="Transcribe handwritten Amharic line images")
    parser.add_argument("weights")
    parser.add_argument("images", nargs="+")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    model, idx_to_char = load_model(args.weights, args.device)
    for path, text in zip(args.images, recognize(model, idx_to_char, args.images, args.device)):
        print(f"{path}\t{text}")


if __name__ == "__main__":
    main()
