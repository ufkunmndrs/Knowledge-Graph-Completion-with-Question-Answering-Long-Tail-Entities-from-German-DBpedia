from evaluate_answers import load_json_dicts, get_avg_metric_score, plot_averages
import os
import pandas as pd


def entity_score_system_gold_tuple_lists(entity_name: str, system_res_list: list, gold_dict_list: list,
                                         return_list_only=False):
    """
    maps system results, their scores and gold standard results together in a list of tuples for a a given entity
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
    entity_name, joint_system_score_gold_list: tuple
        Tuple where the 0th element is the entity name (str), and the 1st element is a list of list of tuples where
        0th element is the system answer (for the property at that position), 1st element is the score for that answer,
        and 2nd element is the gold standard answer

    """
    entity_gold_dict = [d[entity_name] for d in gold_dict_list if entity_name in d][0]
    entity_eval_dict = [d[entity_name] for d in system_res_list if entity_name in d][0]
    entity_gold_answer_dict = list(entity_gold_dict.items())
    entity_system_answer_dict = list(entity_eval_dict.items())
    entity_gold_answer_list = [tup[1]["answer"] for tup in entity_gold_answer_dict]
    entity_system_answer_list = [(tup[1]["answer"], tup[1]["score"]) for tup in entity_system_answer_dict]
    joint_system_gold_list = list(zip(entity_system_answer_list, entity_gold_answer_list))
    joint_system_score_gold_list = [(ent[0][0], ent[0][1], ent[1]) for ent in joint_system_gold_list]
    if return_list_only is True:
        return joint_system_score_gold_list
    else:
        return entity_name, joint_system_score_gold_list


def threshold_entity_precision(entity_name: str, joint_system_gold_list: list, threshold: float,
                               return_score_only=False):
    """
    Computes the precision score for one entity given a list of tuples containing system and gold standard answers

    Parameters
    ----------
    entity_name: str
        Name of the entity for which the precision score will be computed
    joint_system_gold_list: list
        List with tuples as elements where the first element of the tuple is the system answer and the second element
        is the gold standard answer
    threshold: float
        Threshold for the answer scores
    return_score_only: bool
        Determines whether only the score or a tuple of entity_name and score will be returned
    Returns
    -------
    final_precision_score: float
        Precision score for the input entity
    """
    if threshold >= 1.0 or threshold <= 0:
        raise ValueError("Incorrect threshold input: must be a float value lower than 1.0 or higher than 0.0")
    true_positives = 0
    false_positives = 0
    for ans in joint_system_gold_list:
        if ans[2][0] != "nan" and ans[1] >= threshold:
            if ans[0] in ans[2]:
                true_positives += 1
            else:
                false_positives += 1
    denom = true_positives + false_positives
    if denom != 0:
        final_precision_score = round(((true_positives / denom) * 100), 1)
    else:
        final_precision_score = 0.0
    if return_score_only is True:
        return final_precision_score
    else:
        return entity_name, final_precision_score


def threshold_entity_recall(entity_name: str, joint_system_gold_list: list, threshold: float, return_score_only=False):
    """
    Computes the recall score for one entity given a list of tuples containing system and gold standard answers

    Parameters
    ----------
    entity_name: str
        Name of the entity for which the precision score will be computed
    joint_system_gold_list: list
        List with tuples as elements where the first element of the tuple is the system answer and the second element
        is the gold standard answer
    threshold: float
        Threshold for the answer scores
    return_score_only: bool
        Determines whether only the score or a tuple of entity_name and score will be returned
    Returns
    -------

    """
    if threshold >= 1.0 or threshold <= 0:
        raise ValueError("Incorrect threshold input: must be a float value lower than 1.0 or higher than 0.0")
    true_positives = 0
    false_negatives = 0
    for ans in joint_system_gold_list:
        if ans[2][0] != "nan" and ans[1] >= threshold:
            if ans[0] in ans[2]:
                true_positives += 1
                if len(ans[2]) > 1:
                    false_negatives += len(ans[2]) - 1  # minus 1 for the one true positive
            else:
                false_negatives += len(ans[2])
    denom = true_positives + false_negatives
    if denom != 0:
        final_recall_score = round(((true_positives / (true_positives + false_negatives)) * 100), 1)
    else:
        final_recall_score = 0.0
    if return_score_only is True:
        return final_recall_score
    else:
        return entity_name, final_recall_score


def threshold_entity_f1_score(entity_name: str, joint_system_gold_list: list, threshold: float,
                              return_score_only=False):
    """
    Computes the f1 score for a given input entity

     Parameters
    ----------
    entity_name: str
        Name of the entity
    joint_system_gold_list: list
        List of tuples where the first element is the system answer and the 2nd element is a list of gold standard
        answers
    threshold: float
        Threshold for the answer scores
    return_score_only: bool
        determines whether only the score itself (True) or a tuple of entity name and scores (False) will be returned.
        The default is False.

    Returns
    -------
    entity_name, f1: tuple
        a tuple of the input entity name and the corresponding f1 score.
        Setting "return_score_only" will only return the f1 score

    """
    if threshold >= 1 or threshold <= 0:
        raise ValueError("Incorrect threshold value: must be a float higher than 0.0 and lower than 1.0")
    recall = threshold_entity_recall(entity_name, joint_system_gold_list, threshold)[1]  # first element respectively
    precision = threshold_entity_precision(entity_name, joint_system_gold_list, threshold)[
        1]  # as first elem is the score
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


def threshold_exact_match(entity_name: str, joint_system_gold_list: list, threshold: float, return_score_only=False):
    """
    computes the exact match rate

    Parameters
    ----------
    entity_name: str
        name of the respective entity for which exact match will be computed
    joint_system_gold_list: list
        list of tuples where 0th element is system answer and 1st element is list of gold standard answers
    threshold: float
        Threshold for the answer scores
    return_score_only: bool
        determines whether only the score (True) will be returned.

    Returns
    -------

    """
    exact_matches = 0
    incorrect_matches = 0
    for ans in joint_system_gold_list:
        if ans[0] in ans[2] and ans[1] >= threshold or ans[1] <= threshold and ans[2][0] == "nan":
            exact_matches += 1
        elif ans[0] not in ans[2] and ans[1] > threshold:
            incorrect_matches += 1
    exact_match_rate = round(((exact_matches / len(joint_system_gold_list)) * 100), 1)
    if return_score_only is True:
        return exact_match_rate
    else:
        return entity_name, exact_match_rate


def thresholded_entity_score_tuple_list_2_txt(entity_score_tuple_list: list, filename: str, entity_position: str,
                                              metric_type: str, question_type: str, threshold: float,
                                              include_average=False, avg_score=None,
                                              path="C:/Users/ubmen/Desktop/BA_Prog/Evaluation/EvalResultsFiles/"
                                                   "ThresholdedResults"):
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
    path += "/ThresholdedResults" + question_type + "/ThresholdedResults" + question_type + entity_position + "/"
    path += "ThresholdedResults" + str(threshold).replace(".",
                                                          "") + question_type + entity_position + "/" + filename + ".txt"
    # reorder list according to scores
    entity_score_tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    if question_type == "BL":
        if entity_position == "SP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(f"{metric_type} results for Subject Position with Baseline questions "
                        f" with a threshold of {threshold} for answer scores - (e, r, ?): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()
        elif entity_position == "OP":
            with open(os.path.join(filename, path), "w", encoding="utf-8") as f:
                f.write(f"{metric_type} results for Object Position with Baseline questions"
                        f" with a threshold of {threshold} for answer scores - (?, r, e): ")
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
                f.write(f"{metric_type} results for Subject Position with Translation-Based questions"
                        f" with a threshold of {threshold} for answer scores - (e, r, ?): ")
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
                    f"{metric_type} results for Object Position with Translation-Based questions"
                    f" with a threshold of {threshold} for answer scores - (?, r, e): ")
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
                    f"{metric_type} results for Subject Position with Human-Generated questions"
                    f" with a threshold of {threshold} for answer scores - (e, r, ?): ")
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
                    f"{metric_type} results for Object Position with Human-Generated questions"
                    f" with a threshold of {threshold} for answer scores - (?, r, e): ")
                f.write("\n\n")
                f.write('\n'.join("{}: {}".format(ent[0], ent[1]) for ent in entity_score_tuple_list))
                if include_average is True:
                    f.write('\n')
                    f.write('\n')
                    f.write(f"Average {metric_type} score: {avg_score}")
                f.close()


def threshold_metrics_to_csv(bl_list: list, ag_list: list, nl_list: list, metric: str, entity_position: str,
                             threshold: float,
                             path="C:/Users/ubmen/Desktop/BA_Prog/Evaluation/EvalResultsFiles/ThresholdedResults/"
                                  "CSVFilesThresholded/CSVFilesThreshold", to_excel=False, return_df=False):
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
    path += str(threshold).replace(".", "") + "/CSVFilesThreshold" + str(threshold).replace(".", "") + entity_position + "/"
    filename = metric + "Threshold" + str(threshold).replace(".", "") + entity_position
    if to_excel is True:
        filename += ".xlsx"
        entity_score_df.to_excel(os.path.join(path, filename), index=False, encoding="utf-ß-sig")
    else:
        filename += ".csv"
        entity_score_df.to_csv(os.path.join(path, filename), index=False, encoding="utf-8-sig")
    if return_df is True:
        return entity_score_df


if __name__ == "__main__":
    # Thresholded Results for SP --> creating the necessary datastructures
    gs_dict_list_sp = load_json_dicts("gold", "SP")
    all_eval_entities = list(set([key for d in gs_dict_list_sp for key in d]))  # all entities
    system_result_list_sp_bl = load_json_dicts("eval", "SP", "BL")
    system_result_list_sp_ag = load_json_dicts("eval", "SP", "AG")
    system_result_list_sp_nl = load_json_dicts("eval", "SP", "NL")

    # noinspection PyTypeChecker
    ent_gold_system_tup_list_sp_bl = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_sp_bl, gs_dict_list_sp)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    ent_gold_system_tup_list_sp_ag = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_sp_ag, gs_dict_list_sp)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    ent_gold_system_tup_list_sp_nl = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_sp_nl, gs_dict_list_sp)
        for ent in all_eval_entities]

    # noinspection PyTypeChecker
    # precision SP with threshold 0.2
    precision_sp_bl02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_bl]
    avg_prec_sp_bl02 = get_avg_metric_score("precision", precision_sp_bl02)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_bl02, "ThresholdedPrecision02BLSP", "SP", "precision", "BL",
                                              0.2, include_average=True, avg_score=avg_prec_sp_bl02)
    avg_prec_sp_bl02_tup = ("Baseline", avg_prec_sp_bl02)

    # noinspection PyTypeChecker
    precision_sp_ag02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_ag]
    avg_prec_sp_ag02 = get_avg_metric_score("precision", precision_sp_ag02)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_ag02, "ThresholdedPrecision02AGSP", "SP", "precision", "AG",
                                              0.2, include_average=True, avg_score=avg_prec_sp_ag02)
    avg_prec_sp_ag02_tup = ("Translation-Based", avg_prec_sp_ag02)

    # noinspection PyTypeChecker
    precision_sp_nl02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_nl]
    avg_prec_sp_nl02 = get_avg_metric_score("precision", precision_sp_nl02)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_nl02, "ThresholdedPrecision02NLSP", "SP", "precision", "NL",
                                              0.2, include_average=True, avg_score=avg_prec_sp_nl02)
    avg_prec_sp_nl02_tup = ("Human-Generated", avg_prec_sp_nl02)
    precision_02_avgs = [avg_prec_sp_bl02_tup, avg_prec_sp_ag02_tup, avg_prec_sp_nl02_tup]
    plot_averages(precision_02_avgs, "Precision averages for Subject position with threshold 0.2 - (?, r, e)")
    threshold_metrics_to_csv(precision_sp_bl02, precision_sp_ag02, precision_sp_nl02, "Precision", "SP", 0.2)

    # recalls with Threshold 0.2
    recall_sp_bl02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_bl]
    avg_recall_sp_bl02 = get_avg_metric_score("recall", recall_sp_bl02)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_bl02, "ThresholdedRecall02BLSP", "SP", "recall", "BL",
                                              0.2, include_average=True, avg_score=avg_recall_sp_bl02)
    avg_recall_sp_bl02_tup = ("Baseline", avg_recall_sp_bl02)

    recall_sp_ag02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_ag]
    avg_recall_sp_ag02 = get_avg_metric_score("recall", recall_sp_ag02)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_ag02, "ThresholdedRecall02AGSP", "SP", "recall", "AG",
                                              0.2, include_average=True, avg_score=avg_recall_sp_ag02)
    avg_recall_sp_ag02_tup = ("Translation-Based", avg_recall_sp_ag02)

    recall_sp_nl02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_nl]
    avg_recall_sp_nl02 = get_avg_metric_score("recall", recall_sp_nl02)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_nl02, "ThresholdedRecall02NLSP", "SP", "recall", "NL",
                                              0.2, include_average=True, avg_score=avg_recall_sp_nl02)
    avg_recall_sp_nl02_tup = ("Human-Generated", avg_recall_sp_nl02)
    recall_02_avgs = [avg_recall_sp_bl02_tup, avg_recall_sp_ag02_tup, avg_recall_sp_nl02_tup]
    plot_averages(recall_02_avgs, "Recall averages for Subject Position with threshold 0.2 - (e, r, ?)")
    threshold_metrics_to_csv(recall_sp_bl02, recall_sp_ag02, recall_sp_nl02, "Recall", "SP", 0.2)

    # exact matches SP threshold 0.2
    em_sp_bl02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_bl]
    avg_em_sp_bl02 = get_avg_metric_score("exact match", em_sp_bl02)
    thresholded_entity_score_tuple_list_2_txt(em_sp_bl02, "ThresholdedExactMatch02BLSP", "SP", "exact match", "BL", 0.2,
                                              include_average=True, avg_score=avg_em_sp_bl02)
    avg_em_sp_bl02_tup = ("Baseline", avg_em_sp_bl02)
    em_sp_ag02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_ag]
    avg_em_sp_ag02 = get_avg_metric_score("exact match", em_sp_ag02)
    thresholded_entity_score_tuple_list_2_txt(em_sp_ag02, "ThresholdedExactMatch02AGSP", "SP", "exact match", "AG", 0.2,
                                              include_average=True, avg_score=avg_em_sp_ag02)
    avg_em_sp_ag02_tup = ("Translation-Based", avg_em_sp_ag02)
    em_sp_nl02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_sp_nl]
    avg_em_sp_nl02 = get_avg_metric_score("exact match", em_sp_nl02)
    thresholded_entity_score_tuple_list_2_txt(em_sp_nl02, "ThresholdedExactMatch02NLSP", "SP", "exact match", "NL", 0.2,
                                              include_average=True, avg_score=avg_em_sp_bl02)
    avg_em_sp_nl02_tup = ("Human-Generated", avg_em_sp_nl02)
    em_02_averages = [avg_em_sp_bl02_tup, avg_em_sp_ag02_tup, avg_em_sp_nl02_tup]
    plot_averages(em_02_averages, "Exact Match averages for Subject Position with threshold 0.2 - (e, r, ?)")
    threshold_metrics_to_csv(em_sp_bl02, em_sp_ag02, em_sp_nl02, "EM", "SP", 0.2)

    ####################################################################################################################
    # subject Position threshold 0.4
    precision_sp_bl04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_bl]
    avg_prec_sp_bl04 = get_avg_metric_score("precision", precision_sp_bl04)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_bl04, "ThresholdedPrecision04BLSP", "SP", "precision", "BL",
                                              0.4, include_average=True, avg_score=avg_prec_sp_bl04)
    avg_prec_sp_bl04_tup = ("Baseline", avg_prec_sp_bl04)

    precision_sp_ag04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_ag]
    avg_prec_sp_ag04 = get_avg_metric_score("precision", precision_sp_ag04)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_ag04, "ThresholdedPrecision04AGSP", "SP", "precision", "AG",
                                              0.4, include_average=True, avg_score=avg_prec_sp_ag04)
    avg_prec_sp_ag04_tup = ("Translation-Based", avg_prec_sp_ag04)
    precision_sp_nl04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_nl]
    avg_prec_sp_nl04 = get_avg_metric_score("precision", precision_sp_nl04)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_nl04, "ThresholdedPrecision04NLSP", "SP", "precision", "NL",
                                              0.4, include_average=True, avg_score=avg_prec_sp_nl04)
    avg_prec_sp_nl04_tup = ("Human-Generated", avg_prec_sp_nl04)
    precision_04_avgs = [avg_prec_sp_bl04_tup, avg_prec_sp_ag04_tup, avg_prec_sp_nl04_tup]
    plot_averages(precision_04_avgs, "Precision averages for Subject position with threshold 0.4 - (?, r, e)")
    threshold_metrics_to_csv(precision_sp_bl04, precision_sp_ag04, precision_sp_nl04, "Precision", "SP", 0.4)

    # recall SP threshold 0.4
    recall_sp_bl04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_bl]
    avg_recall_sp_bl04 = get_avg_metric_score("recall", recall_sp_bl04)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_bl04, "ThresholdedRecall04BLSP", "SP", "recall", "BL",
                                              0.4, include_average=True, avg_score=avg_recall_sp_bl04)
    avg_recall_sp_bl04_tup = ("Baseline", avg_recall_sp_bl04)

    recall_sp_ag04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_ag]
    avg_recall_sp_ag04 = get_avg_metric_score("recall", recall_sp_ag04)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_ag04, "ThresholdedRecall04AGSP", "SP", "recall", "AG",
                                              0.4, include_average=True, avg_score=avg_recall_sp_ag04)
    avg_recall_sp_ag04_tup = ("Translation-Based", avg_recall_sp_ag04)

    recall_sp_nl04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_nl]
    avg_recall_sp_nl04 = get_avg_metric_score("recall", recall_sp_nl04)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_nl04, "ThresholdedRecall04NLSP", "SP", "recall", "NL",
                                              0.4, include_average=True, avg_score=avg_recall_sp_nl04)
    avg_recall_sp_nl04_tup = ("Human-Generated", avg_recall_sp_nl04)

    recall_04_avgs = [avg_recall_sp_bl04_tup, avg_recall_sp_ag04_tup, avg_recall_sp_nl04_tup]
    plot_averages(recall_04_avgs, "Recall averages for Subject Position with threshold 0.4 - (e, r, ?)")
    threshold_metrics_to_csv(recall_sp_bl04, recall_sp_ag04, recall_sp_nl04, "Recall", "SP", 0.4)

    # exact match SP threshold 0.4
    em_sp_bl04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_bl]
    avg_em_sp_bl04 = get_avg_metric_score("exact match", em_sp_bl04)
    thresholded_entity_score_tuple_list_2_txt(em_sp_bl04, "ThresholdedExactMatch04BLSP", "SP", "exact match", "BL", 0.4,
                                              include_average=True, avg_score=avg_em_sp_bl04)
    avg_em_sp_bl04_tup = ("Baseline", avg_em_sp_bl04)

    em_sp_ag04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_ag]
    avg_em_sp_ag04 = get_avg_metric_score("exact match", em_sp_ag04)
    thresholded_entity_score_tuple_list_2_txt(em_sp_ag04, "ThresholdedExactMatch04AGSP", "SP", "exact match", "AG", 0.4,
                                              include_average=True, avg_score=avg_em_sp_ag04)
    avg_em_sp_ag04_tup = ("Translation-Based", avg_em_sp_ag04)

    em_sp_nl04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_sp_nl]
    avg_em_sp_nl04 = get_avg_metric_score("exact match", em_sp_nl04)
    thresholded_entity_score_tuple_list_2_txt(em_sp_nl04, "ThresholdedExactMatch04NLSP", "SP", "exact match", "NL", 0.4,
                                              include_average=True, avg_score=avg_em_sp_nl04)
    avg_em_sp_nl04_tup = ("Human-Generated", avg_em_sp_nl04)
    em_02_averages = [avg_em_sp_bl04_tup, avg_em_sp_ag04_tup, avg_em_sp_nl04_tup]
    plot_averages(em_02_averages, "Exact Match averages for Subject Position with threshold 0.4- (e, r, ?)")

    ####################################################################################################################
    # Subject Position threshold 0.6
    precision_sp_bl06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_bl]
    avg_prec_sp_bl06 = get_avg_metric_score("precision", precision_sp_bl06)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_bl06, "ThresholdedPrecision06BLSP", "SP", "precision", "BL",
                                              0.6, include_average=True, avg_score=avg_prec_sp_bl06)
    avg_prec_sp_bl06_tup = ("Baseline", avg_prec_sp_bl06)

    precision_sp_ag06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_ag]
    avg_prec_sp_ag06 = get_avg_metric_score("precision", precision_sp_ag06)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_ag06, "ThresholdedPrecision06AGSP", "SP", "precision", "AG",
                                              0.6, include_average=True, avg_score=avg_prec_sp_ag06)
    avg_prec_sp_ag06_tup = ("Translation-Based", avg_prec_sp_ag06)

    precision_sp_nl06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_nl]
    avg_prec_sp_nl06 = get_avg_metric_score("precision", precision_sp_nl06)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_nl06, "ThresholdedPrecision06NLSP", "SP", "precision", "NL",
                                              0.6, include_average=True, avg_score=avg_prec_sp_nl06)
    avg_prec_sp_nl06_tup = ("Human-Generated", avg_prec_sp_nl06)

    precision_06_avgs = [avg_prec_sp_bl06_tup, avg_prec_sp_ag06_tup, avg_prec_sp_nl06_tup]
    plot_averages(precision_06_avgs, "Precision averages for Subject position with threshold 0.6 - (?, r, e)")
    threshold_metrics_to_csv(precision_sp_bl06, precision_sp_ag06, precision_sp_nl06, "Precision", "SP", 0.6)

    # recall SP threshold 0.6
    recall_sp_bl06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_bl]
    avg_recall_sp_bl06 = get_avg_metric_score("recall", recall_sp_bl06)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_bl06, "ThresholdedRecall06BLSP", "SP", "recall", "BL",
                                              0.6, include_average=True, avg_score=avg_recall_sp_bl06)
    avg_recall_sp_bl06_tup = ("Baseline", avg_recall_sp_bl06)

    recall_sp_ag06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_ag]
    avg_recall_sp_ag06 = get_avg_metric_score("recall", recall_sp_ag06)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_ag06, "ThresholdedRecall06AGSP", "SP", "recall", "AG",
                                              0.6, include_average=True, avg_score=avg_recall_sp_ag06)
    avg_recall_sp_ag06_tup = ("Translation-Based", avg_recall_sp_ag06)

    recall_sp_nl06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_nl]
    avg_recall_sp_nl06 = get_avg_metric_score("recall", recall_sp_nl06)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_nl06, "ThresholdedRecall06NLSP", "SP", "recall", "NL",
                                              0.6, include_average=True, avg_score=avg_recall_sp_nl06)
    avg_recall_sp_nl06_tup = ("Human-Generated", avg_recall_sp_nl06)

    recall_06_avgs = [avg_recall_sp_bl06_tup, avg_recall_sp_ag06_tup, avg_recall_sp_nl06_tup]
    plot_averages(recall_06_avgs, "Recall averages for Subject Position with threshold 0.6 - (e, r, ?)")
    threshold_metrics_to_csv(recall_sp_bl06, recall_sp_ag06, recall_sp_nl06, "Recall", "SP", 0.6)

    # exact match SP threshold 0.6
    em_sp_bl06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_bl]
    avg_em_sp_bl06 = get_avg_metric_score("exact match", em_sp_bl06)
    thresholded_entity_score_tuple_list_2_txt(em_sp_bl06, "ThresholdedExactMatch06BLSP", "SP", "exact match", "BL", 0.6,
                                              include_average=True, avg_score=avg_em_sp_bl06)
    avg_em_sp_bl06_tup = ("Baseline", avg_em_sp_bl06)

    em_sp_ag06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_ag]
    avg_em_sp_ag06 = get_avg_metric_score("exact match", em_sp_ag06)
    thresholded_entity_score_tuple_list_2_txt(em_sp_ag06, "ThresholdedExactMatch06AGSP", "SP", "exact match", "AG", 0.6,
                                              include_average=True, avg_score=avg_em_sp_ag06)
    avg_em_sp_ag06_tup = ("Translation-Based", avg_em_sp_ag06)

    em_sp_nl06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_sp_nl]
    avg_em_sp_nl06 = get_avg_metric_score("exact match", em_sp_nl06)
    thresholded_entity_score_tuple_list_2_txt(em_sp_nl06, "ThresholdedExactMatch06NLSP", "SP", "exact match", "NL", 0.6,
                                              include_average=True, avg_score=avg_em_sp_nl06)
    avg_em_sp_nl06_tup = ("Human-Generated", avg_em_sp_nl06)
    em_06_averages = [avg_em_sp_bl06_tup, avg_em_sp_ag06_tup, avg_em_sp_nl06_tup]
    plot_averages(em_06_averages, "Exact Match averages for Subject Position with threshold 0.6 - (e, r, ?)")

    ####################################################################################################################
    # Subject Position metrics threshold 0.8

    precision_sp_bl08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_bl]
    avg_prec_sp_bl08 = get_avg_metric_score("precision", precision_sp_bl08)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_bl08, "ThresholdedPrecision08BLSP", "SP", "precision", "BL",
                                              0.8, include_average=True, avg_score=avg_prec_sp_bl08)
    avg_prec_sp_bl08_tup = ("Baseline", avg_prec_sp_bl08)

    precision_sp_ag08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_ag]
    avg_prec_sp_ag08 = get_avg_metric_score("precision", precision_sp_ag08)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_ag08, "ThresholdedPrecision08AGSP", "SP", "precision", "AG",
                                              0.8, include_average=True, avg_score=avg_prec_sp_ag08)
    avg_prec_sp_ag08_tup = ("Translation-Based", avg_prec_sp_ag08)

    precision_sp_nl08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_nl]
    avg_prec_sp_nl08 = get_avg_metric_score("precision", precision_sp_nl08)
    thresholded_entity_score_tuple_list_2_txt(precision_sp_nl08, "ThresholdedPrecision08NLSP", "SP", "precision", "NL",
                                              0.8, include_average=True, avg_score=avg_prec_sp_nl08)
    avg_prec_sp_nl08_tup = ("Human-Generated", avg_prec_sp_nl08)

    precision_08_avgs = [avg_prec_sp_bl08_tup, avg_prec_sp_ag08_tup, avg_prec_sp_nl08_tup]
    plot_averages(precision_08_avgs, "Precision averages for Subject position with threshold 0.8 - (e, r, ?)")
    threshold_metrics_to_csv(precision_sp_bl08, precision_sp_ag08, precision_sp_nl08, "Precision", "SP", 0.8)

    # recall SP threshold 0.8
    recall_sp_bl08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_bl]
    avg_recall_sp_bl08 = get_avg_metric_score("recall", recall_sp_bl08)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_bl08, "ThresholdedRecall08BLSP", "SP", "recall", "BL",
                                              0.8, include_average=True, avg_score=avg_recall_sp_bl08)
    avg_recall_sp_bl08_tup = ("Baseline", avg_recall_sp_bl08)

    recall_sp_ag08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_ag]
    avg_recall_sp_ag08 = get_avg_metric_score("recall", recall_sp_ag08)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_ag08, "ThresholdedRecall08AGSP", "SP", "recall", "AG",
                                              0.8, include_average=True, avg_score=avg_recall_sp_ag08)
    avg_recall_sp_ag08_tup = ("Translation-Based", avg_recall_sp_ag08)

    recall_sp_nl08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_nl]
    avg_recall_sp_nl08 = get_avg_metric_score("recall", recall_sp_nl08)
    thresholded_entity_score_tuple_list_2_txt(recall_sp_nl08, "ThresholdedRecall08NLSP", "SP", "recall", "NL",
                                              0.8, include_average=True, avg_score=avg_recall_sp_nl08)
    avg_recall_sp_nl08_tup = ("Human-Generated", avg_recall_sp_nl08)

    recall_08_avgs = [avg_recall_sp_bl08_tup, avg_recall_sp_ag08_tup, avg_recall_sp_nl08_tup]
    plot_averages(recall_08_avgs, "Recall averages for Subject Position with threshold 0.8 - (e, r, ?)")
    threshold_metrics_to_csv(recall_sp_bl08, recall_sp_ag08, recall_sp_nl08, "Recall", "SP", 0.8)

    # exact match SP threshold 0.8
    em_sp_bl08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_bl]
    avg_em_sp_bl08 = get_avg_metric_score("exact match", em_sp_bl08)
    thresholded_entity_score_tuple_list_2_txt(em_sp_bl08, "ThresholdedExactMatch08BLSP", "SP", "exact match", "BL", 0.8,
                                              include_average=True, avg_score=avg_em_sp_bl08)
    avg_em_sp_bl08_tup = ("Baseline", avg_em_sp_bl08)

    em_sp_ag08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_ag]
    avg_em_sp_ag08 = get_avg_metric_score("exact match", em_sp_ag08)
    thresholded_entity_score_tuple_list_2_txt(em_sp_ag08, "ThresholdedExactMatch08AGSP", "SP", "exact match", "AG", 0.8,
                                              include_average=True, avg_score=avg_em_sp_ag08)
    avg_em_sp_ag08_tup = ("Translation-Based", avg_em_sp_ag08)

    em_sp_nl08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_sp_nl]
    avg_em_sp_nl08 = get_avg_metric_score("exact match", em_sp_nl08)
    thresholded_entity_score_tuple_list_2_txt(em_sp_nl08, "ThresholdedExactMatch08NLSP", "SP", "exact match", "NL", 0.8,
                                              include_average=True, avg_score=avg_em_sp_nl08)
    avg_em_sp_nl08_tup = ("Human-Generated", avg_em_sp_nl08)
    em_08_averages = [avg_em_sp_bl08_tup, avg_em_sp_ag08_tup, avg_em_sp_nl08_tup]
    plot_averages(em_08_averages, "Exact Match averages for Subject Position with threshold 0.8- (e, r, ?)")

    ####################################################################################################################
    # Object Position threshold evaluation
    ####################################################################################################################

    system_result_list_op_bl = load_json_dicts("eval", "OP", "BL")
    system_result_list_op_ag = load_json_dicts("eval", "OP", "AG")
    system_result_list_op_nl = load_json_dicts("eval", "OP", "NL")

    # noinspection PyTypeChecker
    gs_dict_list_op = load_json_dicts("gold", "OP")
    ent_gold_system_tup_list_op_bl = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_op_bl, gs_dict_list_op)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    ent_gold_system_tup_list_op_ag = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_op_ag, gs_dict_list_op)
        for ent in all_eval_entities]
    # noinspection PyTypeChecker
    ent_gold_system_tup_list_op_nl = [
        entity_score_system_gold_tuple_lists(ent, system_result_list_op_nl, gs_dict_list_op)
        for ent in all_eval_entities]

    # precision SP with threshold 0.2
    precision_op_bl02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_bl]
    avg_prec_op_bl02 = get_avg_metric_score("precision", precision_op_bl02)
    thresholded_entity_score_tuple_list_2_txt(precision_op_bl02, "ThresholdedPrecision02BLOP", "OP", "precision", "BL",
                                              0.2, include_average=True, avg_score=avg_prec_op_bl02)
    avg_prec_op_bl02_tup = ("Baseline", avg_prec_op_bl02)

    # noinspection PyTypeChecker
    precision_op_ag02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_ag]
    avg_prec_op_ag02 = get_avg_metric_score("precision", precision_op_ag02)
    thresholded_entity_score_tuple_list_2_txt(precision_op_ag02, "ThresholdedPrecision02AGOP", "OP", "precision", "AG",
                                              0.2, include_average=True, avg_score=avg_prec_op_ag02)
    avg_prec_op_ag02_tup = ("Translation-Based", avg_prec_op_ag02)

    # noinspection PyTypeChecker
    precision_op_nl02 = [threshold_entity_precision(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_nl]
    avg_prec_op_nl02 = get_avg_metric_score("precision", precision_op_nl02)
    thresholded_entity_score_tuple_list_2_txt(precision_op_nl02, "ThresholdedPrecision02NLOP", "OP", "precision", "NL",
                                              0.2, include_average=True, avg_score=avg_prec_op_nl02)
    avg_prec_op_nl02_tup = ("Human-Generated", avg_prec_op_nl02)
    precision_02_avgs_op = [avg_prec_op_bl02_tup, avg_prec_op_ag02_tup, avg_prec_op_nl02_tup]
    plot_averages(precision_02_avgs_op, "Precision averages for Object position with threshold 0.2 - (?, r, e)")
    threshold_metrics_to_csv(precision_sp_bl02, precision_sp_ag02, precision_sp_nl02, "Precision", "OP", 0.2)

    # recalls OP with Threshold 0.2
    recall_op_bl02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_bl]
    avg_recall_op_bl02 = get_avg_metric_score("recall", recall_op_bl02)
    thresholded_entity_score_tuple_list_2_txt(recall_op_bl02, "ThresholdedRecall02BLOP", "OP", "recall", "BL",
                                              0.2, include_average=True, avg_score=avg_recall_op_bl02)
    avg_recall_op_bl02_tup = ("Baseline", avg_recall_op_bl02)

    recall_op_ag02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_ag]
    avg_recall_op_ag02 = get_avg_metric_score("recall", recall_op_ag02)
    thresholded_entity_score_tuple_list_2_txt(recall_op_ag02, "ThresholdedRecall02AGOP", "OP", "recall", "AG",
                                              0.2, include_average=True, avg_score=avg_recall_op_ag02)
    avg_recall_op_ag02_tup = ("Translation-Based", avg_recall_op_ag02)

    recall_op_nl02 = [threshold_entity_recall(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_nl]
    avg_recall_op_nl02 = get_avg_metric_score("recall", recall_op_nl02)
    thresholded_entity_score_tuple_list_2_txt(recall_op_nl02, "ThresholdedRecall02NLOP", "OP", "recall", "NL",
                                              0.2, include_average=True, avg_score=avg_recall_op_nl02)
    avg_recall_op_nl02_tup = ("Human-Generated", avg_recall_op_nl02)
    recall_02_avgs_op = [avg_recall_op_bl02_tup, avg_recall_op_ag02_tup, avg_recall_op_nl02_tup]
    plot_averages(recall_02_avgs_op, "Recall averages for Object Position with threshold 0.2 - (?, r, e)")
    threshold_metrics_to_csv(recall_op_bl02, recall_op_ag02, recall_op_nl02, "Recall", "OP", 0.2)

    # exact matches OP threshold 0.2
    em_op_bl02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_bl]
    avg_em_op_bl02 = get_avg_metric_score("exact match", em_op_bl02)
    thresholded_entity_score_tuple_list_2_txt(em_op_bl02, "ThresholdedExactMatch02BLOP", "OP", "exact match", "BL", 0.2,
                                              include_average=True, avg_score=avg_em_op_bl02)
    avg_em_op_bl02_tup = ("Baseline", avg_em_op_bl02)
    em_op_ag02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_ag]
    avg_em_op_ag02 = get_avg_metric_score("exact match", em_op_ag02)
    thresholded_entity_score_tuple_list_2_txt(em_op_ag02, "ThresholdedExactMatch02BLOP", "OP", "exact match", "AG", 0.2,
                                              include_average=True, avg_score=avg_em_op_ag02)
    avg_em_op_ag02_tup = ("Translation-Based", avg_em_op_ag02)
    em_op_nl02 = [threshold_exact_match(ent[0], ent[1], 0.2) for ent in ent_gold_system_tup_list_op_nl]
    avg_em_op_nl02 = get_avg_metric_score("exact match", em_op_nl02)
    thresholded_entity_score_tuple_list_2_txt(em_op_nl02, "ThresholdedExactMatch02AGSP", "OP", "exact match", "NL", 0.2,
                                              include_average=True, avg_score=avg_em_op_nl02)
    avg_em_sp_nl02_tup = ("Human-Generated", avg_em_sp_nl02)
    em_02_averages = [avg_em_sp_bl02_tup, avg_em_sp_ag02_tup, avg_em_sp_nl02_tup]
    plot_averages(em_02_averages, "Exact Match averages for Object Position with threshold 0.2 - (?, r, e)")

    ####################################################################################################################
    # Object position metrics with threshold 0.4
    precision_op_bl04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_bl]
    avg_prec_op_bl04 = get_avg_metric_score("precision", precision_op_bl04)
    thresholded_entity_score_tuple_list_2_txt(precision_op_bl04, "ThresholdedPrecision04BLOP", "OP", "precision", "BL",
                                              0.4, include_average=True, avg_score=avg_prec_op_bl04)
    avg_prec_op_bl04_tup = ("Baseline", avg_prec_op_bl04)

    precision_op_ag04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_ag]
    avg_prec_op_ag04 = get_avg_metric_score("precision", precision_op_ag04)
    thresholded_entity_score_tuple_list_2_txt(precision_op_ag04, "ThresholdedPrecision04AGOP", "OP", "precision", "AG",
                                              0.4, include_average=True, avg_score=avg_prec_op_ag04)
    avg_prec_op_ag04_tup = ("Translation-Based", avg_prec_op_ag04)
    precision_op_nl04 = [threshold_entity_precision(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_nl]
    avg_prec_op_nl04 = get_avg_metric_score("precision", precision_op_nl04)
    thresholded_entity_score_tuple_list_2_txt(precision_op_nl04, "ThresholdedPrecision04NLOP", "OP", "precision", "NL",
                                              0.4, include_average=True, avg_score=avg_prec_op_nl04)
    avg_prec_op_nl04_tup = ("Human-Generated", avg_prec_op_nl04)
    precision_04_avgs_op = [avg_prec_op_bl04_tup, avg_prec_op_ag04_tup, avg_prec_op_nl04_tup]
    plot_averages(precision_04_avgs_op, "Precision averages for Object position with threshold 0.4 - (?, r, e)")
    threshold_metrics_to_csv(precision_op_bl04, precision_op_ag04, precision_op_nl04, "Precision", "OP", 0.4)

    # recall OP threshold 0.4
    recall_op_bl04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_bl]
    avg_recall_op_bl04 = get_avg_metric_score("recall", recall_op_bl04)
    thresholded_entity_score_tuple_list_2_txt(recall_op_bl04, "ThresholdedRecall04BLOP", "OP", "recall", "BL",
                                              0.4, include_average=True, avg_score=avg_recall_op_bl04)
    avg_recall_op_bl04_tup = ("Baseline", avg_recall_op_bl04)

    recall_op_ag04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_ag]
    avg_recall_op_ag04 = get_avg_metric_score("recall", recall_op_ag04)
    thresholded_entity_score_tuple_list_2_txt(recall_op_ag04, "ThresholdedRecall04AGOP", "OP", "recall", "AG",
                                              0.4, include_average=True, avg_score=avg_recall_op_ag04)
    avg_recall_op_ag04_tup = ("Translation-Based", avg_recall_op_ag04)

    recall_op_nl04 = [threshold_entity_recall(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_nl]
    avg_recall_op_nl04 = get_avg_metric_score("recall", recall_op_nl04)
    thresholded_entity_score_tuple_list_2_txt(recall_op_nl04, "ThresholdedRecall04NLOP", "OP", "recall", "NL",
                                              0.4, include_average=True, avg_score=avg_recall_op_nl04)
    avg_recall_op_nl04_tup = ("Human-Generated", avg_recall_op_nl04)

    recall_04_avgs_op = [avg_recall_op_bl04_tup, avg_recall_op_ag04_tup, avg_recall_op_nl04_tup]
    plot_averages(recall_04_avgs_op, "Recall averages for Object Position with threshold 0.4 - (?, r, e)")
    threshold_metrics_to_csv(recall_op_bl04, recall_op_ag04, recall_op_nl04, "Recall", "OP", 0.4)

    # exact match OP threshold 0.4
    em_op_bl04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_bl]
    avg_em_op_bl04 = get_avg_metric_score("exact match", em_op_bl04)
    thresholded_entity_score_tuple_list_2_txt(em_op_bl04, "ThresholdedExactMatch04BLOP", "OP", "exact match", "BL", 0.4,
                                              include_average=True, avg_score=avg_em_op_bl04)
    avg_em_op_bl04_tup = ("Baseline", avg_em_op_bl04)

    em_op_ag04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_ag]
    avg_em_op_ag04 = get_avg_metric_score("exact match", em_op_ag04)
    thresholded_entity_score_tuple_list_2_txt(em_op_ag04, "ThresholdedExactMatch04AGOP", "OP", "exact match", "AG", 0.4,
                                              include_average=True, avg_score=avg_em_op_ag04)
    avg_em_op_ag04_tup = ("Translation-Based", avg_em_op_ag04)

    em_op_nl04 = [threshold_exact_match(ent[0], ent[1], 0.4) for ent in ent_gold_system_tup_list_op_nl]
    avg_em_op_nl04 = get_avg_metric_score("exact match", em_op_nl04)
    thresholded_entity_score_tuple_list_2_txt(em_op_nl04, "ThresholdedExactMatch04NLOP", "OP", "exact match", "NL", 0.4,
                                              include_average=True, avg_score=avg_em_op_nl04)
    avg_em_op_nl04_tup = ("Human-Generated", avg_em_op_nl04)
    em_02_averages_op = [avg_em_op_bl04_tup, avg_em_op_ag04_tup, avg_em_op_nl04_tup]
    plot_averages(em_02_averages_op, "Exact Match averages for Object Position with threshold 0.4 - (?, r, e)")

    ####################################################################################################################
    # Object Position metrics with threshold 0.6
    precision_op_bl06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_bl]
    avg_prec_op_bl06 = get_avg_metric_score("precision", precision_op_bl06)
    thresholded_entity_score_tuple_list_2_txt(precision_op_bl06, "ThresholdedPrecision06BLOP", "OP", "precision", "BL",
                                              0.6, include_average=True, avg_score=avg_prec_op_bl06)
    avg_prec_op_bl06_tup = ("Baseline", avg_prec_op_bl06)

    precision_op_ag06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_ag]
    avg_prec_op_ag06 = get_avg_metric_score("precision", precision_op_ag06)
    thresholded_entity_score_tuple_list_2_txt(precision_op_ag06, "ThresholdedPrecision06AGOP", "OP", "precision", "AG",
                                              0.6, include_average=True, avg_score=avg_prec_op_ag06)
    avg_prec_op_ag06_tup = ("Translation-Based", avg_prec_op_ag06)

    precision_op_nl06 = [threshold_entity_precision(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_nl]
    avg_prec_op_nl06 = get_avg_metric_score("precision", precision_op_nl06)
    thresholded_entity_score_tuple_list_2_txt(precision_op_nl06, "ThresholdedPrecision06NLOP", "OP", "precision", "NL",
                                              0.6, include_average=True, avg_score=avg_prec_op_nl06)
    avg_prec_op_nl06_tup = ("Human-Generated", avg_prec_op_nl06)

    precision_06_avgs_op = [avg_prec_op_bl06_tup, avg_prec_op_ag06_tup, avg_prec_op_nl06_tup]
    plot_averages(precision_06_avgs_op, "Precision averages for Object position with threshold 0.6 - (?, r, e)")
    threshold_metrics_to_csv(precision_op_bl06, precision_op_ag06, precision_op_nl06, "Precision", "OP", 0.6)

    # recall OP threshold 0.6
    recall_op_bl06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_bl]
    avg_recall_op_bl06 = get_avg_metric_score("recall", recall_op_bl06)
    thresholded_entity_score_tuple_list_2_txt(recall_op_bl06, "ThresholdedRecall06BLOP", "OP", "recall", "BL",
                                              0.6, include_average=True, avg_score=avg_recall_op_bl06)
    avg_recall_op_bl06_tup = ("Baseline", avg_recall_op_bl06)

    recall_op_ag06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_ag]
    avg_recall_op_ag06 = get_avg_metric_score("recall", recall_op_ag06)
    thresholded_entity_score_tuple_list_2_txt(recall_op_ag06, "ThresholdedRecall06AGOP", "OP", "recall", "AG",
                                              0.6, include_average=True, avg_score=avg_recall_op_ag06)
    avg_recall_op_ag06_tup = ("Translation-Based", avg_recall_op_ag06)

    recall_op_nl06 = [threshold_entity_recall(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_nl]
    avg_recall_op_nl06 = get_avg_metric_score("recall", recall_op_nl06)
    thresholded_entity_score_tuple_list_2_txt(recall_op_nl06, "ThresholdedRecall06NLOP", "OP", "recall", "NL",
                                              0.6, include_average=True, avg_score=avg_recall_op_nl06)
    avg_recall_op_nl06_tup = ("Human-Generated", avg_recall_op_nl06)

    recall_06_avgs_op = [avg_recall_op_bl06_tup, avg_recall_op_ag06_tup, avg_recall_op_nl06_tup]
    plot_averages(recall_06_avgs_op, "Recall averages for Object Position with threshold 0.6 - (?, r, e)")
    threshold_metrics_to_csv(recall_op_bl06, recall_op_ag06, recall_op_nl06, "Recall", "OP", 0.6)

    # exact match OP threshold 0.6
    em_op_bl06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_bl]
    avg_em_op_bl06 = get_avg_metric_score("exact match", em_op_bl06)
    thresholded_entity_score_tuple_list_2_txt(em_op_bl06, "ThresholdedExactMatch06BLOP", "OP", "exact match", "BL", 0.6,
                                              include_average=True, avg_score=avg_em_op_bl06)
    avg_em_op_bl06_tup = ("Baseline", avg_em_op_bl06)

    em_op_ag06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_ag]
    avg_em_op_ag06 = get_avg_metric_score("exact match", em_op_ag06)
    thresholded_entity_score_tuple_list_2_txt(em_op_ag06, "ThresholdedExactMatch06AGOP", "OP", "exact match", "AG", 0.6,
                                              include_average=True, avg_score=avg_em_op_ag06)
    avg_em_op_ag06_tup = ("Translation-Based", avg_em_op_ag06)

    em_op_nl06 = [threshold_exact_match(ent[0], ent[1], 0.6) for ent in ent_gold_system_tup_list_op_nl]
    avg_em_op_nl06 = get_avg_metric_score("exact match", em_op_nl06)
    thresholded_entity_score_tuple_list_2_txt(em_op_nl06, "ThresholdedExactMatch06NLOP", "OP", "exact match", "NL", 0.6,
                                              include_average=True, avg_score=avg_em_op_nl06)
    avg_em_op_nl06_tup = ("Human-Generated", avg_em_op_nl06)
    em_06_averages_op = [avg_em_op_bl06_tup, avg_em_op_ag06_tup, avg_em_op_nl06_tup]
    plot_averages(em_06_averages_op, "Exact Match averages for Object Position with threshold 0.6 - (?, r, e)")

    ####################################################################################################################
    # Object Position metrics with threshold 0.8
    precision_op_bl08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_bl]
    avg_prec_op_bl08 = get_avg_metric_score("precision", precision_op_bl08)
    thresholded_entity_score_tuple_list_2_txt(precision_op_bl08, "ThresholdedPrecision08BLOP", "OP", "precision", "BL",
                                              0.8, include_average=True, avg_score=avg_prec_op_bl08)
    avg_prec_op_bl08_tup = ("Baseline", avg_prec_op_bl08)

    precision_op_ag08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_ag]
    avg_prec_op_ag08 = get_avg_metric_score("precision", precision_op_ag08)
    thresholded_entity_score_tuple_list_2_txt(precision_op_ag08, "ThresholdedPrecision08AGOP", "OP", "precision", "AG",
                                              0.8, include_average=True, avg_score=avg_prec_op_ag08)
    avg_prec_op_ag08_tup = ("Translation-Based", avg_prec_op_ag08)

    precision_op_nl08 = [threshold_entity_precision(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_nl]
    avg_prec_op_nl08 = get_avg_metric_score("precision", precision_op_nl08)
    thresholded_entity_score_tuple_list_2_txt(precision_op_nl08, "ThresholdedPrecision08NLOP", "OP", "precision", "NL",
                                              0.8, include_average=True, avg_score=avg_prec_op_nl08)
    avg_prec_op_nl08_tup = ("Human-Generated", avg_prec_op_nl08)

    precision_08_avgs_op = [avg_prec_op_bl08_tup, avg_prec_op_ag08_tup, avg_prec_op_nl08_tup]
    plot_averages(precision_08_avgs_op, "Precision averages for Object position with threshold 0.8 - (?, r, e)")
    threshold_metrics_to_csv(precision_op_bl08, precision_op_ag08, precision_op_nl08, "Precision", "OP", 0.8)

    # recall OP threshold 0.8
    recall_op_bl08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_bl]
    avg_recall_op_bl08 = get_avg_metric_score("recall", recall_op_bl08)
    thresholded_entity_score_tuple_list_2_txt(recall_op_bl08, "ThresholdedRecall08BLOP", "OP", "recall", "BL",
                                              0.8, include_average=True, avg_score=avg_recall_op_bl08)
    avg_recall_op_bl08_tup = ("Baseline", avg_recall_op_bl08)

    recall_op_ag08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_ag]
    avg_recall_op_ag08 = get_avg_metric_score("recall", recall_op_ag08)
    thresholded_entity_score_tuple_list_2_txt(recall_op_ag08, "ThresholdedRecall08AGOP", "OP", "recall", "AG",
                                              0.8, include_average=True, avg_score=avg_recall_op_ag08)
    avg_recall_op_ag08_tup = ("Translation-Based", avg_recall_op_ag08)

    recall_op_nl08 = [threshold_entity_recall(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_nl]
    avg_recall_op_nl08 = get_avg_metric_score("recall", recall_op_nl08)
    thresholded_entity_score_tuple_list_2_txt(recall_op_nl08, "ThresholdedRecall08NLOP", "OP", "recall", "NL",
                                              0.8, include_average=True, avg_score=avg_recall_op_nl08)
    avg_recall_op_nl08_tup = ("Human-Generated", avg_recall_op_nl08)

    recall_08_avgs_op = [avg_recall_op_bl08_tup, avg_recall_op_ag08_tup, avg_recall_op_nl08_tup]
    plot_averages(recall_08_avgs_op, "Recall averages for Object Position with threshold 0.8 - (?, r, e)")
    threshold_metrics_to_csv(recall_op_bl08, recall_op_ag08, recall_op_nl08, "Recall", "OP", 0.8)

    # exact match OP threshold 0.8
    em_op_bl08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_bl]
    avg_em_op_bl08 = get_avg_metric_score("exact match", em_op_bl08)
    thresholded_entity_score_tuple_list_2_txt(em_op_bl08, "ThresholdedExactMatch08BLOP", "OP", "exact match", "BL", 0.8,
                                              include_average=True, avg_score=avg_em_op_bl08)
    avg_em_op_bl08_tup = ("Baseline", avg_em_op_bl08)

    em_op_ag08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_ag]
    avg_em_op_ag08 = get_avg_metric_score("exact match", em_op_ag08)
    thresholded_entity_score_tuple_list_2_txt(em_op_ag08, "ThresholdedExactMatch08AGOP", "OP", "exact match", "AG", 0.8,
                                              include_average=True, avg_score=avg_em_op_ag08)
    avg_em_op_ag08_tup = ("Translation-Based", avg_em_op_ag08)

    em_op_nl08 = [threshold_exact_match(ent[0], ent[1], 0.8) for ent in ent_gold_system_tup_list_op_nl]
    avg_em_op_nl08 = get_avg_metric_score("exact match", em_op_nl08)
    thresholded_entity_score_tuple_list_2_txt(em_op_nl08, "ThresholdedExactMatch08NLOP", "OP", "exact match", "NL", 0.8,
                                              include_average=True, avg_score=avg_em_op_nl08)
    avg_em_op_nl08_tup = ("Human-Generated", avg_em_op_nl08)
    em_08_averages_op = [avg_em_op_bl08_tup, avg_em_op_ag08_tup, avg_em_op_nl08_tup]
    plot_averages(em_08_averages_op, "Exact Match averages for Object Position with threshold 0.8- (?, r, e)")
