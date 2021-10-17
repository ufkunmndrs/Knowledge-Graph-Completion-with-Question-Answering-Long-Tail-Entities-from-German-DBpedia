# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file retrieves and saves the information about the categories of candidate articles/entities.

This file contains the following functions:
    * get_category: gets categories for a given article, uses greedy matching in order to find ALL categories
    in an article
    * title_category_mapping: maps Wikipedia titles to their corresponding categories that are
    contained within their XML file
    * save_category_mapping: saves title category mapping to .csv or .xlsx file
    * person_or_other: checks in a list of tuples (where first element of tuple is Wikipedia article title,
    and second element is its list of categories) whether the entity is a person or of any other
    category other than person.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from DataSelection.Code.wiki_title_extractor import WikiTitleExtractor


def get_category(article):
    """
    gets categories for a given article, uses greedy matching in order to find ALL categories in an article

    Parameters
    ----------
    article: str
        XML element of Wikipedia article XML as string

    Returns
    -------
    category:

    """
    pattern = "\[Kategorie:(.*)\]\]"
    category = re.findall(pattern, article, flags=re.IGNORECASE)
    return category


def title_category_mapping(articles: list, titles: list, dictionary=True):
    """
    maps Wikipedia titles to their corresponding categories that are contained within their XML file

    Parameters
    ----------
    articles: list
        List of Wikipedia articles as strings, in this case and in this file, only "de_wiki_articles" will be used
    titles: list
        list of Wikipedia titles, where the elements are strings (i.e. the respective Wikipedia title of an article)
    dictionary: True/False
        determines whether a dictionary will be created. Keys are Wikipedia titles, Values are their corresponding
        German Wikipedia categories. If set to false, a list of tuples where first element of the tuple is Wikipedia
        title as string, and 2nd element ist list of categories will be created.

    Returns
    -------
    data_dict: dict
     Dictionary containing all Wikipedia titles (str) as keys, values are their categories in lists
    if dictionary is False:
    data_tuple_list: list
        List of tuples where first element of a tuple is Wikipedia title as String, 2nd element of Tuple is the list
        of categories for the Wikipedia entity

    """
    data_dict = {}
    for string in titles:
        for elem in articles:
            if string in elem:
                data_dict[string] = get_category(elem)
    if dictionary is not True:
        data_tuple_list = [(title, categories) for title, categories in data_dict.items()]
        return data_tuple_list
    else:
        return data_dict


def save_category_mapping(mapping_dict: dict, filename: str, exists=False, all_articles=True, file_format="csv"):
    """
    saves title category mapping to .csv or .xlsx file

    Parameters
    ----------
    mapping_dict: dict
        Dictionary where keys are Wikipedia titles (str) and values are lists of their respective categories
    filename: str
        string for desired json_filename
    file_format: str
        desired fileformat for saving. The default is csv. Can be changed to .xlsx fileformat.
    all_articles: True/False
        Determines whether all articles (i.e neither "persons" nor "other" in particular) will be analyzed.
        File will be stored accordingly.
        The default is True -> will be stored in the corresponding path
    exists: True/False
        Determines whether the articles that exist or don'text exist in German DBpedia will be saved;
        path changes according to the input here.
        The default is True, meaning that per default, only the articles that exist will be saved.

    Returns
    -------

    """
    path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles"
    if exists is True and all_articles is not True:
        path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/DBpediaEntryExists"
    if exists is not True and all_articles is not True:
        path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/NoDBpediaEntry"
    mapping_list = list(mapping_dict.items())
    mapping_df = pd.DataFrame(mapping_list)
    mapping_df.columns = ["Title", "Categories"]
    if file_format == "excel":
        mapping_df.to_excel(os.path.join(path, filename), encoding='utf-8', index=False)
    elif file_format == "csv":
        mapping_df.to_csv(os.path.join(path, filename), sep=",", encoding='utf-8-sig', index=False)
    else:
        raise ValueError("Invalid Dataformat, must either be .xlsx or .csv file")


def person_or_other(title_category: list, persons_only=True):
    """
    checks in a list of tuples (where first element of tuple is Wikipedia article title, and second element is its list
    of categories) whether the entity is a person or of any other category other than person.

    Parameters
    ----------
    title_category: list
        List if tuples where
    persons_only

    Returns
    -------

    """
    person_words = ["Geboren in ", "Mann", "Frau", "Person", "Gestorben in "]
    persons = []
    other = []
    for title in title_category:
        if any(string in title[1] for string in person_words):
            persons.append(title)
        else:
            other.append(title)
    if persons_only is not True:
        return other
    else:
        return persons


# create WikiTitleExtractor object to handle XML file
de_wiki_handler = WikiTitleExtractor("OnlyDeArticlesFinal.xml")
de_wiki_xml = de_wiki_handler.preprocess()
de_wiki_articles = de_wiki_handler.get_articles(de_wiki_xml)
de_wiki_titles = de_wiki_handler.get_titles(de_wiki_articles)

# get mappings for all articles, save them as .csv and .xlsx file respectively
de_full_dict = title_category_mapping(de_wiki_articles, de_wiki_titles)
de_full_tuple_list = title_category_mapping(de_wiki_articles, de_wiki_titles, dictionary=False)
save_category_mapping(de_full_dict, "DeFullCategoryMappings.csv")
save_category_mapping(de_full_dict, "DeFullCategoryMappings.xlsx", file_format="excel")

# get Articles which don'text have a German DBpedia entry, save their categories into data file
no_entry_df = pd.read_csv("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/NoDBpediaEntry/DBpedia_de_no_entry"
                          ".csv")
no_entry_titles = no_entry_df["Title"].tolist()
no_entry_cat_dict = title_category_mapping(de_wiki_articles, no_entry_titles)
no_entry_cat_list = title_category_mapping(de_wiki_articles, no_entry_titles, dictionary=False)
save_category_mapping(no_entry_cat_dict, "NoDBpediaEntryCategories.csv", all_articles=False, exists=False)
save_category_mapping(no_entry_cat_dict, "NoDBpediaEntryCategories.xlsx", all_articles=False, exists=False,
                      file_format="excel")

# get Articles which have a German DBpedia entry, save their categories into data file
DBpedia_entry_df = pd.read_csv("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/DBpediaEntryExists"
                               "/DBpedia_de_exists.csv")
DBpedia_entry_titles = DBpedia_entry_df["Title"].tolist()
DBpedia_entry_dict = title_category_mapping(de_wiki_articles, DBpedia_entry_titles)
DBpedia_entry_list = title_category_mapping(de_wiki_articles, DBpedia_entry_titles, dictionary=False)
# # noinspection PyTypeChecker
save_category_mapping(DBpedia_entry_dict, "DBpediaDEentryCategories.csv", exists=True, all_articles=False)
save_category_mapping(DBpedia_entry_dict, "DBpediaDEentryCategories.xlsx", exists=True, all_articles=False,
                      file_format="excel")

# get persons for all articles, save them to .csv and other file formats for further analysis
persons = person_or_other(de_full_tuple_list)
persons_dict = dict(persons)
save_category_mapping(persons_dict, "Persons.csv")
save_category_mapping(persons_dict, "Persons.xlsx", file_format="excel")

# get other for all articles, save them to .csv and .xlsx file format
other = person_or_other(de_full_tuple_list, persons_only=False)
other_dict = dict(other)
save_category_mapping(other_dict, "Other.csv")
save_category_mapping(other_dict, "Other.xlsx", file_format="excel")

# get articles and entities of category 'persons' that don'text exist in German DBpedia
persons_no_entry = person_or_other(no_entry_cat_list)
persons_no_entry_dict = dict(persons_no_entry)
save_category_mapping(persons_no_entry_dict, "PersonsNoEntry.csv", exists=False, all_articles=False)
save_category_mapping(persons_no_entry_dict, "PersonsNoEntry.xlsx", file_format="excel", exists=False,
                      all_articles=False)

# get articles and entities of category 'other that don'text exist in German DBpedia
other_no_entry = person_or_other(no_entry_cat_list, persons_only=False)
other_no_entry_dict = dict(other_no_entry)
save_category_mapping(other_no_entry_dict, "OtherNoEntry.csv", exists=False, all_articles=False)
save_category_mapping(other_no_entry_dict, "OtherNoEntry.xlsx", exists=False, all_articles=False,
                      file_format="excel")

# get articles and entities of category 'persons' that exist in German DBpedia
persons_with_entry = person_or_other(DBpedia_entry_list)
persons_with_entry_dict = dict(persons_with_entry)
save_category_mapping(persons_with_entry_dict, "PersonsWithEntry.csv", exists=True, all_articles=False)
save_category_mapping(persons_with_entry_dict, "PersonsWithEntry.xlsx", exists=True, all_articles=False,
                      file_format="excel")

# get artices and entities of category 'other' that exist in German DBpedia
other_with_entry = person_or_other(DBpedia_entry_list, persons_only=False)
other_with_entry_dict = dict(other_with_entry)
save_category_mapping(other_with_entry_dict, "OtherWithEntry.csv", exists=True, all_articles=False)
save_category_mapping(other_with_entry_dict, "OtherWithEntry.xlsx", exists=True, all_articles=False,
                      file_format="excel")

# print(len(persons_no_entry))
# print(len(other_no_entry))
# print("--------------------")
# print(len(persons_with_entry))
# print(len(other_with_entry))


# Plot Statistics, first for all Articles
y_pos = len(de_wiki_titles)
plt.ylim(0, len(de_wiki_titles))
plt.title("Category statistics for all candidate articles")
plt.ylabel("Articles DE total")
plt.xlabel("Total amount of candidate DE articles/entities: " f"{len(de_wiki_titles)}")
x = ["Persons", "Other"]
y = [len(persons), len(other)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/Plots/AllCategories.png")

# # plot category statistics for articles without DBpedia entry
y_pos = len(no_entry_titles)
plt.ylim(0, len(no_entry_titles))
plt.title("Category statistics for articles without entry in German DBpedia")
plt.ylabel("Articles with no DBpedia DE entry total")
plt.xlabel("Total amount of candidate DE articles/entities with no DBpedia entry: " f"{len(no_entry_titles)}")
x = ["Persons", "Other"]
y = [len(persons_no_entry), len(other_no_entry)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/Plots/NoEntryCategories.png")

# plot statistics for Articles with DBpedia entry
y_pos = len(DBpedia_entry_titles)
plt.ylim(0, len(DBpedia_entry_titles))
plt.title("Category statistics for articles with entry in German DBpedia")
plt.ylabel("Articles with DBpedia DE entry total")
plt.xlabel("Total amount of candidate DE articles/entities with DBpedia entry: " f"{len(DBpedia_entry_titles)}")
x = ["Persons", "Other"]
y = [len(persons_with_entry), len(other_with_entry)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/Plots/DEEntryCategories.png")
