import simpy
import random
from typing import Generator
import track
from boxes import Boxes
from vehicle import Vehicle
from track import Track
from statistics import StatisticsCollector # type: ignore


pilots_times = dict() #NO PUEDE SER GLOBAL!!
 
# Vehicle generator
def vehicle_generator(env:simpy.Environment, boxes:Boxes, track:Track, statistics:StatisticsCollector) -> Generator:
    """Generates vehicles and sends them to the charging station.

    Args:
        env (simpy.Environment): Simpy simulation environment
        boxes
     (Boxes): Charging station
        statistics (StatisticsCollector): Statistic collector module
        MINIMAL_ARRIVAL_TIME (int): Minimum vehicules arrival time
        MAXIMUM_ARRIVAL_TIME (int): Maximum vehicules arrival time

    Yields:
        Generator: Simpy event generator
    """

    # Creamos de forma aleatoria el nuevo compuesto a poner al principio de la carrera
    Hamilton = Vehicle(env, "Hamilton", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Sainz = Vehicle(env, "Sainz", boxes.selectCompound(track), 0, 0, boxes, track,0, statistics)
    Alonso = Vehicle(env, "Alonso", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Russell = Vehicle(env, "Russel", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Magnussen = Vehicle(env, "Magnussen", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Leclerc = Vehicle(env, "Leclerc", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    Stroll = Vehicle(env, "Stroll", boxes.selectCompound(track), 0, 0, boxes, track, 0, statistics)
    
    env.process(Hamilton.racing(track, pilots_times))
    env.process(Sainz.racing(track, pilots_times))
    env.process(Alonso.racing(track, pilots_times))
    env.process(Hulkenberg.racing(track, pilots_times))
    env.process(Russell.racing(track, pilots_times))
    env.process(Magnussen.racing(track, pilots_times))
    env.process(Leclerc.racing(track, pilots_times))
    env.process(Stroll.racing(track, pilots_times))


    yield env.timeout(10)

def classify_pilots(times):
    # Ordena el diccionario por tiempos de carrera (valores)
    # items() devuelve una lista de tuplas (clave, valor) del diccionario
    # sorted() ordena estas tuplas, donde key=lambda item: item[1] indica ordenar por el segundo elemento de cada tupla (el tiempo)
    sorted_pilots = sorted(times.items(), key=lambda item: item[1])
    # Convierte la lista de tuplas ordenada de nuevo en un diccionario ordenado
    # dict() convierte la lista de tuplas de nuevo en un diccionario
    # enumerate() añade una posición de índice, comenzando en 1, para indicar la clasificación
    classification = {i + 1: (pilot, time) for i, (pilot, time) in enumerate(sorted_pilots)}
    # Imprimir por pantalla la clasificacion
    print("\n\n\t\t\tTABLA DE RESULTADOS\n")
    for rank, (pilot, time) in classification.items():
        print(f'{rank}. {pilot}: {time}')
    print("\n")

    """
    if rank == 1:
        pilot.points += 25
    elif rank == 2:
        pilot.points += 18
    """


if __name__=='__main__':
    # Simulation parameters
    SIMULATION_TIME = 1000000
    
    #Inicializa Circuito
    Suzuka = track.Track("Suzuka", 70, 60)

    #Show Track Information
    Suzuka.showTrackInfo()

    # Setup simulation environment
    env = simpy.Environment()
    boxes = Boxes(env)
    statistics = StatisticsCollector()

    # Run simulation
    env.process(vehicle_generator(env, boxes, Suzuka,statistics))
    env.run(until = SIMULATION_TIME)
    classify_pilots(pilots_times)

    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe()
    df.to_csv('simulation_statistics.csv', index = False)
