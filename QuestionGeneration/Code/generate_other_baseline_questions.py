import ast
import os


def read_other_properties(property_filename: str, other_type: str,
                          path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/OtherProperties/",
                          return_german_only=True):
    """
    reads all properties of categories from "Other"
    Parameters
    ----------
    property_filename: str
        name of the file where all the properties of a category are stored
    other_type: str
        specific type/category of "other"
    path: str
        path where file is stored.
        The default is: "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/OtherProperties/"
    return_german_only: bool
        determines whether a list of only German translated properties will be returned.
        The default is True (since the English ones aren't needed)

    Returns
    -------
    de_property_list: list
        A list containing all the properties for the input category specified in "specific_type"
    """
    path = path + other_type + "Properties/" + other_type + "PropertiesTXTFiles/"
    full_property_file = os.path.join(path, property_filename)
    with open(full_property_file, encoding="utf-8") as f:
        full_property_list = f.readlines()
        full_property_list = [line.strip() for line in full_property_list]
        full_property_list = [ast.literal_eval(tup) for tup in full_property_list]
    if return_german_only is not True:
        return full_property_list
    else:
        de_property_list = [tup[0] for tup in full_property_list]
        return de_property_list


def generate_other_bl_questions(property_list: list, other_type: str, position: str,
                                path="C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/OtherQuestions/"
                                     "OtherQuestionsBL/",
                                german_properties_only=True):
    """
    Generates the Baseline questions for all categories of type "other".
    Parameters
    ----------
    property_list: list
        List of German properties
    other_type: str
        specific type of "other"
    position: str
        position of the entity, either "SP" or "OP"
    path: str
        Filepath where the questions in txt will be stored
    german_properties_only: bool
        Determines whether only the german properties are passed as input

    Returns
    -------
    None
    """
    path = path + other_type + "QuestionsBL/"
    filename = other_type + "Questions" + position + "_BL.txt"
    questions_list = [elem + " von __?" for elem in property_list]
    if german_properties_only is not True:
        questions_list = [elem[0] + " of __?" for elem in property_list]
    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, questions_list)))
        f.close()


def save_other_bl_questions(bl_questions_filename: str, other_type: str, position: str):
    """
    Combines the previous two functions

    Parameters
    ----------
    bl_questions_filename: str
        Specific filename for the Baseline questions file
    other_type: str
        Specific type of the category among "other"
    position: str
        Entity position

    Returns
    -------
    None

    """
    property_list = read_other_properties(bl_questions_filename, other_type)
    generate_other_bl_questions(property_list, other_type, position)


# Building SP and OP
save_other_bl_questions("BuildingTotalPropertiesSP.txt", "Building", "SP")
save_other_bl_questions("BuildingTotalPropertiesOP.txt", "Building", "OP")

# Diseases SP and OP
save_other_bl_questions("DiseaseTotalPropertiesSP.txt", "Disease", "SP")
save_other_bl_questions("DiseaseTotalPropertiesOP.txt", "Disease", "OP")

# History SP and OP
save_other_bl_questions("HistoryTotalPropertiesSP.txt", "History", "SP")
save_other_bl_questions("HistoryTotalPropertiesOP.txt", "History", "OP")

# Literature SP and OP
save_other_bl_questions("LiteratureTotalPropertiesSP.txt", "Literature", "SP")
save_other_bl_questions("LiteratureTotalPropertiesOP.txt", "Literature", "OP")

# Magazine SP and OP
save_other_bl_questions("MagazineTotalPropertiesSP.txt", "Magazine", "SP")
save_other_bl_questions("MagazineTotalPropertiesOP.txt", "Magazine", "OP")

# Newspaper SP and OP
save_other_bl_questions("NewspaperTotalPropertiesSP.txt", "Newspaper", "SP")
save_other_bl_questions("NewspaperTotalPropertiesOP.txt", "Newspaper", "OP")

# Organization SP and OP
save_other_bl_questions("OrganizationTotalPropertiesSP.txt", "Organization", "SP")
save_other_bl_questions("OrganizationTotalPropertiesOP.txt", "Organization", "OP")

# Park SP and OP
save_other_bl_questions("ParkTotalPropertiesSP.txt", "Park", "SP")
save_other_bl_questions("ParkTotalPropertiesOP.txt", "Park", "OP")

# School SP and OP
save_other_bl_questions("SchoolTotalPropertiesSP.txt", "School", "SP")
save_other_bl_questions("SchoolTotalPropertiesOP.txt", "School", "OP")

# Ship SP and OP
save_other_bl_questions("ShipTotalPropertiesSP.txt", "Ship", "SP")
save_other_bl_questions("ShipTotalPropertiesOP.txt", "Ship", "OP")
