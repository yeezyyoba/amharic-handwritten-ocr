# OCR Post-Processing for Low Density Languages (Kolak & Resnik, 2005)
**Theme:** T2
**Read by:** Leawi **Date read:** 2026-11-10
**Citation (IEEE):** O. Kolak and P. Resnik, "OCR post-processing for low density languages," in *Proc. Human Language Technology Conf. and Conf. Empirical Methods in Natural Language Processing (HLT/EMNLP)*, Vancouver, BC, Canada, Oct. 2005, pp. 867–874, doi: 10.3115/1220575.1220684.
**Link / DOI:** https://doi.org/10.3115/1220575.1220684

## Problem
Low-density (low-resource) languages usually lack comprehensive digital lexicons, spell-checkers, and dedicated optical character recognition (OCR) engines. While scanning printed texts is a practical way to build digital corpora for these languages, raw OCR errors degrade downstream natural language processing (NLP) tasks such as lexical resource acquisition and machine translation (MT). Traditional word-level post-OCR systems fail in these settings because they depend on large word dictionaries. The paper investigates whether a lexicon-free, character-level statistical post-processing system can substantially reduce OCR error rates across low-resource languages while treating only the OCR engine's text output as a black box.

## Method
The authors formulate post-OCR correction using a character-level noisy-channel framework implemented with Weighted Finite-State Machines (WFSMs) via the AT&T FSM Toolkit:
$$\hat{C} = \arg\max_{C} P(O \mid C) P(C)$$
* **Source Model $P(C)$:** A character-level $n$-gram language model trained on clean target-language text using the CMU-Cambridge Statistical Language Modeling Toolkit v2. Operating on characters rather than words reduces dependence on a fixed word vocabulary (or, in dictionary-digitization tasks, the source model is constrained to a finite-state lexicon).
* **Channel (Error) Model $P(O \mid C)$:** Probabilistic string edit-distance models trained via Expectation-Maximization (EM) on aligned pairs of noisy OCR output $O$ and ground-truth character sequences $C$. The authors evaluate two variants: a Single-Character (SC) model permitting $1\text{-to-}1$, $1\text{-to-}0$, and $0\text{-to-}1$ character edits, and a Multi-Character (MC) model (adapted from Brill & Moore, 2000, trained with 1 EM iteration) allowing many-to-many character transformations.
* **Word-Boundary & Chunking Mechanism:** Rather than using a separate word segmenter, the channel model treats spaces as regular characters, modeling word splits as space insertions and word merges as space deletions. To keep the WFSM search space tractable across full lines, lines are divided into smaller chunks by using the character source model to identify high-probability space boundaries, and capping maximum edit operations per token.
* **Decoding:** The observed OCR string automaton is composed with the inverted error transducer and the language model automaton to produce a candidate lattice, from which a shortest-path algorithm extracts $\hat{C}$.

## Data
The system is evaluated across four printed-text experiments spanning four languages:
* **Experiment 1 (Igbo — Latin script, low-resource):** Two printed texts splits into $2/3$ training and $1/3$ testing: *Juo Obinna* (*Juo*, a novel, 6,727 words scanned from clean 600 dpi laser prints at 300 dpi) and *Akuko Ife Nke Ndi Igbo* (*Akuko*, short stories, 3,544 words scanned from degraded 300 dpi book photocopies). Processed with ABBYY FineReader 7.0 in both off-the-shelf English mode and user-trained character-shape mode.
* **Experiment 2 (Cebuano — Austronesian language, dictionary acquisition):** Scanned and OCR'd headwords from a printed Cebuano dictionary (isolated words lacking sentence context), tested with training set sizes of 500, 1,000, and 27,363 entries.
* **Experiment 3 (Arabic — cursive script, boundary errors):** The Arabic side of a parallel Bible corpus processed with a commercial native Arabic OCR engine (Sakhr), exhibiting frequent word merge and split errors.
* **Experiment 4 (Arabic & Spanish — downstream MT):** Parallel Arabic-English (Bible sections: 9 sections for MT training, remainder for testing) and Spanish-English corpora processed into three conditions: Clean reference text, Raw OCR output, and Post-corrected OCR text.

## Evaluation
* **Intrinsic Metrics:** Word Error Rate ($\text{WER} = \frac{S + D + I}{N}$, where $S, D, I$ are word substitutions, deletions, and insertions, and $N$ is reference word count) and Relative Error Reduction ($\frac{\text{WER}_{\text{orig}} - \text{WER}_{\text{corr}}}{\text{WER}_{\text{orig}}} \times 100$). The authors select WER over Character Error Rate (CER) because downstream NLP pipelines operate primarily on word tokens.
* **Extrinsic Metric:** BLEU score on downstream English translations produced by a statistical phrase-based MT system (*ReWrite*, trained with GIZA++ and CMU-Cambridge toolkit) and a commercial rule-based MT system (*Systran*).
* **Data Splits:** Standard $2/3$ train / $1/3$ test splits for Igbo; scaled training subsets ($500$, $1\text{k}$, $27.3\text{k}$) for Cebuano; held-out test sections for Arabic and Spanish Bible/parallel texts.

## Key results
**1. Igbo (Low-Resource & Cross-Language OCR):**

| OCR Configuration | Original WER | Corrected WER | Relative Error Reduction |
| :--- | :---: | :---: | :---: |
| English OCR on *Juo* (clean scan) | 35.44% | 7.11% | 78.80% |
| English OCR on *Akuko* (photocopy) | 33.64% | 16.40% | 51.25% |
| Trainable OCR on *Juo* | 7.43% | 3.69% | 50.34% |

* Post-processing English OCR on *Juo* (7.11% WER) slightly outperformed manually training the commercial OCR engine on Igbo character shapes without post-processing (7.43% WER), and combining both achieved the lowest WER (3.69%).
* The Single-Character (SC) error model outperformed the Multi-Character (MC) model on Igbo because MC requires larger training sets to reliably estimate multi-character parameters. In-domain training nearly doubled relative error reduction compared to cross-domain training between *Juo* and *Akuko*.

**2. Cebuano (Zero-Context Dictionary Headwords):**
* From an uncorrected baseline WER of **8.02%**, even 500 training entries with a 3-gram LM and SC model reduced WER to **5.37%** (33.04% reduction). Scaling to 27,363 entries with a 6-gram LM and MC model reduced WER to **3.97%** (50.50% relative reduction).

**3. Arabic (Word Merge/Split Recovery):**
* Starting from a Sakhr OCR baseline WER of **24.69%**, enabling merge/split (space insertion/deletion) modeling with a 3-gram character LM and error limit of 4 reduced WER to **17.74%** (a **28.15%** relative reduction, compared to **22.14%** WER / 10.33% reduction without merge/split modeling at a 3-gram limit of 2).

**4. Downstream Machine Translation (BLEU):**
* **Arabic-to-English (*ReWrite* SMT):** BLEU improved from **0.0116** (Raw OCR) to **0.0141** (Post-corrected), approaching the **0.0154** clean-text upper bound.
* **Spanish-to-English:** On *Systran*, BLEU rose from **0.2000** (Raw OCR) to **0.2606** (Corrected) vs. **0.3188** (Clean). On *ReWrite*, BLEU rose from **0.1792** (Raw OCR) to **0.2234** (Corrected) vs. **0.2590** (Clean).

## Strengths
* **Minimal resource assumptions:** Operates without requiring a full-coverage word lexicon in running text, making it practical for morphologically rich or low-resource languages with only 4–8 pages (~2,000–4,500 words) of paired training data.
* **Unified boundary correction:** Handles word splits and merges directly within the character noisy-channel transducer by treating spaces as editable characters, avoiding a separate word-segmentation module.
* **Both intrinsic and extrinsic validation:** Demonstrates not only substantial WER reductions across multiple scripts and degradation levels, but also concrete BLEU improvements in downstream machine translation.

## Weaknesses
* **Script recognition prerequisite:** Repurposing an English OCR engine worked for Igbo only because Igbo and English share the Latin script; the post-processor cannot recover text if the base OCR engine cannot read the underlying writing system.
* **Domain and scan sensitivity:** Cross-domain evaluation between clean laser prints (*Juo*) and degraded photocopies (*Akuko*) reduced relative error reduction by 15%–30%.
* **Search space and evaluation constraints:** WFSM composition requires strict pruning and per-token error limits to remain computationally tractable, and the authors report only WER (omitting CER and false-positive overcorrection rates).
* **Printed text only:** Evaluates printed documents rather than handwritten text, where character shape variation and baseline irregularity are higher.

## Relevance to our project
* **Character-level modeling for Amharic morphology:** Because Amharic is morphologically rich, a fixed word dictionary will leave many valid inflected forms out-of-vocabulary[cite: 2, 12]. Kolak and Resnik's character-level language model $P(C)$ paired with a learned character error model $P(O \mid C)$ provides a strong foundation for correcting Amharic text without relying on an exhaustive lexicon[cite: 12].
* **Need for a native Ethiopic base recognizer:** Unlike the Igbo experiment—which exploited shared Latin script shapes with an English OCR engine—Amharic uses the Ethiopic (Fidel) abugida script[cite: 2, 12]. Thus, our post-processor must be paired with a recognition model (from T1/T4) explicitly trained on Fidel glyphs, alongside aligned OCR-to-ground-truth pairs to learn actual Fidel visual confusion probabilities[cite: 1, 2, 12].
* **Handling word-boundary errors in handwriting:** Handwritten Amharic lines often exhibit uneven inter-word spacing[cite: 12]. Modeling space insertions and deletions directly inside a character-level error model is a promising hypothesis to test if our recognizer produces frequent word merge or split errors[cite: 12].
* **Metric selection for our FYP:** While Kolak and Resnik evaluate only WER, our handwritten Amharic OCR system should report both **CER** (to measure Fidel character recognition accuracy) and **WER** (to capture whole-word and spacing accuracy)[cite: 4, 12].