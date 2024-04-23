import random
import simpy
from boxes import Boxes
from statistics import StatisticsCollector # type: ignore
from typing import Generator
import aux_function_module  


class Vehicle:
    
    def __init__(self, env: simpy.Environment, name: str, compound_type: str,raceLapsCompleted,compoundLapsCompleted,
                 charging_station: Boxes,circuito,probPinchazo, statistics: StatisticsCollector, 
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
        self.probPinchazo=probPinchazo
        self.accidentProbability=self.calc_vehicule_accident_probability(circuito)
        self.statistics = statistics

    
    def calc_vehicule_accident_probability(self,circuito):
        
        accidentProbability=0
        
        if circuito.typeRain == "Light Rain":
            accidentProbability=accidentProbability + 0.0025
        
        elif circuito.typeRain == "Heavy Rain":
            accidentProbability=accidentProbability + 0.005
          
        if circuito.avgTemperature > 40 :
            accidentProbability = accidentProbability + 0.003

        if circuito.typeRain == "Heavy Rain" and self.compound_type== "Intermediate":
            accidentProbability=accidentProbability + 0.005
        
        accidentProbability=accidentProbability + self.probPinchazo
        
        return accidentProbability
    
    
    def racing(self, circuito, pilots_times):
        
        #print("Weather:",circuito.typeRain)
        #Establecemos unos tiempos de vuelta para cada neumatico que se irán modificando siguiendo parámetros como la temperatura,lluvia...
        
        lap_times={"soft":random.uniform(90,120),"medium":random.uniform(95,125),"hard":random.uniform(100,130),"intermediates":random.uniform(130,140),"wet":random.uniform(140,150)}   
        
        start_time=self.env.now
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t starts the race at {start_time}")
        #start_race_time = self.env.now
        #end_race_time = self.env.now
        
        
        while(self.raceLapsCompleted!=circuito.trackLaps):
        
        #Primera parada
            # Establecer los tiempos por vuelta incluyendo degradación de compuesto + temperatura
            if list(self.compound_type.keys())[0]=="soft":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.003 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="medium":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.002 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="hard":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.0015 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="intermediates":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.0012 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
            else:
                #Si va con wet cuando no llueve tanto
                if circuito.typeRain=="Light Rain":
                    yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.001 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
                else:
                    yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.003 * self.compoundLapsCompleted)) + (1 + (0.01*circuito.avgTemperature))))
            
            
            # Sumar cada vuelta
            self.raceLapsCompleted=self.raceLapsCompleted + 1
            self.compoundLapsCompleted=self.compoundLapsCompleted + 1
            

            #En cada vuelta la probabilidad de pinchazo aumenta un valor de este rango
            self.probPinchazo=self.probPinchazo + random.uniform(0.0001,0.0002)

            # Calcular si tiene un accidente esta vuelta
            probabilitiesAccidente = [self.calc_vehicule_accident_probability(circuito) , 1 - self.calc_vehicule_accident_probability(circuito)]
            opciones = [True, False]
            self.accidentProbability=random.choices(opciones, weights=probabilitiesAccidente, k=1)[0]
            if(self.accidentProbability==True):
                print("Accidente de",self.name)
                break

            # Imprimir Tiempos de vuelta
            #print(self.name,"is in lap",self.raceLapsCompleted,"laptime:",aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))))
            #print(self.name,"is in lap",self.compoundLapsCompleted,"laptime:",aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))))
            
            # Si se les acaba el compuesto pueden parar en boxes o seguir a riesgo de aumentar pinchazo
            if(self.compoundLapsCompleted >= self.compound_type[list(self.compound_type.keys())[0]] ):
                #Las probabilidades de que elijan parar depende de la probabilidad de pinchazo
                probabilitiesParada = [0.6 + self.probPinchazo, 1 - (0.6 + self.probPinchazo)]
                opcionesParada = [True, False]
                parada=random.choices(opcionesParada, weights=probabilitiesParada, k=1)[0]
                if parada == True:
                    yield self.env.process(self.arriveBoxes(circuito))
                    self.compoundLapsCompleted = 0
                    self.probPinchazo=0
                else:
                    self.probPinchazo=self.probPinchazo + 0.02
                
                #Reiniciamos las vueltas del compuesto tras el cambio
                
                
        #end_time=self.env.now
        
        #Acabar carrera
        self.finish(pilots_times)
       
        #self.statistics.add_data(self.name, self.compound_type, start_race_time, end_race_time)
        
    
        
    
    def arriveBoxes(self,circuit) ->  Generator:
        
        """Arrive at the charging station and refuel

        Yields:
            Generator: Simpy event generator
        """
        
        start_refuel_time = self.env.now
        print()
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t arrives at boxes at {aux_function_module.convertir_a_minutos_y_segundos(start_refuel_time)}")
        yield self.env.process(self.charging_station.changeTires(self,circuit))
        #self.statistics.add_data(self.name, self.compound_type, start_refuel_time, end_refuel_time)

    
    def finish(self, pilots_times):
         print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t finishes race at {aux_function_module.convertir_a_minutos_y_segundos(self.env.now)}")
         pilots_times.update({self.name:aux_function_module.convertir_a_minutos_y_segundos(self.env.now)})