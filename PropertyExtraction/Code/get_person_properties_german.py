import os
from property_handler import PropertyHandler

# filepath, same for both csv files
filepath = "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/PersonProperties/PersonPropertiesCSVFiles"
# get properties with German translation and without where the entity is in a subject position
subject_properties_file = os.path.join(filepath, "PersonPropertiesSubject.csv")
sp_entity_handler = PropertyHandler(subject_properties_file)
# no input necessary here, as the csv file will be transformed into a list already by calling this function
# each row will be a tuple where each element corresponds to a column entry in a row
subject_properties_no_translation = sp_entity_handler.propertycsv2list()
subject_properties_translation_exists = sp_entity_handler.propertycsv2list(no_translation=False)
sp_entity_handler.write_property_file(subject_properties_no_translation, "PersonNoTranslationPropertiesSP.txt")
sp_entity_handler.write_property_file(subject_properties_translation_exists, "PersonTranslationExistsSP.txt")

# same for entities at object position
object_properties_file = os.path.join(filepath, "PersonPropertiesObject.csv")
op_entity_handler = PropertyHandler(object_properties_file)
object_properties_no_translation = op_entity_handler.propertycsv2list()
object_properties_translation_exists = op_entity_handler.propertycsv2list(no_translation=False)
op_entity_handler.write_property_file(object_properties_no_translation, "PersonNoTranslationPropertiesOP.txt")
op_entity_handler.write_property_file(object_properties_translation_exists, "PersonTranslationExistsOP.txt")

########################################################################################################################
#            Translate the properties that need translation for both Subject Position and Object Position              #
########################################################################################################################

# Translate Subject Properties
filename_sp = "PersonNoTranslationPropertiesSP.txt"
# sp_list = sp_entity_handler.read_txt(filename_sp)
# sp_list_translated = sp_entity_handler.translate_properties(sp_list, return_tuple_list=True)
# sp_entity_handler.write_property_file(sp_list_translated, "PropertiesTranslatedSP.txt")
sp_entity_handler.full_properties(filename_sp, subject_properties_translation_exists, write2file=True,
                                  properties_filename="PersonTotalPropertiesSP.txt")


# Translate Object Properties
filename_op = "PersonNoTranslationPropertiesOP.txt"
op_list = op_entity_handler.read_txt(filename_op)
# op_list_translated = op_entity_handler.translate_properties(op_list, return_tuple_list=True)
# op_entity_handler.write_property_file(op_list_translated, "PropertiesTranslatedOP.txt")
op_entity_handler.full_properties(filename_op, object_properties_translation_exists, write2file=True,
                                  properties_filename="PersonTotalPropertiesOP.txt")
