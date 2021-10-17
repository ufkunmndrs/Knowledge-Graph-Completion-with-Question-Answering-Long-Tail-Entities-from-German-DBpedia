import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import ast


persons_properties_file_sp = "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/" \
                          "PersonProperties/PersonPropertiesTXTFiles/PersonTotalPropertiesSP.txt"
with open(persons_properties_file_sp, encoding="utf-8") as f:
    full_property_list_sp = f.readlines()
    full_property_list_sp = [line.strip() for line in full_property_list_sp]
    full_property_list_sp = [ast.literal_eval(tup) for tup in full_property_list_sp]
    full_property_list_sp = [tup[0] for tup in full_property_list_sp]

persons_properties_file_op = "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/" \
                          "PersonProperties/PersonPropertiesTXTFiles/PersonTotalPropertiesOP.txt"
with open(persons_properties_file_op, encoding="utf-8") as f:
    full_property_list_op = f.readlines()
    full_property_list_op = [line.strip() for line in full_property_list_op]
    full_property_list_op = [ast.literal_eval(tup) for tup in full_property_list_op]
    full_property_list_op = [tup[0] for tup in full_property_list_op]


def load_persons_json(question_type: str, entity_position: str):
    """
    loads persons JSON file from the directory where it is stored
    Parameters
    ----------
    question_type: str
        Question type, can either be "AG", "BL", "NL"
    entity_position: str
        position of the entities, can either be "OP" or "SP"

    Returns
    -------
    json_dict_list: list
        A list of the persons dictionaries

    """
    persons_path = "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/Results/PersonsResults/" \
                   "PersonsResultsQuestions" + question_type + "/"
    persons_filename = "PersonsResults" + entity_position + "withQuestions" + question_type + "full.json"
    json_dict_list = []
    for line in open(os.path.join(persons_path, persons_filename), encoding="utf-8-sig"):
        json_dict_list.append(json.loads(line))
    return json_dict_list


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


def dict_to_list(dict_list: list):
    """
    transforms a nested dict into a list dataformat
    Parameters
    ----------
    dict_list: list
        list of dictionaries
    Returns
    -------
    nested_dict_list: list
        a list with the nested dicts as elements

    """
    nested_dict_list = [list(d_values(d, 1)) for d in dict_list]
    return nested_dict_list


def get_avg_property_score(nested_dict_list: list, property: str):
    """
    gets the average score for any given property
    Parameters
    ----------
    nested_dict_list: list
        a list of nested dictionaries
    property: str
        a property that belongs to the DBpedia class "Person"

    Returns
    -------
    avg_val, property: tuple
        A tuple where avg_val is the average value (float) and the property (str) that was passed as input

    """
    avg_val = 0
    for lst in nested_dict_list:
        for dctnry in lst:
            avg_val += dctnry[property].get("score")
    avg_val = round(avg_val / len(nested_dict_list), 2)
    return avg_val, property


def get_top_or_bottom_five(question_type: str, entity_position: str, top_or_bottom: str):
    """
    gets top or bottom five properties for "Person" DBpedia class
    Parameters
    ----------
    question_type: str
        The desired question type, can either be "AG", "BL", "NL"
    entity_position: str
        The desired entity position, can either be "SP" or "OP"
    top_or_bottom: str
        determines whether top or bottom 5 properties will be retrieved

    Returns
    -------
    final_result_list: list
        List of the properties ranked according to their average scores

    """
    persons_dicts_list = load_persons_json(question_type, entity_position)
    # noinspection PyTypeChecker
    persons_nested_dicts_to_list = dict_to_list(persons_dicts_list)
    property_avg_tuple_list = []
    if entity_position == "SP":
        # noinspection PyTypeChecker
        property_avg_tuple_list = [get_avg_property_score(persons_nested_dicts_to_list, prop) for
                                   prop in full_property_list_sp]
    elif entity_position == "OP":
        # noinspection PyTypeChecker
        property_avg_tuple_list = [get_avg_property_score(persons_nested_dicts_to_list, prop) for
                                   prop in full_property_list_op]
    final_result_list = sorted(property_avg_tuple_list, key=lambda tup: tup[0], reverse=True)
    if top_or_bottom == "top":
        return final_result_list[:5]
    elif top_or_bottom == "bottom":
        return final_result_list[-5:]


def plot_tuple_list(tuple_list: list, plot_title: str):
    """
    plots a list of tuples

    Parameters
    ----------
    tuple_list: list
        List containing tuples as elements
    plot_title: str
        title for the plot

    Returns
    -------

    """
    x_labels = [tup[1] for tup in tuple_list]
    y_labels = [tup[0] for tup in tuple_list]
    plt.figure()
    ax = pd.Series(y_labels).plot(kind='bar')
    ax.set_xticklabels(x_labels)
    plt.ylim(0, 1.0)
    plt.xticks(rotation=10)
    rects = ax.patches
    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
    plt.title(plot_title)
    plt.show()


def stats_to_txt(tuple_list: list, filename: str, question_type: str, entity_position: str):
    """

    Parameters
    ----------
    tuple_list: list
        List of tuples
    filename: str
        Intended filename
    question_type: str
        Question type for which the file will be created
    entity_position: str
        The position of the entities

    Returns
    -------

    """
    outputpath = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/PersonPropertiesStats/"
    tuple_list = [(tup[1], tup[0]) for tup in tuple_list]
    if question_type == "BL":
        if entity_position == "SP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Person Properties for Baseline Questions Subject Position (e, r, ?): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for Baseline Questions Subject Positions (e, r, ?): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))
        elif entity_position == "OP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Properties for Baseline Questions Object Position (?, r, e): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for Baseline Questions Object Positions (?, r, e): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))
    elif question_type == "AG":
        if entity_position == "SP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Person Properties for TB Questions Subject Position (e, r, ?): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for TB Questions Subject Positions (e, r, ?): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))
        elif entity_position == "OP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Properties for TB Questions Object Position (?, r, e): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for TB Questions Object Positions (?, r, e): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))
    elif question_type == "NL":
        if entity_position == "SP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Person Properties for Human-Generated Questions Subject Position (e, r, ?): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for Human-Generated Questions Subject Positions (e, r, ?): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))
        elif entity_position == "OP":
            with open(os.path.join(outputpath, filename), "w", encoding="utf-8") as f:
                f.write("Top 5 Properties for Human-Generated Questions Object Position (?, r, e): ")
                f.write("\n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[:5]))
                f.write("\n\n")
                f.write("Bottom 5 Person Properties for Human-Generated Questions Object Positions (?, r, e): \n")
                f.write('\n'.join('{}, avg. score: {}'.format(x[0], x[1]) for x in tuple_list[5:]))


# get top/bottom 5 for Baseline questions, first ssubject position, then object position and plot
top_five_sp_bl = get_top_or_bottom_five("BL", "SP", "top")
bottom_five_sp_bl = get_top_or_bottom_five("BL", "SP", "bottom")
joint_sp_bl_list = top_five_sp_bl + bottom_five_sp_bl
# plot_tuple_list(joint_sp_bl_list, "Top/Bottom 5 properties Baseline Questions Subject position: (e, r, ?)")
stats_to_txt(joint_sp_bl_list, "PersonBaselineStatsSP.txt", "BL", "SP")

top_five_sp_ag = get_top_or_bottom_five("AG", "SP", "top")
bottom_five_sp_ag = get_top_or_bottom_five("AG", "SP", "bottom")
joint_sp_ag_list = top_five_sp_ag + bottom_five_sp_ag
# plot_tuple_list(joint_sp_ag_list, "Top/Bottom 5 properties Translation-Based Questions Subject position: (e, r, ?)")
stats_to_txt(joint_sp_ag_list, "PersonTranslationBasedStatsSP.txt", "AG", "SP")

top_five_sp_nl = get_top_or_bottom_five("NL", "SP", "top")
bottom_five_sp_nl = get_top_or_bottom_five("NL", "SP", "bottom")
joint_sp_nl_list = top_five_sp_nl + bottom_five_sp_nl
# plot_tuple_list(joint_sp_nl_list, "Top/Bottom 5 properties Human-Generated Subject position: (e, r, ?)")
stats_to_txt(joint_sp_nl_list, "PersonHumanGeneratedStatsSP.txt", "NL", "SP")


# same for Object Position
top_five_op_bl = get_top_or_bottom_five("BL", "OP", "top")
bottom_five_op_bl = get_top_or_bottom_five("BL", "OP", "bottom")
joint_op_bl_list = top_five_op_bl + bottom_five_op_bl
plot_tuple_list(joint_op_bl_list, "Top/Bottom 5 properties Baseline Questions Object position: (?, r, e)")
stats_to_txt(joint_op_bl_list, "PersonBaselineStatsOP.txt", "BL", "OP")

top_five_op_ag = get_top_or_bottom_five("AG", "OP", "top")
bottom_five_op_ag = get_top_or_bottom_five("AG", "OP", "bottom")
joint_op_ag_list = top_five_op_ag + bottom_five_op_ag
plot_tuple_list(joint_op_ag_list, "Top/Bottom 5 properties Translation-Based Questions Object position: (?, r, e)")
stats_to_txt(joint_op_ag_list, "PersonTranslationBasedStatsOP.txt", "AG", "OP")

top_five_op_nl = get_top_or_bottom_five("NL", "OP", "top")
bottom_five_op_nl = get_top_or_bottom_five("NL", "OP", "bottom")
joint_op_nl_list = top_five_op_nl + bottom_five_op_nl
plot_tuple_list(joint_op_nl_list, "Top/Bottom 5 properties Human-Generated Questions Object position: (?, r, e)")
stats_to_txt(joint_op_nl_list, "PersonHumanGeneratedStatsOP.txt", "NL", "OP")
