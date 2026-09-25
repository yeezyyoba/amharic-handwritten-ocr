"""Greedy CTC decoding and CER/WER evaluation."""

import torch
from jiwer import cer, wer

BLANK_IDX = 0


def greedy_decode(outputs, idx_to_char):
    predictions = outputs.argmax(dim=2)
    results = []

    for sequence in predictions.permute(1, 0):
        text = []
        previous = BLANK_IDX
        for index in sequence.tolist():
            if index != BLANK_IDX and index != previous:
                text.append(idx_to_char.get(index, ""))
            previous = index
        results.append("".join(text))

    return results


def decode_targets(targets, target_lengths, idx_to_char):
    results = []
    offset = 0
    for length in target_lengths.tolist():
        target = targets[offset:offset + length]
        text = "".join(idx_to_char.get(value.item(), "") for value in target)
        results.append(text)
        offset += length
    return results


def evaluate_model(model, loader, idx_to_char, device):
    model.eval()
    predictions, references = [], []

    with torch.no_grad():
        for images, targets, target_lengths in loader:
            images = images.to(device)
            outputs = model(images)
            predictions.extend(greedy_decode(outputs, idx_to_char))
            references.extend(decode_targets(targets, target_lengths, idx_to_char))

    return (
        cer(references, predictions),
        wer(references, predictions),
        references,
        predictions,
    )
