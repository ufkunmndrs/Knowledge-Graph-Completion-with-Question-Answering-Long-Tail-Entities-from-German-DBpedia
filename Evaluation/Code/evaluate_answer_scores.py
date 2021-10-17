import json
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt


def load_json_dict(entity_type: str, question_type: str, entity_position: str, file_path="C:/Users/ubmen/Desktop/"
                                                                                         "BA_Prog/TripleExtraction/Results/"):
    """
    Loads dictionaries from the resulting .json files

    Parameters
    ----------
    entity_type: str
        Name/Type of the entity for which results will be loaded
    question_type: str
        Type of the question for which the results will be loaded
    entity_position: str
        position of the entity for which results will be loaded
    file_path: str
        filepath from where the results will be extracted.
        The default is: "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/Results/"

    Returns
    -------
    json_dict_list: list
        list of dictionaries from the .json result file

    """
    global json_filename
    valid_question_types = ["AG", "BL", "NL"]
    if question_type not in valid_question_types:
        raise ValueError("Incorrect input for question type!")
    other_entity_types = ["Building", "Disease", "History", "Literature", "Magazine", "Newspaper",
                          "Organization", "Park", "School", "Ship"]
    plural_entities = ["Building", "Disease", "Magazine", "Newspaper", "Organization", "Park", "School", "Ship"]
    if entity_type in other_entity_types and entity_type not in plural_entities:
        file_path += "OtherResults/" + entity_type + "Results/" + entity_type + "ResultsQuestions" + question_type + "/"
        json_filename = entity_type + "Results" + entity_position + "withQuestions" + question_type + ".json"
    elif entity_type in other_entity_types and entity_type in plural_entities:
        file_path += "OtherResults/" + entity_type + "sResults/" + entity_type + "sResultsQuestions" + question_type + "/"
        json_filename = entity_type + "sResults" + entity_position + "withQuestions" + question_type + ".json"
    elif entity_type == "Person":
        file_path += "PersonsResults/PersonsResultsQuestions" + question_type + "/"
        json_filename = "PersonsResults" + entity_position + "withQuestions" + question_type + "full.json"
    json_dict_list = []
    for line in open(os.path.join(file_path, json_filename), encoding="utf-8-sig"):
        json_dict_list.append(json.loads(line))
    return json_dict_list


# for j in json_dicts_list:
# print(pd.DataFrame(j))
def d_values(d, depth):
    """
    Extracts inner values of a nested dictionary
    Parameters
    ----------
    d: dict
        nested dict
    depth: int
        the depth of the nested dictionary whose values shall be extracted

    Returns
    -------
    i: dict
        nested value dictionary

    """
    if depth == 1:
        for i in d.values():
            yield i
    else:
        for v in d.values():
            if isinstance(v, dict):
                for i in d_values(v, depth - 1):
                    yield i


def dict_to_list(dict_list: list, question_type: str, entity_type: str):
    """

    Parameters
    ----------
    dict_list: list
        list of dictionaries
    question_type: str
        question type, can be "BL", "AG", "NL"
    entity_type: str
        specific entity type

    Returns
    -------

    """
    nested_dict_list = [list(d_values(d, 2)) for d in dict_list]
    score_list = []
    for elem in nested_dict_list:
        for dctnry in elem:
            score_list.append(dctnry["score"])
    result_list = [(score, question_type, entity_type) for score in score_list]
    return result_list


other_entities = ["Building", "Disease", "History", "Literature", "Magazine", "Newspaper", "Organization", "Park",
                  "School", "Ship"]


def list_to_dataframe(question_type: str, entity_position: str):
    """
    Combination of all the previous functions for "Other" --> takes question types and entity position as inputs
    and returns a dataframe containing all "Other" entities and all question_types

    Parameters
    ----------
    question_type: str
        Question type which will be loaded, cen either be "BL", "AG", "NL"
    entity_position: str
        position of the entity in a phrase, can either be "SP", "OG"

    Returns
    -------
    entity_df = DataFrame
        pandas dataframe containing score, question type and entity category

    """
    valid_question_types = ["BL", "NL", "AG"]
    if question_type not in valid_question_types:
        raise ValueError("Incorrect question type input")
    global formal_qt
    if question_type == "BL":
        formal_qt = "Baseline"
    elif question_type == "AG":
        formal_qt = "Translation-Based"
    elif question_type == "NL":
        formal_qt = "Human-Generated"
    question_type_dict_list = [load_json_dict(ent, question_type, entity_position) for ent in other_entities]
    result_list = []
    entity_result_joint_list = list(zip(other_entities, question_type_dict_list))
    for tup in entity_result_joint_list:
        # noinspection PyTypeChecker
        result_list.append(dict_to_list(tup[1], formal_qt, tup[0]))
    entity_df = pd.DataFrame([tup for lst in result_list for tup in lst],
                             columns=["Score", "Question Type", "Category"])
    return entity_df


if __name__ == "__main__":

    # Results for "Other" SP
    bl_sp_dataframe = list_to_dataframe("BL", "SP")
    ag_sp_dataframe = list_to_dataframe("AG", "SP")
    nl_sp_dataframe = list_to_dataframe("NL", "SP")
    sp_frames_other = [bl_sp_dataframe, ag_sp_dataframe, nl_sp_dataframe]
    sp_final_frame_other = pd.concat(sp_frames_other)
    csv_output_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    csv_filename = "OtherResultsSP.csv"
    sp_final_frame_other.to_csv(os.path.join(csv_output_path, csv_filename), encoding="utf-8-sig", index=False)
    sp_csv = pd.read_csv("C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles/OtherResultsSP.csv")
    ax1 = sns.boxplot(x=sp_csv["Category"], y=sp_csv["Score"], hue=sp_csv["Question Type"])
    ax1.set_title('Subject position scores "Other" based on question type: (e, r, ?)')
    plt.xticks(rotation=20)
    plt.legend(loc='lower right')
    plt.show()

    # Confidence Scores for "Other" OP
    bl_op_dataframe = list_to_dataframe("BL", "OP")
    ag_op_dataframe = list_to_dataframe("AG", "OP")
    nl_op_dataframe = list_to_dataframe("NL", "OP")
    op_frames_other = [bl_op_dataframe, ag_op_dataframe, nl_op_dataframe]
    op_final_frame_other = pd.concat(op_frames_other)
    csv_output_path_op = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    csv_filename_op = "OtherResultsOP.csv"
    op_final_frame_other.to_csv(os.path.join(csv_output_path_op, csv_filename_op), encoding="utf-8-sig", index=False)
    ax2 = sns.boxplot(x="Category", y="Score", hue="Question Type", data=op_final_frame_other)
    ax2.set_title('Object position scores "Other" based on question type: (?, r, e)')
    plt.xticks(rotation=20)
    plt.legend(loc='lower right')
    plt.show()

    persons_bl_sp_json = load_json_dict("Person", "BL", "SP")
    persons_ag_sp_json = load_json_dict("Person", "AG", "SP")
    persons_nl_sp_json = load_json_dict("Person", "NL", "SP")

    # noinspection PyTypeChecker
    persons_bl_sp_list = dict_to_list(persons_bl_sp_json, "Baseline", "Person")
    # noinspection PyTypeChecker
    persons_ag_sp_list = dict_to_list(persons_ag_sp_json, "Translation-Based", "Person")
    # noinspection PyTypeChecker
    persons_nl_sp_list = dict_to_list(persons_nl_sp_json, "Human-Generated", "Person")

    # Confidence Scores "Persons" SP
    entity_df_bl_sp = pd.DataFrame(persons_bl_sp_list, columns=["Score", "Question Type", "Category"])
    entity_df_ag_sp = pd.DataFrame(persons_ag_sp_list, columns=["Score", "Question Type", "Category"])
    entity_df_nl_sp = pd.DataFrame(persons_nl_sp_list, columns=["Score", "Question Type", "Category"])
    persons_sp_frames = [entity_df_bl_sp, entity_df_ag_sp, entity_df_nl_sp]
    persons_sp_final_frame = pd.concat(persons_sp_frames)
    persons_csv_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    persons_csv_filename = "PersonsResultsSP.csv"
    persons_sp_final_frame.to_csv(os.path.join(persons_csv_path, persons_csv_filename), encoding="utf-8-sig", index=False)
    ax3 = sns.boxplot(x="Category", y="Score", hue="Question Type", data=persons_sp_final_frame)
    ax3.set_title('Subject position scores "Person" based on question type: (e, r, ?)')
    plt.legend(loc='upper right')
    plt.show()

    # same for Object Position
    persons_bl_op_json = load_json_dict("Person", "BL", "OP")
    persons_ag_op_json = load_json_dict("Person", "AG", "OP")
    persons_nl_op_json = load_json_dict("Person", "NL", "OP")

    # noinspection PyTypeChecker
    persons_bl_op_list = dict_to_list(persons_bl_op_json, "Baseline", "Person")
    # noinspection PyTypeChecker
    persons_ag_op_list = dict_to_list(persons_ag_op_json, "Translation-Based", "Person")
    # noinspection PyTypeChecker
    persons_nl_op_list = dict_to_list(persons_nl_op_json, "Human-Generated", "Person")

    # Confidence Scores "Persons" OP
    entity_df_bl_op = pd.DataFrame(persons_bl_op_list, columns=["Score", "Question Type", "Category"])
    entity_df_ag_op = pd.DataFrame(persons_ag_op_list, columns=["Score", "Question Type", "Category"])
    entity_df_nl_op = pd.DataFrame(persons_nl_op_list, columns=["Score", "Question Type", "Category"])
    persons_op_frames = [entity_df_bl_op, entity_df_ag_op, entity_df_nl_op]
    persons_op_final_frame = pd.concat(persons_op_frames)
    persons_csv_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    persons_csv_filename_op = "PersonsResultsOP.csv"
    persons_op_final_frame.to_csv(os.path.join(persons_csv_path, persons_csv_filename_op), encoding="utf-8-sig", index=False)
    ax4 = sns.boxplot(x="Category", y="Score", hue="Question Type", data=persons_op_final_frame)
    ax4.set_title('Object position scores "Person" based on question type: (?, r, e)')
    plt.legend(loc='upper right')
    plt.show()

    # finally, plot everything to one plot for all categories
    sp_full_frame_list = [sp_final_frame_other, persons_sp_final_frame]
    sp_full_frame = pd.concat(sp_full_frame_list)
    csv_outputpath = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    sp_csv_full_filename = "AllResultsSP.csv"
    sp_full_frame.to_csv(os.path.join(csv_outputpath, sp_csv_full_filename), encoding="utf-8-sig", index=False)
    ax5 = sns.boxplot(x="Category", y="Score", hue="Question Type", data=sp_full_frame)
    ax5.set_title("Subject position scores based on question type: (e, r, ?)")
    plt.legend(loc="lower left")
    plt.xticks(rotation=20)
    plt.show()

    # same for object position
    op_full_frame_list = [op_final_frame_other, persons_op_final_frame]
    op_full_frame = pd.concat(op_full_frame_list)
    csv_outputpath = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CSVFiles"
    op_csv_full_filename = "AllResultsOP.csv"
    op_full_frame.to_csv(os.path.join(csv_outputpath, op_csv_full_filename), encoding="utf-8-sig", index=False)
    ax6 = sns.boxplot(x="Category", y="Score", hue="Question Type", data=op_full_frame)
    ax6.set_title("Object position scores based on question type: (?, r, e)")
    plt.legend(loc="lower left")
    plt.xticks(rotation=20)
    plt.show()
