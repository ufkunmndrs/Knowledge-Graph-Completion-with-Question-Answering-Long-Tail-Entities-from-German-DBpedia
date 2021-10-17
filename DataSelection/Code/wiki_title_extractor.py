# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file provides a Class "WikiTitleExtractor" to both handle Wikipedia XML files and extract
the titles from these pages.

"""
import os.path
import xml.dom.minidom
import re
import wikipediaapi


wiki = wikipediaapi.Wikipedia("de")


class WikiTitleExtractor:
    """
    Class to load, preprocess and handle XML files of Wikipedia and return their articles and titles.

    Attributes
    -------------
    xml_file: str
        The name of an XML file that will be handled and preprocessed accordingly.
    path: str
        Filepath from which the XML file will be retrieved.
        The default is: C:/Users/ubmen/Desktop/BA_Prog/DataSelection/XMLFiles/

    Methods
    ------------------------
    preprocess(self)
        Preprocesses the input XML file by splitting the lists at "<page>" and returning a list with all
        elements in the XML file
    get_articles(xml_list, tail_entities)
        gets all article names and sorts them according to their infobox existence
    get_titles(articles)
        gets titles of Wikipedia articles
    get_disambiguation_page(articles)
        gets all the disambiguation pages that are within a list of articles. Articles are XML elements as strings
        within the said list of articles
    get_lang_links(article)
        Function which gets the German name of an English input article
    get_de_only(self, articles)
        Functions which gets articles that are IN GERMAN ONLY in a list of articles.
    titles_file(title_list, json_filename)
        creates a .txt file of all candidate article titles
    """

    def __init__(self, xml_file: str, path="C:/Users/ubmen/Desktop/BA_Prog/DataSelection/XMLFiles/"):
        """
        init method of this class

        Parameters
        ----------
        xml_file: str
            The name of an XML file that will be handled and preprocessed accordingly.
        path: str
            Filepath from which the XML file will be retrieved.
            The default is: C:/Users/ubmen/Desktop/BA_Prog/DataSelection/XMLFiles/
        """
        self.xml_file = xml_file
        self._path = path

    # Getter Method for Path
    def get_path(self):
        """
        Getter method for the class, gets the path of the class
        Returns
        -------
        self._path: str
            the filepath for the xml file
        """
        return self._path

    # Setter Method for Path
    def set_path(self, path):
        """
        Setter method for the path of the class
        Parameters
        ----------
        path: str
            new filepath where the xmlfile is being stored
        Returns
        -------

        """
        self._path = path

    def preprocess(self):
        """
        Preprocesses the input XML file by splitting the lists at "<page>" and returning a list with all elements
        in the XML file
        Returns
        -------
        list in which every XML element (i.e. every Wikipedia article) is an element of the list as a String

        """
        xml_file = os.path.join(self._path, self.xml_file)
        xml_object = xml.dom.minidom.parse(xml_file)  # or xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = xml_object.toprettyxml()
        return pretty_xml_as_string.split("<page>")

    @staticmethod
    def get_articles(xml_list: list, tail_entities=True):
        """
        gets all article names and sorts them according to their infobox existence

        Parameters
        ----------
        xml_list: list
        list of all the elements (i.e. articles) in the XML list
        tail_entities: True/False
        decides whether the tail entities containing NO INFOBOX or complete entities with an infobox will be returned.
        The default is true.

        Returns
        -------
        no_infobox_articles:list
        articles containing no infobox in German Wikipedia
        infobox_articles:list
        articles containing an infobox in German Wikipedia

        """
        no_infobox_articles = []
        infobox_articles = []
        pattern = "\{\{\s?(.*)box\s?"
        infobox_string = ["{{Infobox", "{{ Infobox", "{{infobox", "{{ infobox", "{{Taxobox", "{{ Taxobox", "{{ taxobox",
                          "{{taxobox"]
        for article in xml_list:
            if any(substring in article for substring in infobox_string) or re.search(pattern, article):
                infobox_articles.append(article)
            else:
                no_infobox_articles.append(article)
        # delete the first article of the no_infobox_articles list since this is just unnecessary Wikimedia page
        del no_infobox_articles[0]
        if tail_entities is True:
            return no_infobox_articles
        else:
            return infobox_articles

    @staticmethod
    def get_titles(articles: list):
        """
        gets titles of Wikipedia articles

        Parameters
        ----------
        articles:list
        List of the articles that were sorted in the previous step, in this use case we will always use the list
        of articles WITHOUT an infobox (i.e. no_infobox_articles) as input

        Returns
        -------
        titles:list
        List of all the Wikipedia page titles that don´text have an infobox

        """
        pattern = "<title>(.*)</title>"
        titles = [re.search(pattern, xml_str).group(1) for xml_str in articles]
        return titles

    @staticmethod
    def get_disambiguation_page(articles: list):
        """
        gets all the disambiguation pages that are within a list of articles. Articles are XML elements as strings
        within the said list of articles

        Parameters
        ----------
        articles: list
            List which contains each XML element as a string

        Returns
        -------
        disambiguation_pages: list
            List of disambiguation pages from the original list of articles
        """
        disambiguation_pages = []
        for article in articles:
            if "{{Begriffsklärung}}" in article or "{{ Begriffserklärung" in article:
                disambiguation_pages.append(article)
        return disambiguation_pages

    @staticmethod
    def get_lang_links(article):
        """
        Function which gets the German name of an English input article

        Parameters
        ----------
        article: page
            wikipediaapi.page object

        Returns
        -------
        v.title: str
            Title in German
        """
        langlinks = article.langlinks
        links = []
        for k in sorted(langlinks.keys()):
            v = langlinks[k]
            links.append(v.title)
        return links

    def get_de_only(self, articles):
        """
        Functions which gets articles that are IN GERMAN ONLY in a list of articles.

        Parameters
        ----------
        articles:list
            list of Wikipedia articles (i.e. their titles), elements are strings

        Returns
        -------
        de_final: list
            list of articles without any language link, thus only in German
        """
        de_pages = [wiki.page(title) for title in articles]  # make every title into a .page object
        de_pages = list(set(de_pages))
        de_only = []
        for title in de_pages:
            if self.get_lang_links(title) == []:  # if language link list is empty for an article
                de_only.append(title)  # then append that article to list
        de_final = [page.title for page in de_only]
        de_final = list(set(de_final))
        return de_final

    @staticmethod
    def titles_file(title_list: list, filename):
        """
        creates a .txt file of all candidate article titles

        Parameters
        ----------
        title_list: list
            list containing titles
        filename: str
            name of the file to be created; default is german only

        Returns
        -------
        does not return anything, just creates a .txt file
        """
        save_path = "../TXTFiles"
        complete_name = os.path.join(save_path, filename)
        with open(complete_name, "w", encoding="utf8") as f:
            for title in title_list:
                f.write(f"{title}\n")
            f.write(str(len(title_list)))
        f.close()
