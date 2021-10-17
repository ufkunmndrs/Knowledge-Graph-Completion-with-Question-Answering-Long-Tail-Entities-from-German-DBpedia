# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file extracts the titles of all Wikipedia pages in XML format and returns the the titles of all articles
without an infobox and with an Infobox for German and English respectively. Executing the main module will save those
files in the path specified at "wiki_title_extractor.py"

The files gets all

"""
import wikipediaapi
from wiki_title_extractor import WikiTitleExtractor
from article_extraction import target_titles_en, target_titles_de
import matplotlib.pyplot as plt


def get_de_titles(page):
    """
    Function which gets the German name of an English input article

    Parameters
    ----------
    page

    Returns
    -------
    v.title: str
    Title in German

    """
    langlinks = page.langlinks
    for k in sorted(langlinks.keys()):
        v = langlinks[k]
        if v.language == "de":
            return v.title


nt_extractor_de = WikiTitleExtractor("GermanNeedTranslate.xml")
nt_xml = nt_extractor_de.preprocess()
nt_articles_de = nt_extractor_de.get_articles(nt_xml)
nt_titles_de = nt_extractor_de.get_titles(nt_articles_de)

# filter out Category Articles, 9 total
nt_missing_de = [art for art in target_titles_en if art not in nt_titles_de]
for article in nt_missing_de:
    if "Category" in article:
        nt_missing_de.remove(article)

nt_extractor_de.titles_file(nt_titles_de, "GermanNeedTranslate")
nt_extractor_de.titles_file(nt_missing_de, "MissingGermanTitles")

en_wiki = wikipediaapi.Wikipedia("en")

de_2translate_title = [en_wiki.page(art) for art in nt_missing_de]
de_titles_translated = [get_de_titles(art) for art in de_2translate_title]
save_path = "../TXTFiles"
nt_extractor_de.titles_file(de_titles_translated, "MissingGermanTitlesTranslated")

de_titles_all = list(set(de_titles_translated + nt_titles_de + target_titles_de))
# print(len(de_titles))
# print(len(nt_titles_de))
# print(len(final_titles_de))
nt_extractor_de.titles_file(de_titles_all, "GermanTitlesAll")

y_pos = len(nt_titles_de + nt_missing_de)
plt.ylim(0, len(nt_titles_de + nt_missing_de))
plt.title("Which article titles need translation from English to German?")
plt.ylabel("German Need Translate")
plt.xlabel("Total number of articles: " f"{len(nt_titles_de + nt_missing_de)}")
x = ["Title translation to German not required", "Title translation to German required"]
y = [len(nt_titles_de), len(nt_missing_de)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("../WikiTitlePlots/GermanNTStatsTranslation.png")
