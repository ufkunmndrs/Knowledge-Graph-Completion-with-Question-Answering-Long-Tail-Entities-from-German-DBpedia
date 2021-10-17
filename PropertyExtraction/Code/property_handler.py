# -*- coding: utf-8 -*-
"""
Created on Jun 05 10:40:00 2021

@author: Ufkun-Bayram Menderes

This Python file provides a Class "PropertyHandler" to both handle Properties of DBpedia in various ways

"""

import os
import ast
from deep_translator import GoogleTranslator
import time
import pandas as pd


class PropertyHandler:
    def __init__(self, csv_file: str, persons=True):
        """
        Constructor of Property Handler class
        Parameters
        ----------
        csv_file: str
            csv file to be handled. Due to Windows restrictions, the whole PATH has to be passed as input
        persons: True/False
            determines whether DBpedia properties of type person or of other types will be handled
        """
        self.csv_file = csv_file
        self.persons = persons

    def propertycsv2list(self, no_translation=True):
        """
        Maps csv file containing properties of any kind to a list of tuples

        Parameters
        ----------
        self.csv_file: str
            csv file containing the properties and their German translations
        self.path: str
            filepath from which the csv file will be extracted.
            The default is C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/PersonsPropertiesCSV/
        no_translation: True/False
            Decides whether the list of tuples for which a translation of the property is necessary (True) or the ones
            with an existing translation (False) will be returned.
            The default is True.

        Returns
        -------
        no_translation_list/translation_exists: list
            List containing tuples for which tuple needs translation (needs_translation_list) or the ones with existing
            German translation of the property will be returned (translation_exists)

        """
        property_csv = self.csv_file
        property_df = pd.read_csv(property_csv)
        property_df = property_df.fillna(0)
        property_df = property_df.to_records(index=False)
        property_list = list(property_df)
        no_translation_list = [nt for nt in property_list if nt[1] == 0]
        translation_exists = [tup for tup in property_list if tup not in no_translation_list]
        if no_translation is not True:
            return translation_exists
        else:
            return no_translation_list

    @staticmethod
    def write_property_file(input_list: list, filename: str,
                            path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/"
                                 "PersonProperties/PersonPropertiesTXTFiles"):
        """
        writes a list of any given length with any given number/type of elements to a .txt file, where each element
        is a line of the file
        Parameters
        ----------
        input_list: list
            List whose elements will be written to a .txt file
        filename: str
            desired json_filename for the .txt file
        path: str
            Path where the file will be stored:
            The default is: "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/"
                                 "PersonsProperties/PersonsPropertiesTXTFiles"

        Returns
        -------

        """
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write("\n".join(map(str, input_list)))
            f.close()

    @staticmethod
    def read_txt(filename: str, path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/"
                                     "PersonProperties/PersonPropertiesTXTFiles"):
        """
        reads every line of a txt and stores each line as element in a list
        Parameters
        ----------
        filename: str
            name of the txt file
        path: str
            filepath from which the txt file will be extracted

        Returns
        -------
        lines_stripped: list
            list where each line of the txt file is an element of the list (stripped)
        """
        with open(os.path.join(path, filename)) as f:
            lines = f.readlines()
            lines_stripped = [line.strip() for line in lines]
            return lines_stripped

    @staticmethod
    def translate_properties(property_list: list, return_tuple_list=False):
        """
        translate list of English DBpedia properties to German via Google translate
        Parameters
        ----------
        property_list: list
            List of tuples where a German Label for a DBpedia property is not provided already
        return_tuple_list: bool
            Determines whether a list of tuples with English property and corresponding German property (True) or a list
            with just German properties will be created (False).
            The default is False
        Returns
        -------
        translated_properties: list
            list of properties translated from German to English
        en_de_tuples_list: list
            List of properties translated from German to English where in each tuple, first element is the property
            in English and second element its translation in German
        """
        prop_list_ast = [ast.literal_eval(prop) for prop in property_list]
        properties = [prop[2] for prop in prop_list_ast]
        translated_properties = []
        for prop in properties:
            translated_properties.append(GoogleTranslator(source='auto', target='german').translate(prop))
            time.sleep(0.5)
        if return_tuple_list is True:
            en_de_tuple_list = list(zip(translated_properties, properties))
            return en_de_tuple_list
        else:
            return translated_properties

    # noinspection PyTypeChecker
    def full_properties(self, to_translate_file: str, properties_with_de_label: list, write2file=False,
                        path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/"
                             "PersonProperties/PersonPropertiesTXTFiles", properties_filename=None,
                        return_property_list=False):
        """
        gets the full set of properties for both English and German properties of any entity class in DBpedia.
        Does an internal translation of the properties as well
        Parameters
        ----------
        to_translate_file: str
            json_filename of the file which contains all the English properties that need translation to German
        properties_with_de_label: list
            List of tuples with properties for which a German label exists in DBpedia. The first element in each tuple
            is the German label of that property, the 2nd element the corresponding English property label.
        write2file: True/False
            Determines whether a file with these properties will be written or not. If set to True, a fill will be
            created under the input name and path.
            The default is False.
        path: str
            Filepath where the txt file will be stored (if write2file is True).
            The default filepath is that of category "Persons":
            "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/PersonsProperties/PersonsPropertiesTXTFiles"
        properties_filename: None/str
            The designated json_filename for the file of property tuples
        return_property_list: True/False
            Determines whether a the list of tuples with English and German will be returned or not.
            The default is False (since it's of no further use in the program)
        Returns
        -------

        """
        to_translate_properties = self.read_txt(to_translate_file, path=path)
        properties_translated = self.translate_properties(to_translate_properties, return_tuple_list=True)
        properties_finalized = [tuple(list(tup)[1:]) for tup in properties_with_de_label]
        properties_total = properties_finalized + properties_translated
        properties_total = [prop for prop in properties_total if "Wiki" not in prop[0]]
        properties_total = [prop for prop in properties_total if "thumbnail" not in prop[1]]
        properties_total = [prop for prop in properties_total if "has abstract" not in prop[1]]
        properties_total = [prop for prop in properties_total if "sound recording" not in prop[1]]
        if write2file is True and type(properties_filename) == str and return_property_list is True:
            self.write_property_file(properties_total, properties_filename, path=path)
            return properties_total
        elif write2file is True and type(properties_filename) == str and return_property_list is False:
            self.write_property_file(properties_total, properties_filename, path=path)
        else:
            return properties_total
