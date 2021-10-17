import pandas as pd
import os
import json


def tuple_list_to_dict(entity_name: str, tuple_list: list):
    """
    Converts of list of tuples, where each tuple consists of the entity name as first element of the tuple
    and the answer dict as second element of tuple to a dictionary where key is the entity name, and the value
    is yet another dictionary where keys are the predicates and the values are the retrieved answers
    Parameters
    ----------
    entity_name: str
        name of an entity in the gold standard set
    tuple_list: list
        list of dicts as described above

    Returns
    -------
    final_dict: dict
        Dictionary as described above
    """
    single_entity_list = []
    final_dict = {}
    for entity in tuple_list:
        if entity_name == entity[0]:
            single_entity_list.append(entity)
    pred_obj_entity_list = [tup[1] for tup in single_entity_list]
    pred_obj_dict_of_dicts = dict((key, d[key]) for d in pred_obj_entity_list for key in d)
    final_dict[entity_name] = pred_obj_dict_of_dicts
    return final_dict


def list_of_dict2json(filename: str, list_of_dicts: list):
    """
    Converts a list of dictionaries to a json file

    Parameters
    ----------
    filename: str
        Designated filename for the .json file
    list_of_dicts: list
        A list containing the nested dictionaries

    Returns
    -------
    None
    """
    json_path = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/JSONFiles/"
    filename += ".json"
    with open(os.path.join(json_path, filename), 'w', encoding="utf-8-sig") as f:
        for file in list_of_dicts:
            json.dump(file, f, ensure_ascii=False)
            f.write("\n")
        f.close()


# Subject and Object position have to be processed differently, as the respective gold standard values require different
# methods of preprocessing, hence why a function won't be necessary and sufficient
gs_file_sp = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/ExcelAndCSVFiles/GoldStandardSP.xlsx"
gs_df_sp = pd.read_excel(gs_file_sp)
gs_df_sp.to_csv("C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/ExcelAndCSVFiles/GoldStandardSPmod.csv",
                index=False, encoding="utf-8-sig")
gs_df_sp = pd.read_csv("C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/"
                       "ExcelAndCSVFiles/GoldStandardSPmod.csv")
# drop last column (that one only necessary for excel=
gs_df_sp = gs_df_sp.iloc[:, :-1]
subject_entities_sp = gs_df_sp["Subject"].to_list()
# gold standard entity list for less hardcoding
gs_entities = list(set(subject_entities_sp))
predicates_sp = gs_df_sp["Predicate"].to_list()
object_entities_sp = gs_df_sp["Object"].to_list()
object_entities_sp = [str(obj) for obj in object_entities_sp]
predicate_object_only = list(zip(predicates_sp, object_entities_sp))
forbidden_words = ["Höhe", "Breite", "nachfolgende Arbeiten", "basierend auf", "Länge"]
# split at tab since this character does not exist -> anything involving a comma will be preserved as one string
pred_obj_list_fin = [(tup[0], tup[1].split("\t")) if any(w in tup[0] for w in forbidden_words)
                     else (tup[0], tup[1].split(",")) for tup in predicate_object_only]
processed_obj_list = [list(map(str.strip, tup[1])) for tup in pred_obj_list_fin]
processed_pred_obj_list = list(zip(predicates_sp, processed_obj_list))
processed_obj_dict_list = [{"answer": obj[1]} for obj in processed_pred_obj_list]
final_pred_obj_list = list(zip(predicates_sp, processed_obj_dict_list))
final_pred_obj_dict_list = [{k: v} for (k, v) in final_pred_obj_list]
joint_list_sp = list(zip(subject_entities_sp, final_pred_obj_dict_list))


# same now for Object position
gs_file_op = "C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/ExcelAndCSVFiles/GoldStandardOP.xlsx"
gs_df_op = pd.read_excel(gs_file_op, encoding="utf-8-sig")
gs_df_op.to_csv("C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/ExcelAndCSVFiles/GoldStandardOPmod.csv",
                index=False, encoding="utf-8-sig")
gs_df_op = pd.read_csv("C:/Users/ubmen/Desktop/BA_Prog/Evaluation/GoldStandardFiles/ExcelAndCSVFiles/GoldStandardOPmod.csv")
subject_entities_op = gs_df_op["Subject"].to_list()
subject_entities_op = [str(sub) for sub in subject_entities_op]
predicates_op = gs_df_op["Predicate"].to_list()
object_entities_op = gs_df_op["Object"].to_list()
predicate_subject_only = list(zip(subject_entities_op, predicates_op))
predicate_subject_only = [(tup[1], tup[0].split("\t")) if any(w in tup[1] for w in forbidden_words)
                          else (tup[1], tup[0].split(",")) for tup in predicate_subject_only]
processed_subj_list = [list(map(str.strip, tup[1])) for tup in predicate_subject_only]
processed_pred_subj_list = list(zip(predicates_op, processed_subj_list))
processed_subj_dict_list = [{"answer": subj[1]} for subj in processed_pred_subj_list]
final_pred_subj_list = list(zip(predicates_op, processed_subj_dict_list))
final_pred_subj_dict_list = [{k: v} for (k, v) in final_pred_subj_list]
joint_list_op = list(zip(object_entities_op, final_pred_subj_dict_list))


gs_dict_list_sp = [tuple_list_to_dict(entity, joint_list_sp) for entity in gs_entities]
gs_dict_list_op = [tuple_list_to_dict(entity, joint_list_op) for entity in gs_entities]

list_of_dict2json("GoldStandardSP", gs_dict_list_sp)
list_of_dict2json("GoldStandardOP", gs_dict_list_op)

