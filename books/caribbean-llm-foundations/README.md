# Caribbean foundations of Large Language Models

Adrian Dunkley. Published by the Caribbean AI Association. First edition, November 2026.

| Edition | Download |
| --- | --- |
| English | [Caribbean foundations of Large Language Models](Caribbean-Foundations-of-Large-Language-Models-EN.pdf) |
| Español | [Fundamentos caribeños de los grandes modelos de lenguaje](Fundamentos-Caribenos-de-los-Grandes-Modelos-de-Lenguaje-ES.pdf) |

The book begins with a fictional Jamaican patty-shop decision and follows the mathematics from data and tokenisation through attention, pre-training, prompting, retrieval, alignment, inference and verification. Appendix B has a local case index. It covers the 28 UN M49 Caribbean reporting areas and adds constituent islands, mainland Caribbean and other regional contexts.

## Classroom files

Use Python 3.10 or later. The scripts use the standard library and work offline after download.

- Use **python3 checks/verify_examples.py** for site rankings, the time-bounded ferry lookup and the arithmetic on regional observations.
- Use **python3 checks/place_cases.py C01** to inspect the Anguilla practice records and the answer key. Use the case ID beside a place in Appendix B to select another case.
- Use **python3 checks/independent_examples.py** for the independent worked-value and answer-key checks.
- Consult [the source and claim register](references/claim-evidence.tsv) for the reference book, primary studies, regional data and language context.

The patty sites, transport notices, dispatch allocation and place lookup records are fictional. The language file separates authored teaching utterances from lexical sources. The regional observations file preserves the source, measure, period and units for published values. The CTO and STATIN exercises label recalculations separately from reported figures.

## Rebuild the PDFs

From this directory, use TeX Live with XeLaTeX, latexmk, Latin Modern, Babel, TikZ and PGFPlots. Regenerate the geographic table and references with **python3 checks/render_places.py** and **python3 checks/render_references.py**. Then use **latexmk -xelatex en.tex** and **latexmk -xelatex es.tex**. Figures and equations are typeset from source.

## Attribution and reuse

Book text and figures © 2026 Adrian Dunkley. The PDFs are available to read and download. The companion scripts and authored teaching fixtures use the repository licence. Third-party datasets and publications retain their own terms. The Xiao and Zhu reference is cited under its own authorship and is linked at its source.
