# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python test file is supposed to test whether the created lists have the necessary file form format.


"""


from clean_de_disambiguation import de_titles_with_disamb
from wiki_title_extractor import WikiTitleExtractor


def test_de_titles(final_titles, test_titles):
    """
    Test whether title lists are correct and ok
    Parameters
    ----------
    final_titles: list
        final
    test_titles: list

    Returns
    -------

    """
    if final_titles == [] or test_titles == []:
        raise ValueError("at least one of the lists is empty")
    assert len(final_titles) == len(test_titles)
    assert final_titles == test_titles


if __name__ == "__main__":
    test_de = WikiTitleExtractor("FinalDeTitlesNoInfobox.xml")
    test_xml = test_de.preprocess()
    test_articles = test_de.get_articles(test_xml)
    test_titles = test_de.get_titles(test_articles)

    test_de_titles(test_titles, de_titles_with_disamb)
