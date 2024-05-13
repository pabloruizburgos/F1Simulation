import simpy
from typing import Generator
import random
import aux_function_module


class Boxes:
    def __init__(self, env: simpy.Environment) -> None:
        
        """Initialize the charging station

        Args:
            env (simpy.Environment): Simpy simulation environment
        """
        self.env = env
        
        
    def selectCompound(self,circuito):
        
        """
        Selects the type of compound for the vehicle.

        Args:
            circuito: The circuit where the race is taking place.

        Returns:
            dict: A dictionary containing the selected compound type and its duration.
        """

        #Compound Lap Duration
        soft_compound_duration=random.randint(20,30)
        medium_compound_duration=random.randint(25,35)
        hard_compound_duration=random.randint(30,40)
        intermediates_compound_duration=random.randint(20,30)
        wet_compound_duration=random.randint(19,29)
        
        types = [{'soft':soft_compound_duration}, {'medium':medium_compound_duration}, {'hard':hard_compound_duration},{'intermediates':intermediates_compound_duration},{'wet':wet_compound_duration}]
        
        #Tire Selection
        if circuito.typeRain == None:
            return random.choice(types[0:3])
        elif circuito.typeRain == "Light Rain":
            return random.choice(types[3:5])
        else:
            return random.choice(types[3:5])
    
    def changeTires(self, vehicle: object,circuito) ->  Generator:
        
        """
        Changes the tires of a vehicle.

        Args:
            vehicle (object): The Vehicle instance.
            circuito: The circuit where the race is taking place.

        Yields:
            Generator: Simpy event generator.
        """
        
        
        vehicle.compound_type = self.selectCompound(circuito)
        yield self.env.timeout(vehicle.pitStop_time)
        print(f"[Vehicle {vehicle.name}\t| Compound: {vehicle.compound_type}]\t exits boxes at",aux_function_module.convertir_a_minutos_y_segundos(self.env.now))
        
        