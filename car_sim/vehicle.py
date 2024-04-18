import random
import simpy
from boxes import Boxes
from statistics import StatisticsCollector # type: ignore
from typing import Generator
import aux_function_module  



class Vehicle:
    
    def __init__(self, env: simpy.Environment, name: str, compound_type: str,raceLapsCompleted,compoundLapsCompleted,
                 charging_station: Boxes, statistics: StatisticsCollector, 
                 min_pitStop_time:int=20, max_pitStop_time:int=30) -> None:
        """Initialize a vehicle

        Args:
            env (simpy.Environment): Simpy simulation environment
            name (str): Vehicle ID
            compound_type (str): Vehicle fuel type ('electric', 'diesel', 'gasoline')
            charging_station (Boxes): Charging station object
            statistics (StatisticsCollector): Statistics collector
            min_pitStop_time (int): Minimum refueling time 
            max_pitStop_time (int): Maximum refueling time
        """
        self.env = env
        self.name = name
        self.compound_type = compound_type
        self.pitStop_time = random.uniform(min_pitStop_time,max_pitStop_time)  # Random refueling time for other types
        self.charging_station = charging_station
        self.raceLapsCompleted = raceLapsCompleted
        self.compoundLapsCompleted = compoundLapsCompleted
        self.statistics = statistics

    
    
    
    def racing(self,circuito):
        print(circuito.typeRain)
        lap_times={"soft":random.uniform(90,120),"medium":random.uniform(95,125),"hard":random.uniform(100,130),"intermediates":random.uniform(100,130),"wet":random.uniform(100,130)}   
        Total_laps=70
        temperatura={}
        
        start_time=self.env.now
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t starts the race at {start_time}")
        #start_race_time = self.env.now
        #end_race_time = self.env.now
        
        
        while(self.raceLapsCompleted!=Total_laps):
        #Primera parada
            #np.random.choice(len(estados), p=0.8)
            if list(self.compound_type.keys())[0]=="soft":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003*self.compoundLapsCompleted)))
            elif list(self.compound_type.keys())[0]=="medium":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.002*self.compoundLapsCompleted)))
            elif list(self.compound_type.keys())[0]=="hard":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.0015*self.compoundLapsCompleted)))
            elif list(self.compound_type.keys())[0]=="intermediates":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.0012*self.compoundLapsCompleted)))
            else:
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.001*self.compoundLapsCompleted)))
            
            

            self.raceLapsCompleted=self.raceLapsCompleted + 1
            self.compoundLapsCompleted=self.compoundLapsCompleted + 1
            #print(self.name,"is in lap",self.raceLapsCompleted,"time:",convertir_a_minutos_y_segundos(self.env.now))
            print(self.name,"is in lap",self.raceLapsCompleted,"laptime:",aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))))
            if(self.compound_type[list(self.compound_type.keys())[0]] == self.compoundLapsCompleted):
                yield self.env.process(self.arrive(circuito))
                self.compoundLapsCompleted = 0
                
        #end_time=self.env.now
        self.finish()
       
        #self.statistics.add_data(self.name, self.compound_type, start_race_time, end_race_time)
        
    
    def arrive(self,circuit) ->  Generator:
        
        """Arrive at the charging station and refuel

        Yields:
            Generator: Simpy event generator
        """
        
        #with self.charging_station.queue.request() as request:
        #yield request
        start_refuel_time = self.env.now
        print()
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t arrives at boxes at {aux_function_module.convertir_a_minutos_y_segundos(start_refuel_time)}")
        yield self.env.process(self.charging_station.changeTires(self,circuit))
        end_refuel_time = self.env.now
        #self.statistics.add_data(self.name, self.compound_type, start_refuel_time, end_refuel_time)

    
    def finish(self):
         print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t finishes race at {aux_function_module.convertir_a_minutos_y_segundos(self.env.now)}")