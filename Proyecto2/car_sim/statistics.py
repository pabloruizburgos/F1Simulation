import pandas as pd

class StatisticsCollector:
    def __init__(self):
        self.data = []

    def add_data(self, vehicle_name:str, fuel_type:str, arrival_time:int, 
                 start_refuel_time:int, end_refuel_time:int) -> None:
        """Generate dataframe

        Args:
            vehicle_name (str): Vehicle ID
            fuel_type (str): Fuel type
            arrival_time (int): Vehicle arrival time
            start_refuel_time (int): Vehicle refueling initial time
            end_refuel_time (int): Vehicle refueling end time
        """
        dict_data = {
            'Vehicle': vehicle_name, 
            'Fuel Type': fuel_type, 
            'Arrival Time': arrival_time,
            'Start Refuel Time': start_refuel_time, 
            'End Refuel Time': end_refuel_time}
        self.data.append(dict_data)

    def to_dataframe(self):
        return pd.DataFrame(self.data)
 # type: ignore