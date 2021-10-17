# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file extracts all the disambiguation articles from the set of total articles and stores both into
two different .txt files respectively. The disambiguation pages are still contained within the "FinalDeNoInofbox" .txt
will have to be dereferenced manually.

"""
from wiki_title_extractor import WikiTitleExtractor

# preprocess XML file, save titles in "de_titles_file" as list
de_titles = WikiTitleExtractor("AllDeNoInfobox.xml")
de_titles_xml = de_titles.preprocess()
de_titles_articles = de_titles.get_articles(de_titles_xml)
de_titles_with_disamb = de_titles.get_titles(de_titles_articles)
de_titles_file = de_titles.titles_file(de_titles_with_disamb, "FinalDeNoInfobox")


# get disambiguation pages and store them in a txt file in sister directory TXTFiles
dis_pages = de_titles.get_disambiguation_page(de_titles_articles)
dis_pages = de_titles.get_titles(dis_pages)
de_titles.titles_file(dis_pages, "DisambPages")
