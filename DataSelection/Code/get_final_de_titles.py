# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file extracts the titles of the Wikipedia articles/entities in "FullDEdisambiguated.xml" and stores them,
according to their langage links, in two different .txt files:
    - OnlyDeArticlesFinal: All articles from "FullDEdisambiguated.xml" that have no infobox AND are in German only
    - LangLinkDeArticlesFinal: All articles from "FullDEdisambiguated.xml" that have no infobox in German and English,
    but may have infoboxes in other languages as they have language links and thus exist in more languages other than
    German.

The "OnlDeArticlesFinal.txt" ultimately provides the titles of those Wikipedia articles that are the final candidate
entities for this research. The list of those articles can be copypasted into the "Seite exportieren" webbpage of
German Wikipedia and the final XML file containing these candidate entities can be retrieved:
https://de.wikipedia.org/wiki/Spezial:Exportieren

"""

from wiki_title_extractor import WikiTitleExtractor
import wikipediaapi
import time
import matplotlib.pyplot as plt

start_time = time.time()

# create German Wikipedia from wikipediaapi
wiki = wikipediaapi.Wikipedia("de")

# preprocess entire XML file, get articles without infobox,
# get titles of those articles and store them in "final_titles_de" as list
de_final_wiki = WikiTitleExtractor("FullDEdisambiguated.xml")
xml_split_de = de_final_wiki.preprocess()
final_articles_de = de_final_wiki.get_articles(xml_split_de)
final_titles_de = de_final_wiki.get_titles(final_articles_de)

# extract pages that are in German only, store them in a txt in sister directory TXT Files
de_only_pages = de_final_wiki.get_de_only(final_titles_de)
de_final_wiki.titles_file(de_only_pages, "OnlyDeArticlesFinal")

# extract pages that have language links to other languages, store them as TXT in sister directory TXTFiles
langlink_pages = [title for title in final_titles_de if title not in de_only_pages]
de_final_wiki.titles_file(langlink_pages, "LanglinkDeArticlesFinal")

elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time:2f} seconds")


# plotting stats for German Feature Articles in Wikipedia
y_pos = len(de_only_pages + langlink_pages)
plt.ylim(0, len(de_only_pages + langlink_pages))
plt.ylabel(f"Candidate Articles DE Total")
plt.title("Language links statistics for final German candidate articles/entities")
plt.xlabel("Total number of candidate articles/entities: " f"{len(de_only_pages + langlink_pages)}")
x = ["German only", "German with language links"]
y = [len(de_only_pages), len(langlink_pages)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("../WikiTitlePlots/FullDeStats.png")
