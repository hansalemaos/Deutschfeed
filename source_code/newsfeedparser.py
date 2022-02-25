# coding: iso-8859-1 -*-
from collections import defaultdict
from copy import deepcopy
from time import sleep
from farbprinter.farbprinter import Farbprinter
from nested_df_to_html import nested_dataframe_to_html
import webbrowser
drucker=Farbprinter()
import regex
from bs4 import BeautifulSoup
import tqdm
import feedparser
import pandas as pd
import kthread
from einfuehrung import einfuehrung


quellen =  {0: {'name': 'WELT', 'url': 'https://www.welt.de/feeds/latest.rss'},
 1: {'name': 'Focus', 'url': 'https://rss.focus.de/fol/XML/rss_folnews.xml'},
 2: {'name': 'ZEIT', 'url': 'https://newsfeed.zeit.de/all'},
 3: {'name': 'Bild',
     'url': 'https://www.bild.de/rssfeeds/vw-home/vw-home-16725562,sort=1,view=rss2.bild.xml'},
 4: {'name': 'SZ',
     'url': 'https://rss.sueddeutsche.de/app/service/rss/alles/index.rss?output=rss'},
 5: {'name': 'n-tv', 'url': 'https://www.n-tv.de/rss'},
 6: {'name': 'SPIEGEL', 'url': 'https://www.spiegel.de/schlagzeilen/index.rss'},
 7: {'name': 'Stern', 'url': 'https://www.stern.de/feed/standard/all/'},
 8: {'name': 'FAZ', 'url': 'https://www.faz.net/rss/aktuell/'},
 9: {'name': 'Handelsblatt',
     'url': 'https://www.handelsblatt.com/contentexport/feed/schlagzeilen'},
 10: {'name': 'HAZ', 'url': 'https://www.haz.de/rss/feed/haz_schlagzeilen'},
 11: {'name': 'ND',
      'url': 'https://www.neues-deutschland.de/rss/neues-deutschland.xml'},
 12: {'name': 'AZ',
      'url': 'https://www.aachener-zeitung.de/nrw-region/feed.rss'},
 13: {'name': 'Tagesspiegel',
      'url': 'https://www.tagesspiegel.de/contentexport/feed/home'},
 14: {'name': 'ARD Tagesschau', 'url': 'https://www.tagesschau.de/xml/rss2/'},
 15: {'name': 'taz', 'url': 'https://taz.de/!p4608;rss/'},
 16: {'name': 'Berliner Morgenpost',
      'url': 'https://www.morgenpost.de/?service=Rss'},
 17: {'name': 'WAZ', 'url': 'https://www.waz.de/rss'},
 18: {'name': 'Hamburger Abendblatt',
      'url': 'https://www.abendblatt.de/?service=Rss'},
 19: {'name': 'Hessenschau', 'url': 'https://www.hessenschau.de/index.rss'},
 20: {'name': 'T-Online', 'url': 'https://feeds.t-online.de/rss/nachrichten'},
 21: {'name': 'RP Online', 'url': 'https://rp-online.de/feed.rss'},
 22: {'name': 'Yahoo!', 'url': 'https://de.nachrichten.yahoo.com/rss'},
 23: {'name': 'BZ', 'url': 'https://www.bz-berlin.de/feed'},
 24: {'name': 'Berliner Zeitung',
      'url': 'https://www.berliner-zeitung.de/feed.xml'},
 25: {'name': 'Deutschlandfunk',
      'url': 'https://www.deutschlandfunk.de/die-nachrichten.353.de.rss'},
 26: {'name': 'Deutsche Welle', 'url': 'https://rss.dw.com/xml/rss-de-all'},
 27: {'name': 'MZ', 'url': 'https://www.mz-web.de/feed/yahoo.rss'},
 28: {'name': 'NDR', 'url': 'https://www.ndr.de/index-rss.xml'},
 29: {'name': 'Die Presse', 'url': 'https://www.diepresse.com/rss/'},
 30: {'name': 'WDR',
      'url': 'https://www1.wdr.de/wissen/uebersicht-nachrichten-100.feed'},
 31: {'name': 'SWR',
      'url': 'https://www.swr.de/export:xml:rss/swraktuell/swraktuell-100.html'},
 32: {'name': 'Stuttgarter Zeitung',
      'url': 'https://www.stuttgarter-zeitung.de/news.rss.feed'},
 33: {'name': 'ZDF Heute', 'url': 'https://www.zdf.de/rss/zdf/nachrichten'},
 34: {'name': 'Der Freitag', 'url': 'https://www.freitag.de/@@RSS'},
 35: {'name': 'Netzpolitik', 'url': 'https://netzpolitik.org/feed/'},
 36: {'name': 'Wirtschaftswoche',
      'url': 'https://www.wiwo.de/contentexport/feed/rss/schlagzeilen'},
 37: {'name': 'WZ', 'url': 'https://www.wz.de/feed.rss'},
 38: {'name': 'Frankfurter Rundschau', 'url': 'https://www.fr.de/rssfeed.rdf'},
 39: {'name': 'K?ln Stadt-Anzeiger',
      'url': 'https://www.ksta.de/feed/index.rss'},
 40: {'name': 'Aller-Zeitung',
      'url': 'https://www.waz-online.de/rss/feed/waz_schlagzeilen'},
 41: {'name': 'rbb',
      'url': 'https://www.rbb24.de/aktuell/index.xml/feed=rss.xml'},
 42: {'name': 'MDR',
      'url': 'https://www.mdr.de/nachrichten/nachrichten100-rss.xml'},
 43: {'name': 'BR', 'url': 'https://nachrichtenfeeds.br.de/rdf/boards/QXAPkQJ'},
 44: {'name': 'Rhein-Neckar-Zeitung',
      'url': 'https://www.rnz.de/feed/6-regionalticker.xml'},
 45: {'name': 'PNN', 'url': 'https://www.pnn.de/contentexport/feed/home'},
 46: {'name': 'Watson', 'url': 'https://www.watson.de/api/1.0/rss/index.xml'},
 47: {'name': 'Th¨¹ringsche Landeszeitung',
      'url': 'https://www.tlz.de/?service=Rss'},
 48: {'name': 'Hildesheimer Presse',
      'url': 'https://hildesheimer-presse.de/feed/'},
 49: {'name': 'Vice', 'url': 'https://www.vice.com/de/rss'},
 50: {'name': 'Wuppertaler Rundschau',
      'url': 'https://www.wuppertaler-rundschau.de/feed.rss'},
 51: {'name': 'Westfalenpost', 'url': 'https://www.wp.de/rss'},
 52: {'name': 'NRZ', 'url': 'https://www.nrz.de/rss'},
 53: {'name': 'Merkur', 'url': 'https://www.merkur.de/rssfeed.rdf'},
 54: {'name': 'Mannheimer Morgen',
      'url': 'https://www.morgenweb.de/feed/55-politik-rss-feed.xml'},
 55: {'name': 'Spreezeitung', 'url': 'https://www.spreezeitung.de/feed/'},
 56: {'name': 'Neue Osnabrücker Zeitung',
      'url': 'https://www.noz.de/rss/ressort/Osnabr%C3%BCck'},
 57: {'name': 'Buzzfeed',
      'url': 'https://www.buzzfeed.de/recherchen/rssfeed.xml'}}

def delete_duplicates_from_nested_list(nestedlist):
    tempstringlist = {}
    for ergi in nestedlist:
        tempstringlist[str(ergi)] = ergi
    endliste = [tempstringlist[key] for key in tempstringlist.keys()]
    return endliste.copy()


def nesteddicterstellen():
    nested_dict = lambda: defaultdict(nested_dict)
    nest = nested_dict()
    return deepcopy(nest)


def get_neue_nachrichten(url):
    global geparstenachrichten
    d = feedparser.parse(url)
    geparstenachrichten.append(d.copy())


def pd_get_one_row_as_list(df, rownummer, iloc=False):
    datenframe = df.copy()
    """26.11"""
    if iloc is False:
        row1 = [val for val in datenframe.loc[rownummer]]
        datenframe.drop([rownummer], inplace=True)
        datenframe.columns = row1

    if iloc is True:
        row1 = [val for val in datenframe.iloc[rownummer]]
        index = df.iloc[rownummer:rownummer + 1, :].index.tolist()[0]
        datenframe.drop([index], inplace=True)
        datenframe.columns = row1
    return datenframe.copy()

def to_file(datei, text, encoding='utf-8'):
    with open(datei, encoding=encoding, mode='w') as f:
        if isinstance(text, list):
            for l in text:
                try:
                    f.write(str(l))
                    f.write('\n')
                except:
                    continue
        if isinstance(text, str):
            f.write(str(text))


if __name__ == '__main__':
    alleurls = []
    for key, item in quellen.items():
        url = item['url']
        alleurls.append(url)
    aufmachen=False
    while True:
        einfuehrung('Deutschfeed')
        geparstenachrichten = []
        allethreads = []
        for aktion in alleurls:
            allethreads.append(
                kthread.KThread(
                    target=get_neue_nachrichten,
                    name=aktion,
                    args=(aktion,),
                )
            )
        gestartet = [los.start() for los in allethreads]
        nochamleben = [(t.name, t.is_alive()) for t in allethreads]
        nuramleben = [x[1] for x in nochamleben if x[1] == True]
        while any(nuramleben):
            nochamleben = [(t.name, t.is_alive()) for t in allethreads]
            for thr in nochamleben:
                if thr[1] is True:
                    print(drucker.f.black.brightred.italic(f"{thr[0]} -> noch nicht fertig"))
                if thr[1] is False:
                    print(drucker.f.black.brightgreen.italic(f"{thr[0]} ist schon fertig!"))
            sleep(2)
            nuramleben = [x[1] for x in nochamleben if x[1] == True]

        allenachrichten = nesteddicterstellen()
        debug = False
        for nachricht in tqdm.tqdm(geparstenachrichten, position=0):
            for entry in tqdm.tqdm(nachricht['entries'], colour='blue', position=0):

                try:
                    nachricht_titel = entry['title']
                    nachricht_link = entry['links'][0]['href']
                    suppe = BeautifulSoup(entry['summary'], 'html.parser')
                    nachricht_inhalt = suppe.text
                    zeitungsname = regex.findall(r'https?://(?:www\.)([^.]+)', nachricht_link)[0]
                    if debug is True:
                        print(drucker.f.black.brightmagenta.normal(nachricht_titel))
                        print(drucker.f.black.brightyellow.italic(nachricht_link))
                        print(drucker.f.black.brightcyan.italic(nachricht_inhalt))
                    allenachrichten[nachricht_link]['Titel'] = nachricht_titel
                    allenachrichten[nachricht_link]['Text'] = nachricht_inhalt
                    allenachrichten[nachricht_link]['Zeitung'] = zeitungsname

                except Exception as Fehler:
                    if debug is True:
                        print(drucker.f.brightred.brightwhite.bold(Fehler))
                    pass
        df = pd.DataFrame(allenachrichten).T
        df2 = pd.DataFrame(df.groupby(by='Zeitung')).copy()
        df2.columns = ['Zeitung', 'Infos']
        df6 = pd_get_one_row_as_list(df2.T, rownummer='Zeitung', iloc=False)

        for col in df6.columns:
            df6[col].Infos.drop(columns=['Zeitung'], inplace=True)

        for col in df6.columns:
            df6[col]['Infos']['Artikel'] = 'XYZXYZqqq' + df6[col]['Infos']['Titel'] + 'qqqAQAQAQA' + df6[col]['Infos']['Text']

        for col in df6.columns:
            df6[col].Infos.drop(columns=['Titel', 'Text'], inplace=True)

        xxx = nested_dataframe_to_html(dataframe=df6, dateiname=None)
        xxx = regex.sub(r'''<th\s+id="id\d{,6}">\s*Infos\s*</th>''', '', xxx, regex.DOTALL)
        xxx = xxx.replace('XYZXYZqqq', '<strong>')
        xxx = xxx.replace('qqqAQAQAQA', '</strong><br>')
        xxx = regex.sub(r'''<th\s+id="id\d{,6}">\s*Infos\s*</th>''', '', xxx, regex.DOTALL)
        xxx = regex.sub(r'''<th\s+id="id\d{,6}">\s*Artikel\s*</th>''', '', xxx, regex.DOTALL)
        xxx = regex.sub(r'''<th\s+id="id\d{,6}">\s*Infos\s*</th>''', '', xxx, regex.DOTALL)
        xxx = regex.sub(r'''<th\s+id="id\d{,6}">\s*Artikel\s*</th>''', '', xxx, regex.DOTALL)
        xxx = xxx.replace('XYZXYZqqq', '<strong>')
        xxx = xxx.replace('qqqAQAQAQA', '</strong><br>')
        zaehler = 0
        allefertig = []
        gesplittet = xxx.splitlines()
        for ini, te in enumerate(gesplittet):
            gefunden = regex.findall(r'^\s*<td>', te)
            if any(gefunden):
                strongda = regex.findall('<strong>', gesplittet[ini + 1])
                if any(strongda):
                    if zaehler % 2 == 0:
                        te = regex.sub(r'<td>', r'<td style="background-color:#ffff00">', te)
                    if zaehler % 2 != 0:
                        te = regex.sub(r'<td>', r'<td style="background-color:#ffffaa">', te)
                    zaehler = zaehler + 1
            te = regex.sub(r'(https?://(?:www\.)[^\s]+)', '<a href="\g<1>">Text</a>', te)
            allefertig.append(te)

        einfuehrung('Deutschfeed')
        fertightml = '\n'.join(allefertig)
        headeralemao = '''<h1 style="background-color:black;color:red;font-size:36px;">&ensp;&ensp;&ensp;&ensp;&ensp;Made by&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<a href="https://www.queroestudaralemao.com.br/" style="background-color:black;color:yellow;font-size:48px;">queroestudaralemao.com.br</a></h1><br>'''
        # fertightml = regex.sub(r'<table id="id\d+">', headeralemao + '<br>\g<0>', fertightml)
        to_file(datei='deutschfeedtemp.html', text=headeralemao + fertightml, encoding='utf-8')
        if aufmachen is False:
            webbrowser.open('deutschfeedtemp.html')
            aufmachen=True
        sleep(900)








