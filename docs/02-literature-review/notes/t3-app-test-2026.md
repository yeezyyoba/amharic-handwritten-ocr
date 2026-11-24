# Test of existing apps on Amharic text (T3)

**Theme:** T3 **Tested by:** Maryamawit Lemma **Date tested:** 2026-11-23

This was a small practical check, not a formal benchmark or a citable source. It examines how four existing OCR tools handled two Amharic text samples.

## Samples

Two photographs were used:

- **Printed:** a photographed page from the FDRE Constitution (Article 4), containing the heading and one paragraph of five lines.
- **Handwritten:** the same paragraph copied by hand with a pen on ruled paper.
- Both photos were taken sideways and rotated upright before upload. Same two photos for every tool. 

Phone: SM-M156B/DS. 

The original photographs are stored locally and are not included in the repository.

Reference text: the following text was typed from the printed page and used as the reference for comparing the OCR results 

```
አንቀጽ ፬
የኢትዮጵያ ብሔራዊ መዝሙር
የኢትዮጵያ ብሔራዊ መዝሙር የሕገ መንግሥቱን ዓላማዎችና የኢትዮጵያ ሕዝቦች በዴሞክራሲ ሥርዓት አብረው ለመኖር ያላቸውን እምነት፣ እንዲሁም የወደፊት የጋራ ዕድላቸውን የሚያንጸባርቅ ሆኖ በሕግ ይወሰናል።
```

## Results

| Tool | Version | Printed | Handwritten | Works offline? |
|---|---|---|---|---|
| Ethio OCR: Scan & Translate | 1.1.5 | readable, with some recognition errors| unusable | yes |
| Google Lens |  | Readable. Text could be selected and copied.| No text could be selected | needs internet |
| Google Drive OCR (Open with Google Docs) | | Readable, extracted text matched the reference | unusable | needs internet |
| OCR.space API | Engine 3, language: auto| unusable, returned unrelated amharic text | Partly readable, the beginning matched, but the remaining text was incorrect | needs internet |

Outcome words used: readable (a few edits needed), partly readable (many edits), unusable (output unrelated to the text), no output(no text could be selected).

## Summary

Three of the four tools produced usable results from the printed Amharic page, although Ethio OCR had some recognition errors. OCR.space Engine 3 returned Amharic text, but it did not accurately match the printed sample. For handwritten text, none of the tools produced fully usable results. OCR.space partially recognized the beginning of the handwritten text, but the remaining output was incorrect.

## Limits

The test used one printed sample, one handwritten sample, one writer, and one phone. The printed sample was relatively clean. OCR.space was also tested more than once, but its results remained inaccurate. Therefore, the findings only describe the results from these specific samples. They do not establish how the tools perform with other writers, handwriting styles, documents, or image qualities.