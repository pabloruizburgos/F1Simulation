Simulación de Campeonato de F1 en Python

Este repositorio contiene el proyecto de la Práctica 2 entregable de la asignatura de Inteligencia Artificial. En este proyecto, se realiza una simulación de un campeonato de Fórmula 1 utilizando Python y la biblioteca SimPy, con el objetivo de analizar diferentes estrategias y determinar cuál podría ser la más efectiva. Los resultados de la simulación se analizan utilizando un Jupyter Notebook.
Objetivos del Proyecto

El principal objetivo de este proyecto es aplicar técnicas de simulación y análisis de datos para entender qué estrategias de carrera en Fórmula 1 podrían resultar en los mejores resultados bajo diferentes condiciones. Esto incluye:

    Simular múltiples escenarios de carrera.
    Analizar el impacto de distintas estrategias de pit stop y configuraciones de vehículos.
    Utilizar análisis de datos para evaluar el rendimiento de las estrategias simuladas.

Estructura del Repositorio

El repositorio está organizado de la siguiente manera:

    simulacion_f1.py: Script de Python que utiliza SimPy para la simulación del campeonato.
    analisis_resultados.ipynb: Jupyter Notebook para el análisis de los datos generados por la simulación.
    data/: Directorio que contiene los datos generados y utilizados por la simulación.
    docs/: Documentación adicional y recursos utilizados o generados durante el proyecto.

Herramientas Utilizadas

    Python: Lenguaje de programación utilizado para desarrollar la simulación y el análisis de datos.
    SimPy: Biblioteca de Python para la simulación de eventos discretos.
    Jupyter Notebook: Utilizado para el análisis de datos y la visualización de resultados.

Cómo Utilizar Este Repositorio

Para ejecutar este proyecto localmente, siga estos pasos:

    Clone el repositorio en su máquina local usando:

    bash

git clone https://github.com/tu_usuario/tu_repositorio.git

Asegúrese de tener instaladas todas las dependencias necesarias:

pip install simpy matplotlib numpy pandas jupyter

Ejecute el script de simulación:

python simulacion_f1.py

Abra el Jupyter Notebook para analizar los resultados:

jupyter notebook analisis_resultados.ipynb

