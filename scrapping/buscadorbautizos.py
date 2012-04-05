#!/usr/local/bin python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import codecs
import time

def get_uri():
    return 'http://dos.cgssl.net/Zumarraga/ArchivoHistorico/BuscadorBautizos.aspx'

def get_default_parameters(): 
    return {
        '__EVENTTARGET'     : 'ctl00$ContentPlaceHolder1$gvResultados',
        '__EVENTARGUMENT'   : '',
        '__LASTFOCUS'       : '',
        '__VIEWSTATE'       : '',
        '__EVENTVALIDATION' : '',

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
        'ctl00$ContentPlaceHolder1$cmdBuscar'               : 'Buscar'
    }

def get_http_headers():
   return {
        'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES)'
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

def parse_and_save_to_file(html, file_name): 
    f = codecs.open( file_name, 'w', 'utf-8' )
    f.write('"%s";"%s";"%s";"%s";"%s"' % ('id', 'name', 'surname1', 'surname2', 'birthday'))
    f.write("\n".join(get_data_from_html(html)))
    f.close()

def request_initialized_parameters(): 
    req = requests.get(get_uri(), headers=get_http_headers())
    if req.status_code != 200:
        print "error requesting initialized parameters"
        exit()
    return get_parameters_from_html(req.text)

def get_parameters_from_html(html):
    soup = BeautifulSoup(html)
    parameters = get_default_parameters()
    parameters['__VIEWSTATE']          = soup.find('input', id='__VIEWSTATE').get('value')
    parameters['__EVENTVALIDATION']    = soup.find('input', id='__EVENTVALIDATION').get('value') 
    return parameters

def format_eventargument(page = 1):
    return 'Page$%d' % page

def update_parameters_with_page(page, parameters):
    parameters['__EVENTARGUMENT'] = format_eventargument(page) if (page > 1) else ''
    if (page > 1):
        del parameters['ctl00$ContentPlaceHolder1$cmdBuscar']
    return parameters

def request_page_and_save(parameters, filename):
    req = requests.post(get_uri(), data=parameters, headers=get_http_headers())
    if req.status_code != 200:
        print "error!"
        exit()
    html = req.text
    parse_and_save_to_file(html, filename)
    return get_parameters_from_html(html)

if __name__ == "__main__":
    pages = [1, 2, 3]
    print "retrieving initial page"
    parameters = request_initialized_parameters()
    time.sleep(1)
    for page in pages:
        parameters = update_parameters_with_page(page, parameters)
        #print requests.post("http://httpbin.org/post", data=parameters, headers=get_http_headers()).text
        print "retrieving page %d..." % page
        parameters = request_page_and_save(parameters, 'page-%s.txt' % page)
        time.sleep(1)


