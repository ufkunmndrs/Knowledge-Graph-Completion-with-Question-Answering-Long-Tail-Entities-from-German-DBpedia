import os
import ast
import time
from deep_translator import GoogleTranslator


def generate_other_english_questions(property_filename: str, other_type: str,
                                     path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/"
                                          "Properties/OtherProperties/"):
    """
    Generates all questions for categories "other" in English based on their property
    Parameters
    ----------
    property_filename: str
        name of the file where the properties for a given category are stored
    other_type: str
        specific type of the category in "other"
    path: str
        Filepath where the property_filename file is stored.
        The default ist "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/OtherProperties/"

    Returns
    -------
    english_questions: list
        a list with all English Questions based on the respective property
    """
    path = path + other_type + "Properties/" + other_type + "PropertiesTXTFiles/"
    full_property_file = os.path.join(path, property_filename)
    with open(full_property_file, encoding="utf-8") as f:
        full_property_list = f.readlines()
        full_property_list = [line.strip() for line in full_property_list]
    full_property_list = [ast.literal_eval(tup) for tup in full_property_list]
    english_properties = [tup[1] for tup in full_property_list]
    english_questions = ["What is the " + elem + " of __?" for elem in english_properties]
    return english_questions


def translate_english_other_questions(questions_list: list, other_type: str, position: str,
                                      path="C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/OtherQuestions/"
                                           "OtherQuestionsAG/", return_list=False):
    """
    Translates a list of English Questions for categories of "other" to German
    Parameters
    ----------
    questions_list: list
        List of English Questions
    other_type: str
        Specific type of the category in "other"
    position: str
        Position of the entity (questions will be formed accordingly)
    path: str
        path where the Questions will be saved and stored.
        The default is "C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/OtherQuestions/OtherQuestionsAG/"
    return_list: bool
        determines whether a list of questions translated to German will be returned (True) or not (False)

    Returns
    -------
    english2german_translated: list
        A list of questions translated from English to German. Will only be returned if "return_list" param is set
        to True.
    """
    valid_positions = ["SP", "OP"]
    if position not in valid_positions:
        raise ValueError("Invalid input for entity position, must be either SP or OP")
    path = path + other_type + "QuestionsAG/"
    filename = other_type + "Questions" + position + "_AG.txt"
    english2german_translated = []
    for q in questions_list:
        english2german_translated.append(GoogleTranslator(source='auto', target='german').translate(q))
        time.sleep(0.3)
    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, english2german_translated)))
        f.close()
    if return_list is not False:
        return english2german_translated


# noinspection PyTypeChecker
def save_other_ag_questions(ag_questions_filename: str, other_type: str, position: str):
    """
    Saves automatically generated questions to the corresponding file and directory
    Parameters
    ----------
    ag_questions_filename: str
        designated filename for the questions file
    other_type: str
        exact type/category of "other"
    position: str
        entity position

    Returns
    -------
    None

    """
    english_questions_list = generate_other_english_questions(ag_questions_filename, other_type)
    translate_english_other_questions(english_questions_list, other_type, position)


# Building SP and OP
save_other_ag_questions("BuildingTotalPropertiesSP.txt", "Building", "SP")
save_other_ag_questions("BuildingTotalPropertiesOP.txt", "Building", "OP")

# Disease SP and OP
save_other_ag_questions("DiseaseTotalPropertiesSP.txt", "Disease", "SP")
save_other_ag_questions("DiseaseTotalPropertiesOP.txt", "Disease", "OP")

# History SP and OP
save_other_ag_questions("HistoryTotalPropertiesSP.txt", "History", "SP")
save_other_ag_questions("HistoryTotalPropertiesOP.txt", "History", "OP")

# Literature SP and OP
save_other_ag_questions("LiteratureTotalPropertiesSP.txt", "Literature", "SP")
save_other_ag_questions("LiteratureTotalPropertiesOP.txt", "Literature", "OP")

# Magazine SP and OP
save_other_ag_questions("MagazineTotalPropertiesSP.txt", "Magazine", "SP")
save_other_ag_questions("MagazineTotalPropertiesOP.txt", "Magazine", "OP")

# Newspaper SP and OP
save_other_ag_questions("NewspaperTotalPropertiesSP.txt", "Newspaper", "SP")
save_other_ag_questions("NewspaperTotalPropertiesOP.txt", "Newspaper", "OP")

# Organization SP and OP
save_other_ag_questions("OrganizationTotalPropertiesSP.txt", "Organization", "SP")
save_other_ag_questions("OrganizationTotalPropertiesOP.txt", "Organization", "OP")

# Park SP and OP
save_other_ag_questions("ParkTotalPropertiesSP.txt", "Park", "SP")
save_other_ag_questions("ParkTotalPropertiesOP.txt", "Park", "OP")

# School SP and OP
save_other_ag_questions("SchoolTotalPropertiesSP.txt", "School", "SP")
save_other_ag_questions("SchoolTotalPropertiesOP.txt", "School", "OP")

# Ship SP and OP
save_other_ag_questions("ShipTotalPropertiesSP.txt", "Ship", "SP")
save_other_ag_questions("ShipTotalPropertiesOP.txt", "Ship", "OP")
