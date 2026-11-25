# Digitizing Nepal's Written Heritage: A Comprehensive HTR Pipeline for Old Nepali Manuscripts (Sarawgi et al., 2026)

**Citation (IEEE):** A. Sarawgi, E. Garces Arias, and C. Zotter, "Digitizing Nepal's written heritage: A comprehensive HTR pipeline for Old Nepali manuscripts," in *Proc. 64th Annu. Meeting Assoc. Computational Linguistics (Vol. 1: Long Papers)*, Jul. 2026, pp. 14720–14746.
**Link / DOI:** code at https://arxiv.org/abs/2512.17111

## Problem

Old Nepali manuscripts (Devanagari script, 18th and 19th centuries) are degraded, written in varied hands, contain many conjunct characters, have no consistent word boundaries (scriptio continua) and have very little transcribed data. Pre-trained recognisers such as TrOCR are trained on Latin script. The paper asks which interventions (architecture, tokenizer, normalisation, augmentation, staged pre-training, decoding) actually improve recognition for a low-resource non-Latin historical script.

## Method

- Line-level recognition: 155 manuscript images are segmented with Kraken into 3,100 lines. 
- A trocr-base-handwritten ViT encoder (384 × 384 input) with a BERT-style decoder (114.8M parameters) trained from scratch, with a byte-level BPE tokenizer of vocabulary size 500. A GPT-2 decoder, a character BPE tokenizer and a Swin encoder were also compared. 
- Three-stage training: synthetic Devanagari lines, then printed Devanagari lines, then the handwritten manuscripts. 
- Data-centric steps: label normalisation, 20 image augmentations (shape, noise and blur, letter-level damage), no binarisation. 
- Training: AdamW, learning rate 3e-5, batch size 8, seed 42, 6 / 10 / 20 epochs for the three stages. 
- Five decoding strategies compared (beam, contrastive search, temperature, top-k, top-p). 

## Data

| Stage | Data | Train / validation / test |
|---|---|---|
| 1 | Synthetic Devanagari lines (11 fonts, 10 noise types) | 100,000 / 2,500 / 2,500 |
| 2 | Printed Devanagari (heiDATA, 247 scans) | 4,111 / 514 / 514 |
| 3 | Handwritten Old Nepali | 2,480 / 310 / 310 |

Source: Table 1. The handwritten lines average 60 characters (longest 162) and use 80 distinct characters. The test data is confidential. [Tables 10, 11]

## Evaluation

CER (Eq. 1), weighted CER (Eq. 2, weighted by label length) and exact-match accuracy on the handwritten test set. Zero-width Unicode characters (U+200B, U+200C, U+200D) are removed from predictions and labels before scoring. [Section 4.3]

## Key results

| Step | CER | Training samples |
|---|---|---|
| Fine-tuned TrOCR baseline | 0.096 | 2,480 |
| + script-aware decoder | 0.089 | 2,480 |
| + label normalisation | 0.084 | 2,480 |
| + 8x augmentation | 0.056 | 22,320 |
| + larger encoder (TrOCR-large) | 0.049 | 22,320 |

Sources: Figure 16, Table 3. "8x" means the 2,480 original lines plus 8 augmented copies (22,320 = 2,480 × 9). The gain from augmentation stops at 8x (0.056 at 12x and 16x). [Table 3]

- Decoder and tokenizer choice barely matter (CER 0.082 to 0.087 across four combinations). [Table 7]
- Binarisation hurts (0.098 against 0.089). [Table 6]
- Swin encoder 0.174 against 0.056 for the TrOCR encoder. [Table 8]
- All beam sizes and sampling settings give a weighted CER between 0.0483 and 0.0490. [Table 17]
- The final CER on the handwritten test set after each stage: 0.71 (stage 1 model), 0.51 (after stage 2), 0.056 (after stage 3). [Table 18]
- 10 of the 80 characters cause 55.9% of the 859 character errors. The largest are the virama (12.92%) and the space (11.41%). Two visually similar pairs are named: ya/pa and ta/na. [Table 19, Section 5.5]
- Lines longer than 120 characters have a much higher error rate. Only 26 of the 3,100 lines are that long. [Figure 13, Section 5.5]

## Strengths

- A systematic, data-focused study that separates the effect of each step on a low-resource non-Latin script.
- Training code, configurations and evaluation scripts are released, and the paper includes error analysis and a model-confidence analysis for post-correction.
- Three-stage transfer from synthetic and printed data to handwriting is clearly described.

## Weaknesses

- The test set is confidential (310 lines), one seed is used, and no confidence intervals are given, so small differences cannot be judged.
- The Figure 17 caption describes lines from the same paragraph being split 80/10/10 across training, validation and test. The paper does not state that the split is by manuscript or writer.
- No CRNN+CTC baseline. The statement that Transformers beat CNN-RNN models is taken from Garces Arias et al. (2023). The comparison with Google Cloud Vision is one example line, with no CER.
- Table 18 shows the model after each stage but no run without stages 1 and 2, so the benefit of the earlier stages is not isolated.
- Some figures disagree between tables (for example the same configuration is 0.082 in Table 7 and 0.084 in Table 3, and Table 19 gives 25 errors and a 2.79% share for one character where 25/859 is 2.91%).
- Every line is resized to 384 × 384, although the average line image is 1593 × 133 pixels.

## Relevance to our project

- Fidel has the same three kinds of data as the three stages: synthetic (297,810 lines), typed (28,342) and handwritten (40,855). Staged training from synthetic and typed text to handwriting is an option for both of our models.

- Label normalisation is directly relevant: our results README notes double spaces in the ground truth, and the datasheet still has to decide how homophone characters and punctuation are handled. The paper normalised extra spaces, bullets and other symbols before training.
- The error analysis (spaces and diacritic-like marks as the biggest sources) is a model for our error analysis and for deciding what the correction module should target. It needs to be repeated on Fidel predictions.
- Our 512-pixel fixed width has the same issue as the 384 × 384 resize, and long Fidel lines should be checked for a rise in error.
- It is the only low-resource non-Latin source in this theme, but it has no CTC model, so it supports the TrOCR side of our comparison and not the CRNN side.