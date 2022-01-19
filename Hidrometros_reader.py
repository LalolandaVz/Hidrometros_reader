# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 02:54:05 2022

@author: hid28serv
"""
from datetime import datetime
from datetime import timedelta
import pytesseract
from PIL import Image
import numpy as np
import time
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tesseract"'


def get_text(image):
    return pytesseract.image_to_string(image)

#file_destination = IMAGES_FOLDER + Name_URL[i] + '.png'
def screenshot_cut_read_1(URL,file_destination):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"chromedriver.exe",chrome_options=options)
    driver.get(URL)
    driver.execute_script("document.body.style.zoom='250%'")
    #get window size
    s = driver.get_window_size()
    #obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    #set to new window size
    driver.set_window_size(w*25, h*25)

    #Tardan mas en abrir estos hidrometros, le doy tiempo:
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'clips-cards ')))
    except TimeoutException:
        print('Page timed out after 6 secs.')

    #obtain screenshot of page within body tag
    driver.find_element_by_tag_name('body').screenshot(file_destination)
    driver.set_window_size(s['width'], s['height'])
    driver.quit()

    img = Image.open(file_destination)

    img_cut= img.crop((750,180,925,350))
    Tide = get_text(img_cut)

    img_cut= img.crop((1275,180,1605,350))
    Date = get_text(img_cut)

    img_cut= img.crop((1600,180,1865,350))
    Times = get_text(img_cut)

    return [Tide,Date,Times]

def screenshot_cut_read_2(URL,file_destination):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"chromedriver.exe",chrome_options=options)
    driver.get(URL)
    driver.execute_script("document.body.style.zoom='250%'")
    #get window size
    s = driver.get_window_size()
    #obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    #set to new window size
    driver.set_window_size(w*25, h*25)

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'clips-cards ')))
    except TimeoutException:
        print('Page timed out after 2 secs.')

    #obtain screenshot of page within body tag
    driver.find_element_by_tag_name('body').screenshot(file_destination)
    driver.set_window_size(s['width'], s['height'])
    driver.quit()

    img = Image.open(file_destination)

    img_cut= img.crop((680,180,810,290))
    Tide = get_text(img_cut)

    img_cut= img.crop((1055,180,1353,290))
    Date = get_text(img_cut)

    img_cut= img.crop((1360,180,1600,290))
    Times = get_text(img_cut)

    return [Tide,Date,Times]

def screenshot_cut_read_3(URL,file_destination):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"chromedriver.exe",chrome_options=options)
    driver.get(URL)
    driver.execute_script("document.body.style.zoom='500%'")
    #get window size
    s = driver.get_window_size()
    #obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    #set to new window size
    driver.set_window_size(w*50, h*50)

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'clips-cards ')))
    except TimeoutException:
        print('Page timed out after 2 secs.')

    #obtain screenshot of page within body tag
    driver.find_element_by_tag_name('body').screenshot(file_destination)
    driver.set_window_size(s['width'], s['height'])
    driver.quit()

    img = Image.open(file_destination)

    img_cut= img.crop((1380,410,1600,580))
    Tide = get_text(img_cut)

    img_cut= img.crop((2150,410,2700,580))
    Date = get_text(img_cut)

    img_cut= img.crop((2730,410,3200,580))
    Times = get_text(img_cut)

    return [Tide,Date,Times]


Info_hidrometros = np.genfromtxt(r'Info_hidrometros.txt',delimiter='	',dtype=str)
folders = np.genfromtxt(r'Folders_datos.txt',delimiter='	',dtype=str)

#index es el indice con el que comienza la string de cada hidrometro.

index = Info_hidrometros[:,0]
index = list(index)

for i in range(0,len(Info_hidrometros[:,0])):
    index[i] = int(index[i])

BASE_URL = Info_hidrometros[:,2]
Name_URL = Info_hidrometros[:,1]
IMAGES_FOLDER = folders[0]
DATA_FOLDER = folders[1]



def job():
    Tide = ['']*len(BASE_URL)
    Times = ['']*len(BASE_URL)
    Date = ['']*len(BASE_URL)
    Emptys=['']*len(BASE_URL)
    print('comienza ciclo')
    print(datetime.now())

    for h in range(0,len(Times)):
        Emptys[h]=Times[h]==''
    repeater = 0 #indice para limitar las repeticiones cuando no encuentra fecha en el sitio
    while any(Emptys):
        repeater = repeater + 1
        print('repeater =' + str(repeater))
        if repeater==4:
            print('repeater =' + str(repeater) + ' Corta ciclo')
            break

        for i in range(0,len(BASE_URL)):

            if Times[i] == '':
                print('Hidrometro '+ Name_URL[i])
                #Si estoy viendo Brasileria u Oyarvide, tiene distinto tamaño la imagen:
                if Name_URL[i] == 'Brasileira' or Name_URL[i] == 'Oyarvide':

                    [Tide[i],Date[i],Times[i]] = screenshot_cut_read_1(
                        BASE_URL[i],IMAGES_FOLDER + Name_URL[i] + '.png')

                    print('Tide = ' + Tide[i])

                elif Name_URL[i] == 'Carabelitas': #si estoy viendo cualquiera que no sea brasileira y oyarvide

                    [Tide[i],Date[i],Times[i]] = screenshot_cut_read_3(
                        BASE_URL[i],IMAGES_FOLDER + Name_URL[i] + '.png')

                    print('Tide = ' + Tide[i])

                else:
                    
                    [Tide[i],Date[i],Times[i]] = screenshot_cut_read_2(
                        BASE_URL[i],IMAGES_FOLDER + Name_URL[i] + '.png')

                    print('Tide = ' + Tide[i])

        for h in range(0,len(Times)):
            Emptys[h]=Times[h]==''

        print('¿Any emptys?')
        print(Emptys)
        print(any(Emptys))

    #print('todavia sigue 0')
    for i in range(0,len(Times)):
        if Times[i]=='': #para el caso en que falle la web
            Times[i] = '   '
            Date[i] = '   '

        Tide[i]=Tide[i][0:-1]
        Times[i]=Times[i][0:-1]
        Date[i]=Date[i][0:-1]

        if Tide[i]=='NAN' or Tide[i]=='':
            Tide[i]='-9999.0'

    #print('todavia sigue 2')
    DateandTime = ['None']*len(Date)
    for i in range(0,len(Times)):
        DateandTime[i] = Date[i] + ' ' + Times[i]
        if Times[i]=='   ' or Date[i]=='   ':
            DateandTime[i]=''
        else:
            if Name_URL[i] == 'Brasileira' or Name_URL[i] == 'Oyarvide':
                #esta escrita distinta la fecha para oyarvide y brasileira
                print('')
            else:
                DateandTime[i] = datetime.strptime(DateandTime[i],'%d/%m/%Y %H:%M:%S')
                DateandTime[i] = DateandTime[i].strftime('%Y-%m-%d %H:%M:%S')

    #print('todavia sigue 3')

    index2=12   #otro index que deberia tener un numero segun hidrometro,
    #pero al tidemanager no le molesta su valor
    for i in range(0,len(Times)):


        try:
            HIDROMETRO = np.genfromtxt(DATA_FOLDER + Name_URL[i] + '.txt',delimiter='\n',dtype=str)
            HIDROMETRO = list(HIDROMETRO)
            #print('todavia sigue 4')
            if DateandTime[i]=='':
                print('no se agrega')
            else:
                #print('todavia sigue 5, i=' + str(i))
                if Name_URL[i] == 'Brasileira' or Name_URL[i] == 'Baliza Mitre':
                    string=str(index[i])+ '|' + Name_URL[i] + '|' + \
                        DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'
                else:
                    string=str(index[i])+'|Estacion ' + Name_URL[i] + \
                        '|' + DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'

                if string!=HIDROMETRO[-1]:
                    HIDROMETRO.append(string)
                    HIDROMETRO = np.array(HIDROMETRO)
                    np.savetxt(DATA_FOLDER + Name_URL[i] + '.txt',HIDROMETRO,fmt='%s')

        except:
            #print('todavia sigue 4')
            if DateandTime[i]=='':
                print('no se agrega')
            else:

                if Name_URL[i] == 'Brasileira' or Name_URL[i] == 'Baliza Mitre':
                    HIDROMETRO = list([str(index[i])+ '|' + Name_URL[i] + '|' + \
                                       DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'])
                else:
                    HIDROMETRO = list([str(index[i])+'|Estacion ' + Name_URL[i] + '|' + \
                                       DateandTime[i] +'|'+str(index2)+'|Level|'+Tide[i]+'|NULL'])
                HIDROMETRO.append(HIDROMETRO[0])
                HIDROMETRO = np.array(HIDROMETRO)
                np.savetxt(DATA_FOLDER + Name_URL[i] + '.txt',HIDROMETRO,fmt='%s')

        index2 = index2 + 1

Actualizacion = []
horario = datetime(2022,1,1,0,0,0)
Actualizacion.append(horario.strftime('%H:%M'))
for i in range(0,287):
    horario = horario + timedelta(minutes=5)
    Actualizacion.append(horario.strftime('%H:%M'))

for i in range(0,len(Actualizacion)):
    schedule.every().day.at(Actualizacion[i]).do(job)

#schedule.every().day.at('17:57').do(job)

while 1:
    try:
        schedule.run_pending()
        time.sleep(1)
    except:

        continue
