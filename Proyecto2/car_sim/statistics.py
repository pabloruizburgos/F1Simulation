import pandas as pd

class StatisticsCollector:
    def __init__(self):
        self.data = []
        self.data_season_classification = []
        self.data_race_classification = []

    def add_data_pit_stops(self, vehicle_name:str, fuel_type:str, 
                 stop_time:int,circuit:str,escuderia:str) -> None:
        """Generate dataframe

        Args:
            vehicle_name (str): Vehicle ID
            fuel_type (str): Fuel type
            arrival_time (int): Vehicle arrival time
            start_refuel_time (int): Vehicle refueling initial time
            end_refuel_time (int): Vehicle refueling end time
        """
        dict_data = {'Vehicle': vehicle_name, 'Fuel Type': fuel_type, 'PitStop Time': stop_time, 'Circuit': circuit, 'Escuderia':escuderia}
        self.data.append(dict_data)


    def add_data_season_classification(self, vehicle_name:str, puntos:int, escuderia:str) -> None:
        dict_data = {'Vehicle': vehicle_name, 'Puntos': puntos, 'Escuderia':escuderia}
        self.data_season_classification.append(dict_data)


    def add_data_race_classification(self, circuit:str, race_classification:dict) -> None:
        dict_data = {'Circuit':circuit, 'xd':race_classification}
        self.data_race_classification.append(dict_data)


    def to_dataframe_pit_stops(self):
        return pd.DataFrame(self.data)
    

    def to_dataframe_race_classification(self):
        return pd.DataFrame(self.data_race_classification)
