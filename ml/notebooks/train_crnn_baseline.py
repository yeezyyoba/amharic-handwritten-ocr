# %% [markdown]
# # CRNN + CTC baseline for handwritten Amharic OCR
#
# Downloads the Fidel dataset, builds a writer-disjoint train/val split,
# trains the CRNN+CTC baseline, and saves the best checkpoint by CER.
#
# Run this as a Jupyter/Colab notebook (each `# %%` block is a cell), or as
# a plain script.

# %%
!pip install -q transformers datasets huggingface_hub evaluate jiwer pillow opencv-python

# %%
import os
import random
import sys

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_prep import build_dataframe, build_vocab, download_fidel, writer_split
from src.dataset import FidelDataset, collate_fn
from src.decode import evaluate_model
from src.model import CRNN

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", DEVICE)

# %%
WORK_DIR = "/content/amharic_htr"
DATA_DIR = f"{WORK_DIR}/data"
EXP_DIR = f"{WORK_DIR}/experiments"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXP_DIR, exist_ok=True)

BATCH_SIZE = 16
EPOCHS = 5

# %%
labels_path, extract_dir = download_fidel(DATA_DIR)
df = build_dataframe(labels_path, extract_dir)
train_df, val_df = writer_split(df)
characters, char_to_idx, idx_to_char = build_vocab(train_df)

print("Training writers:", train_df["writer"].nunique())
print("Validation writers:", val_df["writer"].nunique())
print("Training samples:", len(train_df))
print("Validation samples:", len(val_df))
print("Vocabulary size:", len(characters))

# %%
train_loader = DataLoader(
    FidelDataset(train_df, char_to_idx, augment=False),
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=collate_fn,
    num_workers=2,
    pin_memory=True,
)
val_loader = DataLoader(
    FidelDataset(val_df, char_to_idx, augment=False),
    batch_size=BATCH_SIZE,
    shuffle=False,
    collate_fn=collate_fn,
    num_workers=2,
    pin_memory=True,
)

print("Train batches:", len(train_loader))
print("Validation batches:", len(val_loader))

# %%
model = CRNN(len(characters) + 1).to(DEVICE)
criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

best_cer = float("inf")

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    for batch_idx, (images, targets, target_lengths) in enumerate(train_loader):
        images = images.to(DEVICE)
        targets = targets.to(DEVICE)
        target_lengths = target_lengths.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        input_lengths = torch.full((images.size(0),), outputs.size(0), dtype=torch.long)

        loss = criterion(outputs.log_softmax(2), targets, input_lengths, target_lengths)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 200 == 0:
            print(f"Epoch {epoch + 1}/{EPOCHS} Batch {batch_idx}/{len(train_loader)} Loss {loss.item():.4f}")

    val_cer, val_wer, refs, preds = evaluate_model(model, val_loader, idx_to_char, DEVICE)
    train_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch + 1} | Loss {train_loss:.4f} | CER {val_cer:.4f} | WER {val_wer:.4f}")

    if val_cer < best_cer:
        best_cer = val_cer
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "char_to_idx": char_to_idx,
                "idx_to_char": idx_to_char,
                "cer": val_cer,
                "wer": val_wer,
            },
            f"{EXP_DIR}/crnn_baseline.pt",
        )
        print("Saved CRNN baseline.")

print("Baseline CER:", best_cer)
