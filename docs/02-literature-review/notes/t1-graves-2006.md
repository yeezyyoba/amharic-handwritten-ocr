# Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks (Graves et al., 2006)

**Citation (IEEE):** A. Graves, S. Fernández, F. Gomez, and J. Schmidhuber, "Connectionist temporal classification: Labelling unsegmented sequence data with recurrent neural networks," in *Proc. 23rd Int. Conf. Machine Learning (ICML)*, Pittsburgh, PA, USA, 2006, pp. 369–376.
**Link / DOI:** (https://www.cs.toronto.edu/~graves/icml_2006.pdf)

## Problem

Recurrent networks are trained with a loss defined for every time step, so the training data has to be pre-segmented and the outputs have to be post-processed into a label sequence. Real tasks such as speech and handwriting give an input sequence and a label sequence of different lengths, with no alignment between them. HMMs and CRFs can handle this, but they need task-specific design, explicit dependency assumptions, and (for HMMs) generative training. The paper asks how an RNN can be trained directly on unsegmented sequences.

## Method

- The network has a softmax output layer with one more unit than the label set. The extra unit is a "blank" (no label). 
- The probability of a path of labels is the product of the output probabilities at each step . This assumes outputs at different times are conditionally independent given the network's internal state. 
- A many-to-one map B removes repeated labels and then blanks from a path. The paper's example is B(a-ab-) = aab. The probability of a labelling is the sum over all paths that map to it . 
- The target sequence can be at most as long as the input sequence (U ≤ T). 
- Summing over all paths is done with a forward-backward dynamic programme . Training minimises the negative log-likelihood of the target labellings  with standard backpropagation through time. 
- Decoding is approximate. **Best path** takes the most active output at every step and applies B . **Prefix search** expands label prefixes and finds the most probable labelling in principle, but grows exponentially, so the paper splits the output at frames where the blank probability is above 99.99%. 

## Data

TIMIT speech corpus, 61 phoneme labels. 4,620 training and 1,680 test utterances, with 5% (184) of the training utterances used for validation. Input is 26 coefficients per 10 ms frame (MFCCs, log-energy and first derivatives). The CTC network is a bidirectional LSTM with 100 blocks per direction, 62 outputs (61 phonemes plus blank) and 114,662 weights. 

## Evaluation

Label error rate (LER): total edit distance between the predicted and target label sequences, divided by the total number of target labels (Eq. 1). CTC and hybrid results are means over 5 runs. 

## Key results

| System | LER (%) |
|---|---|
| Context-independent HMM | 38.85 |
| Context-dependent HMM | 35.21 |
| BLSTM/HMM hybrid | 33.84 ± 0.06 |
| Weighted-error BLSTM/HMM hybrid | 31.57 ± 0.06 |
| CTC, best path | 31.47 ± 0.21 |
| CTC, prefix search | 30.51 ± 0.19 |

Source: Table 1. The paper reports all differences as significant (p < 0.01) except between the weighted-error hybrid and CTC best path. Prefix search is 0.96 points better than best path. The best hybrid result needed a weighting heuristic that CTC does not need. 

## Strengths

- Removes the need for pre-segmented data and for post-processing of network outputs.
- Needs only the label sequence, not label positions or durations.
- Multiple runs with significance tests, and a matched BLSTM architecture for the CTC and hybrid systems.

## Weaknesses

- One experiment, on speech (61 labels). There is no handwriting experiment and no test with a large label set.
- Prefix search needs a heuristic to be usable and can fail when the same label is predicted weakly on both sides of a section boundary.
- The paper states that CTC does not explicitly model dependencies between labels, and that good generalisation is difficult with maximum likelihood training, "particularly" for CTC. [Section 6]

## Relevance to our project

- Our CRNN (`ml/src/model.py`, trained with `nn.CTCLoss`) needs only a line image and its transcription. No character segmentation of Fidel lines is needed.
- The U ≤ T condition applies to our setup. The first two pooling layers halve the width twice, so a 512-pixel-wide input gives 128 frames. A label can have at most 128 characters, and fewer if it contains repeated characters, since repeats need a blank between them. The longest labels in Fidel and AHL-D 29K have to be checked against this limit.
- `ml/src/decode.py` uses greedy (best path) decoding, which is Eq. 4 in this paper. The 0.96 point gain from prefix search on TIMIT shows decoding matters little compared with the model itself, but it is a decoding option we have not tried.
- Section 6 is the basis for the correction module: CTC does not model label dependencies explicitly, so errors that depend on context (similar Fidel characters, word boundaries) are not fixed by the recogniser itself.
- Our CER follows the same idea as Eq. 1: edit distance divided by the number of reference characters.