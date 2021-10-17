# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file provides checks the DBpedia entry status for the candidate entities in German/English.
The candidate entities and their corresponding articles are retrieved from the .txt file "OnlyDeArticlesFinal", in
which all German only Wikipedia articles without an infobox are stored. The results are stored and saved in .csv and
.xlsx files respectively and stored in the folders/paths that are specified within the corresponding functions.

This file contains the following functions:
    * check_DBpedia_status: Checks whether a DBpedia article is available for a list of strings Parameters
    * count_status: Counts the amount of status code responses in an input list, status codes are DBpedia queries
    * save_datafile: saves a dict with wiki titles and their DBpedia status code responses to a .csv or .xlsx file
    * save_specific_titles: saves specific types of DBpedia entries (i.e. wiki titles) and their DBpedia status into
     a .csv or a .xlsx file
"""

import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import os


def check_DBpedia_status(titles: list, language="German"):
    """
    Checks whether a DBpedia article is available for a list of strings
    Parameters
    ----------
    titles: list
        Titles as strings
    language: String
        Language for which DBpedia shall be checked.
        The default is German.

    Returns
    -------
    status_list: list
        list storing the values of the status responses, elements are ints
    """
    uri = "http://de.dbpedia.org/page/"
    if language == "English":
        uri = "https://dbpedia.org/page/"
    status_list = []
    for title in titles:
        response = requests.get(uri + title)
        status_list.append(response.status_code)
        time.sleep(0.7)
    return status_list


def count_status(status_list: list, pos=True):
    """
    Counts the amount of status code responses in an input list, status codes are DBpedia queries

    Parameters
    ----------
    status_list: list
        List of DBpedia availability statuses, elements are of type "int"
    pos: True/False
        Determines whether positive counts (i.e. title and corresponding entity exist in German DBpedia) or negative
        counts (title and entity don'text exist in German DBpedia)

    Returns
    -------
    pos_count, neg_count: int
        pos_count = int, counf of title for which a DBpedia entry exists
        neg_count = int, count of titles for which a DBpedia entry doesn'text exist
    """
    pos_count = 0
    neg_count = 0
    for status in status_list:
        if status == 404:
            neg_count += 1
        else:
            pos_count += 1
    if pos is not True:
        return neg_count
    else:
        return pos_count


def save_datafile(title_status_dict: dict, filename: str,  file_format="csv"):
    """
    saves a dict with wiki titles and their DBpedia status code responses to a .csv or .xlsx file

    Parameters
    ----------
    title_status_dict: dict
        dict where keys are Wikipedia article titles, values are their server response (either 200 or 404)
    filename: str
        designated json_filename
    file_format:
        desired format to save titles and status, can be either csv or excel
        The default is csv

    Returns
    -------
    doesn'text return anything, just saves the file

    """
    title_status_dict = {k.replace("_", " "): v for k, v in title_status_dict.items()}
    path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles"
    df_list = list(title_status_dict.items())
    df = pd.DataFrame(df_list)
    df.columns = ["Title", "Status"]
    if file_format != "csv":
        df.to_excel(os.path.join(path, filename), encoding='utf-8', index=False)
    else:
        df.to_csv(os.path.join(path, filename), sep=",", encoding='utf-8', index=False)


def save_specific_titles(title_status_dict: dict, filename: str, exists=True, file_format="csv"):
    """
    saves specific types of DBpedia entries (i.e. wiki titles) and their DBpedia status into a .csv
    or a .xlsx file

    Parameters
    ----------
    title_status_dict: dict
        dict in which keys are wiki titles and values are status codes in DBpedia (either 200 or 404 for de DBpedia)
    filename: str
        designated json_filename
    exists: True/False
        decides which types of titles will be stored in the file. Setting it to "False" will only store the titles
        and entities that do not have a DBpedia entry (i.e. status code = 404). The default is True.
    file_format: str
        desired file format, if "excel" as input here then an Excel file will be created. The default is csv

    Returns
    -------

    """
    if exists is not True:
        path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/NoDBpediaEntry"
    else:
        path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/DBpediaEntryExists"
    title_status_dict = {k.replace("_", " "): v for k, v in title_status_dict.items()}
    df_list = list(title_status_dict.items())
    df_final_list = []
    for title in df_list:
        if exists is False:
            if title[1] == 404:
                df_final_list.append(title)
        else:
            if title[1] == 200:
                df_final_list.append(title)
    df = pd.DataFrame(df_final_list)
    df.columns = ["Title", "Status"]
    if file_format == "excel":
        df.to_excel(os.path.join(path, filename), encoding='utf-8', index=False)
    elif file_format == "csv":
        df.to_csv(os.path.join(path, filename), sep=",", encoding='utf-8', index=False)
    else:
        raise ValueError("Invalid Data Format, only .xlsx or .csv file accepted")


# extract candidate entities from XML file
candidate_entities = "C:/Users/ubmen/Desktop/BA_Prog/DataSelection/TXTFiles/OnlyDeArticlesFinal"

# store entities, i.e. their titles in a list
with open(candidate_entities, encoding="utf8") as f:
    entities = f.readlines()

# clean up title strings for each entity
wiki_titles = [entity.strip() for entity in entities]
wiki_titles = [entity.replace(" ", "_") for entity in wiki_titles]
del wiki_titles[-1]  # delete last element of the list since it's just the total number of articles


# pass entity title list as input, check for their DBpedia status
de_status = check_DBpedia_status(wiki_titles)
wiki_title_status = list(zip(wiki_titles, de_status))

# create a dict where keys are entity titles (str) and values are their DBpedia status code (int)
wiki_title_dict = {k: v for k, v in wiki_title_status}


# Plot statistics
y_pos = len(wiki_titles)
plt.ylim(0, len(wiki_titles))
plt.title("German DBpedia entry status of all candidate articles")
plt.ylabel("Articles DE total")
plt.xlabel("Total amount of DE candidate articles/entities: " f"{len(de_status)}")
x = ["Has entry in de DBpedia", "No entry in de DBpedia"]
y = [count_status(de_status), count_status(de_status, pos=False)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/Plots/DB_status.png")


save_datafile(wiki_title_dict, "DBpedia_status.xlsx", file_format="excel")
save_datafile(wiki_title_dict, "DBpedia_status.csv")

save_specific_titles(wiki_title_dict, "DBpedia_de_exists.xlsx", file_format="excel")
save_specific_titles(wiki_title_dict, "DBpedia_de_exists.csv")

save_specific_titles(wiki_title_dict, "DBpedia_de_no_entry.xlsx", file_format="excel", exists=False)
save_specific_titles(wiki_title_dict, "DBpedia_de_no_entry.csv", exists=False)
