import pandas
import openpyxl
import lxml
import os

#Tomar el archivo de la carpeta para extraer el dataframe
class Conversor:
    def __init__(self):
        self.output = os.getenv('OUTPUT_PATH')
        
    def process(self,ruta):
       
        table = pandas.read_html(ruta)[0]
        table.to_excel(self.output,index=False,index_label=False,header=False,sheet_name="Reporte")

if __name__ == '__main__':
    ruta = input('Copia la ruta del archivo que quieres convertir:')
    app = Conversor()
    app.process(ruta)
