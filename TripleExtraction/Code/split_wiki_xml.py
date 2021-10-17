import os
import re

# get parsed Wiki File, delete info about categories and types
"C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/PreprocessedTXTFiles/preprocessed_xml.txt"
txt_file = open("C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/PreprocessedTXTFiles/"
                "FullWikiTXT/ParsedWikiXMLFile.txt", "r", encoding="utf-8")
wiki_content = txt_file.read()
wiki_content_split = wiki_content.split("\n\n\n")
remove_patterns = ["#Type: (.*)", "Kategorie:(.*)", "Einzelnachweise", "minimini", "miniatur"]
wiki_content_split = [re.sub("#Type: (.*)", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("Kategorie:(.*)", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("Einzelnachweise", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("minimini", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("miniatur", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("thumb", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("\nmini", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("mini\n", "", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("\n+", "\n", article_text) for article_text in wiki_content_split]
wiki_content_split = [re.sub("\t", "", article_text) for article_text in wiki_content_split]
pattern = "#Article: (.*)"


# for loop for better clarity, alternatively:
# tatl = [(re.search(pattern, article).group(1), article) for article in wiki_content_split]
# elems are tuples where the 0th element (m.group(1)) of the tuple is the entity name as str (hence the pattern that was matched
# and 1st element is the corresponding Wiki article text (article)
title_article_tuple_list = []
for article in wiki_content_split:
    m = re.search(pattern, article)
    title_article_tuple_list.append((m.group(1), article))

# strip Wiki Text of unnecessary chars
title_article_tuple_list = [(article[0], article[1].strip()) for article in title_article_tuple_list]
# print(len(wiki_content_split))

# save wiki text
filepath = "C:/Users/ubmen/Desktop/BA_Prog/TripleExtraction/PreprocessedTXTFiles/FullWikiTXT/"
json_filename = "FullWikiTXTsplit.txt"
with open(os.path.join(filepath, json_filename), "w", encoding="utf-8") as f:
    f.write("\n".join(map(str, title_article_tuple_list)))
    f.close()
