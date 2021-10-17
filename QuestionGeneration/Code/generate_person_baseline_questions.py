import ast
import os


def read_persons_properties(property_filename: str, path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/"
                                                         "PersonProperties/PersonPropertiesTXTFiles",
                            return_german_only=True):
    """
    reads German, English properties as tuples for persons in DBpedia and returns them in a list
    Parameters
    ----------
    property_filename: str
        Filename of the txt file where the property tuples are stored
    path: str
        Filepath of the txt file "property_filename"
    return_german_only: True/False
        Determines wheter a list of tuples with English and German Properties will be returned, or only a list of
        German properties.
        The default is True.

    Returns
    -------
    de_property_list: list
        List containing property tuples from Text files (ships). Will only be returned if
        "return_german_only" is set to False.
        List containing the German properties and German properties only. Will be returned at default since
        "return_german_only" is set to "True" at default.

    """
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


def generate_persons_bl_questions(property_list: list, filename: str,
                                  path="C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/"
                                       "PersonQuestions/PersonQuestionsBL",
                                  german_properties_only=True):
    """
    Generate the baseline person_questions_sp for properties of entity class "Person" of DBpedia
    Parameters
    ----------
    property_list: list
        List of ("German") properties.
    filename: str
        Designated name for the txt file to be created
    path: str
        Filepath where the file will be stored. The default is:C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/"
                                       "PersonQuestions/PersonQuestionsBL"
    german_properties_only: True/False


    Returns
    -------
    None
    """
    questions_list = [elem + " von __?" for elem in property_list]
    if german_properties_only is not True:
        questions_list = [elem[0] + " von __?" for elem in property_list]
    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, questions_list)))
        f.close()


# subject position
filename_sp = "PersonTotalPropertiesSP.txt"
person_sp_list = read_persons_properties(filename_sp, return_german_only=True)
generate_persons_bl_questions(person_sp_list, "PersonQuestionsSP_BL.txt", german_properties_only=True)

# object position
filename_op = "PersonTotalPropertiesOP.txt"
person_op_list = read_persons_properties(filename_op, return_german_only=True)
generate_persons_bl_questions(person_op_list, "PersonQuestionsOP_BL.txt", german_properties_only=True)
