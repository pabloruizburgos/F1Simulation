import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./simulation_statistics.csv')

# Limpiar los datos y convertir las columnas apropiadamente
df['Compound Type'] = df['Compound Type'].apply(lambda x: eval(x.replace('\'', '\"')))
df['Vuelta'] = pd.to_numeric(df['Vuelta'])
df['PitStop Time'] = pd.to_numeric(df['PitStop Time'])

# Crear un diccionario para mapear los compuestos de neumáticos
compound_map = {'soft': 'S', 'medium': 'M','hard':'H'}

# Función para obtener el compuesto de neumáticos de una vuelta
def obtener_compuesto(row):
    neumaticos = row['Compound Type']
    compuesto = list(neumaticos.keys())[0]
    return compound_map[compuesto]

# Aplicar la función para obtener el compuesto de neumáticos en cada vuelta
df['Compuesto'] = df.apply(obtener_compuesto, axis=1)

# Crear el gráfico
plt.figure(figsize=(12, 8))

# Iterar sobre cada Vehicle y plotear sus cambios de neumáticos
for Vehicle, datos_Vehicle in df.groupby('Vehicle'):
    plt.plot(datos_Vehicle['Vuelta'], datos_Vehicle['Compuesto'], marker='o', label=Vehicle)

# Añadir detalles al gráfico
plt.title('Cambios de Neumáticos por Vuelta')
plt.xlabel('Vuelta')
plt.ylabel('Compuesto de Neumáticos')
plt.yticks(['S','M','H'], ['Soft', 'Medium','Hard'])
plt.legend(title='Vehicle', loc='upper right')
plt.grid(True)
plt.tight_layout()

# Mostrar el gráfico
plt.show()