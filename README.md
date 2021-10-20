# Knowledge-Graph-Completion-with-Question-Answering-Long-Tail-Entities-from-German-DBpedia

This project contains the code for the Bachelor Thesis of the same, submitted to the University of Heidelberg on the 18th of October, 2021.

The main goal of thesis was to analyze if and how a combination of a language-model-based German Question-Answering System, long-tail entities of the German DBpedia, the DBpedia ontology and German Wikipedia article texts can perform in retrieving valid RDF triples for a selection of long-tail entities. The approach itself is divided into several stages; the repository is divided accordingly.


## 1. Data Selection 📚
The data selection phase identifies long-tail entities of the German DBpedia by analyzing metadata pages of Wikipedia in order to locate the entities without an infobox and without a language link in the German Wikipedia. The code and the results can be seen in the according files.

## 2. Data Exploration 🔍
The data exploration serves to further explore the data selected from the first step. The exploration is divided into two parts:
- DBpedia statuses for selected articles/entities
- Categories for selected articles/entities

The code can be found in the `Code` directory. The Wikipedia categories for every article can be found in `CSVFiles/DeFullCategoryMappings`, the category-wise distribution of articles can be found in `Plots/EntityCategories`. The detailed number of each category contained in *Other* can be found in `Plots/OtherCategoryDetailed`. Finally, `EndResults.txt` provides a summary of this stage.

## 3. Property Extraction 💡
The property extraction assigns each entity of the dataset its set of DBpedia properties, based on their entity class/category. The properties themselves are extracted jointly from the German and English DBpedia.
The code can be found in the `Code` directory. The final set of properties for *Person* can be found in `Properties/PersonProperties/PersonPropertiesTXTFiles`; the subject position properties are located in `PersonTotalPropertiesSP`, and accordingly, the object properties are in `PersonTotalPropertiesOP`.
All the properties in *Other* can be accessed the same way by accessing `Properties/OtherProperties` and then the respective category in *Other*.
The remaining files in these directories contain the properties with German label (i.e. every file having the suffix `Exists.txt`, denoting the existence of a German label for that property, and the properties where a translation was needed are denoted by the `Nt.txt` suffix.

## 4. Question Generation ❓
This stage of the thesis generates the input questions for the QA-system. The code for this stage can be found in the `Code` directory. The questions for each category are divided into three different parts:

- Baseline ➡️ BL
- Translation-Based ➡️ AG (for "automatically generated")
- Human-Generated ➡️ NL (for "natural language")

The are also divided into subject and object position, since the the set of properties are different according to entity position. Subject position questions can be accessed via `SP_Question Type`, where the abbreviation after the underscore indidcates the exact question type, accordingly, object position can be accessed via `OP_Question Type`. `PersonsQuestions` contains the set of questions for each position and is divided into the three question types, `OtherQuestions` contains each category in other which must be accessed first in order to access the questions for the specific category.

## Triple Extraction ⚙️
The triple extraction contains all the files 
