# Knowledge-Graph-Completion-with-Question-Answering-Long-Tail-Entities-from-German-DBpedia

This project contains the code for the Bachelor Thesis of the same, submitted to the University of Heidelberg on the 18th of October, 2021.

The main goal of thesis was to analyze if and how a combination of a language-model-based German Question-Answering System, long-tail entities of the German DBpedia, the DBpedia ontology and German Wikipedia article texts can perform in retrieving valid RDF triples for a selection of long-tail entities. The approach itself is divided into several stages; the repository is divided accordingly.


## 1. Data Selection 📚
The data selection phase identifies long-tail entities of the German DBpedia by analyzing metadata pages of Wikipedia in order to locate the entities without an infobox and without a language link in the German Wikipedia. The codecan be found in the `Code` directory. 

All XML files, including the final `FullDEdisambiguated.xml` containing the WikiXML of the final set of candidate articles, can be found in the `XMLFiles` directory.

All TXT files can be found in the `TXTFiles` directory; the file `OnlyDeArticlesFinal` contains the final 1268 article titles/entity names.

## 2. Data Exploration 🔍
The data exploration serves to further explore the data selected from the first step. The exploration is divided into two parts:
- DBpedia statuses for selected articles/entities
- Categories for selected articles/entities

The code can be found in the `Code` directory. 

The Wikipedia categories for every article can be found in `CSVFiles/DeFullCategoryMappings`, the category-wise distribution of articles can be found in `Plots/EntityCategories`. 

The detailed number of articles in each category contained in *Other* can be found in `Plots/OtherCategoryDetailed`. 

Details about entities in *Person* (i.e. gender, current status and nationalities) can be found in `Plots/PersonsCategories`; since these did not make into the final thesis, they are worth a look as they provide additional information about the entities in *Person*.

Finally, `EndResults.txt` provides a summary of this stage.

## 3. Property Extraction 💡
The property extraction assigns each entity of the dataset its set of DBpedia properties, based on their entity class/category. The properties themselves are extracted jointly from the German and English DBpedia.

The code can be found in the `Code` directory. 

The final set of properties for *Person* can be found in `Properties/PersonProperties/PersonPropertiesTXTFiles`; the subject position properties are located in `PersonTotalPropertiesSP`, and accordingly, the object properties are in `PersonTotalPropertiesOP`.

All the properties in *Other* can be accessed the same way by accessing `Properties/OtherProperties` and then the respective category in *Other*.

The remaining files in these directories contain the properties with German label (i.e. every file having the suffix `Exists.txt`, denoting the existence of a German label for that property, and the properties where a translation was needed are denoted by the `Nt.txt` suffix.

## 4. Question Generation ❓
This stage of the thesis generates the input questions for the QA-system. The code for this stage can be found in the `Code` directory. The questions for each category are divided into three different parts:

- Baseline ➡️ BL
- Translation-Based ➡️ AG (for "automatically generated")
- Human-Generated ➡️ NL (for "natural language")

The are also divided into subject and object position, since the the set of properties are different according to entity position. 

Subject position questions can be accessed via `SP_Question Type`, where the abbreviation after the underscore indidcates the exact question type, accordingly, object position can be accessed via `OP_Question Type`. 

`PersonsQuestions` contains the set of questions for each position and is divided into the three question types, `OtherQuestions` contains each category in other which must be accessed first in order to access the questions for the specific category.

## 5. Triple Extraction ⚙️
This stage of the thesis extracts the RDF triples by receiving the answers to the input questions for every property.
The class `TripleExtractor` in `Code/triple_extractor.py` contains all the functionalities necessary to execute the Question-Answering. This includes:
- loading input questions of the specific input type
- loading properties for a category
- loading all the Wikipedia article texts for each category
- creating and saving the result dictionaries

The preprocessed article texts with their entity name can be found in the `PreprocessedTXTFiles` directory.

The entire code (including the runfiles) can be found in the `Code` directory.

The result as JSON files containing a dictionary for each entity of *Person* can be found in `Results/PersonResults`. From here, the specific suffix for the question type (same as already shown in Question Generation) contains the resulting JSON files for that dictionary. These directories contain both subject and object position results already.

Accordingly, the resulting JSON files for entities in *Other* can be found in `Results/OtherResults`. From here on, the specific entity type in *Other* must be accessed, e.g. `Results/OtherResults/BuildingsResults`. The same applies here as in *Person* for the results of the specific question types.

## 6. Evaluation 📊
The final stage of the thesis is the evaluation. The evaluation evaluates the performance of the approach and the quality of the RDF triples. It is structured in several parts.

### Confidence Score Evaluation
The confidence score evaluation analyzes the confidence scores for the returned answers for each questiont tpye. This determines how confident the system is for its answers givent the category and the respective question type. The code for this part can be found in `Code/evaluate_answer_scores.py`. The results themselves can be accessed via the boxplots in `Plots/AllCategoryPlots`, which contains the boxplots for subject and object position respectively. The individual values themselves can be accessed in `CSVFiles`.

Additionally, the evaluation of the confidence scores for the properties in *Person* can be found in `PersonPropertiesStats`. These files contain the top/bottom 5 properties for *Person* in subject/object position based on questiont type.

#### Answer Quality Evaluation
This part of the evaluation analyzes the answer quality by comparing the system answers to a gold standard. The metrics used here:
- Precision
- Recall
- F1
- Exact Match

The code for the creation of the gold standard can be found in `Code/goldstandard_to_json.py`. The gold standard files themselves can be found in `GoldstandardFiles`, where they are divided into JSON and Excel files. The directories contain the according files for subject and object position separately.

The code for the evaluation of the answer quality can be found in `Code/evaluate_answers.py`.

The results for the answer quality evaluation can be found in `EvalResultsFiles`. The directory is structured s.t. the `CSVFiles` directory contains the results for metrics according to their entity position. The csv/excel files contain the respective metric score for each entity in the evaluation set based on their question type.



## Acknowledgements
I would like to extend my deepest gratitude to Prof. Dr. Maribel Acosta for her impeccable supervision of the thesis, which made all of this possible in the first place. 
Furthermore, I would like to thank Michael Staniek for helping me to run the code on the ICL clusters.

