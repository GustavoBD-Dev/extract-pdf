import pandas as pd
import re, os, camelot
from PyPDF2 import PdfFileReader
from pathlib import Path
import csv
files = "C:/Users/FINSUS-Admin/Downloads/Constancias Cartera/" # ROUTE TO FIND FILES PDF
dirFiles = os.listdir(files) # LIST FILES INROUTE FOLDER
DATA_FILES_PDF =  []    # LIST TO STORE DATA OF FILE PDF
files_no_read = []
# NAME OF HEAD COLUMNS
columnas = ['RFC', 'CURP', 'Nombre (S)', 'Primer apellido', 'Segundo Apellido', 
            'Fecha incio de operaciones', 'Estatus en el padrón', 'Fecha de ultimo cambio de estado', 
            'Nombre comercial', 'Codigo Postal', 'Nombre de vialidad', 
            'Numero Interior', 'Nombre de la Localidad', 'Nombre de la entidad Federativa', 'Tipo de vialidad', 
            'Numero exterior', 'Nombre de la colonia', 'Nombre del municipio', 'Entre calle']
DATA_FILES_PDF.append(columnas)
for fichero in dirFiles: # EACH FILE TO DO
    # IGNORES FILES THAT DO NOT HAVE THE FORMAT
    try:
        print(fichero)
        data_in_file = []
        ficheropath = os.path.join(files, fichero) 
        filename = Path(ficheropath).stem
        if os.path.isfile(ficheropath) and (fichero.endswith('.pdf') or fichero.endswith('.PDF')):  # VALIDATE FILE PDF
            temp = open(os.path.join(files, fichero), 'rb')
            PDF_read = PdfFileReader(temp)
            first_page = PDF_read.getPage(0)
            text = str(first_page.extractText()) 
            tables = camelot.read_pdf(os.path.join(files, fichero)) 
            df = tables[0].df 
            df_out = pd.DataFrame(df)
            for i in range(1,10):
                data_in_file.append(df_out[1][i])
            tables = camelot.read_pdf(os.path.join(files, fichero)) 
            df = tables[1].df 
            df_out = pd.DataFrame(df)  
            for i in range(2):
                for j in range(1, 6):
                    data_in_file.append(str(str(df_out[i][j]).split(':')[1]).replace('\n',' '))
            # ADD DATA OF FILE IN LIST
            DATA_FILES_PDF.append(data_in_file)
    except:
        print(fichero, ' NO SE PUDO LEER')
        files_no_read.append(fichero)

# SAVE DATA IN FILE CSV
with open('DATAPDF.csv', 'w', newline='') as file:
    writer = csv.writer(file,delimiter=',')
    writer.writerows(DATA_FILES_PDF)
# SAVE DATA IN FILE CSV NAME OF FILES COULDN´T BE READ
with open('DATAPDF_NO_READ.csv', 'w', newline='') as file:
    writer = csv.writer(file,delimiter=',')
    writer.writerows(files_no_read)
