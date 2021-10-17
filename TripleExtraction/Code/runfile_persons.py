from triple_extractor_cluster import TripleExtractor

# get all entities of Persons
entity_obj_sp = TripleExtractor("Person", "SP")
# load the entity-text tuple list for the first batch of Person
entities_sp = entity_obj_sp.load_entity_text_list(persons_full=False, persons_file_num=1)
# load the Baseline questions for Person
entity_questions_sp = entity_obj_sp.load_questions("BL")
# load all properties for Person
entity_properties_sp = entity_obj_sp.load_properties()

# extract the triples by calling the QA-system and passing entities, the respective questions and propertie as input
entity_res_list_sp = [entity_obj_sp.extract_triples(entity, entity_questions_sp, entity_properties_sp) for entity in entities_sp]
# save result dicts for each entity in json Files
entity_obj_sp.dict_list2json(entity_res_list_sp, "BL")


# same procedure for Object position
entity_obj_op = TripleExtractor("Building", "OP")
entities_op = entity_obj_op.load_entity_text_list(persons_full=False, persons_file_num=1)
entity_questions_op = entity_obj_op.load_questions("BL")
entity_properties_op = entity_obj_op.load_properties()

entity_res_list_op = [entity_obj_op.extract_triples(entity, entity_questions_op, entity_properties_op) for entity in entities_op]
entity_obj_op.dict_list2json(entity_res_list_op, "BL")
