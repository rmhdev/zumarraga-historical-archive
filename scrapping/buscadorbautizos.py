#!/usr/local/bin python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import codecs

uri = 'http://dos.cgssl.net/Zumarraga/ArchivoHistorico/BuscadorBautizos.aspx'

parameters_aspx = {
    '__EVENTTARGET'     : 'ctl00$ContentPlaceHolder1$gvResultados',
    '__EVENTARGUMENT'   : 'Page$1',
    '__LASTFOCUS'       : '',
    '__VIEWSTATE'       : '',
    '__EVENTVALIDATION' : ''
}

parameters_search = {
    'ctl00$SeleccionIdioma'                             : 'es-ES',
    'ctl00$ContentPlaceHolder1$txtNombre'               : '',
    'ctl00$ContentPlaceHolder1$txtApellido1'            : '',
    'ctl00$ContentPlaceHolder1$txtApellido2'            : '',
    'ctl00$ContentPlaceHolder1$ddlSexo'                 : '-',
    'ctl00$ContentPlaceHolder1$txtToponimo'             : '',
    'ctl00$ContentPlaceHolder1$txtPoblacionPariente'    : '',
    'ctl00$ContentPlaceHolder1$txtBusquedaLibre'        : '',
    'ctl00$ContentPlaceHolder1$txtFechaIni'             : '',
    'ctl00$ContentPlaceHolder1$txtFechaFin'             : '',
    'ctl00$ContentPlaceHolder1$cmdBuscar'               : 'Buscar',
}


def get_data_from_html(html):
    soup = BeautifulSoup(html)
    table = soup.find('table', id='ctl00_ContentPlaceHolder1_gvResultados')
    result = []
    for row in table.find_all('tr', recursive=False):
        result.append(get_data_from_row(row))
    return result

def get_data_from_row(row): 
    cols = row.find_all('td', recursive=False)
    if len(cols) != 5:
        return ""
    return get_data_from_cols(cols)

def get_data_from_cols(cols):
    id = re.findall(r'\d+', cols[4].find('a').get('href'))[0]
    name = cols[0].string.strip()
    surname1 = cols[1].string.strip()
    surname2 = cols[2].string.strip()
    birthday = cols[3].string.strip()
    return '"%s";"%s";"%s";"%s";"%s"' % (id, name, surname1, surname2, birthday)

if __name__ == "__main__":
    f = open('test.html', 'r')
    html = f.read()
    f.close()

    soup = BeautifulSoup(html)
    parameters_aspx['__VIEWSTATE']          = soup.find('input', id='__VIEWSTATE').get('value')
    parameters_aspx['__EVENTVALIDATION']    = soup.find('input', id='__EVENTVALIDATION').get('value')
    parameters = dict( parameters_aspx.items() + parameters_search.items() )

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES)'
    }
    req = requests.post(uri, data=parameters, headers=headers)
    if req.status_code != 200:
        print "error!"
        exit()

    html = req.text
    #print html

    f = codecs.open( 'result.txt', 'w', 'utf-8' )
    f.write("\n".join(get_data_from_html(html)))
    f.close()
