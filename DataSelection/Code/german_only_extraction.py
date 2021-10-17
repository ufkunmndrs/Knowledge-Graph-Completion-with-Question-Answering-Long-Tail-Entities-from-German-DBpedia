# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:35:42 2021

@author: Ufkun-Bayram Menderes

This Python file extracts the titles of all Wikipedia pages in XML format and returns the the titles of all articles
without an infobox and with an Infobox for German and English respectively. Executing the main module will save those
files in the path specified at "wiki_title_extractor.py"

The files gets all

"""

import os

articles_string = """de:Acetabuloplastik
de:Adelsgesellschaft
de:Afghanischer Bürgerkrieg (1989–2001)
de:Agneta Matthes
de:Albrecht Graf von Bernstorff
de:Alte Brücke (Frankfurt)
de:Alte Brücke (Heidelberg)
de:Alte Synagoge (Heilbronn)
de:Alter Friedhof Bonn
de:Altes Stadthaus (Berlin)
de:Am Brunnen vor dem Tore
de:Amendingen
de:Angus Campbell
de:Animal forensics
de:Apulische Bildervasen für eine Totenfeier (Antikensammlung Berlin)
de:Armee (Deutsches Kaiserreich)
de:Aubing
de:Babesiose des Hundes
de:Bäke (Telte)
de:Bauernkriegspanorama
de:Bebop head
de:Belziger Landschaftswiesen
de:Berliner wissenschaftliche Luftfahrten
de:Besteigung aller Achttausender
de:Binghöhle
de:Blaubart (Erzählung)
de:Blue Yodeling
de:Breisacher Stephansmünster
de:Bremer Marktplatz
de:Buchenwald-Hauptprozess
de:Bücherverluste in der Spätantike
de:Bullengraben
de:Burg Groitzsch
de:Bürgerpark und Stadtwald
de:Buxheimer Chorgestühl
de:Charles de Visscher
de:Charlottenhöhle
de:Chronische Niereninsuffizienz der Katze
de:Corsia
de:Das entschleierte Christentum
de:Das Kloster der Minne
de:Das Meininger Theater
de:Dativius-Victor-Bogen
de:Dauerwaldvertrag
de:DDR von unten
de:De coniuratione Catilinae
de:Depublizieren
de:Deutsche Rasenbinse
de:Deutsch-österreichische Zollunion
de:Die Amazonenschlacht
de:Die gelbe Kuh
de:Die Geschäfte des Herrn Julius Caesar
de:Die ungewöhnlichen Abenteuer des Julio Jurenito
de:Dienstgebäude der Königlichen Eisenbahndirektion Berlin
de:Dieter Süverkrüp
de:DKB-Ski-Arena Oberhof
de:Donezbecken-Operation
de:Donez-Mius-Offensive
de:Doppelgrab von Oberkassel
de:Doppelschlacht bei Wjasma und Brjansk
de:Dresden Leipziger Bahnhof
de:Dritte Ladoga-Schlacht
de:Eberstadter Tropfsteinhöhle
de:Eiger-Nordwand
de:Ein Mann der schläft
de:Einküchenhaus
de:Encephalitozoonose
de:Erdfunkstelle Fuchsstadt
de:Erinnerung an die Marie A.
de:Erna Wazinski
de:Essener Domschatzkammer Hs. 1
de:Fadenwurminfektionen des Hundes
de:Feline Hyperthyreose
de:Femeiche
de:Fettmilch-Aufstand
de:Filbinger-Affäre
de:Finnische Verfassung von 1919
de:Forschungsreaktor Haigerloch
de:Frankfurter Stadtbefestigung
de:Frankfurter Stadtgeläute
de:Franz Exner
de:Frauenkirche (Dresden, gotischer Vorgängerbau)
de:Friedhof der Märzgefallenen
de:Friedrich III. von Saarwerden
de:Friedrich Wolters
de:Fußballauswahl des FLN
de:Fußball im Ruhrgebiet
de:Gebäude der Jugoslawischen Gesandtschaft in Berlin
de:Geschichte Aubings
de:Geschichte der Berliner U-Bahn
de:Geschichte der First Nations
de:Geschichte der Juden in Ostfriesland
de:Geschichte des Kirchenbaus in Ostfriesland
de:Geschichte der Stadt Mainz
de:Geschichte des Kantons Aargau
de:Geschichte Heidelbergs
de:Geschichte Lörrachs
de:Geschichte Matreis in Osttirol
de:Geschichte Osttirols
de:Geschichte Rostocks
de:Geschichte von Höchst am Main
de:Gesetz über die Unterbrechung der Schwangerschaft
de:Gewerbesteuer (Deutschland)
de:Goetz-Höhle
de:Gotische Buchmalerei
de:Gotthard Neumann
de:Grabeiche
de:Graf Öderland
de:Gröben (Ludwigsfelde)
de:Große Dhünntalsperre
de:Große Mainzer Jupitersäule
de:Großer Speicher
de:Großer und Kleiner Engel
de:Haida (Röderland)
de:Hamburger Hafenarbeiterstreik 1896/97
de:Harvestehuder Weg
de:Hauptfriedhof Frankfurt
de:Haus Fürsteneck
de:Heidelberg in römischer Zeit
de:Heiligtum der Isis und Mater Magna (Mainz)
de:Heiratsurkunde der Kaiserin Theophanu
de:Hemerochorie
de:Heppenheimer Tagung
de:Hermannstraße
de:Hirnmetastase
de:Hochwasser in Würzburg
de:Hochwasserrückhaltebecken Jonenbach
de:Hochwasserschutz in Dresden
de:Hungersnot in Zentralkenia 1899
de:Im Sommer
de:Innsbrucker Mittelgebirgsbahn
de:Inselbergschanze
de:Isis (Zeitschrift, 1816)
de:Jagdschloss Grunewald
de:Jagdschloss Stern
de:Jakob Meyer zum Hasen
de:Jaxa von Köpenick
de:Jerusalemer Urgemeinde
de:Johannisberg (Jena-Lobeda)
de:Jüdische Gemeinde Esens
de:Justizanstalt
de:Kabinett Müller II
de:Kalmenhof
de:Kapellenkreuzweg Kloster Altstadt
de:Karl Helbig
de:Karolingische Buchmalerei
de:Kasberger Linde
de:Kastell Ala Nova
de:Kastell Buch
de:Kastell Hesselbach
de:Kastell Klosterneuburg
de:Kastell Stockstadt
de:Kettenschifffahrt auf dem Main
de:Kettenschifffahrt auf der Elbe und Saale
de:Kettenschleppschiff
de:Kirchenburg Ostheim
de:Kittelsthaler Tropfsteinhöhle
de:Kloster Oelinghausen
de:Köln-Ostheim
de:König-Ludwig-Eiche
de:König-Otto-Tropfsteinhöhle
de:Königseiche
de:Konzepte zur Überwindung der Blut-Hirn-Schranke
de:Kornmarkt (Frankfurt)
de:Kraftregelung
de:Kreuz mit den großen Senkschmelzen
de:Kreuzbergschanzen
de:Krönungsmantel
de:Kulturareal Desert
de:Kulturheidelbeeren
de:Kursächsische Postmeilensäule
de:KZ Ladelund
de:Lachsargument
de:Landesbühne Niedersachsen Nord
de:Le petit Lange
de:Leonhardskirche (Frankfurt)
de:Lily-Mottle-Virus
de:Limestor Dalkingen
de:Linde in Schenklengsfeld
de:Linzer Lokalbahn
de:Loschwitzer Kirche
de:Ludwig Frank (SPD)
de:Luftkrieg während der Operation Overlord
de:Luftsack (Vogel)
de:Lustschloss Favorite (Mainz)
de:LZ 120
de:Marburger Schloss
de:Maria-Magdalenen-Gymnasium
de:Marienglashöhle
de:Markthalle III
de:Markthalle IV
de:Martha Goldberg
de:Materialismusstreit
de:Massaker von Dinant
de:Mathias Metternich
de:Mathilde II. (Essen)
de:Max Windmüller
de:Meteorologisches Observatorium Hohenpeißenberg
de:Mogontiacum
de:Neue Berliner Pferdebahn
de:Neues Königliches Opernhaus Berlin
de:Nida (römische Stadt)
de:Nördlicher Felsenpython
de:Nosseni-Altar
de:Nosseni-Epitaph
de:Nur zwei Dinge
de:Oberlausitzer Pönfall
de:Orgel von St. Martin (Memmingen)
de:Orgellandschaft Hessen
de:Orgellandschaft Ostfriesland
de:Ostfriesland zur Zeit des Dreißigjährigen Krieges
de:Otto Regenbogen
de:Otto-Mathilden-Kreuz
de:Ottos mops
de:Palast Barberini
de:Pantherfell (Ägyptische Mythologie)
de:Parforceheide
de:Partei für gemäßigten Fortschritt in den Schranken der Gesetze
de:Paul Moder
de:Pegel Würzburg
de:Pferdeeisenbahn Budweis–Linz–Gmunden
de:Phantom Ride
de:Präsidentschaftswahl in Finnland 1956
de:Praviršulio tyrelis
de:Preußische Reformen
de:Prieschka
de:Psychopathographie Adolf Hitlers
de:Puhl & Wagner
de:Ragöse
de:Rapoport-Luebering-Zyklus
de:Rathaus Schmargendorf
de:Reichsburg Kyffhausen
de:Rettershof
de:Ries-Ereignis
de:Ringzug
de:Römische Villa Haselburg
de:Rotes Moor
de:Rudolph-Wilde-Park
de:Rurik-Expedition
de:Saathain
de:Salemer Münster
de:Salzhaus (Frankfurt)
de:Santanachelys gaffneyi
de:Schaffermahlzeit
de:Schanzenanlage im Kanzlersgrund
de:Schaumzikaden
de:Schellenberger Eishöhle
de:Schildhorn
de:Schloss Ahrensburg
de:Schloss Neudeck
de:Schloss Raesfeld
de:Schöne Eiche (Harreshausen)
de:Schönwalde (Wandlitz)
de:Schopenhauerhaus
de:Schraden (Landschaft)
de:Schulprogramm (historisch)
de:Schwarzes Moor
de:Schwedeneinfall 1674/75
de:Schweiz ohne Armee? Ein Palaver
de:Seekrieg während der Operation Overlord
de:Senat Momper
de:Sensor Media Access Control
de:Skating-Technik
de:Skigebiet Kreuzberg
de:Sophienhöhle
de:St. Martin (Memmingen)
de:St. Nikolaikirche (Potsdam)
de:St. Ulrich (Amendingen)
de:St.-Veit-Kirche (Gärtringen)
de:Staatsforst Burgholz
de:Steinernes Haus (Frankfurt)
de:Stiftskirche St. Cyriakus (Gernrode)
de:Stiftung Scheuern
de:Straßenbahn Graz
de:Straßenbahn Innsbruck
de:Straßenbahn Ravensburg–Weingarten–Baienfurt
de:Straßenbahn Timișoara
de:Strumaresektion
de:Stufentheorie (Harmonik)
de:Suanhild (Essen)
de:T-80 (leichter Panzer)
de:Tanzlinde (Effeltrich)
de:Tell el-Maschuta
de:Temesvári Közúti Vaspálya
de:Tendabahn
de:Teufelshöhle (bei Steinau)
de:Theophanu (Essen)
de:Theuerdank
de:Thüringenschanze
de:Tiefwerder Wiesen
de:Todesopfer an der Berliner Mauer
de:Tomus ad Antiochenos
de:Transregionaler Karawanenhandel in Ostafrika
de:Trio (Album)
de:Triple-Osteotomie
de:Tumorkachexie
de:Unser Frauen (Memmingen)
de:Untere Kochertalbahn
de:Ur- und frühgeschichtliche Sammlung der Universität Jena
de:Useless
de:Verschneite Dächer
de:Vertrauensfrage
de:Vetera
de:Vicke Schorler
de:Vom Nutzen und Nachteil der Historie für das Leben
de:Waldviertler Schmalspurbahnen
de:Wallfahrtskirche Birnau
de:Wandbilddruck
de:Wandermenagerie
de:Wanderungen durch die Mark Brandenburg
de:Wedeler Au
de:Weihnachtslied, chemisch gereinigt
de:Weinbau in Stuttgart
de:Weinbergkirche (Dresden)
de:Weinhaus Rheingold
de:Weiße Rose Hamburg
de:Weltbühne-Prozess
de:Windbergbahn
de:Windmühlen in Berlin
de:Wolfgang Diewerge
de:Würdenhain
de:Wurminfektionen der Katze
de:Zeremonialschwert (Essen)
de:Zitadelle Petersberg
de:Zitzengallenfliege"""


def main():
    save_path = "../TXTFiles"
    filename = "GermanFeatureFull"
    full_fn = os.path.join(save_path, filename)
    with open(full_fn, "w", encoding="utf8") as f:
        f.write(articles_string.replace("de:", ""))
    f.close()


if __name__ == "__main__":
    main()
