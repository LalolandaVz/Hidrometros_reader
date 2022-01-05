# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 02:54:05 2022

@author: hid28serv
"""

import pytesseract as pytesseract
from PIL import Image
from selenium import webdriver
import numpy as np
from datetime import datetime
import time
import schedule

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
TESSDATA_PREFIX = 'C:\Program Files\Tesseract-OCR'
tessdata_dir_config = '--tessdata-dir "C:\Program Files\Tesseract-OCR\tesseract"'


def get_text(image):
    return pytesseract.image_to_string(image)


URL_Ramallo = 'http://hidrografia2.agpse.gob.ar/Ramallo/index.html'
URL_SanNicolas = 'http://hidrografia2.agpse.gob.ar/SanNicolas/index.html'
URL_VillaConstitucion = 'http://hidrografia2.agpse.gob.ar/VillaConstitucion/index.html'
URL_Rosario = 'http://hidrografia2.agpse.gob.ar/Rosario/index.html'
URL_SanLorenzo = 'http://hidrografia2.agpse.gob.ar/SanLorenzo/index.html'
URL_Parana = 'http://hidrografia2.agpse.gob.ar/Parana/index.html'
URL_SantaFe = 'http://hidrografia.agpse.gob.ar:53880/SantaFe/index.html'
URL_Hernandarias = 'http://hidrografia2.agpse.gob.ar/Hernandarias/index.html'
URL_SantaElena = 'http://hidrografia.agpse.gob.ar:53880/SantaElena/index.html'
URL_LaPaz = 'http://hidrografia2.agpse.gob.ar/LaPaz/index.html'
URL_Reconquista = 'http://hidrografia2.agpse.gob.ar/Reconquista/index.html'
URL_Goya = 'http://hidrografia2.agpse.gob.ar/Goya/index.html'
URL_BellaVista='http://hidrografia2.agpse.gob.ar/BellaVista/index.html'
URL_Empedrado = 'http://hidrografia2.agpse.gob.ar/Empedrado/index.html'
URL_Barranqueras = 'http://hidrografia2.agpse.gob.ar/Barranqueras/index.html'
URL_Corrientes='http://hidrografia2.agpse.gob.ar/Corrientes/index.html'
URL_PasodelaPatria='http://hidrografia2.agpse.gob.ar/PasodelaPatria/index.html'

BASE_URL = [URL_Ramallo,URL_SanNicolas,URL_VillaConstitucion,URL_Rosario,URL_SanLorenzo,URL_Parana,URL_SantaFe,URL_Hernandarias,URL_SantaElena,URL_LaPaz,URL_Reconquista,URL_Goya,URL_BellaVista,URL_Empedrado,URL_Barranqueras,URL_Corrientes,URL_PasodelaPatria]
Name_URL = ['Ramallo','San Nicolas','Villa Constitucion','Rosario','San Lorenzo','Parana','Santa Fe','Hernandarias','Santa Elena','La Paz','Reconquista','Goya','Bella Vista','Empedrado','Barranqueras','Corrientes','Paso de La Patria']
IMAGES_FOLDER = 'C:/Users/Marea/Documents/Hidrometros_reader/IMAGES_files/'
DATA_FOLDER = 'C:/Users/Marea/Documents/Hidrometros_reader/DATA_files/'



def job():
    Tide = ['']*len(BASE_URL)
    Times = ['']*len(BASE_URL)
    Date = ['']*len(BASE_URL)
    Emptys=['']*len(BASE_URL)
    for h in range(0,len(Times)): Emptys[h]=Times[h]==''

    while any(Emptys):    
        for i in range(0,len(BASE_URL)):

            if Times[i]=='':            
                #BASE_URL = 'http://hidrografia2.agpse.gob.ar/SanLorenzo/index.html'
                print(datetime.now())
    
                
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                
                
                driver = webdriver.Chrome(r"chromedriver.exe",chrome_options=options)
                
                driver.get(BASE_URL[i])
                driver.execute_script("document.body.style.zoom='250%'")
                #get window size
                s = driver.get_window_size()
                #obtain browser height and width
                w = driver.execute_script('return document.body.parentNode.scrollWidth')
                h = driver.execute_script('return document.body.parentNode.scrollHeight')
                #set to new window size
                driver.set_window_size(w*25, h*25)
                
                
                
                #obtain screenshot of page within body tag
                driver.find_element_by_tag_name('body').screenshot(IMAGES_FOLDER + Name_URL[i] + '.png')
                driver.set_window_size(s['width'], s['height'])
                driver.quit()
                
                img = Image.open(IMAGES_FOLDER + Name_URL[i] + '.png')
                
                img_cut= img.crop((680,180,810,290))
                Tide[i] = get_text(img_cut)
                
                
                img = Image.open(IMAGES_FOLDER + Name_URL[i] + '.png')
                
                img_cut= img.crop((1055,180,1353,290))
                Date[i] = get_text(img_cut)
                
                
                
                img = Image.open(IMAGES_FOLDER + Name_URL[i] + '.png')
                
                img_cut= img.crop((1360,180,1600,290))
                Times[i] = get_text(img_cut)

        for h in range(0,len(Times)): Emptys[h]=Times[h]==''        
    
    
    
    for i in range(len(Tide)):
        Tide[i]=Tide[i][0:-1]
        Times[i]=Times[i][0:-1]
        Date[i]=Date[i][0:-1]

    for i in range(0,len(Tide)):
        if Tide[i]=='NAN':
            Tide[i]='-9999.0'
        elif Tide[i]=='':
            Tide[i]='-9999.0'
    
    DateandTime = ['None']*len(Date)
    for i in range(0,len(Times)):
        DateandTime[i] = Date[i] + ' ' + Times[i]
        DateandTime[i] = datetime.strptime(DateandTime[i],'%d/%m/%Y %H:%M:%S')
        DateandTime[i] = DateandTime[i].strftime('%Y-%m-%d %H:%M:%S')
        
    
    
    index=[95,29,30,27,99,19,2,5,6,7,10, 9,11,12,16,13,4]
    index2=12   
    for i in range(0,len(Times)):
        
        
        try:
            HIDROMETRO = np.genfromtxt(DATA_FOLDER + Name_URL[i] + '.txt',delimiter='\n',dtype=str)
            HIDROMETRO = list(HIDROMETRO)
            string=str(index[i])+'|Estacion ' + Name_URL[i] + '|' + DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'
            if string!=HIDROMETRO[-1]:
                HIDROMETRO.append(string)
                HIDROMETRO = np.array(HIDROMETRO)
                np.savetxt(DATA_FOLDER + Name_URL[i] + '.txt',HIDROMETRO,fmt='%s')            
            
        except:
            HIDROMETRO = list([str(index[i])+'|Estacion ' + Name_URL[i] + '|' + DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'])
            HIDROMETRO.append(HIDROMETRO[0])
            HIDROMETRO = np.array(HIDROMETRO)
            np.savetxt(DATA_FOLDER + Name_URL[i] + '.txt',HIDROMETRO,fmt='%s')
    
        index2 = index2 + 1 


Actualizacion = ["00:02","02:00","04:00","06:02","08:00","10:00","12:02","14:00","16:00","18:02","20:00","22:00"]
schedule.every().day.at(Actualizacion[0]).do(job)
schedule.every().day.at(Actualizacion[1]).do(job)
schedule.every().day.at(Actualizacion[2]).do(job)
schedule.every().day.at(Actualizacion[3]).do(job)
schedule.every().day.at(Actualizacion[4]).do(job)
schedule.every().day.at(Actualizacion[5]).do(job)
schedule.every().day.at(Actualizacion[6]).do(job)
schedule.every().day.at(Actualizacion[7]).do(job)
schedule.every().day.at(Actualizacion[8]).do(job)
schedule.every().day.at(Actualizacion[9]).do(job)
schedule.every().day.at(Actualizacion[10]).do(job)
schedule.every().day.at(Actualizacion[11]).do(job)

while 1:
    try:
        schedule.run_pending()    
        time.sleep(1)
    except:

        continue



