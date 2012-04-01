import requests
from bs4 import BeautifulSoup
import re

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

f = open('test.html', 'r')
html = f.read()
f.close()

soup = BeautifulSoup(html)
parameters_aspx['__VIEWSTATE']          = soup.find('input', id='__VIEWSTATE').get('value')
parameters_aspx['__EVENTVALIDATION']    = soup.find('input', id='__EVENTVALIDATION').get('value')
parameters = dict( parameters_aspx.items() + parameters_search.items() )

headers = {
    'User-Agent' : ''
}
req = requests.post('http://httpbin.org/post', data=parameters, headers=headers)
html = req.text
print html
exit()

soup = BeautifulSoup(html)
table = soup.find('table', id='ctl00_ContentPlaceHolder1_gvResultados')
for rows in table.find_all('tr', recursive=False):
    cols = rows.find_all('td', recursive=False)
    if len(cols) == 5:
        id = re.findall(r'\d+', cols[4].find('a').get('href'))[0]
        name = cols[0].string.strip()
        surname1 = cols[1].string.strip()
        surname2 = cols[2].string.strip()
        birthday = cols[3].string.strip()
        print '"%s";"%s";"%s";"%s";"%s"' % (id, name, surname1, surname2, birthday)
