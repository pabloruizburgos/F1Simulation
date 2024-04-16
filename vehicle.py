import random
import simpy
from boxes import Boxes
from statistics import StatisticsCollector # type: ignore
from typing import Generator


def convertir_a_minutos_y_segundos(numero):
    minutos = numero // 60
    segundos = numero % 60
    centesimas = int((numero % 1) * 100)
    milesimas = int((numero % 0.01) * 1000)
    return minutos,"minutes",segundos,"seconds",centesimas,"centesimas",milesimas,"milesimas"

class Vehicle:
    def __init__(self, env: simpy.Environment, name: str, fuel_type: str,raceLapsCompleted,compoundLapsCompleted,
                 charging_station: Boxes, statistics: StatisticsCollector, 
                 min_refueling_time:int=20, max_refueling_time:int=30) -> None:
        """Initialize a vehicle

        Args:
            env (simpy.Environment): Simpy simulation environment
            name (str): Vehicle ID
            fuel_type (str): Vehicle fuel type ('electric', 'diesel', 'gasoline')
            charging_station (Boxes): Charging station object
            statistics (StatisticsCollector): Statistics collector
            min_refueling_time (int): Minimum refueling time 
            max_refueling_time (int): Maximum refueling time
        """
        self.env = env
        self.name = name
        self.fuel_type = fuel_type
        self.refueling_time = random.uniform(min_refueling_time,max_refueling_time)  # Random refueling time for other types
        self.charging_station = charging_station
        self.raceLapsCompleted = raceLapsCompleted
        self.compoundLapsCompleted = compoundLapsCompleted
        self.statistics = statistics

    def racing(self):
        lap_times={"soft":random.uniform(90,120),"medium":random.uniform(95,125),"hard":random.uniform(100,130)}   
        Total_laps=70
        start_time=self.env.now
        print(f"[Vehicle {self.name}\t| Compound: {self.fuel_type}]\t starts the race at {start_time}")
        #start_race_time = self.env.now
        #end_race_time = self.env.now
        
        while(self.raceLapsCompleted!=Total_laps):
        #Primera parada
            yield self.env.timeout(lap_times[list(self.fuel_type.keys())[0]])
            self.raceLapsCompleted=self.raceLapsCompleted + 1
            self.compoundLapsCompleted=self.compoundLapsCompleted + 1
            #print(self.name,"is in lap",self.raceLapsCompleted,"time:",convertir_a_minutos_y_segundos(self.env.now))
            if(self.fuel_type[list(self.fuel_type.keys())[0]] == self.compoundLapsCompleted):
                yield self.env.process(self.arrive())
                self.compoundLapsCompleted = 0
                
        #end_time=self.env.now

        print(f"[Vehicle {self.name}\t| Compound: {self.fuel_type}]\t finishes race at {convertir_a_minutos_y_segundos(self.env.now)}")
        #self.statistics.add_data(self.name, self.fuel_type, start_race_time, end_race_time)
        
    
    def arrive(self) ->  Generator:
        """Arrive at the charging station and refuel

        Yields:
            Generator: Simpy event generator
        """
        
        with self.charging_station.queue.request() as request:
            yield request
            start_refuel_time = self.env.now
            print()
            print(f"[Vehicle {self.name}\t| Compound: {self.fuel_type}]\t arrives at boxes at {convertir_a_minutos_y_segundos(start_refuel_time)}")
            yield self.env.process(self.charging_station.changeTires(self))
            end_refuel_time = self.env.now
            #self.statistics.add_data(self.name, self.fuel_type, start_refuel_time, end_refuel_time)
