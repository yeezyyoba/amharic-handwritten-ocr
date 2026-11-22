# Generative-AI use disclosure (Appendix L)

Keep this record **as you go** (Section 15.3). A completed copy is attached to
**every report** (FYP I document, FYP II report, and check whether CoSc4511
also needs one).

Rules to remember:
- AI may be used, with the advisor's knowledge, for brainstorming, language
  editing, code help, debugging and finding literature.
- Never cite a source you have not read and verified. An AI summary does not
  replace reading the source.
- Understand, review and test any AI-generated text or code. Attribute
  substantial AI-generated code in code comments.
- No confidential or personal data (for example questionnaire responses) in
  public AI services.
- AI tools may not be used to answer questions during the defense, and
  examiners can question you on any AI-assisted part.

**Project title:** Handwritten Amharic Text Recognition Mobile Application
**Group members:** Eyob Nebyou, Hallelujah Ezra, Leawi Tadesse, Maryamawit Lemma

- [ ] We did not use generative-AI tools in this project.
- [x] We used generative-AI tools as listed below.

| Tool and version | Dates | Purpose | Where used (section or module) | How the output was checked | Member |
|---|---|---|---|---|---|
| Claude (Anthropic), Claude Opus 5.5 | 2026-11-06 | Repository review against the FYP guideline; folder reorganisation; document templates and checklists; Flutter skeleton for `mobile/`; editing the team message that assigned literature review themes. Not used to find, summarise or select literature sources: the reading matrix was cleared so members start their source search from scratch | `docs/` structure, templates, README files, `mobile/` skeleton | Reviewed by the team against the guideline | Eyob |
| Claude (Anthropic), Claude Sonnet 5.5 | 2026-11-21 | Theme T4 (Amharic/Ethiopic OCR studies and datasets): suggested candidate sources and drafted their IEEE citations; explained the note format; gave feedback on Eyob's notes on Fidel, HHD-Ethiopic (dropped), AHWR-Net and GCSEN; compared the numbers in the notes against the papers' tables; rewrote some wording and converted the Fidel, AHWR-Net and GCSEN notes to Markdown. Eyob read the papers and wrote the analysis. | `docs/02-literature-review/` (`notes/t4-chamisso-2026.md`, `notes/t4-abdurahman-2021.md`, `notes/t4-tadesse-2023.md`) | Numbers compared with the papers' own tables (screenshots from the publishers' pages and the open-access PDF); citations checked against publisher or dataset pages; notes reviewed by Eyob | Eyob |
| ChatGPT (OpenAI), GPT-6 (web app) | 2026-11-07 – 2026-11-15 | Theme T2 (Post-OCR error correction): located survey DOI and candidate papers (Sources 3 and 4) and clarified technical concepts in post-OCR methods and Sources 1, 3, and 4. Leawi read the papers and wrote the notes. | `docs/02-literature-review/` (`notes/t2-nguyen-2021.md`, `notes/t2-guan-2024.md`, `notes/t2-<source-4>.md`) | Opened and read the full papers directly; removed tracking tags from DOIs and verified metadata on ACM Digital Library and ACL Anthology | Leawi |
| Gemini (Google), Gemini 4 Argon | 2026-11-09 – 2026-11-22 | Theme T2 (Post-OCR error correction): explained concepts in Sources 1 and 4, reviewed Leawi's study notes against mentor feedback, restructured notes into the FYP Markdown template, and formatted notes in the T2 literature | `docs/02-literature-review/` (`notes/t2-nguyen-2021.md`, `notes/t2-kolak-2005.md`, `notes/t2-guan-2024.md`, `notes/t2-<source-4>.md`, `reading-matrix.md`, `references.md`), `docs/compliance/ai-use-disclosure.md` | Cross-checked all summarized methods, experimental numbers, tables, and IEEE citations against the original PDFs; verified separation of paper findings from Amharic project hypotheses | Leawi |



We confirm that all AI-assisted text and code was reviewed, understood and
tested by us, that all references were verified, and that no confidential or
personal data was entered into public AI services.

Signatures: ____________________ ____________________ ____________________ ____________________

Date: ____________________
