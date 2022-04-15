from os import remove
import xml.etree.ElementTree as Xet
#import pandas as pd
import gzip
import requests
import time
#from selenium.webdriver.chrome.service import Service
#from selenium import webdriver
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import datetime
import sys
from datetime import datetime, date, timedelta
canales = []
canal = []
horarios = []
horario = []
linea = 1
texto = ''
anterior = ''


def cambio_hora(fecha, hora_texto, modif_horaria):
    global anterior
    partes = (hora_texto.split('-'))
    parte0 = partes[0].strip()
    pp1 = parte0.split(' ')[0]
    p1 = parte0.split(' ')[1]
    h1 = int(pp1.split(':')[0].replace('24', '00'))
    m1 = int(pp1.split(':')[1].replace(' ', '0'))
    parte1 = partes[1].strip()
    pp2 = parte1.split(' ')[0]
    p2 = parte1.split(' ')[1]
    h2 = int(pp2.split(':')[0].replace('24', '00'))
    m2 = int(pp2.split(':')[1].replace(' ', '0'))
    if p1 == 'P.M.':
        h1 = h1+12
    if p2 == 'P.M.':
        h2 = h2+12
    dia = fecha.day
    mes = fecha.month
    año = fecha.year
    ahora = datetime.now()
    dia2 = dia
    mes2 = mes
    año2 = año
    if p1 == 'A.M.' and anterior == 'P.M.':
        fecha2 = (fecha+timedelta(days=1))
        dia2 = (fecha2).day
        mes2 = (fecha2).month
        año2 = (fecha2).year
        pass

    res = ' start ="' + str(año*10000000000+mes*100000000+dia *
                            1000000+h1*10000+m1*100)+' '+modif_horaria+'" stop="'+str(año2*10000000000+mes2*100000000+dia2 *
                                                                                      1000000+h2*10000+m2*100)+' '+modif_horaria+'">\n'

    anterior = p2
    return res


def extrae(texto_origen, texto_buscado, texto_fin):
    i = texto_buscado
    f = texto_fin
    try:
        esta = texto_origen.find(i)

        if esta >= 0:
            inicio = texto_origen.find(i)+len(i)
            fin = texto_origen.find(f, inicio)
            r = texto_origen[inicio: fin]
            return [r, fin]
        else:
            r = ['', fin]
            return r
    except:
        r = ['', 0]
        return r


x = datetime.now()
fecha = "%s/%s/%s" % (x.day, x.month, x.year)
"""
driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://www.izzi.mx/webApps/entretenimiento/guia")
time.sleep(2)

#chrome_options = driver.__getattribute__()
#print (chrome_options)
def lee_horarios(canal):
    global texto
    global linea
    try:
        xpath = f"/html/body/main/section/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[{linea}]"
        lista_horarios = driver.find_element(
            by=By.XPATH, value=xpath).get_attribute('outerHTML')
        linea = linea+1
        salida = 1

        while(salida > 0):
            texto = texto+'<programme channel="' + \
                canal.replace('&amp;', ' y ')+'_la"'
            resultado = extrae(lista_horarios, 'data-duracion="', '"')
            lista_horarios = lista_horarios[resultado[1]:]
            horarios.append(resultado[0])
            if resultado[1] > 0:
                resultado = extrae(
                    lista_horarios, '"hora-inicial">', '</span>')
                lista_horarios = lista_horarios[resultado[1]:]
                title = extrae(lista_horarios, 'alt="', '"')[0]
                lista_horarios = lista_horarios[resultado[1]:]
                #texto = texto+'<channel id ="'+resultado[0]+'">\n'
                horarios.append(resultado[0])
                resultado = extrae(
                    lista_horarios, '<p class="fw-medium">', '</p>')
                lista_horarios = lista_horarios[resultado[1]:]
                start_stop = cambio_hora(datetime.now(), resultado[0], '+0500')
                img = extrae(lista_horarios, '<img data-src="', '"')
                lista_horarios = lista_horarios[resultado[1]:]
                horarios.append(resultado[0])
                desc = extrae(
                    lista_horarios, '<p>', '</p>')[0].replace('<span class="bold program-label">', '').replace('<span class="bold program-label">Actores:</span> ', '').replace('<span class="program-content">', '').replace('</span>', '')
                lista_horarios = lista_horarios[resultado[1]:]
                horarios.append(resultado[0])
                resultado = extrae(lista_horarios, 'program-langs', '">')
                lista_horarios = lista_horarios[resultado[1]:]
                pass

            texto = texto+start_stop+'<title>'+title + \
                '</title>\n'+'<desc>'+desc+'</desc>\n</programme>\n'

            if len(lista_horarios) > 150:
                salida = 1
            else:
                salida = 0

        pass

    except:
        print("Error inesperado:", sys.exc_info()[0])


# d0.click()
# time.sleep(1)
xpath = "/html/body/main/section/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul"
lista_canales = driver.find_element(
    by=By.XPATH, value=xpath).get_attribute('outerHTML')
salida = 1
while(salida > 0):
    resultado = extrae(lista_canales, '<img src="', '"')
    lista_canales = lista_canales[resultado[1]:]
    logo = 'https://www.izzi.mx'+resultado[0]
    #texto = texto+'<channel id ="'+canal_id+'">\n'
    #canal.append(resultado[0].replace('"', ''))
    if resultado[1] > 0:
        resultado = extrae(lista_canales, 'alt="', '"')
        canal_id = resultado[0]
        canal.append(canal_id)
        texto = texto+'<channel id = "'+canal_id.replace('&amp;', ' y ')+'_la">\n<display-name>' + \
            canal_id.replace('&amp;', ' y ')+'_la' + \
            ' </display-name>\n </channel>\n'
        lista_canales = lista_canales[resultado[1]:]

        resultado = extrae(lista_canales, '</l', '>')
        lista_canales = lista_canales[resultado[1]:]

    if len(lista_canales) > 8:
        salida = 1
    else:
        salida = 0
    #texto = texto+'<channel id ="'+canal_id+'">\n'
    #texto = texto+'<display-name>' + resultado[0]+'</display-name>\n</channel>\n'
    #texto = texto+'<programme channel="'+resultado[0]+'_la"'
    canales.append(canal)
    canal = []

# lee_horarios()
for can in canales:

    lee_horarios(can[0])


driver.close()
f = open('aizzi.xml', 'w')
f.write(texto.replace('></desc>', '>nn</desc>'))
f.close
"""
# descarga xml de la red y combina tambien suma aizzi.xml local

"""
    ["es.xml", 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/es.xml', 'es'],
          ["mx.xml", 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/mx.xml', 'mx'],
          ["smes.xml", 'https://i.mjh.nz/SamsungTVPlus/es.xml', ''],
"""
mylist = [ ["mv.xml", 'https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guia.xml', '']]
mylist_locales = [["aizzi.xml", 'aizzi.xml', '']]

i = 1
primera = ""
otras = ""


def insertar_texto(cadena, texto):
    posicion = cadena.find('<programme channel="')
    if posicion <= len(cadena):
        izquierda = cadena[:posicion]
        derecha = cadena[posicion:]

        return '{} {} {}'.format(izquierda, texto, derecha)
    else:
        raise ValueError(
            'La posición donde se quiere insertar el texto no existe.')


for x in mylist:
    url = x[1]
    myfile = requests.get(url)
    open(x[0], 'wb').write(myfile.content)
    f = open(x[0], 'r', encoding="utf8")

    if i == 1:
        primera = f.read()
        f.close()
        primera = primera.replace('<channel id="', '<channel id="' +
                                  x[2]).replace('<programme channel="', '<programme channel="'+x[2]).replace("</display-name>", "_"+x[2]+"</display-name>")
    else:
        otras = f.read()
        f.close()
        otras = otras[otras.find('<channel id="'):]
        otras = otras.replace('<channel id="', '<channel id="' +
                              x[2]).replace('<programme channel="', '<programme channel="'+x[2]).replace("</display-name>", "_"+x[2]+"</display-name>")
        otras = otras.replace("</tv>", "")
        primera = insertar_texto(primera, otras)
        #p1 = otras[0: otras.find('<programme channel="')]
        #p2 = otras[otras.find('<programme channel="'):len(otras)]
        #primera = primera[otras.find('<channel id="'):len(otras)]

    i = i+1


locales = open(mylist_locales[0][1], "r")
otras = locales.read()
locales.close
primera = insertar_texto(primera, otras)

f = open('todo.xml', 'w', encoding="utf8")
f.write(primera.replace('></desc>', '>x</desc>'))
f.close()
for x in mylist:
    remove(x[0])
# crea el xml con los datos recopilados
lista_canales = ["ESAJ45000181E", "A y E_la", "CINEMAX", "ESBC40000248", "mx5e972a21ad709d00074195ba", "CINE", "es5f1ac2591dd8880007bb7d6d", "mx5dcb62e63d4d8f0009f36881", "ESAJ3800001KT", "es5f1ac1f1b66c76000790ef27", "mx5dcde437229eff00091b6c30", "mx5ddc4e8bcbb9010009b4e84f", "mx5dcddf1ed95e740009fef7ab", "es5f6a38eaa5b68b0007a00e7a", "mx5f2817d3d7573a00080f9175", "es5f1ac8a87cd38d000745d7cf", "SONY CHANELS", "STUDIO UNIVERSAL", "TCM", "TNT", "WARNER", "butaca tv 2", "ESBA3300019NX", "ESBA3300022SL", "cine life", "cinema+", "ESBA3300021PZ", "ESAJ4500019AM", "ESBA2200008NQ", "cosmos tv", "DARK", "ESAJ4500020V7", "ESBA3300017FA", "FX", "GOLDEN PLUS", "ESBA2200004G5", "Peliculas 28", "peliculas pluto", "ESBC400001QQ", "es6086d3f420fc8500075f8dbf", "runtime-espanol-roku", "topcine", "ESBA3300039ZX", "wow", "Peliculas 01", "Peliculas 02", "Peliculas 03", "Peliculas 04", "Peliculas 05", "Peliculas 06", "Peliculas 07", "Peliculas 08", "Peliculas 09", "Peliculas 10", "Peliculas 11", "Peliculas 12", "Peliculas 13", "Peliculas 14", "Peliculas 15", "Peliculas 16", "Peliculas 17", "Peliculas 18", "Peliculas 19", "Peliculas 20", "Peliculas 21", "Peliculas 22", "Peliculas 23", "Peliculas 24", "Peliculas 25", "Peliculas 26", "Peliculas 27", "Peliculas 29", "Peliculas 30", "Peliculas 31", "Peliculas 32", "Cartelera lavozdetucuman", "es5f984c1dc54853000797a5e8", "CINE.AR", "EvaRetro", "EvaStream", "feel good verdi hd españa", "frecuencia musical tv", "LATINO DE PELICULA", "MiTVTelevisiónClásica", "my time movies 1", "my time movies 2", "PELICULAS CB", "planeta tv", "es61373bb45168fe000773eecd", "mx609059dc63be6e0007b4eca6", "es5f1ac8099c49f600076579b2", "mx5dcdde78f080d900098550e4", "es5f1ac947dcd00d0007937c08", "mx5dcddfcb229eff00091b6bdf", "mx5dd6ddb30a1d8a000908ed4c", "mx5dd7ea2aeab5230009986735", "es5f1ac9a2d3611d0007a844bb", "mx5fcea359e533cb0007215c71", "es60cc807324d60a0007708dc8", "mx5defde6d6c07b50009cf0757", "es60c8a24e17da110007eed4fd", "rakuten tv acción hd españa", "rakuten tv comedias hd españa", "rakuten tv drama hd españa", "24 HORAS", "ARAGON TV INT", "EL TRECE", "LA 1", "LA 2", "LA SEXTA", "CANAL10", "CANAL26", "canl nn", "CRONICA", "EL TRECE ARG", "EL12TV", "NETTV", "TELECANAL12HD", "TELEFERO", "alf", "ESBA1400001OG", "es60d3574e97f10800078455de", "ELCHAVODEL8", "ESBA3300027H5", "LOS SIMSONS", "The Walking Dead en español", "Viaje a las estrellas", "307SonyComedias", "central comedy", "cultura 24 tv", "Discovery Science",
                 "ENCUENTRO", "HISTORY", "LOVE NATURE EN ESPAÑOL", "ESBA22000102A", "ESBA3300036W1", "mx5dd8364ea1d6780009929902", "mx5de5758e1a30dc00094fcd6c", "mx5dd85eac039bba0009e86d1d", "SaberMas", "miami tv internacional hd estados unidos", "miami tv jenny for you hd estados unidos", "miami tv méxico hd méxico", "ESBA1400008NE", "ESBA3300024AJ", "buin somos todos cl", "ESAJ3800005C5", "ESBA2200005D6", "DISTRITOTV", "es60218baa464ef900073168c1", "mx5f23102d5e239d00074b092a", "ESBA22000094V", "ESBA1400006NP", "mx6095ad97351eb0000754c1e6", "ESAJ49000017H", "mx615b9855c6b58b000724477f", "ivestigacion", "m+", "mx5e3ddbd27091820009f86dd9", "ESAJ4500023Y5", "ESAJ3800007PC", "mx5dcde2f53449c50009b2b4dc", "ESAJ3800008ZD", "ESAJ4500021HQ", "retro plus tv señal 3 cl", "ESBA2200006B4", "ESAJ4500016BH", "ESBA330004121", "mx5efb8c19b2678b000780d032", "es60ed5fb9c4716d0007d180c5", "mx6109a9f5531b840007a4a187", "es61922be835f3910007fc58f6", "es5f1acbed25948a0007ffbe65", "mx5e67d41b93312100076f3fca", "es5f1acba0d1f6340007db8843", "mx5f610042272f68000867685b", "es5f984f4a09e92d0007d74647", "es602ba1cfb386d30007aecbbe", "mx5dcde27ffae9520009c0c75a", "es612ce5214bb5790007ad3016", "es5f1acc3e061597000768d4ea", "es5f1aca8310a30e00074fab92", "es60dafb9a0df1ba000758d37b", "es6193963c5a960200074ce816", "es60c343007bcabe0007242aa6", "es5f1acb4eebe0f0000767b40f", "ESBA3300025WZ", "es5f1acc91cc9e1b000711ff21", "mx5dd837642c6e9300098ad484", "mx5dd837642c6e9300098ad484", "mx5de802659167b10009e7deba", "mx5de802659167b10009e7deba", "es5f1acc3e061597000768d4ea", "es5f1abce155a03d0007718834", "mx5ffcc21a432945000762d06b", "mx609ae5cd48d3200007b0a98e", "mx5e8397936791b30007ebb5a7", "es5f9853138d19af0007104a8d", "74 tv", "canal visión dorada sd caldas", "mx5f9992c685a2a80007fa414a", "es60e45687313c5f0007bc8e94", "ELTOROTV", "EXTREMATV", "mx5ebaccf1734aaf0007142c86", "gourmet tv", "HMTV", "es60dd6b1da79e4d0007309455", "es60e4573c9f963e00077ecf25", "mx5f230e416b68ff00075b0139", "MTMAD24H", "mx5f9afb01816137000737f799", "mx5dd834c66fe2ca0009303b8d", "mx5ddc266f80e3550009136843", "es5f1acdaa8ba90f0007d5e760", "mx5dcde0657444a40009cd2422", "es61cd78920b90cb0007e28231", "mx61099f2b40d0640007fc5aa2", "mx5dd6ab8056beb000091fc6b6", "mx6109ab25b84d6a0007504886", "mx5dcde197f6591d0009839e04", "mx609062295c2b8f0007199e7a", "es60c343ad476ec00007c2ec1a", "mx5dcddfbdb7cf0e0009ae09ea", "mx5df265697ec3510009df1ef0", "7NNNOTICIAS", "samsung1", "mx619d59b7cbef25000728221c"]

start = ""
stop = ""
channel = ""
desc = ""
title = ""
icon = ""
url = ""
country = ""
episodenum = ""
starrating = ""
subtitle = ""
category = ""
id = ""
displayname = ""

cols_channels = ["id", "display-name", "url", "icon"]
rows_channels = []
cols_programmes = ["start", "stop", "channel",
                   "desc", "title", "icon", "url",
                   "country", "episode-num", "star-rating",
                   "sub-title", "category"]
rows_programmes = []
lin = '<?xml version = "1.0" encoding = "UTF-8"?> <!DOCTYPE tv SYSTEM "xmltv.dtd" ><tv generator-info-name = "www.matthuisman.nz" >\n'
linp = ''
try:
    xmlparse = Xet.parse('todo.xml')
    root = xmlparse.getroot()
    # print(root)
    i = 0
    for hijo in root:
        if hijo.tag == 'channel':
            i = i+1
            # print(str(i))
            id = hijo.attrib["id"]
            for nieto in hijo:
                if nieto.tag == 'display-name':
                    displayname = nieto.text
                elif nieto.tag == 'url':
                    url = (nieto.text)
                elif nieto.tag == 'icon':
                    icon = (nieto.attrib["src"])
            if id in lista_canales:
                lin = lin+'<channel id="'+id+'">\n'
                lin = lin+'<display-name>'+displayname+'</display-name>\n'
                lin = lin+'</channel>\n'
                rows_channels.append({"id": id,
                                      "display-name": displayname,
                                      "url": url,
                                      "icon": icon})
                id = ""
                displayname = ""
                url = ""
                icon = ""

        elif hijo.tag == 'programme':

            i = i+1
            # print(str(i))
            start = (hijo.attrib["start"])
            stop = (hijo.attrib["stop"])
            channel = (hijo.attrib["channel"])

            for nieto in hijo:
                if nieto.tag == 'desc':
                    desc = (nieto.text.replace('&amp;', '').replace(
                        '\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace(';', '.\n'))
                    #print(desc)
                elif nieto.tag == 'title':
                    title = (nieto.text.replace(
                        '&amp;', ' ').replace(';', ' '))
                elif nieto.tag == 'icon':
                    icon = (nieto.attrib["src"])
                elif nieto.tag == 'url':
                    url = (nieto.text)
                elif nieto.tag == 'country':
                    country = (nieto.text)
                elif nieto.tag == 'episode-num':
                    episodenum = (nieto.text)
                elif nieto.tag == 'star-rating':
                    starrating = (nieto[0].text)
                elif nieto.tag == 'sub-title':
                    subtitle = (nieto.text.replace(
                        '&amp;', ' ').replace(';', ' '))
                elif nieto.tag == 'category':
                    category = (nieto.text.replace(
                        '&amp;', ' ').replace(';', ' '))
            if channel in lista_canales:
                linp = linp+'<programme channel="'+channel + \
                    '" start="'+start+'" stop="'+stop+'">\n'
                linp = linp+'<title>'+title+'</title>\n'
                linp = linp+'<desc>'+desc+'</desc>\n'
                linp = linp+'</programme>\n'
                rows_programmes.append({"start": start,
                                        "stop": stop,
                                        "channel": channel,
                                        "desc": desc,
                                        "title": title,
                                        "icon": icon,
                                        "url": url,
                                        "country": country,
                                        "episode-num": episodenum,
                                        "star-rating": starrating,
                                        "sub-title": subtitle,
                                        "category": category})
                start = ""
                stop = ""
                channel = ""
                desc = ""
                title = ""
                icon = ""
                url = ""
                country = ""
                episodenum = ""
                starrating = ""
                subtitle = ""
                category = ""


except Exception as err:
    print("Error:", err)
finally:
    pass

f = open('./templates/todon.xml', 'w')
f.write(lin+linp+'</tv>')
f.close()
remove("todo.xml")
#df_channels = pd.DataFrame(rows_channels, columns=cols_channels)
#df_programmes = pd.DataFrame(rows_programmes, columns=cols_programmes)
# Writing dataframe to csv
#df_channels.to_csv('channels.csv', sep=';')
#df_programmes.to_csv('programmes.csv', sep=';')
