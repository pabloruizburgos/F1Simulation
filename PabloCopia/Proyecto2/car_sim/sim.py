import simpy
import random
from typing import Generator

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
    soft_compound_duration=random.randint(10,20) #Duración en vueltas
    medium_compound_duration=random.randint(18,30)
    hard_compound_duration=random.randint(28,40)
    types = [{'soft':soft_compound_duration}, {'medium':medium_compound_duration}, {'hard':hard_compound_duration}]
     
    Hamilton = Vehicle(env, "Hamilton", random.choice(types), 0 ,0 , boxes, statistics)
    Sainz = Vehicle(env, "Sainz",random.choice(types), 0 , 0 , boxes ,statistics)
    Alonso = Vehicle(env, "Alonso",random.choice(types), 0 , 0 , boxes ,statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg",random.choice(types), 0 , 0 , boxes ,statistics)
    Russell = Vehicle(env, "Russel",random.choice(types), 0 , 0 , boxes ,statistics)
    Magnussen=Vehicle(env, "Magnussen",random.choice(types), 0 , 0 , boxes ,statistics)
    Leclerc=Vehicle(env, "Leclerc",random.choice(types), 0 , 0 , boxes ,statistics)
    Stroll=Vehicle(env, "Stroll",random.choice(types), 0 , 0 , boxes ,statistics)

    env.process(Hamilton.racing())
    env.process(Sainz.racing())
    env.process(Alonso.racing())
    env.process(Hulkenberg.racing())
    env.process(Russell.racing())
    env.process(Magnussen.racing())
    env.process(Leclerc.racing())
    env.process(Stroll.racing())
    yield env.timeout(10)


    # yield env.timeout(nextForPitStop.fuel_type[list(nextForPitStop.fuel_type.keys())[0]]) #Tiempo que están en pista
    # env.process(nextForPitStop.arrive())
        
    #yield env.timeout(random.randint(MINIMAL_ARRIVAL_TIME, MAXIMUM_ARRIVAL_TIME))  # Generate new vehicle arrival


if __name__=='__main__':
    # Simulation parameters
    SIMULATION_TIME = 1000000
    
    
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
