# Hidrometros_reader
Program for reading data of hydrometers in https://www.argentina.gob.ar/transporte/administracion-general-puertos-se/via-navegable-troncal/hidrometros


Requires having installed tesseract for reading images, and having a chromedrive.exe file for corresponding browser in root.


##########################################################
Programa para leer mareas de los hidrometros presentes en 
https://www.argentina.gob.ar/transporte/administracion-general-puertos-se/via-navegable-troncal/hidrometros

En carpeta /DATA_files guarda los archivos de cada hidrómetro.
En carpeta /IMAGES_files guarda último screenshot de la web
de cada hidrómetro.
En caso de querer modificar destino de archivos de los hidrómetros,
modificar Folders_datos.txt. 

Para funcionar, el programa necesita que en el directorio de
Hidrometros_reader.py o de Hidrometros_reader.exe (en /dist este último),
según como se ejecute, este el ejecutable chromedriver.exe (correspondiente
a la versión de google chrome instalada en la PC).
A su vez, necesita que en la PC se encuentre instalado el programa
Tesseract en C:\Program Files\Tesseract-OCR.

En caso de aparecer nuevos hidrómetros en la web, o de cambiar la dirección
de alguno, modificar archivo Info_hidrometros.txt (el mismo contiene
índice del hidrómetro (para TideManager), nombre y dirección web.
