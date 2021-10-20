# Knowledge-Graph-Completion-with-Question-Answering-Long-Tail-Entities-from-German-DBpedia

This project contains the code for the Bachelor Thesis of the same, submitted to the University of Heidelberg on the 18th of October, 2021.

The main goal of thesis was to analyze if and how a combination of a language-model-based German Question-Answering System, long-tail entities of the German DBpedia, the DBpedia ontology and German Wikipedia article texts can perform in retrieving valid RDF triples for a selection of long-tail entities. The approach itself is divided into several stages; the repository is divided accordingly.


## 1. Data Selection 📚
The data selection phase identifies long-tail entities of the German DBpedia by analyzing metadata pages of Wikipedia in order to locate the entities without an infobox and without a language link in the German Wikipedia. The code and the results can be seen in the according files.

## 2. Data Exploration 🔍
The data exploration serves to further explore the data selected from the first step. The exploration is divided into two parts:
- DBpedia statuses for selected articles/entities
- Categories for selected articles/entities

The code can be found in the `Code` directory, the results for categories can be found in `CSVFiles/DeFullCategoryMappings`, the category-wise distribution of articles can be found in `Plots/EntityCategories`.  
