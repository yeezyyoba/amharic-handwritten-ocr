# An Unsupervised Method for OCR Post-Correction and Spelling Normalisation for Finnish (Duong et al., 2021)
**Theme:** T2
**Read by:** Leawi **Date read:** 2026-11-23
**Citation (IEEE):** Q. Duong, M. Hämäläinen, and S. Hengchen, "An unsupervised method for OCR post-correction and spelling normalisation for Finnish," in *Proc. 23rd Nordic Conf. Computational Linguistics (NoDaLiDa)*, Reykjavik, Iceland, 2021, pp. 240–248. [Online]. Available: https://aclanthology.org/2021.nodalida-main.24/
**Link / DOI:** https://aclanthology.org/2021.nodalida-main.24/ (No DOI listed in ACL Anthology)

## Problem
Historical Finnish documents digitized via OCR frequently contain recognition errors and archaic spelling conventions that differ from modern Finnish. Because Finnish is morphologically rich with numerous inflected word forms, standard word-list lookups struggle to distinguish valid inflections from OCR errors. Furthermore, manually annotating parallel OCR-to-ground-truth training data is costly. The authors aim to build an unsupervised post-OCR correction and spelling normalization pipeline that requires no manually annotated parallel training pairs.

## Method
The paper extends character-level neural OCR correction (Hämäläinen & Hengchen, 2019) through a multi-stage unsupervised pipeline:
* **Baseline Pair Extraction (NATAS):** Trains a Word2Vec model on historical OCR text, uses the Finnish morphological finite-state transducer (FST) **Omorfi** (via UralicNLP) and a Finnish Wiktionary lemma list to identify valid inflected words, and retrieves contextually similar Word2Vec neighbors within a Levenshtein distance $\le 4$ to automatically build noisy-to-clean training pairs. These pairs train a bidirectional LSTM with global attention (OpenNMT, 10,000 steps).
* **Artificial OCR-Error Generation:** To overcome noisy Word2Vec pairs and limited vocabulary coverage, the authors corrupt clean modern Finnish news text using two methods:
  1. *Random Generator:* Randomly inserts, deletes, or substitutes Finnish alphabet characters using a noise rate of $0.07 \times \text{word length}$.
  2. *Trained Error Generator:* Reverses the NATAS pairs (clean $\rightarrow$ noisy) to train a GRU sequence-to-sequence model (teacher forcing rate $0.5$, with a custom loss penalizing identical copying) to generate realistic OCR-like character errors.
* **Context-Aware Character-Level Transformer:** Trains PyTorch character-level Seq2Seq Transformers (3 encoder layers, 3 decoder layers, 8 attention heads, learned positional encodings, Adam optimizer with $\text{lr} = 0.0005$, beam search size 3) across three context windows: **W1** (target word only), **W3** (1 word left/right), and **W5** (2 words left/right). The model predicts only the corrected target word.
* **Morphological & Historical Post-Processing:** Because raw neural outputs sometimes generate non-words or modernize historical spellings, a final filter checks predictions with Omorfi (retaining the original OCR token if unrecognized) and replaces `v` with `w` to match historical Finnish orthography.

## Data
* **Unsupervised OCR Extraction Corpus:** Historical Newspaper of Finland corpus (1771–1929) for Word2Vec training and NATAS pair extraction.
* **Clean Modern Corpus (for synthetic generation):** Yle News corpus (>700,000 modern Finnish news articles, 2011–2018), stripped of punctuation and non-Finnish characters.
* **Evaluation Dataset:** Ground Truth Finnish Fraktur dataset from the National Library of Finland—479 historical newspaper and journal pages (1836–1918), totaling 471,903 aligned entries with ground truth and outputs from three OCR engines: **Tesseract** (88.29% baseline word accuracy), **FR11** (79.79%), and **OLD** (75.34%).

## Evaluation
* **Metrics:** Whole-word accuracy (chosen over character accuracy due to long Finnish words and compounds), decomposed into:
  * *Post-processed accuracy:* Overall word accuracy after correction.
  * *Error-word accuracy:* Proportion of originally erroneous OCR words successfully fixed.
  * *Correct-word accuracy:* Proportion of originally correct OCR words preserved without damage.

## Key results
Before morphological/spelling post-processing, all neural models scored *below* the original OCR baselines (e.g., `TFTrainW5` reached 71.24% on Tesseract, 69.30% on OLD, and 73.21% on FR11), largely due to modernizing historical spellings and generating invalid words.

**Final Whole-Word Accuracy (After Omorfi Validation & `v` $\rightarrow$ `w` Normalization):**

| Model | Error Generator | Window | Tesseract (Orig: 88.29%) | OLD (Orig: 75.34%) | FR11 (Orig: 79.79%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| NATAS (Baseline) | Extracted | W1 | 74.71% | 71.19% | 75.06% |
| TFRandW1 / W3 / W5 | Random | 1 / 3 / 5 | 80.49% / 80.79% / 81.89% | 75.10% / 75.40% / 76.26% | 79.66% / 80.06% / 81.09% |
| TFTrainW1 | Trained GRU | 1 | 83.05% | 78.19% | 82.39% |
| TFTrainW3 | Trained GRU | 3 | 83.96% | **79.26%** | **83.50%** |
| TFTrainW5 | Trained GRU | 5 | **84.00%** | 79.17% | 83.34% |

* **Key Takeaways:**
  * Synthetic data with character-level Transformers consistently outperformed the NATAS baseline.
  * The **trained error generator** outperformed random character corruption, and adding surrounding context (**W3/W5**) outperformed isolated-word correction (**W1**).
  * `TFTrainW3` improved both **OLD** ($75.34\% \rightarrow 79.26\%$) and **FR11** ($79.79\% \rightarrow 83.50\%$), but no model beat the already-strong **Tesseract** baseline (88.29%).
  * **Overcorrection trade-off:** On Tesseract, `TFTrainW5` fixed **18.02%** of originally incorrect words but only preserved **92.75%** of originally correct words, showing how damaging valid words lowers aggregate accuracy when baseline OCR is already high.

## Strengths
* Eliminates the need for manually annotated parallel OCR-to-ground-truth training data by combining unsupervised pair extraction with synthetic error generation.
* Demonstrates that a trained error generator mimicking real OCR mistakes outperforms random character noise, and that local word context (W3/W5) improves character-level Transformer correction.
* Explicitly handles rich morphology via an FST analyzer (Omorfi) and transparently reports the trade-off between fixing errors and preserving already-correct words.

## Weaknesses
* Still depends on substantial linguistic infrastructure: a large OCR corpus, a clean text corpus, a lemma list, and a morphological analyzer (Omorfi).
* Fails to improve upon the strongest OCR baseline (Tesseract, 88.29%) due to overcorrection of valid words and domain mismatch between modern Finnish training news and historical Fraktur ground truth.
* The morphological filter can reject valid historical or fragmented forms absent from the analyzer.
* Evaluates only historical printed Finnish text, leaving generalization to handwritten text and non-Latin scripts untested.

## Relevance to our project
* **Unsupervised / synthetic error generation for Amharic:** Because manually aligned handwritten Amharic post-OCR datasets are scarce, training a character-level error generator (or extracting confusion distributions) from our own recognizer's outputs to synthesize training data is a promising strategy—and likely more effective than purely random character corruption.
* **Context windows & character-level modeling:** Testing small context windows (e.g., W1 vs. W3 vs. W5) with a character-level Transformer is directly applicable to Amharic's rich morphology, where isolated word lists suffer from out-of-vocabulary failures.
* **Morphological validation & error preservation:** The paper's finding that neural correction can degrade an already-strong OCR engine (preserving only 92.75% of correct Tesseract words) directly informs our evaluation design: we must track both error-word correction rate and correct-word preservation rate, and investigate whether an Amharic morphological analyzer or vocabulary filter can guard against overcorrection.
* **Scope caveat:** Finnish and Amharic differ significantly in morphology and script, and equivalent morphological tooling for Amharic must be verified before assuming similar gains on modern handwritten Amharic.