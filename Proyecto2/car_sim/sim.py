import simpy
from typing import Generator
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
    
    Hamilton = Vehicle(env, "Hamilton", boxes.selectCompound(track), 0 ,0 , boxes, track,0,"Mercedes",statistics)
    Sainz = Vehicle(env, "Sainz",boxes.selectCompound(track), 0 , 0 , boxes, track,0,"Ferrari", statistics)
    Alonso = Vehicle(env, "Alonso",boxes.selectCompound(track), 0 , 0 , boxes, track, 0,"Aston Martin", statistics)
    Hulkenberg = Vehicle(env, "Hulkenberg",boxes.selectCompound(track), 0 , 0 , boxes,track, 0,"Haas",statistics)
    Russell = Vehicle(env, "Russell",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Mercedes",statistics)
    Magnussen = Vehicle(env, "Magnussen",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Haas",statistics)
    Leclerc = Vehicle(env, "Leclerc",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Ferrari",statistics)
    Stroll = Vehicle(env, "Stroll",boxes.selectCompound(track), 0 , 0 , boxes ,track, 0,"Aston Martin",statistics)
    

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
    statistics = StatisticsCollector()
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

    circuitList = [Suzuka,Monza,Interlagos,Monaco,Silverstone,Spa,Hungaroring,Hockenheimring,YasMarina,Shanghai,Sepang,RedBullRing,GillesVilleneuve,Bahrain,Sochi,Australia,Imola]
    season_classification={"Hamilton":0, "Sainz":0, "Alonso":0, "Hulkenberg":0, "Russell":0, "Magnussen":0, "Leclerc":0, "Stroll":0}
    
    # Setup simulation environment
    
    for circuit in circuitList:

        env = simpy.Environment()
        boxes = Boxes(env)

        #Show Track Information
        circuit.showTrackInfo()

        # Run simulation
        env.process(vehicle_generator(env, boxes, circuit,statistics))
        env.run(until=SIMULATION_TIME)
        circuit.classify_pilots(season_classification)
        
    
    season_classification = sorted(season_classification.items(), key=lambda item: item[1], reverse=True)
    print(season_classification)
    statistics.add_data_season_classification(season_classification)

    # Save statistics to pandas DataFrame
    df = statistics.to_dataframe_pit_stops()
    df_race = statistics.to_dataframe_race_classification()
    df_season=statistics.to_dataframe_season_classification()
    df.to_csv('simulation_statistics.csv', index=False)
    df_race.to_csv('race_classification.csv', index=False)
    df_season.to_csv('season_classification.csv', index=False)
    