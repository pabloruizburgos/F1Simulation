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
        
        soft_compound_duration=random.randint(20,30)
        medium_compound_duration=random.randint(25,35)
        hard_compound_duration=random.randint(30,40)
        intermediates_compound_duration=random.randint(20,30)
        wet_compound_duration=random.randint(20,30)
        types = [{'soft':soft_compound_duration}, {'medium':medium_compound_duration}, {'hard':hard_compound_duration},{'intermediates':intermediates_compound_duration},{'wet':wet_compound_duration}]
        if circuito.typeRain == None:
            return random.choice(types[0:3])
        elif circuito.typeRain == "Light Rain":
            return random.choice(types[3:5])
        else:
            return random.choice(types[3:5])
    
    def changeTires(self, vehicle: object,circuito) ->  Generator:
        """Refuel a vehicle

        Args:
            vehicle (object): Vehicle instance

        Yields:
            Generator: Simpy event generator
        """
        
        
        vehicle.compound_type = self.selectCompound(circuito)
        yield self.env.timeout(vehicle.pitStop_time)
        print(f"[Vehicle {vehicle.name}\t| Compound: {vehicle.compound_type}]\t exits boxes at",aux_function_module.convertir_a_minutos_y_segundos(self.env.now))
        print()
        