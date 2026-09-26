"""Download the Fidel dataset and build the writer-disjoint train/val split and vocabulary."""

import os
import random
import zipfile

import pandas as pd
from huggingface_hub import hf_hub_download

SEED = 42


def download_fidel(data_dir):
    """Download labels and images for the Fidel dataset, extracting once."""
    labels_path = hf_hub_download(
        repo_id="upanzi/fidel-dataset", filename="train_labels.csv", repo_type="dataset"
    )
    zip_path = hf_hub_download(
        repo_id="upanzi/fidel-dataset", filename="train-clean.zip", repo_type="dataset"
    )

    extract_dir = os.path.join(data_dir, "fidel_train")
    os.makedirs(extract_dir, exist_ok=True)
    marker = os.path.join(extract_dir, ".extracted")

    if not os.path.exists(marker):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)
        with open(marker, "w") as f:
            f.write("done")

    return labels_path, extract_dir


def build_dataframe(labels_path, extract_dir):
    """Load labels, keep non-empty handwritten lines, and map filenames to paths."""
    df = pd.read_csv(labels_path)
    df["writer"] = df["writer"].astype(str)
    df["image_filename"] = df["image_filename"].astype(str)
    df["line_text"] = df["line_text"].fillna("").astype(str)

    df = df[df["type"] == "handwritten"].copy()
    df = df[df["line_text"].str.strip() != ""].reset_index(drop=True)

    image_map = {}
    for root, _, files in os.walk(extract_dir):
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_map[filename] = os.path.join(root, filename)

    df["image_path"] = df["image_filename"].map(image_map)
    return df.dropna(subset=["image_path"]).reset_index(drop=True)


def writer_split(df, val_fraction=0.10, seed=SEED):
    """Split by writer, not by row, so validation writers are unseen during training."""
    writers = list(df["writer"].dropna().unique())
    random.Random(seed).shuffle(writers)

    val_count = max(1, int(len(writers) * val_fraction))
    val_writers = set(writers[:val_count])
    train_writers = set(writers[val_count:])

    train_df = df[df["writer"].isin(train_writers)].reset_index(drop=True)
    val_df = df[df["writer"].isin(val_writers)].reset_index(drop=True)
    return train_df, val_df


def build_vocab(train_df):
    """Character-level vocabulary. Index 0 is reserved for the CTC blank."""
    characters = sorted(set("".join(train_df["line_text"].tolist())))
    char_to_idx = {char: i + 1 for i, char in enumerate(characters)}
    idx_to_char = {i: char for char, i in char_to_idx.items()}
    return characters, char_to_idx, idx_to_char
