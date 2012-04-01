import requests
from bs4 import BeautifulSoup

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

parameters = dict( parameters_aspx.items() + parameters_search.items() )

req = requests.post('http://httpbin.org/post', data=parameters)
print req.text
