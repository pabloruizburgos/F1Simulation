import simpy
import random
from typing import Generator
import track
from boxes import Boxes
from vehicle import Vehicle
from statistics import StatisticsCollector # type: ignore



# Vehicle generator
def vehicle_generator(env: simpy.Environment, boxes: Boxes,statistics: StatisticsCollector) -> Generator:
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
    
    Hamilton = Vehicle(env, "Hamilton", boxes.selectCompound(Suzuka), 0 ,0 , boxes, statistics)
    Sainz = Vehicle(env, "Sainz",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Alonso = Vehicle(env, "Alonso",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Russell = Vehicle(env, "Russel",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Magnussen=Vehicle(env, "Magnussen",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Leclerc=Vehicle(env, "Leclerc",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    Stroll=Vehicle(env, "Stroll",boxes.selectCompound(Suzuka), 0 , 0 , boxes ,statistics)
    


    env.process(Hamilton.racing(Suzuka))
    #env.process(Sainz.racing())
    #env.process(Alonso.racing())
    #env.process(Hulkenberg.racing())
    #env.process(Russell.racing())
    #env.process(Magnussen.racing())
    #env.process(Leclerc.racing())
    #env.process(Stroll.racing())

    yield env.timeout(10)


if __name__=='__main__':
    # Simulation parameters
    SIMULATION_TIME = 1000000
    
    #Inicializa Circuito
    Suzuka=track.Track("Suzuka")

    # Setup simulation environment
    env = simpy.Environment()
    boxes = Boxes(env)
    statistics = StatisticsCollector()

    # Run simulation
    env.process(vehicle_generator(env, boxes,statistics))
    env.run(until=SIMULATION_TIME)

    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe()
    df.to_csv('simulation_statistics.csv', index=False)
