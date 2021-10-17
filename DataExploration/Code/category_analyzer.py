import pandas as pd
import ast
import matplotlib.pyplot as plt
import os


class CategoryAnalyzer:
    """
    Class to process .csv files of categories "persons" and "other" and analyze them for further attributes.
    Class loads csv file first and then provides additional functionalities of plotting.

    """
    def __init__(self, csv_file: str):
        """
        init method of the class
        Parameters
        ----------
        csv_file: str
            CSV file containing persons/other which will be analyzed
        """
        self.csv_file = csv_file

    def preprocess(self, return_dict=False):
        """
        Preprocesses a csv file containing entities and their categories
        Parameters
        ----------
        return_dict: bool
            Determines whether a dict (True) or a list of tuples will (False) be returned.
            The default is False.

        Returns
        -------
        type_list: list
            list of tuples where entity title is first element and second element are their categories
        """

        # load csv file
        type_df = pd.read_csv(self.csv_file)
        type_df_titles = type_df["Title"].tolist()
        type_df_categories = type_df["Categories"].tolist()

        # make list of tuples first, convert list as string to list object
        global type_list
        type_list = list(zip(type_df_titles, type_df_categories))
        type_list = [(pairs[0], ast.literal_eval(pairs[1])) for pairs in type_list]
        type_dict = dict(type_list)

        if type_dict is True:
            return type_dict
        else:
            return type_list

    @staticmethod
    def plot_categories(category_list: list, other=True, persons_attribute=None):
        """
        plots the distribution of cateogories

        Parameters
        ----------
        category_list: list
            list of (entity, categories) tuples where entity is a string and categories is a list of strings
        other: True/False
            determines whether articles of type "other" will be analyzed (True) or persons (False).
            The default is True.
        persons_attribute: str/None
            determines according to which attribute the plotting will be done. Will only be triggered/necessary
            if other is not True.
            The default is None.

        Returns
        -------
        Just plots, doesn'text return anything

        """
        valid_persons_attributes = [None, "gender", "doa", "nationality"]
        if persons_attribute not in valid_persons_attributes:
            raise ValueError("Invalid persons attribute")
        y_pos = len(type_list)
        plt.ylim(0, len(type_list))
        plt.title("Category statistics for all candidate articles of category Other")
        plt.ylabel("Other Articles total")
        plt.xlabel("Total amount of candidate DE articles/entities as Other: " f"{len(type_list)}")
        if other is not True:
            plt.ylabel("Persons Articles total")
            plt.xlabel("Total amount of candidate DE articles/entities as Persons: " f"{len(type_list)}")
            if persons_attribute == "gender":
                plt.title("Gender statistics for all candidate articles of category Persons")
            elif persons_attribute == "doa":
                plt.title("DOA statistics for all candidate articles of category Persons")
            else:
                plt.title("Nationalities for all candidate articles of category Persons")
        x = [elem[0] for elem in category_list]
        y = [elem[1] for elem in category_list]
        for index, value in enumerate(y):
            plt.text(index, value, str(value))
        plt.bar(x, y, width=0.5)
        plt.show()

    @staticmethod
    def other_detailed_to_csv(titles_list: list, filename: str, title_only=False):
        df = pd.DataFrame(titles_list, columns=["Title", "Categories"])
        if title_only is True:
            df = df.drop(columns=["Categories"])
        path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/OtherDetailed/"
        df.to_csv(os.path.join(path, filename), sep=",", encoding="utf-8-sig", index=False)

