# -*- coding: utf-8 -*-
"""
Created on June 3rd 20:30:00 2021

@author: Ufkun-Bayram Menderes

This Python file provides further analysis of the candidate articles/entities contained within the large subgroup
"Persons" by accessing the Persons.csv file. The modules provided in this file are meant to extract the current status,
gender and nationality of persons. Further analysis, however, will not be provided, as there are too many intersections
which could negatively impact the accuracy of the analysis.

This file contains the following functions:
    * get_gender: gets the genders for every entity in a list of (entity, categories) tuples
    * get_doa: gets the current living status (dead vs. alive) for every entity in a list of (entity, categories) tuples
    * get_nationality: gets nationality for every entity in a list of (entity, categories) tuples.
"""
from category_analyzer import CategoryAnalyzer


person_analyzer = CategoryAnalyzer("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/Persons.csv")
persons_all_list = person_analyzer.preprocess()


def get_gender(titles_categories: list, gender: str):
    """
    gets the genders for every entity in a list of (entity, categories) tuples
    Parameters
    ----------
    titles_categories: list
        List of Tuples where first element is Title/Entity, Second Element is List of categories
    gender: str
        Gender which shall be retrieved. Can only be "men" or "women"

    Returns
    -------
    men/women: lists
        List containing the entities of the input gender
    """
    valid_genders = ["men", "women"]
    if gender not in valid_genders:
        raise ValueError("Input gender must be either man or woman")
    men = []
    women = []
    for pairs in titles_categories:
        if "Mann" in pairs[1]:
            men.append(pairs)
        elif "Frau" in pairs[1]:
            women.append(pairs)
    if gender == "men":
        return men
    else:
        return women


def get_doa(titles_categories: list, status: str):
    """
    gets the current living status (dead vs. alive) for every entity in a list of (entity, categories) tuples
    Parameters
    ----------
    titles_categories: list
        List of (entity, category) tuples
    status: str
        desired status which shall be checked, can be either "dead" or "alive". Any other input string will
        throw an Error and prompt the program to stop

    Returns
    -------
    dead_list: list
    alive_list: list
        List of entities that are dead at the date of this research (25.05.21)
        List of entities that are alive at the date of this research (25.05.21)

    """
    valid_status = ["dead", "alive"]
    if status not in valid_status:
        raise ValueError("Invalid input status")
    dead_list = []
    alive_list = []
    for pairs in titles_categories:
        if any("Gestorben" in word for word in pairs[1]):
            dead_list.append(pairs)
        else:
            alive_list.append(pairs)
    if status == "dead":
        return dead_list
    else:
        return alive_list


def get_nationality(title_categories: str, nationality: str):
    """
    gets nationality for every entity in a list of (entity, categories) tuples

    Parameters
    ----------
    title_categories: list
        List of (entity, category) tuples
    nationality:
        Desired nationality for which entities shall be checked and retrieved. If an invalid nationality is passed as
        an input, the program will throw an error

    Returns
    -------
    nationality_list:
        List of entities according to the input nationality
    """
    valid_nationalities = ["German", "Austrian", "Swiss", "American", "British", "French", "Prussian"]
    german_denom = ["Deutscher", "Maler (Deutschland)", "Bildhauer (Deutschland)", "Musiker (Deutschland)",
                    "Unternehmer (Deutschland)", "Beamter (Deutschland)"]
    austrian_denom = ["Österreicher", "Maler (Österreich)", "Person (Kaisertum Österreich)",
                      "Unternehmer (Österreich-Ungarn)", "Musiker (Österreich)", "Unternehmer (Österreich)",
                      "Landtagspräsident (Oberösterreich)"]
    swiss_denom = ["Schweizer"]
    american_denom = ["US-Amerikaner"]
    british_denom = ["Brite"]
    french_denom = ["Franzose"]
    prussion_denom = ["Preuße", "Major (Preußen)"]
    if nationality not in valid_nationalities:
        raise ValueError("Invalid input nationality")
    nationality_list = []
    for pairs in title_categories:
        if any(de_denom in german_denom for de_denom in pairs[1]) and nationality == "German":
            nationality_list.append(pairs)
        elif any(aut_denom in austrian_denom for aut_denom in pairs[1]) and nationality == "Austrian":
            nationality_list.append(pairs)
        elif any(ch_denom in swiss_denom for ch_denom in pairs[1]) and nationality == "Swiss":
            nationality_list.append(pairs)
        elif any(us_denom in american_denom for us_denom in pairs[1]) and nationality == "American":
            nationality_list.append(pairs)
        elif any(uk_denom in british_denom for uk_denom in pairs[1]) and nationality == "British":
            nationality_list.append(pairs)
        elif any(fr_denom in french_denom for fr_denom in pairs[1]) and nationality == "French":
            nationality_list.append(pairs)
        elif any(pr_denom in prussion_denom for pr_denom in pairs[1]) and nationality == "Prussian":
            nationality_list.append(pairs)
    return nationality_list


# get genders
gender_list_lengths = []
men_persons = get_gender(persons_all_list, "men")
gender_list_lengths.append(("Men", len(men_persons)))

women_persons = get_gender(persons_all_list, "women")
gender_list_lengths.append(("Women", len(women_persons)))

# get dead/alive persons
doa_list_lengths = []
dead_persons = get_doa(persons_all_list, "dead")
doa_list_lengths.append(("Dead", len(dead_persons)))

alive_persons = get_doa(persons_all_list, "alive")
doa_list_lengths.append(("Alive", len(alive_persons)))

# Get nationalities
total_nationalities = []
nationality_list_length = []
germans = get_nationality(persons_all_list, "German")
nationality_list_length.append(("Germans", len(germans)))
total_nationalities += germans

austrians = get_nationality(persons_all_list, "Austrian")
austrians_true = [austrian for austrian in austrians if austrian not in germans]
nationality_list_length.append(("Austrians", len(austrians_true)))
total_nationalities += austrians_true

swiss = get_nationality(persons_all_list, "Swiss")
swiss_true = [ch for ch in swiss if ch not in total_nationalities]
nationality_list_length.append(("Swiss", len(swiss_true)))
total_nationalities += swiss_true

americans = get_nationality(persons_all_list, "American")
americans_true = [us for us in americans if us not in total_nationalities]
nationality_list_length.append(("Americans", len(americans_true)))
total_nationalities += americans_true


prussian = get_nationality(persons_all_list, "Prussian")
prussian_true = [prus for prus in prussian if prus not in total_nationalities]
nationality_list_length.append(("Prussians", len(prussian_true)))
total_nationalities += prussian_true


german_speaking = germans + austrians_true + swiss_true + prussian_true
missing = [mis for mis in persons_all_list if mis not in total_nationalities]

final_nat_list = sorted(nationality_list_length, key=lambda tup: tup[1], reverse=True)
final_nat_list.append(("N/A, Other", len(missing)))
# print(final_nat_list)

person_analyzer.plot_categories(gender_list_lengths, other=False, persons_attribute="gender")
person_analyzer.plot_categories(doa_list_lengths, other=False, persons_attribute="doa")
person_analyzer.plot_categories(final_nat_list, other=False, persons_attribute="nationality")
