import simpy
from typing import Generator
from boxes import Boxes
from vehicle import Vehicle
from track import Track
from statistics import StatisticsCollector # type: ignore



def vehicle_generator(env: simpy.Environment, boxes: Boxes,track:Track,statistics: StatisticsCollector,race_classification:dict) -> Generator:
    
    """Generates vehicles and sends them to the charging station.

    Args:
        env (simpy.Environment): Simpy simulation environment
        boxes(Boxes): Charging station
        statistics (StatisticsCollector): Statistic collector module
        race_classification:dict

    Yields:
        Generator: Simpy event generator
    """
    
    # We create each vehicle with a random compound
    for i in range(NUMBER_PILOTS):
        
        Vehicle1=Vehicle(env, f"Vehicle{i}", boxes.selectCompound(track), RACE_LAPS_COMPLETED ,COMPOUND_LAPS_COMPLETED , boxes, track,INITIAL_PUNT_PROBABILITY,statistics)
        env.process(Vehicle1.racing(track))
        race_classification.update({f"Vehicle{i}":0})
 
    yield env.timeout(0)


if __name__=='__main__':
    
    # Simulation parameters
    SIMULATION_TIME = 1000000
    NUMBER_PILOTS = 50
    INITIAL_LAPS = 0
    RACE_LAPS_COMPLETED = 0
    COMPOUND_LAPS_COMPLETED = 0
    INITIAL_PUNT_PROBABILITY = 0
    
    #We start the initializacion variables
    statistics = StatisticsCollector()
    race_classification={}

    #We create the following circuits following -> Circuit Name, Laps, Temperature and Statistics 
    Suzuka=Track("Suzuka", 70, 45,statistics)
    Monza=Track("Monza", 50, 33,statistics)
    Interlagos=Track("Interlagos", 60, 40, statistics)
    Monaco=Track("Monaco", 78, 30,statistics)
    Silverstone=Track("Silverstone", 52, 21,statistics)
    Spa=Track("Spa", 44, 20,statistics)
    Hungaroring=Track("Hungaroring", 70, 27,statistics)
    Hockenheimring=Track("Hockenheimring", 67, 22,statistics)
    YasMarina=Track("YasMarina", 55, 60,statistics)
    Shanghai=Track("Shanghai", 56, 57,statistics)
    Sepang=Track("Sepang", 56, 55,statistics)
    RedBullRing=Track("RedBullRing", 71, 25,statistics)
    GillesVilleneuve=Track("GillesVilleneuve", 70, 30,statistics)
    Bahrain=Track("Bahrain", 57, 60,statistics)
    Sochi=Track("Sochi", 53, 20,statistics)
    Australia=Track("Australia", 58, 30,statistics)
    Imola=Track("Imola", 63, 59,statistics) 

    #We store the circuits in a list
    circuitList = [Suzuka, Monza, Interlagos, Monaco, Silverstone, Spa, Hungaroring,
                   Hockenheimring, YasMarina, Shanghai, Sepang, RedBullRing, GillesVilleneuve,
                   Bahrain, Sochi, Australia, Imola]
    
    
    # Setup simulation environment
    for circuit in circuitList:

        # We create the environment and the resource Boxes
        env = simpy.Environment()
        boxes = Boxes(env)

        # Show Track Information
        circuit.showTrackInfo()

        # Run simulation
        env.process(vehicle_generator(env, boxes, circuit, statistics, race_classification))
        env.run(until=SIMULATION_TIME)

        # Shows Race Classification
        circuit.classify_pilots(race_classification)
        
    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe_pit_stops()
    df_race = statistics.to_dataframe_race_classification()
    df_lap_time = statistics.to_dataframe_lap_times()
    df_chrases = statistics.to_dataframe_chrases()
    df.to_csv('pitstops.csv', index=False)
    df_race.to_csv('race_classification.csv', index=False)
    df_lap_time.to_csv('lap_times.csv', index=False)
    df_chrases.to_csv('chrases.csv', index=False)
    