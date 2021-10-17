# -*- coding: utf-8 -*-
"""
Created on May 29th 19:30:00 2021

@author: Ufkun-Bayram Menderes

This Python file analyzes the specific categories of those Wikipedia articles/entities that were classified as "other"
in broader detail and provides some plots for better visualization. The datafiles containing the articles/entities have
to be loaded first.

This file contains the following functions:
    * other_category_specific: gets the specific category for entities within "other"
    * plot_categories: plots the given categories for better visualization
    * chunks: chunks a list into parts of n elements. Is needed for better data visualization
"""
import os.path

import matplotlib.pyplot as plt
from category_analyzer import CategoryAnalyzer

other_analyzer = CategoryAnalyzer("C:/Users/ubmen/Desktop/BA_Prog/DataExploration/CSVFiles/AllArticles/Other.csv")
other_all_list = other_analyzer.preprocess()


def other_category_specific(titles_categories: list, category_type: str):
    """

    Parameters
    ----------
    titles_categories
    category_type

    Returns
    -------
    the list specified in category_types string
    unfortunately, due to the very specific nature of the categories, this requires some hardcoding
    """
    valid_category_types = ["building", "club", "prize", "street", "literature", "magazine", "borough",
                            "politics", "company", "newspaper", "bridge", "school", "organisation", "process",
                            "bank", "sport", "corps", "history", "gastronomy", "government", "nature", "museum",
                            "culture", "diplomacy", "vocation", "cafe", "architecture", "park", "memorial", "music",
                            "ship", "cemetary", "geography", "justice", "illness"]
    # specifying all possible cases and categories unfortunately requires some hardcoding
    if category_type not in valid_category_types:
        raise ValueError("Input must be from a valid category")
    titles = []
    for pairs in titles_categories:
        if any("bauwerk" in word.lower() for word in pairs[1]) and category_type == "building":
            titles.append(pairs)
        elif any("verein" in word.lower() for word in pairs[1]) and category_type == "club":
            titles.append(pairs)
        elif any("preis" in word.lower() for word in pairs[1]) and category_type == "prize":
            titles.append(pairs)
        elif any("straße" in word.lower() for word in pairs[1]) and category_type == "street":
            titles.append(pairs)
        elif any("stadtteil" in word.lower() for word in pairs[1]) and category_type == "borough":
            titles.append(pairs)
        elif any("literatur" in word.lower() for word in pairs[1]) and category_type == "literature":
            titles.append(pairs)
        elif any("zeitschrift" in word for word in pairs[1]) and category_type == "magazine":
            titles.append(pairs)
        elif any("politik" in word.lower() for word in pairs[1]) and category_type == "politics":
            titles.append(pairs)
        elif any("Unternehmen" in word for word in pairs[1]) and category_type == "company":
            titles.append(pairs)
        elif any("Zeitung" in word for word in pairs[1]) and category_type == "newspaper":
            titles.append(pairs)
        elif any("Brücke" in word for word in pairs[1]) and category_type == "bridge":
            titles.append(pairs)
        elif any("Schul" in word for word in pairs[1]) and category_type == "school":
            titles.append(pairs)
        elif any("organisation" in word.lower() for word in pairs[1]) and category_type == "organisation":
            titles.append(pairs)
        elif any("Diplomatie" in word for word in pairs[1]) and category_type == "diplomacy":
            titles.append(pairs)
        elif any("Sport" in word for word in pairs[1]) and category_type == "sport":
            titles.append(pairs)
        elif any("Natur" in word for word in pairs[1]) and category_type == "nature":
            titles.append(pairs)
        elif any("Verfahren" in word for word in pairs[1]) and category_type == "process":
            titles.append(pairs)
        elif any("Berufsbildung" in word for word in pairs[1]) and category_type == "vocation":
            titles.append(pairs)
        elif any("Gastronomiebetrieb" in word for word in pairs[1]) and category_type == "gastronomy":
            titles.append(pairs)
        elif any("Kreditinstitut" in word for word in pairs[1]) and category_type == "bank":
            titles.append(pairs)
        elif any("Café" in word for word in pairs[1]) and category_type == "cafe":
            titles.append(pairs)
        elif any("Geschichte" in word for word in pairs[1]) and category_type == "history":
            titles.append(pairs)
        elif any("Corps" in word for word in pairs[1]) and category_type == "corps":
            titles.append(pairs)
        elif any("Museum" in word for word in pairs[1]) and category_type == "museum":
            titles.append(pairs)
        elif any("Kultur" in word for word in pairs[1]) and category_type == "culture":
            titles.append(pairs)
        elif any("Architekt" in word for word in pairs[1]) and category_type == "architecture":
            titles.append(pairs)
        elif any("Park" in word for word in pairs[1]) and category_type == "park":
            titles.append(pairs)
        elif any("Brücke" in word for word in pairs[1]) and category_type == "bridge":
            titles.append(pairs)
        elif any("denkmal" in word.lower() for word in pairs[1]) and category_type == "memorial":
            titles.append(pairs)
        elif any("Musik" in word for word in pairs[1]) and category_type == "music":
            titles.append(pairs)
        elif any("Schiff" in word for word in pairs[1]) and category_type == "ship":
            titles.append(pairs)
        elif any("Friedhof" in word for word in pairs[1]) and category_type == "cemetary":
            titles.append(pairs)
        elif any("Geographie" in word for word in pairs[1]) and category_type == "geography":
            titles.append(pairs)
        elif any("Justiz" in word for word in pairs[1]) and category_type == "justice":
            titles.append(pairs)
        elif any("Parasit" in word for word in pairs[1]) and category_type == "illness":
            titles.append(pairs)
    return titles


def plot_categories(category_list: list):
    """
    Function to plot specific categories of type "other"
    Parameters
    ----------
    category_list: list
        List with tuples where first element is the list of category types and second element is the length of that
        list

    Returns
    -------
    just plots the figures
    """
    y_pos = len(other_all_list)
    plt.ylim(0, len(other_all_list))
    plt.title("Category statistics for all articles of category 'other")
    plt.ylabel("Other Articles total")
    plt.xlabel("Total amount of candidate DE articles/entities as 'other': " f"{len(other_all_list)}")
    x = [elem[0] for elem in category_list]
    y = [elem[1] for elem in category_list]
    for index, value in enumerate(y):
        plt.text(index, value, str(value))
    plt.bar(x, y, width=0.5)
    plt.show()


def chunks(lst: list, n: int):
    """
    chunks a list into n even parts

    Parameters
    ----------
    lst: list
        Any arbitrary list that can contain any arbitrary datastructure
    n: int
        Size of the chunks
    Returns
    -----------
    a list of n sized chunks from the original input list lst
    -------

    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


list_lengths = []
buildings = other_category_specific(other_all_list, "building")
list_lengths.append(("Buildings", len(buildings)))

clubs = other_category_specific(other_all_list, "club")
list_lengths.append(("Clubs", len(clubs)))

prizes = other_category_specific(other_all_list, "prize")
list_lengths.append(("Prizes", len(prizes)))

literature = other_category_specific(other_all_list, "literature")
list_lengths.append(("Literature", len(literature)))

magazines = other_category_specific(other_all_list, "magazine")
list_lengths.append(("Magazines", len(magazines)))

politics = other_category_specific(other_all_list, "politics")
list_lengths.append(("Politics", len(politics)))

newspaper = other_category_specific(other_all_list, "newspaper")
list_lengths.append(("Newspapers", len(newspaper)))

diplomacy = other_category_specific(other_all_list, "diplomacy")
list_lengths.append(("Diplomacy", len(diplomacy)))

nature = other_category_specific(other_all_list, "nature")
list_lengths.append(("Nature", len(nature)))

process = other_category_specific(other_all_list, "process")
list_lengths.append(("Process", len(process)))

companies = other_category_specific(other_all_list, "company")
vocational = other_category_specific(other_all_list, "vocation")
gastros = other_category_specific(other_all_list, "gastronomy")
cafes = other_category_specific(other_all_list, "cafe")
sport = other_category_specific(other_all_list, "sport")
banks = other_category_specific(other_all_list, "bank")
streets = other_category_specific(other_all_list, "street")
history = other_category_specific(other_all_list, "history")
corps = other_category_specific(other_all_list, "corps")
schools = other_category_specific(other_all_list, "school")
museums = other_category_specific(other_all_list, "museum")
culture = other_category_specific(other_all_list, "culture")
orgs = other_category_specific(other_all_list, "organisation")
architecture = other_category_specific(other_all_list, "architecture")
bridges = other_category_specific(other_all_list, "bridge")
parks = other_category_specific(other_all_list, "park")
memorials = other_category_specific(other_all_list, "memorial")
music = other_category_specific(other_all_list, "music")
ships = other_category_specific(other_all_list, "ship")
cemetaries = other_category_specific(other_all_list, "cemetary")
geography = other_category_specific(other_all_list, "geography")
justice = other_category_specific(other_all_list, "justice")
diseases = other_category_specific(other_all_list, "illness")

# get all categories that are no duplicates or not within intersections
total = buildings + clubs + prizes + literature + magazines + politics + newspaper + diplomacy + nature + process

# filter categories s.text. no intersections are available
companies_true = [company for company in companies if company not in total]
list_lengths.append(("Companies", len(companies_true)))

gastros_true = [cafe for cafe in gastros if cafe not in total]
list_lengths.append(("Gastronomy", len(gastros_true)))

sport_true = [sports for sports in sport if sports not in total]
list_lengths.append(("Sports", len(sport_true)))

banks_true = [bank for bank in banks if bank not in total]
list_lengths.append(("Banks", len(banks_true)))

cafes_true = [cafe for cafe in cafes if cafe not in total]
list_lengths.append(("Cafés", len(cafes_true)))

streets_true = [street for street in streets if street not in total]
list_lengths.append(("Streets", len(streets_true)))

history_true = [hist for hist in history if hist not in total]
list_lengths.append(("History", len(history_true)))

corps_true = [corp for corp in corps if corp not in total]
list_lengths.append(("Corps", len(corps_true)))

museums_true = [museum for museum in museums if museum not in total]
list_lengths.append(("Museums", len(museums_true)))

# update total list
total = buildings + clubs + prizes + literature + magazines + politics + newspaper + diplomacy + nature + process
total += companies_true
total += vocational
total += gastros_true
total += sport_true
total += banks_true
total += cafes_true
total += streets_true
total += history_true
total += corps_true


# put schools here in order to distinguish between category "school" and "vocational"
schools_true = [school for school in schools if school not in total]
list_lengths.append(("Schools", len(schools_true)))
list_lengths.append(("Vocational", len(vocational)))
total += schools_true
total += museums_true

# put category culture here since many overlaps and intersections for this as well
culture_true = [cult for cult in culture if cult not in total]
list_lengths.append(("Culture", len(culture_true)))
total += culture_true

orgs_true = [org for org in orgs if org not in total]
list_lengths.append(("Organizations", len(orgs_true)))
total += orgs_true

architecture_true = [arc for arc in architecture if arc not in total]
list_lengths.append(("Architecture", len(architecture_true)))
total += architecture_true

parks_true = [park for park in parks if park not in total]
list_lengths.append(("Parks", len(parks_true)))
total += parks_true

memorials_true = [mem for mem in memorials if mem not in total]
list_lengths.append(("Memorials", len(memorials_true)))
total += memorials_true

music_true = [mus for mus in music if mus not in total]
list_lengths.append(("Music", len(music_true)))
total += music_true

ships_true = [ship for ship in ships if ship not in total]
list_lengths.append(("Ships", len(ships_true)))
total += ships_true

cemetaries_true = [cem for cem in cemetaries if cem not in total]
list_lengths.append(("Cemetaries", len(cemetaries_true)))
total += cemetaries_true

geography_true = [geo for geo in geography if geo not in total]
list_lengths.append(("Geography", len(geography_true)))
total += geography_true

justice_true = [just for just in justice if just not in total]
list_lengths.append(("Justice", len(justice_true)))
total += justice_true

diseases_true = [illness for illness in diseases if illness not in total]
list_lengths.append(("Illness", len(diseases_true)))
total += diseases_true

missing = [tuples for tuples in other_all_list if tuples not in total]
# print(len(missing))
# print(len(total))
# print(missing)

final_list_length = sorted(list_lengths, key=lambda tup: tup[1], reverse=True)
final_list_length.append(("too specific", len(missing)))

# chunk list into parts s.text. each part has 5 elements
chunked_list = chunks(final_list_length, 5)

# plot the batches
# for items in chunked_list:
#     other_analyzer.plot_categories(items)

# create csv files --> the ones commented out are either grouped together for properties or don'text have a
# fitting set of properties in DBpedia
# other_analyzer.other_detailed_to_csv(literature, "Literature.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(magazines, "Magazines.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(politics, "Politics.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(newspaper, "Newspapers.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(diplomacy, "Diplomacy.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(nature, "Nature.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(companies_true, "Companies.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(vocational, "Vocational.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(gastros_true, "Gastros.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(sport_true, "Sports.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(banks_true, "Banks.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(cafes_true, "Cafes.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(streets_true, "Streets.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(history_true, "History.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(corps_true, "Corps.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(schools_true, "Schools.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(culture_true, "Culture.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(orgs_true, "Orgs.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(architecture_true, "Architecture.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(parks_true, "Parks.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(memorials_true, "Memorials.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(music_true, "Music.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(ships_true, "Ships.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(cemetaries_true, "Cemetaries.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(geography_true, "Geography.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(justice_true, "Justice.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(diseases_true, "Diseases.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(missing, "TooDetailed.csv", title_only=True)

actual_other_category_lens = []
# group the categories in order to get as much properties as possible
buildings_general = buildings + cafes_true + architecture_true + memorials_true + cemetaries_true + streets_true
actual_other_category_lens.append(("Buildings", len(buildings_general)))

organizations_general = companies_true + orgs_true + banks_true + cafes_true + gastros_true + clubs + corps_true
actual_other_category_lens.append(("Organizations", len(organizations_general)))

parks_general = parks_true + nature
actual_other_category_lens.append(("Parks", len(parks_general)))

schools_general = schools_true + vocational
actual_other_category_lens.append(("Schools", len(schools_general)))

actual_other_category_lens.append(("Literature", len(literature)))
actual_other_category_lens.append(("Magazines", len(magazines)))
actual_other_category_lens.append(("Newspapers", len(newspaper)))
actual_other_category_lens.append(("History", len(history_true)))
actual_other_category_lens.append(("Ships", len(ships_true)))
actual_other_category_lens.append(("Diseases", len(diseases_true)))

# map them all to csv files
# other_analyzer.other_detailed_to_csv(buildings_general, "Buildings.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(organizations_general, "Organizations.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(parks_general, "Parks.csv", title_only=True)
# other_analyzer.other_detailed_to_csv(schools_general, "Schools.csv", title_only=True)

final_other_list = buildings_general + organizations_general + parks_general + schools_general + literature + \
                   newspaper + magazines + ships_true + diseases + history_true
print(len(final_other_list))
print(buildings_general)
discarded_entities = [ent for ent in other_all_list if ent not in final_other_list]
# remove entity "Lotosblüte" since this one has no categories to it
discarded_entities = [ent for ent in discarded_entities if ent[0] != "Lotosblüte"]
actual_other_category_lens = sorted(actual_other_category_lens, key=lambda tup: tup[1], reverse=True)
actual_other_category_lens.append(("Discarded entities", len(discarded_entities)))
chunked_final_list = chunks(actual_other_category_lens, 4)

for item in chunked_final_list:
    other_analyzer.plot_categories(item)

# create joint list for comparison of entities that have properties

joint_list = [("Entities with DBpedia Properties", len(final_other_list)),
              ("Entities with no DBpedia Properties", len(discarded_entities))]
other_analyzer.plot_categories(joint_list)
final_amount_articles = len(final_other_list) + 1038  # 1038 is the number of "Person" in the dataset
print(final_amount_articles)

# Data selection final results in a txt file
txtfile_path = "C:/Users/ubmen/Desktop/BA_Prog/DataExploration/"
txt_filename = "EndResults.txt"
with open(os.path.join(txtfile_path, txt_filename), "w") as f:
    f.write("Total number of candidate articles/entities after Property Analysis/Extraction: " 
            f"{final_amount_articles}\n")
    f.write('Number of candidate articles/entities in "other" that do not have matching properties in DBpedia: '
            f"{len(discarded_entities)}\n")
    f.write('Total number of candidate entities/articles "other" after Property Analysis/Extraction: '
            f"{len(final_other_list)}\n")
    f.write('In total, ' f"{len(discarded_entities)}" ' candidate entities/articles had to be discarded due to the fact'
            ' that they do not have a set of properties in DBpedia at this point of the research, which means that '
            'even if valid triples will be extracted, they cannot be inserted to the DBpedia Knowledge Graph due '
            'to the lack of proper representation (i.e. triples) for the predicates that were found.\n'
            'For future research, this could be still of interest one these properties are curated.\n'
            'This leaves us with a total amount of ' 
            f"{final_amount_articles}" ' candidate articles for the triple extraction part, ' 
            f"{len(final_other_list)}" ' of which are of type "other"')
    f.close()
