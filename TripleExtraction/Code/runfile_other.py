from triple_extractor_cluster import TripleExtractor

entity_obj_sp = TripleExtractor("Building", "SP")
entities_sp = entity_obj_sp.load_entity_text_list()
entity_questions_sp = entity_obj_sp.load_questions("BL")
entity_properties_sp = entity_obj_sp.load_properties()

entity_res_list_sp = [entity_obj_sp.extract_triples(entity, entity_questions_sp, entity_properties_sp) for entity in entities_sp]
entity_obj_sp.dict_list2json(entity_res_list_sp, "BL")

entity_obj_op = TripleExtractor("Building", "OP")
entities_op = entity_obj_op.load_entity_text_list()
entity_questions_op = entity_obj_op.load_questions("BL")
entity_properties_op = entity_obj_op.load_properties()

entity_res_list_op = [entity_obj_op.extract_triples(entity, entity_questions_op, entity_properties_op) for entity in entities_op]
entity_obj_op.dict_list2json(entity_res_list_op, "BL")
