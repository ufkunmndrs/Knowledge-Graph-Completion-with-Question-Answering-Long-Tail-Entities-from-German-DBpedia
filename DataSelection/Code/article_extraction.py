# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file extracts the titles of all Wikipedia pages in XML format and returns the the titles of all articles
without an infobox and with an Infobox for German and English respectively.

This, however, is not the final solution for German articles as some of them need translation from English. The trans-
lations is being handled in other Python files of this same directory, the resulting .txt files can be used further.
Some additional statistics and plottings are also provided with this file.
"""

from wiki_title_extractor import WikiTitleExtractor
import matplotlib.pyplot as plt

# create objects to load and preprocess XML files
# german_NT1: articles needing translation from German, these articles are in English, but some of their titles
# map without translation to German
# german_NT1 is thus a SUBSET of EnglishArticles, namely those that can be exported in Wikipedia without translating
# the title to German
extractor_de = WikiTitleExtractor("GermanFeatured.xml")
extractor_en = WikiTitleExtractor("EnglishArticles.xml")

# split XMLs into lists
xml_split_de = extractor_de.preprocess()
xml_split_en = extractor_en.preprocess()

# extract target articles (those without infoboxes) for German and English
target_articles_de = extractor_de.get_articles(xml_split_de)
target_articles_en = extractor_en.get_articles(xml_split_en)

# extract articles with infoboxes for German and English
infobox_articles_de = extractor_de.get_articles(xml_split_de, tail_entities=False)
infobox_articles_en = extractor_en.get_articles(xml_split_en, tail_entities=False)

# get names of target articles for German and English
target_titles_de = extractor_de.get_titles(target_articles_de)
target_titles_en = extractor_en.get_titles(target_articles_en)

# get names of articles with infoboxes for German and English
infobox_titles_de = extractor_de.get_titles(infobox_articles_de)
infobox_titles_en = extractor_en.get_titles(infobox_articles_en)

# save TXT file with target article names in sister directory TXT Files
extractor_de.titles_file(target_titles_de, "GermanOnly")
extractor_en.titles_file(target_titles_en, "NoInfoboxEnglishFull")

# same as above for infobox articles
extractor_de.titles_file(infobox_titles_de, "InfoboxGermanOnly")
extractor_en.titles_file(infobox_titles_en, "InfoboxEnglishFull")

# plotting stats for German Feature Articles in Wikipedia
y_pos = len(target_titles_de + infobox_titles_de)
plt.ylim(0, len(target_titles_de + infobox_titles_de))
plt.title("German Feature Articles Infobox statistics")
plt.ylabel("German Feature Articles Total")
plt.xlabel("Total amount of articles: " f"{len(target_articles_de + infobox_titles_de)}")
x = ["German No Infobox", "German Infobox"]
y = [len(target_titles_de), len(infobox_titles_de)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("../WikiTitlePlots/InfoboxGermanStats.png")

y_en_pos = len(target_titles_en + infobox_titles_en)
plt.ylim(0, len(target_titles_en + infobox_titles_en))
plt.title("Infobox statistics for Articles Needing Translation from German")
plt.ylabel("Need Translation Articles from German in English Total")
plt.xlabel("Total amount of articles: " f"{len(target_articles_en + infobox_titles_en)}")
x = ["No Infobox", "Infobox"]
y = [len(target_titles_en), len(infobox_titles_en)]
for index, value in enumerate(y):
    plt.text(index, value, str(value))
plt.bar(x, y, width=0.5)
plt.show()
plt.savefig("../WikiTitlePlots/GermanNeedTranslationStats.png")
