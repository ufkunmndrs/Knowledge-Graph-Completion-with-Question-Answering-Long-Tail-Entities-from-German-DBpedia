import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_json_dicts(set_type: str, entity_position: str, question_type=None,
                    file_path="C:/Users/ubmen/Desktop/BA_Prog/Evaluation/"):
    """
    Loads dictionaries from the resulting .json files

    Parameters
    ----------
    set_type: str
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
    # noinspection PyGlobalUndefined
    global json_filename
    valid_question_types = ["AG", "BL", "NL", None]
    if question_type not in valid_question_types:
        raise ValueError("Incorrect input for question type!")
    set_type = set_type.lower()
    if set_type == "gold":
        json_filename = file_path + "GoldStandardFiles/JSONFiles/GoldStandard" + entity_position + ".json"
    elif set_type == "eval":
        json_filename = file_path + "EvalSetFiles/Questions" + question_type + "/EvalSet" + entity_position + question_type + ".json"
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


def entity_joint_system_gold_lists(entity_name: str, system_res_list: list, gold_dict_list: list,
                                   return_list_only=False):
    """
    maps system results and gold standard results together in a list of tuples for a a given entity
    Parameters
    ----------
    entity_name: str
        Name of the entity
    gold_dict_list: list
        List where the elements are the dictionaries from the gold standard
    system_res_list: list
        List where the elements are the dictionaries from the system results
    return_list_only: True/False
        determines whether only a list (True) or a tuple of entity and the joint system/gold list will be returned
        (False). The default is False.
    Returns
    -------
    entity_name, joint_system_gold_list: tuple
        First element is the name of the entity as str datatype, and the 2nd element of the tuple is the list
        system and gold standard output as yet another tuple, where the system answer output is the first element of the
        tuple as str, and the 2nd element is the list of gold standard answers
        it has the following form:
        (entity, [(system_answer, [gold_standard_answer(s)])])

    """
    entity_eval_dict = [d[entity_name] for d in system_res_list if entity_name in d][0]
    entity_gold_dict = [d[entity_name] for d in gold_dict_list if entity_name in d][0]
    entity_system_answer_dict = list(entity_eval_dict.items())
    entity_gold_answer_dict = list(entity_gold_dict.items())
    entity_system_answer_list = [tup[1]["answer"] for tup in entity_system_answer_dict]
    entity_gold_answer_list = [tup[1]["answer"] for tup in entity_gold_answer_dict]
    joint_system_gold_list = list(zip(entity_system_answer_list, entity_gold_answer_list))
    if return_list_only is True:
        return joint_system_gold_list
    else:
        return entity_name, joint_system_gold_list


def entity_precision(entity_name: str, joint_system_gold_list: list, return_score_only=False):
    """
    Computes the precision score for one entity given a list of tuples containing system and gold standard answers

    Parameters
    ----------
    entity_name: str
        Name of the entity for which the precision score will be computed
    joint_system_gold_list: list
        List with tuples as elements where the first element of the tuple is the system answer and the second element
        is the goldstandard answer
    return_score_only: bool
        Determines whether only the score or a tuple of entity_name and score will be returned
    Returns
    -------
    final_precision_score: float
        Precision score for the input entity
    """
    true_positives = 0
    false_positives = 0
    for ans in joint_system_gold_list:
        if ans[1][0] != "nan":
            if ans[0] in ans[1]:
                true_positives += 1
            else:
                false_positives += 1
    final_precision_score = round((true_positives / (true_positives + false_positives) * 100), 1)
    if return_score_only is True:
        return final_precision_score
    else:
        return entity_name, final_precision_score


def entity_recall(entity_name: str, joint_system_gold_list: list, return_score_only=False):
    """
    Computes the recall score for one entity given a list of tuples containing system and gold standard answers

    Parameters
    ----------
    entity_name: str
        Name of the entity for which the precision score will be computed
    joint_system_gold_list: list
        List with tuples as elements where the first element of the tuple is the system answer and the second element
        is the gold standard answer
    return_score_only: bool
        Determines whether only the score or a tuple of entity_name and score will be returned
    Returns
    -------
    final_precision_score: float
        Precision score for the input entity
    """
    true_positives = 0
    false_negatives = 0
    for ans in joint_system_gold_list:
        if ans[1][0] != "nan":
            if ans[0] in ans[1]:
                true_positives += 1
                if len(ans[1]) > 1:
                    false_negatives += len(ans[1]) - 1  # minus 1 for the one true positive
            else:
                false_negatives += len(ans[1])
    final_recall_score = round((true_positives / (true_positives + false_negatives) * 100), 1)
    if return_score_only is True:
        return final_recall_score
    else:
        return entity_name, final_recall_score


def entity_exact_match(entity_name: str, joint_system_gold_list: list, return_score_only=False):
    """
    computes the exact match rate

    Parameters
    ----------
    entity_name: str
        name of the respective entity for which exact match will be computed
    joint_system_gold_list: list
        list of tuples where 0th element is system answer and 1st element is list of gold standard answers
    return_score_only: bool
        determines whether only the score (True) will be returned.

    Returns
    -------

    """
    exact_matches = 0
    incorrect_matches = 0
    for ans in joint_system_gold_list:
        if ans[0] in ans[1]:
            exact_matches += 1
        else:
            incorrect_matches += 1
    exact_match_rate = round((exact_matches / len(joint_system_gold_list) * 100), 1)
    if return_score_only is True:
        return exact_match_rate
    else:
        return entity_name, exact_match_rate


def entity_f1_score(entity_name: str, joint_system_gold_list: list, return_score_only=False):
    """
    computes the f1 score for a list of tuples with entities as 0th element, and a tuple of system answers and
    gold standard answers as 2nd element

    Parameters
    ----------
    entity_name: str
        Name of the entity
    joint_system_gold_list: list
        List of tuples where the first element is the system answer and the 2nd element is a list of gold standard
        answers
    return_score_only: bool
        determines whether only the score itself (True) or a tuple of entity name and scores (False) will be returned.
        The default is False.

    Returns
    -------
    entity_name, f1: tuple
        a tuple of the input entity name and the corresponding f1 score.
        Setting "return_score_only" will only return the f1 score.
    """
    recall = entity_recall(entity_name, joint_system_gold_list)[1]  # first element respectively
    precision = entity_precision(entity_name, joint_system_gold_list)[1]  # as first elem is the score
    counter = precision * recall
    denom = precision + recall
    if denom != 0:
        f1 = round(2 * (counter / denom), 1)
    else:
        f1 = 0.0
    if return_score_only is True:
        return f1
    else:
        return entity_name, f1


def get_avg_metric_score(metric_type: str, entity_metric_score_list: list):
    """
    computes the average metric score for a list of entities and their respective scores for that given metric.

    Parameters
    ----------
    metric_type: str
        the desired metric type
    entity_metric_score_list: list
        a list of tuples where the 0th element is the entity as type str, and the 1st element is the metric score
        as type float

    Returns
    -------
    avg_metric_score: float
        the average score for the input metric
    """
    possible_metrics = ["precision", "recall", "exact match", "f1"]
    metric_type = metric_type.lower()
    if metric_type not in possible_metrics:
        raise ValueError("Incorrect metric type")
    # noinspection PyGlobalUndefined
    score_only_list = [ent[1] for ent in entity_metric_score_list]
    avg_metric_score = round((sum(score_only_list) / len(score_only_list)), 1)
    return avg_metric_score


def plot_averages(question_type_score_tuple_list: list, plot_title: str):
    """
    plots the average metric scores for any one of the given metrics above (Precision, Recall, Exact Match, F1)

    Parameters
    ----------
    question_type_score_tuple_list: list
        List of tuples where the 0th element is the name of question/approach type (i.e. Baseline, Translation-Based,
        Human-Generated) and 1st element is the average score of this question type for any given metric
    plot_title: str
        title of the plot

    Returns
    -------
    returns None, merely plots

    """
    question_type_score_tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    x_labels = [tup[0] for tup in question_type_score_tuple_list]
    y_labels = [tup[1] for tup in question_type_score_tuple_list]
    plt.figure()
    ax = pd.Series(y_labels).plot(kind='bar')
    ax.set_xticklabels(x_labels)
    plt.ylim(0, 100)
    plt.xticks(rotation=0)
    rects = ax.patches
    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha='center', va='bottom')
    plt.title(plot_title)
    plt.show()


# noinspection PyShadowingNames
def metric_stats_to_csv(bl_list: list, ag_list: list, nl_list: list, metric: str, entity_position: str,
                        path="C:/Users/ubmen/Desktop/BA_Prog/Evaluation/EvalResultsFiles/CSVFiles", return_df=False,
                        to_excel=False):
    """
    Creates a csv file to store the results of a metric for each entity

    Parameters
    ----------
    bl_list: list
        baseline list (list of tuples), 0th element name of entity (str), 1st element baseline score for that metric
        (float)
    ag_list: list
        translation-based list (list of tuples), 0th element name of the entity (str), 1st element translation-based
        score for the input metric
    nl_list: list
        human-generated list (list of tuples), 0th element name of the entity (str), 1st element human-generated
        questions score for the input metric (float)
    metric: str
        Type/name of the metric
    entity_position: str
        position of the entity (i.e. either OP/SP)
    path: str
        path where the file will be stored
    return_df: bool
        determines whether a pd.DataFrame object will be returned. The default is False.
    to_excel: bool
        determines whether a .xlsx file will be created. The default is False, which means that automatically a .csv
        file will be created

    Returns
    -------
    entity_score_df: pd.DataFrame
        a dataframe with Entity, Baseline, Translation-Based, Human-Generated metric scores as columns
        (i.e. the scores for any of those above metrics as row entries for any given entity in the evaluation set)
        Will only be returned if return_df is set to True.

    """
    valid_metrics = ["Precision", "Recall", "F1", "EM"]
    if metric not in valid_metrics:
        raise ValueError("invalid input metric")
    # sort entities in each list of tuples alphabetically to ensure that tuples are zipped correctly
    # and for better overview of the files
    bl_list.sort(key=lambda tup: tup[0])
    ag_list.sort(key=lambda tup: tup[0])
    nl_list.sort(key=lambda tup: tup[0])
    zipped_list = list(zip(bl_list, ag_list, nl_list))
    entity_scores_tuple_list = [(ent[0][0], ent[0][1], ent[1][1], ent[2][1]) for ent in zipped_list]
    # ent[0] = entity, ent[0][1] = Baseline score, ent[1][1] = tb score, ent[2][1]= hg score
    entity_score_df = pd.DataFrame(entity_scores_tuple_list, columns=["Entity", "Baseline " + metric,
                                                                      "Translation-Based " + metric,
                                                                      "Human-Generated " + metric])
    # noinspection PyGlobalUndefined
    path += "/CSVFiles" + entity_position + "/"
    filename = metric + entity_position
    if to_excel is True:
        filename += ".xlsx"
        entity_score_df.to_excel(os.path.join(path, filename), index=False, encoding="utf-ß-sig")
    else:
        filename += ".csv"
        entity_score_df.to_csv(os.path.join(path, filename), index=False, encoding="utf-8-sig")
    if return_df is True:
        return entity_score_df


def entity_score_tuple_list_to_txt(entity_score_tuple_list: list, filename: str, entity_position: str, metric_type: str,
                                   question_type: str, include_average=False, avg_score=None,
                                   path="C:/Users/ubmen/Desktop/BA_Prog/Evaluation/EvalResultsFiles"):
    """
    gets the list of entity and score and stores them to txt
    Parameters
    ----------
    entity_score_tuple_list: list
        list of tuples where the entity name is the first element and score the second element, one list for
        each question type
    filename: list
        intended filename
    entity_position: str
        position of the entity
    metric_type: str
        type of the metric
    question_type: str
        Type of the question (Baseline, Human-Generated, Translation-Based)
    include_average: bool
        determines whether the averages will be included
    avg_score: float:
        the average score (only necessary if include_average is set to True)
    path:
        path where the file will be stored

    Returns
    -------

    """
    valid_metrics = ["PRECISION", "RECALL", "F1", "EXACT MATCH"]
    metric_type = metric_type.upper()
    if metric_type not in valid_metrics:
        raise ValueError("Incorrect input metric")
    path += "/EvalResults" + question_type + "/EvalResults" + question_type + entity_position + "/" + filename + ".txt"
    # reorder list according to scores
    entity_score_tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    if question_type == "BL":
        if entity_position == "SP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(f"{metric_type} results for Subject Position with Baseline questions - (e, r, ?): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
        elif entity_position == "OP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(f"{metric_type} results for Object Position with Baseline questions - (?, r, e): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
    elif question_type == "AG":
        if entity_position == "SP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(f"{metric_type} results for Subject Position with Translation-Based questions - (e, r, ?): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
        elif entity_position == "OP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(
                    f"{metric_type} results for Object Position with Translation-Based questions - (?, r, e): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
    elif question_type == "NL":
        if entity_position == "SP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(
                    f"{metric_type} results for Subject Position with Human-Generated questions - (e, r, ?): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
        elif entity_position == "OP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(
                    f"{metric_type} results for Object Position with Human-Generated questions - (?, r, e): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()


# noinspection PyGlobalUndefined
def category_score_tuples(entity_category: str, entity_score_tuple_list: list, question_type: str):
    """
    creates tuples of where entities are replaced with their respective category (e.g. "Haus Fürsteneck" will be
    replaced by "Building") and the metric score for that entity
    Parameters
    ----------
    entity_category: str
        The category from the total set of categories in the research.
    entity_score_tuple_list: list
        a list of tuples where 0th element is the entity name (str) and 1st element is the corresponding metric score,
        regardless of the specific metric itself.
    question_type: str
        the corresponding question type (i.e. "BL", "AG", "NL")
    Returns
    -------
    cat_score_qt_tuples: list
        List of tuples where first element is the category and 2nd element is its metric score
    """
    # noinspection PyGlobalUndefined
    plural_entities = ["Building", "Disease", "Magazine", "Newspaper", "Organization", "Park", "School", "Ship",
                       "Person"]
    global csv_path
    if entity_category in plural_entities:
        entity_category += "s"
    global filename
    if "Person" != entity_category:
        csv_path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/OtherDetailed/"
        filename = entity_category + ".csv"
    elif entity_category == "Person":
        csv_path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/"
        filename = "Persons.csv"
    ent_df = pd.read_csv(os.path.join(csv_path, filename), encoding="utf-8-sig")
    entity_name_list = ent_df["Title"].to_list()
    category_score_tuple_list = [(entity_category, ent[0], ent[1]) for ent in entity_score_tuple_list if ent[0] in
                                 entity_name_list]
    scores_only = [ent[2] for ent in category_score_tuple_list]
    cat_score_qt_tuples = [(entity_category, score, question_type) for score in scores_only]
    return cat_score_qt_tuples


def cat_score_question_type_list_to_csv(bl_list: list, ag_list: list, nl_list: list, metric: str,
                                        entity_position: str, return_df=False):
    """
    creates a pd.Dataframe object and stores category, their score, and question type to a csv file

    Parameters
    ----------
    bl_list: list
        List of tuples where 0th element is a category (str) and 1st element is the corresponding metric score
        for that category (float) for BASELINE questions
    ag_list: list
        List of tuples where 0th element is a category (str) and 1st element is the corresponding metric score
        for that category (float) for TRANSLATION-BASED questions
    nl_list: list
        List of tuples where 0th element is a category (str) and 1st element is the corresponding metric score
        for that category (float) for HUMAN-GENERATED questions
    metric: str
        The metric for which the scores in the lists will be stored
    entity_position: str
        position of the entities
    return_df: bool
        determines whether pd.DataFrame object will be returned. The default is False; if set to True,
        an object will be returned
    Returns
    -------
    flattened_tuple_df: pd.DataFrame
        A pandas Dataframe containing the input information
    """
    csv_save_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/CategoryMetricScores/CategoryMetricScores" + entity_position + "/"
    metric = metric.capitalize()
    csv_filename = metric + "CategoryScores" + entity_position + ".csv"
    joint_qt_list = bl_list + ag_list + nl_list
    flattened_tuple_df = pd.DataFrame([tup for lst in joint_qt_list for tup in lst],
                                      columns=["Category", "Score", "Question Type"])
    flattened_tuple_df.to_csv(os.path.join(csv_save_path, csv_filename), encoding="utf-8-sig", index=False)
    if return_df is True:
        return flattened_tuple_df


def category_score_boxplot(metric: str, entity_position: str, return_df=False):
    """
    Retrieves category scores from the corresponding csv files and plots to a seaborn boxplot which shows
    the ranges and median of the input metric for each category

    Parameters
    ----------
    metric: str
        Metric for which the performance will be plotted to the boxplot
    entity_position: str
        position of the entity
    return_df: bool
        determines whether a pd.DataFrame object will containing the data from the csv file will be returned.
        The default is False since this would only make sense for testing.
    Returns
    -------
    category_score_qt_df: pd.DataFrame object
        A pandas DataFrame object containing the data from the csv file.
    """
    metric = metric.capitalize()
    csv_ret_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/" \
                   "CategoryMetricScores/CategoryMetricScores" + entity_position + "/"
    filename_ret = metric + "CategoryScores" + entity_position + ".csv"
    category_score_qt_df = pd.read_csv(os.path.join(csv_ret_path, filename_ret), encoding="utf-8-sig")
    ax = sns.boxplot(x="Category", y="Score", hue="Question Type", data=category_score_qt_df)
    if entity_position == "SP":
        ax.set_title(f"Subject position {metric} scores based on question type - (e, r, ?)")
    else:
        ax.set_title(f"Object position {metric} scores based on question type - (?, r, e)")
    plt.xticks(rotation=20)
    plt.legend(loc='upper right')
    plt.show()
    if return_df is True:
        return category_score_qt_df


if __name__ == "__main__":
    # evaluation of all metrics, first for SP
    gs_dict_list_sp = load_json_dicts("gold", "SP")
    all_eval_entities = list(set([key for d in gs_dict_list_sp for key in d]))  # all entities
    system_result_list_sp_bl = load_json_dicts("eval", "SP", "BL")
    system_result_list_sp_ag = load_json_dicts("eval", "SP", "AG")
    system_result_list_sp_nl = load_json_dicts("eval", "SP", "NL")
    # noinspection PyTypeChecker
    entity_system_gold_tuple_list_sp_bl = [
        entity_joint_system_gold_lists(ent, system_result_list_sp_bl, gs_dict_list_sp)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    entity_system_gold_tuple_list_sp_ag = [
        entity_joint_system_gold_lists(ent, system_result_list_sp_ag, gs_dict_list_sp)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    entity_system_gold_tuple_list_sp_nl = [
        entity_joint_system_gold_lists(ent, system_result_list_sp_nl, gs_dict_list_sp)
        for ent in all_eval_entities]

    # Computing the metrics for each and writing them to text files
    # precision scores for SP
    precisions_sp_bl = [entity_precision(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_bl]
    avg_precision_sp_bl = get_avg_metric_score("precision", precisions_sp_bl)
    entity_score_tuple_list_to_txt(precisions_sp_bl, "PrecisionResultBLSP", "SP", "precision", "BL",
                                   include_average=True, avg_score=avg_precision_sp_bl)
    avg_precision_sp_bl_tup = ("BL", avg_precision_sp_bl)

    precisions_sp_ag = [entity_precision(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_ag]
    avg_precision_sp_ag = get_avg_metric_score("precision", precisions_sp_ag)
    entity_score_tuple_list_to_txt(precisions_sp_ag, "PrecisionResultAGSP", "SP", "precision", "AG",
                                   include_average=True, avg_score=avg_precision_sp_ag)
    avg_precision_sp_ag_tup = ("TB", avg_precision_sp_ag)

    precisions_sp_nl = [entity_precision(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_nl]
    avg_precision_sp_nl = get_avg_metric_score("precision", precisions_sp_nl)
    entity_score_tuple_list_to_txt(precisions_sp_nl, "PrecisionResultNLSP", "SP", "precision", "NL",
                                   include_average=True, avg_score=avg_precision_sp_nl)
    avg_precision_sp_nl_tup = ("HG", avg_precision_sp_nl)
    sp_precision_averages = [avg_precision_sp_bl_tup, avg_precision_sp_ag_tup, avg_precision_sp_nl_tup]
    plot_averages(sp_precision_averages, "Precision Averages for Subject Position - (e, r, ?)")
    metric_stats_to_csv(precisions_sp_bl, precisions_sp_ag, precisions_sp_nl, "Precision", "SP")
    metric_stats_to_csv(precisions_sp_bl, precisions_sp_ag, precisions_sp_nl, "Precision", "SP", to_excel=True)

    # recall scores for SP
    recalls_sp_bl = [entity_recall(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_bl]
    avg_recall_sp_bl = get_avg_metric_score("recall", recalls_sp_bl)
    entity_score_tuple_list_to_txt(recalls_sp_bl, "RecallResultBLSP", "SP", "recall", "BL", include_average=True,
                                   avg_score=avg_recall_sp_bl)
    avg_recall_sp_bl_tup = ("Baseline", avg_recall_sp_bl)

    recalls_sp_ag = [entity_recall(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_ag]
    avg_recall_sp_ag = get_avg_metric_score("recall", recalls_sp_ag)
    entity_score_tuple_list_to_txt(recalls_sp_ag, "RecallResultAGSP", "SP", "recall", "AG", include_average=True,
                                   avg_score=avg_recall_sp_ag)
    avg_recall_sp_ag_tup = ("Translation-Based", avg_recall_sp_ag)

    recalls_sp_nl = [entity_recall(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_nl]
    avg_recall_sp_nl = get_avg_metric_score("recall", recalls_sp_nl)
    entity_score_tuple_list_to_txt(recalls_sp_bl, "RecallResultNLSP", "SP", "recall", "NL", include_average=True,
                                   avg_score=avg_recall_sp_nl)
    avg_recall_sp_nl_tup = ("Human-Generated", avg_recall_sp_nl)
    sp_recall_averages = [avg_recall_sp_bl_tup, avg_recall_sp_ag_tup, avg_recall_sp_nl_tup]
    plot_averages(sp_recall_averages, "Recall averages for Subject position - (e, r, ?)")
    metric_stats_to_csv(recalls_sp_bl, recalls_sp_ag, recalls_sp_nl, "Recall", "SP")
    metric_stats_to_csv(recalls_sp_bl, recalls_sp_ag, recalls_sp_nl, "Recall", "SP", to_excel=True)

    # f1 scores for SP
    f1_scores_sp_bl = [entity_f1_score(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_bl]
    avg_f1_score_sp_bl = get_avg_metric_score("f1", f1_scores_sp_bl)
    entity_score_tuple_list_to_txt(f1_scores_sp_bl, "F1ResultBLSP", "SP", "f1", "BL", include_average=True,
                                   avg_score=avg_f1_score_sp_bl)
    avg_f1_score_sp_bl_tup = ("Baseline", avg_f1_score_sp_bl)

    f1_scores_sp_ag = [entity_f1_score(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_ag]
    avg_f1_score_sp_ag = get_avg_metric_score("f1", f1_scores_sp_ag)
    entity_score_tuple_list_to_txt(f1_scores_sp_ag, "F1ResultAGSP", "SP", "f1", "AG", include_average=True,
                                   avg_score=avg_f1_score_sp_ag)
    avg_f1_score_sp_ag_tup = ("Translation-Based", avg_f1_score_sp_ag)

    f1_scores_sp_nl = [entity_f1_score(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_nl]
    avg_f1_score_sp_nl = get_avg_metric_score("f1", f1_scores_sp_nl)
    entity_score_tuple_list_to_txt(f1_scores_sp_nl, "F1ResultNLSP", "SP", "f1", "NL", include_average=True,
                                   avg_score=avg_f1_score_sp_nl)
    avg_f1_score_sp_nl_tup = ("Human-Genereated", avg_f1_score_sp_nl)
    sp_f1_averages = [avg_f1_score_sp_bl_tup, avg_f1_score_sp_ag_tup, avg_f1_score_sp_nl_tup]
    plot_averages(sp_f1_averages, "F1 Score averages for Subject Position - (e, r, ?)")
    metric_stats_to_csv(f1_scores_sp_bl, f1_scores_sp_ag, f1_scores_sp_nl, "F1", "SP")
    metric_stats_to_csv(f1_scores_sp_bl, f1_scores_sp_ag, f1_scores_sp_nl, "F1", "SP", to_excel=True)

    # exact matches for SP
    em_scores_sp_bl = [entity_exact_match(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_bl]
    avg_em_score_sp_bl = get_avg_metric_score("exact match", em_scores_sp_bl)
    entity_score_tuple_list_to_txt(em_scores_sp_bl, "ExactMatchBLSP", "SP", "exact match", "BL", include_average=True,
                                   avg_score=avg_em_score_sp_bl)
    avg_em_score_sp_bl_tup = ("Baseline", avg_em_score_sp_bl)

    em_scores_sp_ag = [entity_exact_match(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_ag]
    avg_em_score_sp_ag = get_avg_metric_score("exact match", em_scores_sp_ag)
    entity_score_tuple_list_to_txt(em_scores_sp_ag, "ExactMatchAGSP", "SP", "exact match", "AG", include_average=True,
                                   avg_score=avg_em_score_sp_ag)
    avg_em_score_sp_ag_tup = ("Translation-Based", avg_em_score_sp_ag)

    em_scores_sp_nl = [entity_exact_match(ent[0], ent[1]) for ent in entity_system_gold_tuple_list_sp_nl]
    avg_em_score_sp_nl = get_avg_metric_score("exact match", em_scores_sp_nl)
    entity_score_tuple_list_to_txt(em_scores_sp_nl, "ExactMatchNLSP", "SP", "exact match", "NL", include_average=True,
                                   avg_score=avg_em_score_sp_nl)
    avg_em_score_sp_nl_tup = ("Translation-Based", avg_em_score_sp_nl)
    sp_em_score_averages = [avg_em_score_sp_bl_tup, avg_em_score_sp_ag_tup, avg_em_score_sp_nl_tup]
    plot_averages(sp_em_score_averages, "Exact match averages for Subject Position - (e, r, ?)")
    metric_stats_to_csv(em_scores_sp_bl, em_scores_sp_ag, em_scores_sp_nl, "EM", "SP")
    metric_stats_to_csv(em_scores_sp_bl, em_scores_sp_ag, em_scores_sp_nl, "EM", "SP", to_excel=True)

    # Boxplot Precision SP
    category_list = ["Person", "Building", "Disease", "History", "Literature", "Magazine", "Newspaper",
                     "Organization", "Park", "School", "Ship"]
    bl_list_category_precision_sp = [category_score_tuples(ent, precisions_sp_bl, "Baseline") for ent in category_list]
    ag_list_category_precision_sp = [category_score_tuples(ent, precisions_sp_ag, "Translation-Based") for ent in category_list]
    nl_list_category_precision_sp = [category_score_tuples(ent, precisions_sp_nl, "Human-Generated") for ent in category_list]
    joint_list_precision_sp = cat_score_question_type_list_to_csv(bl_list_category_precision_sp, ag_list_category_precision_sp,
                                                                  nl_list_category_precision_sp, "Precision", "SP")
    category_score_boxplot("Precision", "SP")

    # Boxplot Recall SP
    bl_list_category_recall_sp = [category_score_tuples(ent, recalls_sp_bl, "Baseline") for ent in category_list]
    ag_list_category_recall_sp = [category_score_tuples(ent, recalls_sp_ag, "Translation-Based") for ent in category_list]
    nl_list_category_recall_sp = [category_score_tuples(ent, recalls_sp_nl, "Human-Generated") for ent in category_list]
    joint_list_recalls_sp = cat_score_question_type_list_to_csv(bl_list_category_recall_sp, ag_list_category_recall_sp,
                                                                nl_list_category_recall_sp, "Recall", "SP")
    category_score_boxplot("Recall", "SP")

    # Boxplot F1 SP
    bl_list_category_f1_sp = [category_score_tuples(ent, f1_scores_sp_bl, "Baseline") for ent in category_list]
    ag_list_category_f1_sp = [category_score_tuples(ent, f1_scores_sp_ag, "Translation-Based") for ent in category_list]
    nl_list_category_f1_sp = [category_score_tuples(ent, f1_scores_sp_nl, "Human-Generated") for ent in category_list]
    joint_list_f1_sp = cat_score_question_type_list_to_csv(bl_list_category_f1_sp, ag_list_category_f1_sp,
                                                           nl_list_category_f1_sp, "F1-Score", "SP")
    category_score_boxplot("F1-Score", "SP")

    # Boxplot Exact Match SP
    bl_list_category_em_sp = [category_score_tuples(ent, em_scores_sp_bl, "Baseline") for ent in category_list]
    ag_list_category_em_sp = [category_score_tuples(ent, em_scores_sp_ag, "Translation-Based") for ent in category_list]
    nl_list_category_em_sp = [category_score_tuples(ent, em_scores_sp_nl, "Human-Generated") for ent in category_list]
    joint_list_sp_em_sp = cat_score_question_type_list_to_csv(bl_list_category_em_sp, ag_list_category_em_sp,
                                                              nl_list_category_em_sp, "Exact Match", "SP")
    category_score_boxplot("Exact Match", "SP")

    ####################################################################################################################
    # evaluation of all metrics for Object Position (OP)
    ####################################################################################################################

    gs_dict_list_op = load_json_dicts("gold", "OP")
    system_result_list_op_bl = load_json_dicts("eval", "OP", "BL")
    system_result_list_op_ag = load_json_dicts("eval", "OP", "AG")
    system_result_list_op_nl = load_json_dicts("eval", "OP", "NL")

    # noinspection PyTypeChecker
    entity_gold_system_tuple_list_op_bl = [
        entity_joint_system_gold_lists(ent, system_result_list_op_bl, gs_dict_list_op)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    entity_gold_system_tuple_list_op_ag = [
        entity_joint_system_gold_lists(ent, system_result_list_op_ag, gs_dict_list_op)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    entity_gold_system_tuple_list_op_nl = [
        entity_joint_system_gold_lists(ent, system_result_list_op_nl, gs_dict_list_op)
        for ent in all_eval_entities]

    # precision scores for OP
    precisions_op_bl = [entity_precision(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_bl]
    avg_precision_op_bl = get_avg_metric_score("precision", precisions_op_bl)
    entity_score_tuple_list_to_txt(precisions_op_bl, "PrecisionResultBLOP", "OP", "precision", "BL",
                                   include_average=True, avg_score=avg_precision_op_bl)
    avg_precision_op_bl_tup = ("Baseline", avg_precision_op_bl)

    precisions_op_ag = [entity_precision(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_ag]
    avg_precision_op_ag = get_avg_metric_score("precision", precisions_op_ag)
    entity_score_tuple_list_to_txt(precisions_op_ag, "PrecisionResultAGOP", "OP", "precision", "AG",
                                   include_average=True, avg_score=avg_precision_op_ag)
    avg_precision_op_ag_tup = ("Translation-Based", avg_precision_op_ag)

    precisions_op_nl = [entity_precision(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_nl]
    avg_precision_op_nl = get_avg_metric_score("precision", precisions_op_nl)
    entity_score_tuple_list_to_txt(precisions_op_nl, "PrecisionResultNLOP", "OP", "precision", "NL",
                                   include_average=True, avg_score=avg_precision_op_nl)
    avg_precision_op_nl_tup = ("Human-Generated", avg_precision_op_nl)
    op_precision_averages = [avg_precision_op_bl_tup, avg_precision_op_ag_tup, avg_precision_op_nl_tup]
    plot_averages(op_precision_averages, "Precision averages for Object position - (?, r, e)")
    metric_stats_to_csv(precisions_op_bl, precisions_op_ag, precisions_op_nl, "Precision", "OP")
    metric_stats_to_csv(precisions_op_bl, precisions_op_ag, precisions_op_nl, "Precision", "OP", to_excel=True)

    # recall scores for OP
    recalls_op_bl = [entity_recall(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_bl]
    avg_recall_op_bl = get_avg_metric_score("recall", recalls_op_bl)
    entity_score_tuple_list_to_txt(recalls_op_bl, "RecallResultBLOP", "OP", "recall", "BL", include_average=True,
                                   avg_score=avg_recall_op_bl)
    avg_recall_op_bl_tup = ("Baseline", avg_recall_op_bl)

    recalls_op_ag = [entity_recall(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_ag]
    avg_recall_op_ag = get_avg_metric_score("recall", recalls_op_ag)
    entity_score_tuple_list_to_txt(recalls_op_ag, "RecallResultAGOP", "OP", "recall", "AG", include_average=True,
                                   avg_score=avg_recall_op_ag)
    avg_recall_op_ag_tup = ("Translation-Based", avg_recall_op_ag)

    recalls_op_nl = [entity_recall(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_nl]
    avg_recall_op_nl = get_avg_metric_score("recall", recalls_op_nl)
    entity_score_tuple_list_to_txt(recalls_op_bl, "RecallResultNLOP", "OP", "recall", "NL", include_average=True,
                                   avg_score=avg_recall_op_nl)
    avg_recall_op_nl_tup = ("Human-Generated", avg_recall_op_nl)
    op_recall_averages = [avg_recall_op_bl_tup, avg_recall_op_ag_tup, avg_recall_op_nl_tup]
    plot_averages(op_recall_averages, "Recall averages for Object Position - (?, r, e)")
    metric_stats_to_csv(recalls_op_bl, recalls_op_ag, recalls_op_nl, "Recall", "OP")
    metric_stats_to_csv(recalls_op_bl, recalls_op_ag, recalls_op_nl, "Recall", "OP", to_excel=True)

    # f1 scores for OP
    f1_scores_op_bl = [entity_f1_score(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_bl]
    avg_f1_score_op_bl = get_avg_metric_score("f1", f1_scores_op_bl)
    entity_score_tuple_list_to_txt(f1_scores_op_bl, "F1ResultBLOP", "OP", "f1", "BL", include_average=True,
                                   avg_score=avg_f1_score_op_bl)
    avg_f1_score_op_bl_tup = ("Baseline", avg_f1_score_op_bl)

    f1_scores_op_ag = [entity_f1_score(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_ag]
    avg_f1_score_op_ag = get_avg_metric_score("f1", f1_scores_op_ag)
    entity_score_tuple_list_to_txt(f1_scores_op_ag, "F1ResultAGOP", "OP", "f1", "AG", include_average=True,
                                   avg_score=avg_f1_score_op_ag)
    avg_f1_score_op_ag_tup = ("Translation-Based", avg_f1_score_op_ag)

    f1_scores_op_nl = [entity_f1_score(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_nl]
    avg_f1_score_op_nl = get_avg_metric_score("f1", f1_scores_op_nl)
    entity_score_tuple_list_to_txt(f1_scores_op_nl, "F1ResultNLOP", "OP", "f1", "NL", include_average=True,
                                   avg_score=avg_f1_score_op_nl)
    avg_f1_score_op_nl_tup = ("Human-Generated", avg_f1_score_op_nl)
    op_f1_score_averages = [avg_f1_score_op_bl_tup, avg_f1_score_op_ag_tup, avg_f1_score_op_nl_tup]
    plot_averages(op_f1_score_averages, "F1 Score averages for Object position - (?, r, e)")
    metric_stats_to_csv(f1_scores_op_bl, f1_scores_op_ag, f1_scores_op_nl, "F1", "OP")
    metric_stats_to_csv(f1_scores_op_bl, f1_scores_op_ag, f1_scores_op_nl, "F1", "OP", to_excel=True)

    # exact matches for OP
    em_scores_op_bl = [entity_exact_match(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_bl]
    avg_em_score_op_bl = get_avg_metric_score("exact match", em_scores_op_bl)
    entity_score_tuple_list_to_txt(em_scores_op_bl, "ExactMatchBLOP", "OP", "exact match", "BL", include_average=True,
                                   avg_score=avg_em_score_op_bl)
    avg_em_score_op_bl_tup = ("Baseline", avg_em_score_op_bl)

    em_scores_op_ag = [entity_exact_match(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_ag]
    avg_em_score_op_ag = get_avg_metric_score("exact match", em_scores_op_ag)
    entity_score_tuple_list_to_txt(em_scores_op_ag, "ExactMatchAGOP", "OP", "exact match", "AG", include_average=True,
                                   avg_score=avg_em_score_op_ag)
    avg_em_score_op_ag_tup = ("Translation-Based", avg_em_score_op_ag)

    em_scores_op_nl = [entity_exact_match(ent[0], ent[1]) for ent in entity_gold_system_tuple_list_op_nl]
    avg_em_score_op_nl = get_avg_metric_score("exact match", em_scores_op_nl)
    entity_score_tuple_list_to_txt(em_scores_op_nl, "ExactMatchNLOP", "OP", "exact match", "NL", include_average=True,
                                   avg_score=avg_em_score_op_nl)
    avg_em_score_op_nl_tup = ("Human-Generated", avg_em_score_op_nl)
    op_em_score_averages = [avg_em_score_op_bl_tup, avg_em_score_op_nl_tup, avg_em_score_op_ag_tup]
    plot_averages(op_em_score_averages, "Exact match averages for Object Position - (?, r, e)")
    metric_stats_to_csv(em_scores_op_bl, em_scores_op_ag, em_scores_op_nl, "EM", "OP")
    metric_stats_to_csv(em_scores_op_bl, em_scores_op_ag, em_scores_op_nl, "EM", "OP", to_excel=True)

    # Boxplot precision OP
    bl_list_category_precision_op = [category_score_tuples(ent, precisions_op_bl, "Baseline") for ent in category_list]
    ag_list_category_precision_op = [category_score_tuples(ent, precisions_op_ag, "Translation-Based") for ent in
                                     category_list]
    nl_list_category_precision_op = [category_score_tuples(ent, precisions_op_nl, "Human-Generated") for ent in
                                     category_list]
    joint_list_precision_op = cat_score_question_type_list_to_csv(bl_list_category_precision_op,
                                                                  ag_list_category_precision_op,
                                                                  nl_list_category_precision_op, "Precision", "OP")
    category_score_boxplot("Precision", "OP")

    # Boxplot Recall OP
    bl_list_category_recall_op = [category_score_tuples(ent, recalls_op_bl, "Baseline") for ent in category_list]
    ag_list_category_recall_op = [category_score_tuples(ent, recalls_op_ag, "Translation-Based") for ent in
                                  category_list]
    nl_list_category_recall_op = [category_score_tuples(ent, recalls_op_nl, "Human-Generated") for ent in category_list]
    joint_list_recalls_op = cat_score_question_type_list_to_csv(bl_list_category_recall_op,
                                                                ag_list_category_recall_op,
                                                                nl_list_category_recall_op, "Recall", "OP")
    category_score_boxplot("Recall", "OP")

    # Boxplot F1 OP
    bl_list_category_f1_op = [category_score_tuples(ent, f1_scores_op_bl, "Baseline") for ent in category_list]
    ag_list_category_f1_op = [category_score_tuples(ent, f1_scores_op_ag, "Translation-Based") for ent in category_list]
    nl_list_category_f1_op = [category_score_tuples(ent, f1_scores_op_nl, "Human-Generated") for ent in category_list]
    joint_list_f1_op = cat_score_question_type_list_to_csv(bl_list_category_f1_op, ag_list_category_f1_op,
                                                           nl_list_category_f1_op, "F1-Score", "OP")
    category_score_boxplot("F1-Score", "OP")

    # Boxplot Exact Match OP
    bl_list_category_em_op = [category_score_tuples(ent, em_scores_op_bl, "Baseline") for ent in category_list]
    ag_list_category_em_op = [category_score_tuples(ent, em_scores_op_ag, "Translation-Based") for ent in category_list]
    nl_list_category_em_op = [category_score_tuples(ent, em_scores_op_nl, "Human-Generated") for ent in category_list]
    joint_list_em_op = cat_score_question_type_list_to_csv(bl_list_category_em_op, ag_list_category_em_op,
                                                           nl_list_category_em_op, "Exact Match", "OP")
    category_score_boxplot("Exact Match", "OP")
