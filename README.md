# FII the Best at SemEval 2025 Task 2: EA-MT

## Entity-Aware Machine Translation (EA-MT)

This repository contains the implementation of our system for SemEval 2025 Task 2: **Entity-Aware Machine Translation (EA-MT)**. Our approach focuses on improving the accuracy of machine translation (MT) systems when handling named entities, including proper names, domain-specific terms, and structured references.

Our system ranked **1st among models without fine-tuning, retrieval-augmented generation (RAG), or gold information** using our second strategy and **3rd using the first strategy**.

## Features
- Multilingual **Named Entity Recognition (NER)** and structured knowledge bases for preprocessing and integration.
- **Large Language Models (LLMs)** with optimized prompts and validation mechanisms for improved entity translation.
- Handles **ten languages**: Arabic, Chinese (Traditional), French, German, Italian, Japanese, Korean, Spanish, Thai, and Turkish.
- Evaluated using **COMET and M-ETA** metrics.

## Strategies
### First Strategy
This approach relies on **multilingual Named Entity Recognition (NER)** to identify named entities before translation. The extracted entities are then mapped to **structured knowledge bases (e.g., Wikidata)** to ensure accurate translations. The modified sentences are translated using traditional machine translation models, with entity placeholders replaced after translation to maintain contextual accuracy.

### Second Strategy
This approach leverages **Large Language Models (LLMs)** with optimized **prompt engineering and validation mechanisms**. Instead of relying on structured databases, this method dynamically refines translations by instructing LLMs to preserve named entities while ensuring fluency and grammatical correctness. The system is designed to adaptively correct entity preservation errors, making it more robust for diverse language pairs.

## Results
Our system was evaluated on COMET and M-ETA scores:
| Language | First Strategy | Second Strategy |
|----------|---------------|----------------|
| Arabic (AE) | 77.54 | 76.91 |
| German (DE) | 73.56 | 77.27 |
| Spanish (ES) | 79.1 | 81.22 |
| French (FR) | 77.5 | 80.52 |
| Italian (IT) | 76.7 | 83.4 |
| Japanese (JP) | 77.26 | 78.11 |
| Korean (KR) | 75.13 | 77.14 |
| Thai (TH) | 67.15 | 75.16 |
| Turkish (TR) | 69.77 | 77.77 |
| Chinese (TW) | 40.71 | 74.19 |

---
**GitHub Repository:** [FII-the-best-SemEval2025](https://github.com/deliagrigorita/FII-the-best-SemEval2025)
