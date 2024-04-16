import simpy
from typing import Generator
import random

def convertir_a_minutos_y_segundos(numero):
    minutos = numero // 60
    segundos = numero % 60
    centesimas = int((numero % 1) * 100)
    milesimas = int((numero % 0.01) * 1000)
    return minutos,"minutes",segundos,"seconds",centesimas,"centesimas",milesimas,"milesimas"


class Boxes:
    def __init__(self, env: simpy.Environment) -> None:
        """Initialize the charging station

        Args:
            env (simpy.Environment): Simpy simulation environment
        """
        self.env = env
        # Only five vehicle can refuel at a time
        self.queue = simpy.Resource(env, capacity=10)  

    def changeTires(self, vehicle: object) ->  Generator:
        """Refuel a vehicle

        Args:
            vehicle (object): Vehicle instance

        Yields:
            Generator: Simpy event generator
        """
        
        soft_compound_duration=random.randint(20,30)
        medium_compound_duration=random.randint(25,35)
        hard_compound_duration=random.randint(30,40)
        types = [{'soft':soft_compound_duration}, {'medium':medium_compound_duration}, {'hard':hard_compound_duration}]
        vehicle.fuel_type = random.choice(types)
        yield self.env.timeout(vehicle.refueling_time)
        print(f"[Vehicle {vehicle.name}\t| Compound: {vehicle.fuel_type}]\t finishes refueling at {convertir_a_minutos_y_segundos(self.env.now)}")
        print()
        