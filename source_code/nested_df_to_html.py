import itertools
import numpy as np
import regex
from json2html import json2html
import bs4 as bs
import pandas as pd
def nested_dataframe_to_html(dataframe, dateiname=None):
    """usage: df = pd.read_html('https://de.wikipedia.org/wiki/Starkes_Verb')[0]
    datenframe_to_html(dataframe=df, dateiname='filenamewithoutending')
    """
    df = dataframe.copy()
    if dateiname is not None:
        dateiname = regex.sub(r'\..*$', '', dateiname)
    my_style = '''background-color: rgba(0, 0, 0, 0);
    border-bottom-color: rgb(0, 0, 0);
    border-bottom-style: none;
    border-bottom-width: 0px;
    border-collapse: collapse;
    border-image-outset: 0px;
    border-image-repeat: stretch;
    border-image-slice: 100%;
    border-image-source: none;
    border-image-width: 1;
    border-left-color: rgb(0, 0, 0);
    border-left-style: none;
    border-left-width: 0px;
    border-right-color: rgb(0, 0, 0);
    border-right-style: none;
    border-right-width: 0px;
    border-top-color: rgb(0, 0, 0);
    border-top-style: none;
    border-top-width: 0px;
    box-sizing: border-box;
    color: rgb(0, 0, 0);
    display: table;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 12px;
    line-height: 20px;
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 12px;
    text-size-adjust: 100%;
    -webkit-border-horizontal-spacing: 0px;
    -webkit-border-vertical-spacing: 0px;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);'''

    mystyleheader = r'''background-color: DarkOrange;
                border-width: 1px;'''

    mystylewichtigeheader = r'''background-color: GoldenRod;
                border-width: 0px;'''

    mystylewichtigeheaderspah = r'''background-color: SandyBrown;
                border-width: 0px;'''

    mystylewichtigeheaderspai = r'''background-color: Yellow;
                border-width: 0px;'''
    jsondatei = df.to_json()
    df_html = json2html.convert(json=jsondatei)
    soup = bs.BeautifulSoup(df_html, features="lxml")  # make BeautifulSoup
    df_html = soup.prettify()  # prettify the html
    random_id = 'id%d' % np.random.choice(np.arange(1000000))
    random_id_wichtige_header = 'id%d' % np.random.choice(np.arange(1000000))
    random_id_spacyh = 'id%d' % np.random.choice(np.arange(1000000))
    random_id_spacyi = 'id%d' % np.random.choice(np.arange(1000000))
    spacycolumns = [bbbb for bbbb in df.columns.to_list() if 'spacy' in bbbb]
    allespacycolumns = []
    allespacyindex = []
    for aaa in spacycolumns:
        try:
            for babaa in df.hilfsspalte.to_list():
                allespacycolumns.append(df[aaa][babaa].columns.to_list())
                allespacyindex.append(df[aaa][babaa].index.to_list())

        except:
            continue
    allespacycolumns = list(itertools.chain.from_iterable(allespacycolumns))
    allespacyindex = list(itertools.chain.from_iterable(allespacyindex))

    anfanghtml = '''<!DOCTYPE html>
    <html>
    <head>
    <style>'''

    endeheader = '''</style>
    </head>'''

    style = rf"""

        table#{random_id} {{{my_style}}}

    """

    random_id_th = 'id%d' % np.random.choice(np.arange(1000000))

    thstyle = rf"""

        th#{random_id_th} {{{mystyleheader}}}

    """
    wichtigeheader = rf"""

        th#{random_id_wichtige_header} {{{mystylewichtigeheader}}}

    """

    spacyh = rf"""

        th#{random_id_spacyh} {{{mystylewichtigeheaderspah}}}

    """
    spacyi = rf"""

        th#{random_id_spacyi} {{{mystylewichtigeheaderspai}}}

    """
    stylelliste = [style + thstyle + wichtigeheader + spacyh + spacyi]

    df_html = regex.sub(r'<table', r'<table id=%s ' % random_id, df_html)
    df_html = regex.sub(r'<th', r'<th id=%s ' % random_id_th, df_html)

    df_html = regex.sub(r'border="1"', '', df_html)

    zeileninlinien = df_html.split('\n')
    printfreigeschaltet = False
    grossesdf_index = df.index.to_list()
    grossesdf_columns = df.columns.to_list()
    for zzz in range(len(zeileninlinien)):
        if 'table id=' in zeileninlinien[zzz]:
            printfreigeschaltet = True
        if '<th>' in zeileninlinien[zzz]:
            printfreigeschaltet = True
        if '</th>' in zeileninlinien[zzz]:
            printfreigeschaltet = False
        if '<' not in zeileninlinien[zzz] and '>' not in zeileninlinien[zzz]:
            if str(
                    zeileninlinien[zzz]).strip() in grossesdf_columns or str(
                zeileninlinien[zzz]).strip() in grossesdf_index:
                zeileninlinien[zzz - 1] = regex.sub(f'id={random_id_th}', f'id={random_id_wichtige_header}',
                                                    zeileninlinien[zzz - 1])
            if str(zeileninlinien[zzz]).strip() in allespacycolumns:
                zeileninlinien[zzz - 1] = regex.sub(f'id={random_id_th}', f'id={random_id_spacyh}',
                                                    zeileninlinien[zzz - 1])
            if str(zeileninlinien[zzz]).strip() in allespacyindex:
                zeileninlinien[zzz - 1] = regex.sub(f'id={random_id_th}', f'id={random_id_spacyh}',
                                                    zeileninlinien[zzz - 1])

    del zeileninlinien[0]
    df_html = anfanghtml + '\n'.join(stylelliste) + endeheader + '\n'.join(zeileninlinien)
    soup = bs.BeautifulSoup(df_html, features="lxml")  # make BeautifulSoup
    df_html = soup.prettify()  # prettify the html
    if dateiname is not None:
        with open(f'{dateiname}.html', 'w', encoding='utf-8') as f:
            f.write(df_html)
    return df_html
