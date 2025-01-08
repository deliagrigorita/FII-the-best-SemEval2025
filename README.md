# SemEval-task-2-2025

This repository implements a pipeline for Entity-Aware Machine Translation (EA-MT), as described in the task introduced [here](https://sapienzanlp.github.io/ea-mt/docs/task/introduction). Our system focuses on preserving named entities (NEs) during translation while ensuring grammatically correct outputs.



This project focuses on Entity-Aware Machine Translation (EA-MT), ensuring the accurate handling of named entities during translation while maintaining grammatical correctness.

Key steps in the process include:

* Extracting named entities using the WikiNEuRal multilingual NER model.
* Translating the entities with the Wikidata API to guarantee precision and contextual relevance.
* Replacing entities in the original sentence with placeholders to translate the remaining content independently.
* Translating the sentence without entities into the target language.
* Replacing placeholders with translated entities and refining the final output to ensure grammatical accuracy.
  
This method is particularly effective for tasks where preserving the integrity of named entities is crucial. The implementation is modular and can be customized for different languages or translation requirements.






