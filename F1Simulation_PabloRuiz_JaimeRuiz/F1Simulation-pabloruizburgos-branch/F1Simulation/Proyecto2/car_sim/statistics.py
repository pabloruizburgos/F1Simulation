import pandas as pd

class StatisticsCollector:
    def __init__(self):
        self.data_pitstops = []
        self.data_lap_times = []
        self.data_race_classification = []
        self.data_chrases = []

    def add_data_pit_stops(self, vehicle_name:str, compound_type:str,lap, 
                 stop_time:int,circuit:str,typeRain:str,trackLaps:int) -> None:
        """Generate dataframe

        Args:
            vehicle_name (str): Vehicle ID
            fuel_type (str): Fuel type
            arrival_time (int): Vehicle arrival time
            start_refuel_time (int): Vehicle refueling initial time
            end_refuel_time (int): Vehicle refueling end time
        """
        dict_data = {'Vehicle': vehicle_name, 'Compound Type': compound_type,"Lap":lap, 'PitStop Time': stop_time, 'Circuit': circuit, 'Type Rain':typeRain, 'Track Laps':trackLaps}
        self.data_pitstops.append(dict_data)


    def add_data_lap_times(self,name,lapsCompleted,lapTime, compoundLapsCompleted) -> None:
        dict_data = {'Vehicle': name,'Lap':lapsCompleted, 'Lap Time':lapTime, 'Compound laps':compoundLapsCompleted}
        self.data_lap_times.append(dict_data)


    def add_data_race_classification(self, circuit:str, race_classification:dict) -> None:
        dict_data = {'Circuit':circuit, 'Race Positions':race_classification}
        self.data_race_classification.append(dict_data)

    def add_data_chrases(self, compound, compoundLapsCompleted, rain, lap, temperature) -> None:
        dict_data = {'Rain':rain, 'Temperature':temperature, 'Compound':compound, 'Compound laps completed':compoundLapsCompleted, 'Lap':lap}
        self.data_chrases.append(dict_data)

    def to_dataframe_pit_stops(self):
        return pd.DataFrame(self.data_pitstops)
    
    def to_dataframe_race_classification(self):
        return pd.DataFrame(self.data_race_classification)
    
    def to_dataframe_lap_times(self):
        return pd.DataFrame(self.data_lap_times)
    
    def to_dataframe_chrases(self):
        return pd.DataFrame(self.data_chrases)