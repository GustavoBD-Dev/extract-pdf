import pandas as pd
import re, os, camelot
from PyPDF2 import PdfFileReader
from pathlib import Path
import csv
files = "C:/Users/FINSUS-Admin/Documents/Code/read-pdf/inputs/" # route to find files PDF
dirFiles = os.listdir(files) # list files in route
DATA_FILES_PDF =  []    # list to save data in files PDF
# name of columns to get data 
columnas = ['RFC', 'CURP', 'Nombre (S)', 'Primer apellido', 'Segundo Apellido', 
            'Fecha incio de operaciones', 'Estatus en el padrón', 'Fecha de ultimo cambio de estado', 
            'Nombre comercial', 'Codigo Postal', 'Nombre de vialidad', 
            'Numero Interior', 'Nombre de la Localidad', 'Nombre de la entidad Federativa', 'Tipo de vialidad', 
            'Numero exterior', 'Nombre de la colonia', 'Nombre del municipio', 'Entre calle']
DATA_FILES_PDF.append(columnas)
for fichero in dirFiles: # each file to do
    data_in_file = []
    ficheropath = os.path.join(files, fichero) 
    filename = Path(ficheropath).stem
    if os.path.isfile(ficheropath) and (fichero.endswith('.pdf') or fichero.endswith('.PDF')):  # validate PDF
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

# save data in file CSV
with open('DATAPDF.csv', 'w', newline='') as file:
    writer = csv.writer(file,delimiter=',')
    writer.writerows(DATA_FILES_PDF)
