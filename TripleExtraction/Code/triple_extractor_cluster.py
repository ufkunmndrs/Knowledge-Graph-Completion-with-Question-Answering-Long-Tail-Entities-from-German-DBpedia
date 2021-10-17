import os
import ast
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import json

# model_name = "deepset/roberta-base-squad2"
# model_name = "Sahajtomar/GBERTQnA"
# model_name = "dbmdz/bert-base-german-uncased"
model_name = "Sahajtomar/GELECTRAQA"
# model_name = "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/"
# model_name = "/home/students/menderes/venv/GELECTRA Model/"
# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


class TripleExtractor:
    def __init__(self, category_type: str, entity_position):
        self.category_type = category_type
        self.entity_position = entity_position

    def load_entity_text_list(self, persons_full=False, persons_file_num=None):
        valid_persons_file_nums = [1, 2, 3, 4, None]
        if persons_file_num not in valid_persons_file_nums:
            raise ValueError("Incorrect input number for persons file, must be between 1 and 4 or of type None")
        plural_entities = ["Building", "Disease", "Magazine", "Organization", "Park", "School", "Ship"]
        entity_filepath = "../TripleExtraction/PreprocessedTXTFiles/"
        if self.category_type != "Person" and self.category_type not in plural_entities:
            entity_filepath += "OtherWikiTXT/" + self.category_type + "WikiTXT/" + self.category_type + "WikiTXT.txt"
        elif self.category_type != "Person" and self.category_type in plural_entities:
            entity_filepath += "OtherWikiTXT/" + self.category_type + "sWikiTXT/" + self.category_type + "sWikiTXT.txt"
        elif self.category_type == "Person" and persons_full is True:
            entity_filepath += "PersonsWikiTXT/PersonsFullWikiTXT.txt"
        elif self.category_type == "Person" and type(persons_file_num) == "int":
            entity_filepath += "PersonsWikiTXT/PersonsWikiTXT" + str(persons_file_num) + ".txt"
        with open(entity_filepath, encoding="utf-8") as f:
            entity_text_tuple_list = f.readlines()
            entity_text_tuple_list = [line.strip() for line in entity_text_tuple_list]
            entity_text_tuple_list = [ast.literal_eval(tup) for tup in entity_text_tuple_list]
        return entity_text_tuple_list

    def load_questions(self, question_type: str):
        question_file = "../QuestionGeneration/"
        if self.category_type != "Person":
            question_file += "OtherQuestions/"
            if question_type == "AG":
                question_file += "OtherQuestionsAG/" + self.category_type + "QuestionsAG/"
                if self.entity_position == "SP":
                    question_file += self.category_type + "QuestionsSP_AG.txt"
                elif self.entity_position == "OP":
                    question_file += self.category_type + "QuestionsOP_AG.txt"
            elif question_type == "BL":
                question_file += "OtherQuestionsBL/" + self.category_type + "QuestionsBL/"
                if self.entity_position == "SP":
                    question_file += self.category_type + "QuestionsSP_BL.txt"
                elif self.entity_position == "OP":
                    question_file += self.category_type + "QuestionsOP_BL.txt"
            elif question_type == "NL":
                question_file += "OtherQuestionsNL/" + self.category_type + "QuestionsNL/"
                if self.entity_position == "SP":
                    question_file += self.category_type + "QuestionsSP_NL.txt"
                elif self.entity_position == "OP":
                    question_file += self.category_type + "QuestionsOP_NL.txt"
        else:
            question_file += "PersonQuestions/"
            if question_type == "AG":
                if self.entity_position == "SP":
                    question_file += "PersonQuestionsAG/PersonQuestionsSP_AG.txt"
                elif self.entity_position == "OP":
                    question_file += "PersonQuestionsAG/PersonQuestionsOP_AG.txt"
            elif question_type == "BL":
                if self.entity_position == "SP":
                    question_file += "PersonQuestionsBL/PersonQuestionsSP_BL.txt"
                elif self.entity_position == "OP":
                    question_file += "PersonQuestionsBL/PersonQuestionsOP_BL.txt"
            elif question_type == "NL":
                if self.entity_position == "SP":
                    question_file += "PersonQuestionsNL/PersonQuestionsSP_NL.txt"
                elif self.entity_position == "OP":
                    question_file += "PersonQuestionsNL/PersonQuestionsOP_NL.txt"
        with open(question_file, encoding="utf-8-sig") as f:
            questions = f.readlines()
            questions = [line.strip() for line in questions]
        return questions

    def load_properties(self):
        properties_file = "../PropertyExtraction/Properties/"
        if self.category_type != "Person":
            properties_file += "OtherProperties/" + self.category_type + "Properties/" + self.category_type
            properties_file += "PropertiesTXTFiles/" + self.category_type + "TotalProperties" + self.entity_position + ".txt"
        else:
            properties_file += "PersonProperties/PersonPropertiesTXTFiles/PersonTotalProperties" + self.entity_position + ".txt"
        with open(properties_file, encoding="utf-8-sig") as f:
            properties = f.readlines()
            properties = [line.strip() for line in properties]
            properties = [ast.literal_eval(tup) for tup in properties]
        return properties

    @staticmethod
    def extract_triples(entity_context_tuple: tuple, questions_list: list, predicate_list: list):
        if len(questions_list) != len(predicate_list):
            raise ValueError("Questions and lengths have different lengths, they are most likely "
                             "incompatible!")
        entity = entity_context_tuple[0]
        context = entity_context_tuple[1]
        questions_updated = [q.replace("__", entity) for q in questions_list]
        german_predicate_list = [tup[0] for tup in predicate_list]
        dict_of_dicts = {}
        final_dict = {}
        i = 0
        for q in questions_updated:
            # print(q)
            q_dict = {'question': q, "context": context}
            q_dict_nlp = nlp(q_dict)
            result_dict = {'answer': q_dict_nlp['answer'], 'score': q_dict_nlp['score']}
            dict_of_dicts[german_predicate_list[i]] = result_dict
            i += 1
        final_dict[entity] = dict_of_dicts
        return final_dict

    def dict_list2json(self, list_of_dicts: list, question_type: str):
        global filename
        plural_entities = ["Building", "Disease", "Magazine", "Organization", "Park", "School", "Ship"]
        json_path = "../TripleExtraction/Results/"
        if self.category_type != "Person" and self.category_type not in plural_entities:
            json_path += "OtherResults/" + self.category_type + "Results/"
            filename = self.category_type + "Results" + self.entity_position + "withQuestions" + question_type + ".json"
        elif self.category_type != "Person" and self.category_type in plural_entities:
            json_path += "OtherResults/" + self.category_type + "sResults/"
            filename = self.category_type + "sResults" + self.entity_position + "withQuestions" + question_type + ".json"
        elif self.category_type == "Person":
            json_path += "PersonResults"
            filename = "PersonsResults" + self.entity_position + "withQuestions" + question_type + ".json"
        with open(os.path.join(json_path, filename), 'w', encoding="utf-8-sig") as f:
            for file in list_of_dicts:
                json.dump(file, f, ensure_ascii=False)
                f.write("\n")
            f.close()
