import os
import ast
import time
from deep_translator import GoogleTranslator


def generate_english_person_questions(property_filename: str, path="C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/"
                                                                   "Properties/PersonProperties"
                                                                   "/PersonPropertiesTXTFiles"):
    """
    Generates the English questions from the properties.
    These English questions can then be translated with the "translate_english_questions_function" below.
    Parameters
    ----------
    property_filename: str
        Filename of the txt file where the properties are stored.
    path: str
        File path where the "property_filename" file is stored.

    Returns
    -------
    english_questions: list
        List of questions where each element is a question formed given the corresponding property.
    """
    full_property_file = os.path.join(path, property_filename)
    with open(full_property_file, encoding="utf-8") as f:
        full_property_list = f.readlines()
        full_property_list = [line.strip() for line in full_property_list]
    full_property_list = [ast.literal_eval(tup) for tup in full_property_list]
    english_properties = [tup[1] for tup in full_property_list]
    english_questions = ["What is the " + elem + " of __?" for elem in english_properties]
    return english_questions


def translate_english_person_questions(questions_list: list, filename: str,
                                       path="C:/Users/ubmen/Desktop/BA_Prog/QuestionGeneration/PersonQuestions/"
                                            "PersonQuestionsAG", return_list=False):
    """
    translates the english questions to German via Google Translator

    Parameters
    ----------
    questions_list: list
        List of English questions
    filename: str
        designated filename for the textfile
    path: str
        Designated filepath where the file will be stored
    return_list: bool
        determines whether a list containing the translated questions will be returned. The default is False.

    Returns
    -------

    """
    english2german_translated = []
    for q in questions_list:
        english2german_translated.append(GoogleTranslator(source='auto', target='german').translate(q))
        time.sleep(0.3)
    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, english2german_translated)))
        f.close()
    if return_list is not False:
        return english2german_translated


# Subject Position
person_questions_sp = generate_english_person_questions("PersonTotalPropertiesSP.txt")
translate_english_person_questions(person_questions_sp, "PersonQuestionsSP_AG.txt")

# Object Position
person_questions_op = generate_english_person_questions("PersonTotalPropertiesOP.txt")
translate_english_person_questions(person_questions_op, "PersonQuestionsOP_AG.txt")
