import os
import datetime

os.system('cls' if os.name == 'nt' else 'clear')

fecha_inicio_contrato = input("Fecha Inicio Contrato DD-MM-YYYY: ")
fecha_contrato = datetime.datetime.strptime(fecha_inicio_contrato, '%d-%m-%Y')

print(fecha_contrato)