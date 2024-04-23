import simpy
import random
from typing import Generator
import track
from boxes import Boxes
from vehicle import Vehicle
from track import Track
from statistics import StatisticsCollector # type: ignore

pilots_times = dict()

# Vehicle generator
def vehicle_generator(env: simpy.Environment, boxes: Boxes,track:Track,statistics: StatisticsCollector) -> Generator:
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
    
    Hamilton = Vehicle(env, "Hamilton", boxes.selectCompound(track), 0 ,0 , boxes, track,0,"Mercedes",statistics)
    Sainz = Vehicle(env, "Sainz",boxes.selectCompound(track), 0 , 0 , boxes, track,0,"Ferrari", statistics)
    Alonso = Vehicle(env, "Alonso",boxes.selectCompound(track), 0 , 0 , boxes, track, 0,"Aston Martin", statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg",boxes.selectCompound(track), 0 , 0 , boxes,track, 0,"Haas",statistics)
    Russell = Vehicle(env, "Russel",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Mercedes",statistics)
    Magnussen=Vehicle(env, "Magnussen",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Haas",statistics)
    Leclerc=Vehicle(env, "Leclerc",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Ferrari",statistics)
    Stroll=Vehicle(env, "Stroll",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Aston Martin",statistics)
    

    env.process(Hamilton.racing(track, pilots_times))
    env.process(Sainz.racing(track, pilots_times))
    env.process(Alonso.racing(track, pilots_times))
    env.process(Hulkenberg.racing(track, pilots_times))
    env.process(Russell.racing(track, pilots_times))
    env.process(Magnussen.racing(track, pilots_times))
    env.process(Leclerc.racing(track, pilots_times))
    env.process(Stroll.racing(track, pilots_times))
    
    yield env.timeout(10)

def classify_pilots_v2(times):
    # Filtra los pilotos con tiempo de carrera y los ordena por tiempo
    valid_pilots = {pilot: time for pilot, time in times.items() if time is not None}
    sorted_pilots = sorted(valid_pilots.items(), key=lambda item: item[1])

    # Calcula el número de pilotos sin tiempo de carrera
    no_time_pilots = len(times) - len(valid_pilots)

    # Convierte la lista de pilotos ordenados de nuevo en un diccionario ordenado
    classification = {i + 1: (pilot, time) for i, (pilot, time) in enumerate(sorted_pilots)}
    
    # Agrega los pilotos sin tiempo de carrera al final del ranking
    no_time_rank = len(classification) + 1
    for pilot, time in times.items():
        if time is None:
            classification[no_time_rank] = (pilot, None)
            no_time_rank += 1

    # Imprime cada piloto con su tiempo en una línea separada
    print("\n\n\t\t\tTABLA DE RESULTADOS\n")
    for rank, (pilot, time) in classification.items():
        if time is not None:
            print(f'{rank}. {pilot}: {time}')
        else:
            print(f'{rank}. {pilot}: Not finished')
    print("\n")
    

if __name__=='__main__':
    # Simulation parameters
    SIMULATION_TIME = 1000000
    
    #Inicializa Circuito
    Suzuka=track.Track("Suzuka", 70, 60)
    Monza=track.Track("Monza", 50, 65)
    Interlagos=track.Track("Interlagos", 60, 55)
    Monaco=track.Track("Monaco", 78, 58)
    Silverstone=track.Track("Silverstone", 52, 62)
    Spa=track.Track("Spa", 44, 57)
    Hungaroring=track.Track("Hungaroring", 70, 60)
    Hockenheimring=track.Track("Hockenheimring", 67, 61)
    YasMarina=track.Track("YasMarina", 55, 64)
    Shanghai=track.Track("Shanghai", 56, 63)
    Sepang=track.Track("Sepang", 56, 63)
    RedBullRing=track.Track("RedBullRing", 71, 35)
    GillesVilleneuve=track.Track("GillesVilleneuve", 70, 60)
    Bahrain=track.Track("Bahrain", 57, 55)
    Sochi=track.Track("Sochi", 53, 20)
    Australia=track.Track("Australia", 58, 30)
    Imola=track.Track("Imola", 63, 59) 

    circuitList=[Suzuka,Monza,Interlagos,Monaco,Silverstone,Spa,Hungaroring,Hockenheimring,YasMarina,Shanghai,Sepang,RedBullRing,GillesVilleneuve,Bahrain,Sochi,Australia,Imola]

    # Setup simulation environment
    
    statistics = StatisticsCollector()
    for circuit in circuitList:

        env = simpy.Environment()
        boxes = Boxes(env)
        

        #Show Track Information
        circuit.showTrackInfo()

        # Run simulation
        env.process(vehicle_generator(env, boxes, circuit,statistics))
        env.run(until=SIMULATION_TIME)
        classify_pilots_v2(pilots_times)

    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe()
    df.to_csv('simulation_statistics.csv', index=False)

    