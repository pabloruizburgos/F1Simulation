import simpy
import random
from typing import Generator
import track
from boxes import Boxes
from vehicle import Vehicle
from track import Track
from statistics import StatisticsCollector # type: ignore



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
    
    Hamilton = Vehicle(env, "Hamilton", boxes.selectCompound(track), 0 ,0 , boxes, track,0, statistics)
    Sainz = Vehicle(env, "Sainz",boxes.selectCompound(track), 0 , 0 , boxes, track,0, statistics)
    Alonso = Vehicle(env, "Alonso",boxes.selectCompound(track), 0 , 0 , boxes, track, 0, statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg",boxes.selectCompound(track), 0 , 0 , boxes,track, 0,statistics)
    Russell = Vehicle(env, "Russel",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,statistics)
    Magnussen=Vehicle(env, "Magnussen",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,statistics)
    Leclerc=Vehicle(env, "Leclerc",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,statistics)
    Stroll=Vehicle(env, "Stroll",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,statistics)
    


    env.process(Hamilton.racing(track))
    env.process(Sainz.racing(track))
    env.process(Alonso.racing(track))
    env.process(Hulkenberg.racing(track))
    env.process(Russell.racing(track))
    env.process(Magnussen.racing(track))
    env.process(Leclerc.racing(track))
    env.process(Stroll.racing(track))

    yield env.timeout(10)


if __name__=='__main__':
    # Simulation parameters
    SIMULATION_TIME = 1000000
    
    #Inicializa Circuito
    Suzuka=track.Track("Suzuka", 70, 60)

    #Show Track Information
    Suzuka.showTrackInfo()

    # Setup simulation environment
    env = simpy.Environment()
    boxes = Boxes(env)
    statistics = StatisticsCollector()

    # Run simulation
    env.process(vehicle_generator(env, boxes, Suzuka,statistics))
    env.run(until=SIMULATION_TIME)

    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe()
    df.to_csv('simulation_statistics.csv', index=False)
