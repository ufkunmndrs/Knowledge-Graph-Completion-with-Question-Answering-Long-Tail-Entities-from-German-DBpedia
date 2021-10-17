import os
import ast
import pandas as pd
import numpy as np

# load split Wiki TXT file containing entity name and entity text tuples
wiki_split_txt = "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/PreprocessedTXTFiles/FullWikiTXT/FullWikiTXTsplit.txt"
with open(wiki_split_txt, encoding="utf-8") as f:
    wiki_article_list = f.readlines()
    wiki_article_list = [line.strip() for line in wiki_article_list]
    wiki_article_list = [ast.literal_eval(tup) for tup in wiki_article_list]


def wiki_csv2list(category_type: str, path="C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/"):
    """
    Reads and transforms a CSV file containing Wikipedia entities to a list
    Parameters
    ----------
    category_type: str
        Specific type/name of an entity
    path: str
        Filepath from which the entities will be retrieved

    Returns
    -------
    wiki_df_list: list
        A list of titles of the input category

    """
    valid_categories = ["Persons", "Buildings", "Diseases", "Literature", "Magazines", "Newspapers", "Organizations",
                        "Parks", "Schools", "Ships", "History"]
    if category_type not in valid_categories:
        raise ValueError("Invalid input category")
    if category_type == "Persons":
        wiki_df = pd.read_csv(path + "Persons.csv", encoding="utf-8-sig")
        wiki_df = wiki_df.drop("Categories", axis=1)
        wiki_df_list = wiki_df["Title"].to_list()
    else:
        path = path + "OtherDetailed/"
        wiki_df = pd.read_csv(path + category_type + ".csv")
        wiki_df_list = wiki_df["Title"].to_list()
    return wiki_df_list


def write_and_save_wiki_texts(category_type: str,
                              path="C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/"
                                   "PreprocessedTXTFiles/", write_file=True, return_list=False):
    """
    writes and saves Wikipedia texts to the corresponding directory/file according to their respective category

    Parameters
    ----------
    category_type: str
        Specific type/name of the category
    path: str
        File/Directory path
    write_file: bool
        determines whether the file should actually be written and saved
    return_list: bool
        Determines whether a list containing the article texts will be returned

    Returns
    -------
    title_article_text: list

    """
    if category_type != "Persons":
        path = path + "OtherWikiTXT/" + category_type + "WikiTXT"
        filename = category_type + "WikiTXT.txt"
    else:
        path = path + category_type + "WikiTXT/"
        filename = category_type + "FullWikiTXT.txt"
    category_list = wiki_csv2list(category_type)
    title_article_text = [article for article in wiki_article_list if article[0] in category_list]
    if write_file is True:
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write("\n".join(map(str, title_article_text)))
            f.close()
    if return_list is True:
        return title_article_text


def chunks(lst: list, n: int):
    """
    chunks a list into n even parts

    Parameters
    ----------
    lst: list
        Any arbitrary list that can contain any arbitrary data structure
    n: int
        Size of the chunks
    Returns
    -----------
    a list of n sized chunks from the original input list lst
    -------

    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def split_list(a_list: list, n=2):
    """
    splits any given list into n parts
    Parameters
    ----------
    a_list: list
        Input list
    n: int
        parts into which the list will be split

    Returns
    -------

    """
    half = len(a_list)//n
    return a_list[:half], a_list[half:]


# get all txt files and save them
wiki_categories = ["Persons", "Buildings", "Diseases", "History", "Literature", "Magazines", "Newspapers",
                   "Organizations", "Parks", "Schools", "Ships"]


# chunk Persons
persons_list = write_and_save_wiki_texts("Persons", write_file=False, return_list=True)
# chunked_persons_list = chunks(persons_list, 50)
# print(len(chunked_persons_list))

persons_chunked_to_three = np.array_split(persons_list, 3)
persons_list_1 = list(persons_chunked_to_three[0])
persons_list_1 = [tuple(elem) for elem in persons_list_1]

persons_list_2 = list(persons_chunked_to_three[1])
persons_list_2 = [tuple(elem) for elem in persons_list_2]

persons_list_3 = list(persons_chunked_to_three[2])
persons_list_3 = [tuple(elem) for elem in persons_list_3]

for w in wiki_categories:
    write_and_save_wiki_texts(w)

# save chunked Persons fo filepath
save_path = "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/PreprocessedTXTFiles/PersonsWikiTXT/"

with open(os.path.join(save_path, "PersonsWikiTXT1.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(map(str, persons_list_1)))
    f.close()

with open(os.path.join(save_path, "PersonsWikiTXT2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(map(str, persons_list_2)))
    f.close()

with open(os.path.join(save_path, "PersonsWikiTXT3.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(map(str, persons_list_3)))
    f.close()
