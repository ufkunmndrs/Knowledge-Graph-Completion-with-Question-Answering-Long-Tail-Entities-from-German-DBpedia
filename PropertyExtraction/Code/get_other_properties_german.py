import os
from property_handler import PropertyHandler


# properties for Buildings

# noinspection PyGlobalUndefined


def get2translate_and_exists_files(filepath: str, csv_filename: str, to_translate_filename: str,
                                   exists_filename: str, outputpath: str, write_only=True):
    """
    accesses and retrieves property csv files with German labels and where German labels don't exist
    Parameters
    ----------
    filepath: str
        path where csv files are stored
    csv_filename: str
        name of the respective csv file
    to_translate_filename: str
        name of the file where the properties which need translation are stored
    exists_filename: str
        name of the file for which a translation of the properties exist
    outputpath: str
        path of the output txt file
    write_only: bool
        determines whether only a txt file will be written or a list of properties with their translation will be
        returned

    Returns
    -------
    properties_wt: list
        List containing the properties with translations

    """
    global default_other_handler
    properties_file = os.path.join(filepath, csv_filename)
    default_other_handler = PropertyHandler(properties_file, persons=False)
    properties_nt = default_other_handler.propertycsv2list()
    properties_wt = default_other_handler.propertycsv2list(no_translation=False)
    default_other_handler.write_property_file(properties_nt, to_translate_filename, path=outputpath)
    default_other_handler.write_property_file(properties_wt, exists_filename, path=outputpath)
    if write_only is not True:
        return properties_wt


def get_translated_properties(to_tranlsatefilename: str, translated_properties: list, properties_filename: str,
                              txtfilepath: str):
    """
    retrieves the properties translated from English to German.

    Parameters
    ----------
    to_tranlsatefilename: str
        name of the file which needs its properties translated
    translated_properties: list
        list of translated properties
    properties_filename: str
        name of the properties file
    txtfilepath: str
        path where the txt file will be stored

    Returns
    -------
    None
    """
    default_other_handler.full_properties(to_tranlsatefilename, translated_properties, write2file=True,
                                          properties_filename=properties_filename, path=txtfilepath)


general_other_filepath = "C:/Users/ubmen/Desktop/BA_Prog/PropertyExtraction/Properties/OtherProperties/"
# Buildings, SP and OP
buildings_filepaths = general_other_filepath + "BuildingProperties/BuildingPropertiesCSVFiles/"
buildings_txtpath = general_other_filepath + "BuildingProperties/BuildingPropertiesTXTFiles/"
buildings_sp = "BuildingPropertiesSP.csv"
buildings_sp_wt = get2translate_and_exists_files(buildings_filepaths, buildings_sp, "BuildingPropertiesNtSP.txt",
                                                 "BuildingPropertiesExistsSP.txt", buildings_txtpath,
                                                 write_only=False)
get_translated_properties("BuildingPropertiesNtSP.txt", buildings_sp_wt, "BuildingTotalPropertiesSP.txt",
                          buildings_txtpath)

buildings_op = "BuildingPropertiesOP.csv"
buildings_op_wt = get2translate_and_exists_files(buildings_filepaths, buildings_op, "BuildingPropertiesNtOP.txt",
                                                 "BuildingPropertiesExistsOP.txt",
                                                 buildings_txtpath, write_only=False)
get_translated_properties("BuildingPropertiesNtOP.txt", buildings_op_wt, "BuildingTotalPropertiesOP.txt",
                          buildings_txtpath)


# Diseases, SP and OP
diseases_filepath = general_other_filepath + "DiseaseProperties/DiseasePropertiesCSVFiles/"
diseases_txtpath = general_other_filepath + "DiseaseProperties/DiseasePropertiesTXTFiles/"
diseases_sp = "DiseasePropertiesSP.csv"
diseases_sp_wt = get2translate_and_exists_files(diseases_filepath, diseases_sp, "DiseasePropertiesNtSP.txt",
                                                "DiseasePropertiesExistsSP.txt", diseases_txtpath, write_only=False)
get_translated_properties("DiseasePropertiesNtSP.txt", diseases_sp_wt, "DiseaseTotalPropertiesSP.txt",
                          diseases_txtpath)

diseases_op = "DiseasePropertiesOP.csv"
diseases_op_wt = get2translate_and_exists_files(diseases_filepath, diseases_op, "DiseasePropertiesNtOP.txt",
                                                "DiseasePropertiesExistsOP.txt", diseases_txtpath, write_only=False)
get_translated_properties("DiseasePropertiesNtOP.txt", diseases_op_wt, "DiseaseTotalPropertiesOP.txt",
                          diseases_txtpath)

# History Properties
history_filepath = general_other_filepath + "HistoryProperties/HistoryPropertiesCSVFiles/"
history_txtpath = general_other_filepath + "HistoryProperties/HistoryPropertiesTXTFiles/"
history_sp = "HistoryPropertiesSP.csv"
history_sp_wt = get2translate_and_exists_files(history_filepath, history_sp, "HistoryPropertiesNtSP.txt",
                                               "HistoryPropertiesExistsSP.txt", history_txtpath, write_only=False)
get_translated_properties("HistoryPropertiesNtSP.txt", history_sp_wt, "HistoryTotalPropertiesSP.txt",
                          history_txtpath)

history_op = "HistoryPropertiesOP.csv"
history_op_wt = get2translate_and_exists_files(history_filepath, history_op, "HistoryPropertiesNtOP.txt",
                                               "HistoryPropertiesExistsOP.txt", history_txtpath, write_only=False)
get_translated_properties("HistoryPropertiesNtOP.txt", history_op_wt, "HistoryTotalPropertiesOP.txt",
                          history_txtpath)

# Literature Properties
lit_filepath = general_other_filepath + "LiteratureProperties/LiteraturePropertiesCSVFiles/"
lit_txtpath = general_other_filepath + "LiteratureProperties/LiteraturePropertiesTXTFiles/"
lit_sp = "LiteraturePropertiesSP.csv"
lit_sp_wt = get2translate_and_exists_files(lit_filepath, lit_sp, "LiteraturePropertiesNtSP.txt",
                                           "LiteraturePropertiesExistsSP.txt", lit_txtpath, write_only=False)
get_translated_properties("LiteraturePropertiesNtSP.txt", lit_sp_wt, "LiteratureTotalPropertiesSP.txt",
                          lit_txtpath)

lit_op = "LiteraturePropertiesOP.csv"
lit_op_wt = get2translate_and_exists_files(lit_filepath, lit_op, "LiteraturePropertiesNtOP.txt",
                                           "LiteraturePropertiesExistsOP.txt", lit_txtpath, write_only=False)
get_translated_properties("LiteraturePropertiesNtOP.txt", lit_op_wt, "LiteratureTotalPropertiesOP.txt",
                          lit_txtpath)

# Magazine Properties
mag_filepath = general_other_filepath + "MagazineProperties/MagazinePropertiesCSVFiles/"
mag_txtpath = general_other_filepath + "MagazineProperties/MagazinePropertiesTXTFiles/"
mag_sp = "MagazinePropertiesSP.csv"
mag_sp_wt = get2translate_and_exists_files(mag_filepath, mag_sp, "MagazinePropertiesNtSP.txt",
                                           "MagazinePropertiesExistsSP.txt", mag_txtpath, write_only=False)
get_translated_properties("MagazinePropertiesNtSP.txt", mag_sp_wt, "MagazineTotalPropertiesSP.txt", mag_txtpath)

mag_op = "MagazinePropertiesOP.csv"
mag_op_wt = get2translate_and_exists_files(mag_filepath, mag_op, "MagazinePropertiesNtOP.txt",
                                           "MagazinePropertiesExistsOP.txt", mag_txtpath, write_only=False)
get_translated_properties("MagazinePropertiesNtOP.txt", mag_op_wt, "MagazineTotalPropertiesOP.txt", mag_txtpath)

# Newspaper Properties
nw_filepath = general_other_filepath + "NewspaperProperties/NewspaperPropertiesCSVFiles/"
nw_txtpath = general_other_filepath + "NewspaperProperties/NewspaperPropertiesTXTFiles/"
nw_sp = "NewspaperPropertiesSP.csv"
nw_sp_wt = get2translate_and_exists_files(nw_filepath, nw_sp, "NewspaperPropertiesNtSP.txt",
                                          "NewspaperPropertiesExistsSP.txt", nw_txtpath, write_only=False)
get_translated_properties("NewspaperPropertiesNtSP.txt", nw_sp_wt, "NewspaperTotalPropertiesSP.txt", nw_txtpath)

nw_op = "NewspaperPropertiesOP.csv"
nw_op_wt = get2translate_and_exists_files(nw_filepath, nw_op, "NewspaperPropertiesNtOP.txt",
                                          "NewspaperPropertiesExistsOP.txt", nw_txtpath, write_only=False)
get_translated_properties("NewspaperPropertiesNtOP.txt", nw_op_wt, "NewspaperTotalPropertiesOP.txt", nw_txtpath)


# Organization Properties
org_filepath = general_other_filepath + "OrganizationProperties/OrganizationPropertiesCSVFiles/"
org_txtpath = general_other_filepath + "OrganizationProperties/OrganizationPropertiesTXTFiles/"
org_sp = "OrganizationPropertiesSP.csv"
org_sp_wt = get2translate_and_exists_files(org_filepath, org_sp, "OrganizationPropertiesNtSP.txt",
                                           "OrganizationPropertiesExistsSP.txt", org_txtpath, write_only=False)
get_translated_properties("OrganizationPropertiesNtSP.txt", org_sp_wt, "OrganizationTotalPropertiesSP.txt",
                          org_txtpath)

org_op = "OrganizationPropertiesOP.csv"
org_op_wt = get2translate_and_exists_files(org_filepath, org_op, "OrganizationPropertiesNtOP.txt",
                                           "OrganizationPropertiesExistsOP.txt", org_txtpath, write_only=False)
get_translated_properties("OrganizationPropertiesNtOP.txt", org_op_wt, "OrganizationTotalPropertiesOP.txt",
                          org_txtpath)


# Park Properties
park_filepath = general_other_filepath + "ParkProperties/ParkPropertiesCSVFiles/"
park_txtpath = general_other_filepath + "ParkProperties/ParkPropertiesTXTFiles/"
park_sp = "ParkPropertiesSP.csv"
park_sp_wt = get2translate_and_exists_files(park_filepath, park_sp, "ParkPropertiesNtSP.txt",
                                            "ParkPropertiesExistsSP.txt", park_txtpath, write_only=False)
get_translated_properties("ParkPropertiesNtSP.txt", park_sp_wt, "ParkTotalPropertiesSP.txt", park_txtpath)

park_op = "ParkPropertiesOP.csv"
park_op_wt = get2translate_and_exists_files(park_filepath, park_op, "ParkPropertiesNtOP.txt",
                                            "ParkPropertiesExistsOP.txt", park_txtpath, write_only=False)
get_translated_properties("ParkPropertiesNtOP.txt", park_op_wt, "ParkTotalPropertiesOP.txt", park_txtpath)


# School Properties
sch_filepath = general_other_filepath + "SchoolProperties/SchoolPropertiesCSVFiles/"
sch_txtpath = general_other_filepath + "SchoolProperties/SchoolPropertiesTXTFiles/"
sch_sp = "SchoolPropertiesSP.csv"
sch_sp_wt = get2translate_and_exists_files(sch_filepath, sch_sp, "SchoolPropertiesNtSP.txt",
                                           "SchoolPropertiesExistsSP.txt", sch_txtpath, write_only=False)
get_translated_properties("SchoolPropertiesNtSP.txt", sch_sp_wt, "SchoolTotalPropertiesSP.txt", sch_txtpath)

sch_op = "SchoolPropertiesOP.csv"
sch_op_wt = get2translate_and_exists_files(sch_filepath, sch_op, "SchoolPropertiesNtOP.txt",
                                           "SchoolPropertiesExistsOP.txt", sch_txtpath, write_only=False)
get_translated_properties("SchoolPropertiesNtOP.txt", sch_op_wt, "SchoolTotalPropertiesOP.txt", sch_txtpath)


# Ship Properties, finally
ship_filepath = general_other_filepath + "ShipProperties/ShipPropertiesCSVFiles/"
ship_txtpath = general_other_filepath + "ShipProperties/ShipPropertiesTXTFiles/"
ship_sp = "ShipPropertiesSP.csv"
ship_sp_wt = get2translate_and_exists_files(ship_filepath, ship_sp, "ShipPropertiesNtSP.txt",
                                            "ShipPropertiesExistsSP.txt", ship_txtpath, write_only=False)
get_translated_properties("ShipPropertiesNtSP.txt", ship_sp_wt, "ShipTotalPropertiesSP.txt", ship_txtpath)

ship_op = "ShipPropertiesOP.csv"
ship_op_wt = get2translate_and_exists_files(ship_filepath, ship_op, "ShipPropertiesNtOP.txt",
                                            "ShipPropertiesExistsOP.txt", ship_txtpath, write_only=False)
get_translated_properties("ShipPropertiesNtOP.txt", ship_op_wt, "ShipTotalPropertiesOP.txt", ship_txtpath)
