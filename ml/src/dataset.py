"""Dataset utilities for the Fidel handwritten Amharic OCR dataset."""

import random

import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageOps
from torch.utils.data import Dataset

IMG_HEIGHT = 64
IMG_WIDTH = 512


class FidelDataset(Dataset):
    """Loads Fidel line images and their Amharic transcriptions."""

    def __init__(self, dataframe, char_to_idx, augment=False):
        self.df = dataframe.reset_index(drop=True)
        self.char_to_idx = char_to_idx
        self.augment = augment

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image = Image.open(row["image_path"]).convert("L")

        if self.augment:
            image = self._augment(image)

        image = image.resize((IMG_WIDTH, IMG_HEIGHT))
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.tensor(image).unsqueeze(0)

        text = row["line_text"]
        target = torch.tensor(
            [self.char_to_idx[c] for c in text if c in self.char_to_idx],
            dtype=torch.long,
        )
        return image, target

    @staticmethod
    def _augment(image):
        if random.random() < 0.35:
            image = ImageEnhance.Contrast(image).enhance(random.uniform(0.7, 1.3))
        if random.random() < 0.25:
            image = ImageEnhance.Brightness(image).enhance(random.uniform(0.8, 1.2))
        if random.random() < 0.20:
            image = ImageOps.autocontrast(image)
        return image


def collate_fn(batch):
    images = torch.stack([item[0] for item in batch])
    targets = torch.cat([item[1] for item in batch])
    target_lengths = torch.tensor([len(item[1]) for item in batch], dtype=torch.long)
    return images, targets, target_lengths
