import random
import simpy
from boxes import Boxes
from statistics import StatisticsCollector # type: ignore
from typing import Generator
import aux_function_module  



class Vehicle:
    
    def __init__(self, env: simpy.Environment, name: str, compound_type: str,raceLapsCompleted,compoundLapsCompleted,
                 charging_station: Boxes,circuit,punctureProbability, statistics: StatisticsCollector, 
                 min_pitStop_time:int=20, max_pitStop_time:int=30) -> None:
        
        """
        Initializes a Vehicle instance.

        Args:
            env (simpy.Environment): The Simpy simulation environment.
            name (str): The name of the vehicle.
            compound_type (str): The type of compound used by the vehicle.
            raceLapsCompleted (int): The number of laps completed by the vehicle in the race.
            compoundLapsCompleted (int): The number of laps completed by the vehicle on the current compound.
            charging_station (Boxes): The charging station for the vehicle.
            circuit: The circuit where the race is taking place.
            punctureProbability: Probability of tire puncture.
            statistics (StatisticsCollector): An instance of StatisticsCollector for collecting race statistics.
            min_pitStop_time (int, optional): The minimum pit stop time. Defaults to 20.
            max_pitStop_time (int, optional): The maximum pit stop time. Defaults to 30.
        """
       
       
        self.env = env
        self.name = name
        self.compound_type = compound_type
        self.pitStop_time = random.uniform(min_pitStop_time,max_pitStop_time)  # Random refueling time for other types
        self.charging_station = charging_station
        self.raceLapsCompleted = raceLapsCompleted
        self.compoundLapsCompleted = compoundLapsCompleted
        self.punctureProbability=punctureProbability
        self.accidentProbability=self.calc_vehicule_accident_probability(circuit)
        self.statistics = statistics
        

    
    def calc_vehicule_accident_probability(self,circuit):
        
        """
        Calculates the probability of the vehicle having an accident based on circuit conditions.

        Args:
            circuit: The circuit where the race is taking place.

        Returns:
            float: The calculated accident probability.
        """

        accidentProbability = 0
        
        if circuit.typeRain == "Light Rain":
            accidentProbability = accidentProbability + 0.00025
        
        elif circuit.typeRain == "Heavy Rain":
            accidentProbability = accidentProbability + 0.0005
          
        if circuit.avgTemperature > 40 :
            accidentProbability = accidentProbability + 0.0003

        if circuit.typeRain == "Heavy Rain" and self.compound_type== "Intermediate":
            accidentProbability=accidentProbability + 0.005
        
        accidentProbability = accidentProbability + self.punctureProbability
        
        return accidentProbability
    

    def racing(self, circuit, crashed = False) -> Generator:
        
        """
        Simulates the vehicle racing on the circuit.

        Args:
            circuit: The circuit where the race is taking place.
            crashed (bool, optional): Whether the vehicle has crashed. Defaults to False.

        Yields:
            Generator: Simpy event generator.
        """
       
        #Establecemos unos tiempos de vuelta para cada neumatico que se irán modificando siguiendo parámetros como la temperatura,lluvia...
        lap_times={"soft":random.uniform(90,93),"medium":random.uniform(95,98),"hard":random.uniform(100,103),"intermediates":random.uniform(133,147),"wet":random.uniform(141,144)}   
        
        start_time=self.env.now
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t starts the race at {start_time}")
        self.statistics.add_data_pit_stops(self.name, self.compound_type,self.raceLapsCompleted, 0 , circuit.name, circuit.typeRain, circuit.trackLaps)
        
        while(self.raceLapsCompleted!=circuit.trackLaps):
        
            # Establecer los tiempos por vuelta incluyendo degradación de compuesto + temperatura
            if list(self.compound_type.keys())[0]=="soft":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.003 * self.compoundLapsCompleted)) + (1 + (0.03*circuit.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="medium":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.002 * self.compoundLapsCompleted)) + (1 + (0.02*circuit.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="hard":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.0015 * self.compoundLapsCompleted)) + (1 + (0.01*circuit.avgTemperature))))
            elif list(self.compound_type.keys())[0]=="intermediates":
                yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.0012 * self.compoundLapsCompleted)) + (1 + (0.01*circuit.avgTemperature))))
            else:
                #Si va con wet cuando no llueve tanto
                if circuit.typeRain=="Light Rain":
                    yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.001 * self.compoundLapsCompleted)) + (1 + (0.01*circuit.avgTemperature))))
                else:
                    yield self.env.timeout(lap_times[list(self.compound_type.keys())[0]] * ((1 + (0.003 * self.compoundLapsCompleted)) + (1 + (0.01*circuit.avgTemperature))))
            
            
            # Sumar cada vuelta
            self.raceLapsCompleted=self.raceLapsCompleted + 1
            self.compoundLapsCompleted=self.compoundLapsCompleted + 1
            

            #En cada vuelta la probabilidad de pinchazo aumenta un valor de este rango
            self.punctureProbability=self.punctureProbability + random.uniform(0.00001,0.00005)

            # Calcular si tiene un accidente esta vuelta
            probabilitiesAccidente = [self.calc_vehicule_accident_probability(circuit) , 1 - self.calc_vehicule_accident_probability(circuit)]
            opciones = [True, False]
            self.accidentProbability=random.choices(opciones, weights=probabilitiesAccidente, k = 1)[0]
            if(self.accidentProbability==True):
                print("Accidente de", self.name)
                crashed = True
                self.statistics.add_data_chrases(self.compound_type, self.compoundLapsCompleted, circuit.typeRain, self.raceLapsCompleted, circuit.avgTemperature)
                break


            #Imprimir Tiempos de vuelta
            #print(self.name,"is in lap",self.raceLapsCompleted,"laptime:",aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))))
            #print(self.name,"is in lap",self.compoundLapsCompleted,"laptime:",aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))))
            self.statistics.add_data_lap_times(self.name, self.raceLapsCompleted,aux_function_module.convertir_a_minutos_y_segundos(lap_times[list(self.compound_type.keys())[0]] * (1 + (0.003 * self.compoundLapsCompleted))), self.compoundLapsCompleted)

            # Si se les acaba el compuesto pueden parar en boxes o seguir a riesgo de aumentar pinchazo
            if(self.compoundLapsCompleted >= self.compound_type[list(self.compound_type.keys())[0]] ):
                #Las probabilidades de que elijan parar depende de la probabilidad de pinchazo
                probabilitiesParada = [0.6 + self.punctureProbability, 1 - (0.6 + self.punctureProbability)]
                opcionesParada = [True, False]
                parada=random.choices(opcionesParada, weights=probabilitiesParada, k=1)[0]
                if parada == True:
                    yield self.env.process(self.arriveBoxes(circuit))
                    self.compoundLapsCompleted = 0
                    self.punctureProbability=0
                else:
                    self.punctureProbability=self.punctureProbability + 0.02
                
                #Reiniciamos las vueltas del compuesto tras el cambio
                
                
        
        #Acabar carrera
        self.finish(circuit.race_classification, crashed,circuit)
       
    def arriveBoxes(self,circuit) ->  Generator:
        
        """
        Arrives at the charging station and refuels.

        Args:
            circuit: The circuit where the race is taking place.

        Yields:
            Generator: Simpy event generator.
        
        """
        
        start_refuel_time = self.env.now
        print(f"\n[Vehicle {self.name}\t| Compound: {self.compound_type}]\t arrives at boxes at {aux_function_module.convertir_a_minutos_y_segundos(start_refuel_time)}")
        yield self.env.process(self.charging_station.changeTires(self,circuit))
        self.statistics.add_data_pit_stops(self.name, self.compound_type,self.raceLapsCompleted ,self.pitStop_time, circuit.name, circuit.typeRain, circuit.trackLaps)

    
    def finish(self, race_classification:dict, crashed:bool,circuit):
        
        """
        Finish the race and update race results.

        Args:
            race_classification (dict): The race classification dictionary.
            crashed (bool): Whether the vehicle has crashed.
            circuit: The circuit where the race is taking place.
        """
        
        print(f"[Vehicle {self.name}\t| Compound: {self.compound_type}]\t finishes race at {aux_function_module.convertir_a_minutos_y_segundos(self.env.now)}")
        if crashed:
            race_classification.update({self.name:(None)})
        else:
            race_classification.update({self.name:(aux_function_module.convertir_a_minutos_y_segundos(self.env.now))})
        self.statistics.add_data_pit_stops(self.name, self.compound_type,self.raceLapsCompleted,0, circuit.name, circuit.typeRain, circuit.trackLaps)
        
