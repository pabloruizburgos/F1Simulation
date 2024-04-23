import pandas as pd

class StatisticsCollector:
    def __init__(self):
        self.data = []

    def add_data(self, vehicle_name:str, fuel_type:str, 
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

    def to_dataframe(self):
        return pd.DataFrame(self.data)
