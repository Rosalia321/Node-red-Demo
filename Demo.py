import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

csv = pd.read_csv('Linea Bob_DashboardData_20240701-030000000_20240729-030000000.csv',sep=';')
dataframe = pd.DataFrame(csv[["Calidad","Disponibilidad","EstadoTexto"]])
estado = dataframe["EstadoTexto"].value_counts()  
t = csv["_time"]
disponibilidad = csv["Disponibilidad"]
parada = csv["CantMinutosParadaTotales"]
print(parada)

fig, ax = plt.subplots(figsize=(10,7))
ax.plot(t,parada)

#plt.subplot(1,2,1)
#estado.plot(kind="pie",autopct='%1.01f%%')
#plt.title("xd")

plt.show()

