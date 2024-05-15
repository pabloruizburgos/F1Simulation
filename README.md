# Simulación de Campeonato de F1 en Python

Este repositorio contiene el proyecto de la Práctica 2 entregable de la asignatura de Inteligencia Artificial. En este proyecto, se realiza una simulación de un campeonato de Fórmula 1 utilizando Python y la biblioteca SimPy principalmente, con el objetivo final de analizar diferentes estrategias y determinar cuál podría ser la más efectiva. Los resultados de la simulación se analizan posteriormente utilizando un Jupyter Notebook.



## Objetivos del Proyecto

El principal objetivo de este proyecto es aplicar técnicas de simulación y análisis de datos para entender qué estrategias de carrera podrían resultar en los mejores resultados, bajo diferentes condiciones. Esto incluye:
- Simular múltiples escenarios de carrera (climatología cambiante y condiciones de circuito puntuales).
- Analizar el impacto de distintas estrategias de pit stop y elecciones de compuestos.
- Utilizar análisis de datos para evaluar el rendimiento de las estrategias simuladas.



## Estructura del Repositorio

Dentro de la carpeta principal `F1Simulation_PabloRuiz_JaimeRuiz`, el repositorio está organizado de la siguiente manera:
- `AI_Python_Formula_One_Pablo_Ruiz_Jaime_Ruiz.pdf`: PDF (realizado en LaTeX) que contiene la explicación más profunda de la simulación.
- `analysis.ipynb`: Jupyter Notebook para el análisis de los datos generados por la simulación. 
- `sim.py`: Script de Python con la simulación del campeonato.



## Cómo Utilizar Este Repositorio

Para ejecutar este proyecto localmente, siga estos pasos:

1. Clone el repositorio en su máquina local usando:
   ```
   git clone https://github.com/pabloruizburgos/F1Simulation/tree/main
   ```
2. Asegúrese de tener instaladas todas las dependencias necesarias:
   ```
   pip install simpy matplotlib numpy pandas jupyter random
   ```
3. Ejecute el script de simulación:
   ```
   python3 sim.py
   ```
4. Abra el Jupyter Notebook para analizar los resultados:
   ```
   jupyter notebook analysis.ipynb
   ```


**Nota:** Tras la primera ejecución del código se generarán 4 archivos .csv que contienen datos recopilados durante la simulación. Estos son necesarios para el Jupyter Notebook y su análisis. Todas las nuevas ejecuciones posteriores sobreescribirán estos mismos archivos.


## Autores

Este repositorio ha sido realizado por *Jaime Ruiz* (jaime.ruiz@cunef.edu) y *Pablo Ruiz* (pablo.ruizburgos@cunef.edu).
