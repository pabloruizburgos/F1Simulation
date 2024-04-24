import random
from statistics import StatisticsCollector

class Track:
    
    def __init__(self,name,trackLaps,avgTemperature,statistics: StatisticsCollector) -> None:
        self.name=name
        self.rain=self.rain_probability()
        self.trackLaps=trackLaps
        self.avgTemperature=avgTemperature
        self.race_classification = dict()
        if self.rain:
            self.typeRain = random.choice(["Heavy Rain" , "Light Rain"])
        else:
            self.typeRain = None
        self.statistics = statistics
        
    
    def rain_probability(self):
        opciones = [True, False]
        probabilities = []
        if self.name == "Suzuka":
            probabilities = [0.2, 0.8]
        elif self.name == "Monza":
            probabilities = [0.3, 0.7]
        elif self.name == "Interlagos":
            probabilities = [0.4, 0.6]
        elif self.name == "Monaco":
            probabilities = [0.5, 0.5]
        elif self.name == "Silverstone":
            probabilities = [0.6, 0.4]
        elif self.name == "Spa":
            probabilities = [0.8, 0.2]
        elif self.name == "Hungaroring":
            probabilities = [0.2, 0.8]
        elif self.name == "Hockenheimring":
            probabilities = [0.3, 0.7]
        elif self.name == "YasMarina":
            probabilities = [0.4, 0.6]
        elif self.name == "Shanghai":
            probabilities = [0.5, 0.5]
        elif self.name == "Sepang":
            probabilities = [0.6, 0.4]
        elif self.name == "RedBullRing":
            probabilities = [0.7, 0.3]
        elif self.name == "GillesVilleneuve":
            probabilities = [0.8, 0.2]
        elif self.name == "Bahrain":
            probabilities = [0.9, 0.1]
        elif self.name == "Sochi":
            probabilities = [0.2, 0.8]
        elif self.name == "Australia":
            probabilities = [0.3, 0.7]
        elif self.name == "Imola":
            probabilities = [0.4, 0.6] 
        
        return random.choices(opciones, weights=probabilities, k=1)[0]
    
    def classify_pilots(self, season_classification):
        # Filtra los pilotos con tiempo de carrera y los ordena por tiempo
        valid_pilots = {pilot:(time,escuderia) for pilot, (time,escuderia) in self.race_classification.items() if time is not None}
        sorted_pilots = sorted(valid_pilots.items(), key=lambda item: item[1])

        # Convierte la lista de pilotos ordenados de nuevo en un diccionario ordenado
        classification = {i + 1: (pilot, (time, escuderia)) for i, (pilot, (time, escuderia)) in enumerate(sorted_pilots)}
        
        # Agrega los pilotos sin tiempo de carrera al final del ranking
        no_time_rank = len(classification) + 1
        for pilot, (time, escuderia) in self.race_classification.items():
            if time is None:
                classification[no_time_rank] = (pilot, (None, escuderia))
                no_time_rank += 1

        self.race_classification = classification
        # Imprime cada piloto con su tiempo en una línea separada y actualiza sus puntos según su ranking
        print("\n\n\t\t\tTABLA DE RESULTADOS\n")
        for rank, (pilot, (time,escuderia)) in self.race_classification.items():
            if time is not None:
                if rank == 1:
                    season_classification[pilot] += 25
                elif rank == 2:
                    season_classification[pilot] += 18
                elif rank == 3:
                    season_classification[pilot] += 15
                elif rank == 4:
                    season_classification[pilot] += 12
                elif rank == 5:
                    season_classification[pilot] += 10
                elif rank == 6:
                    season_classification[pilot] += 8
                elif rank == 7:
                    season_classification[pilot] += 6
                elif rank == 8:
                    season_classification[pilot] += 4
                elif rank == 9:
                    season_classification[pilot] += 2
                elif rank == 10:
                    season_classification[pilot] += 1

                print(f'{rank}. {pilot}: {time}. {escuderia}')
            else:
                print(f'{rank}. {pilot}: Not finished. {escuderia}')
        print("\n")       

        self.statistics.add_data_race_classification(self.name, self.race_classification)


    def showTrackInfo(self):
        print("-------------------------------------------------------------------------------------------------")
        if self.typeRain == None:
            print("Weather: Clear")
        else:
            print("Weather:",self.typeRain)
        
        print("Track Name:",self.name)
        print("Average Temperature:",self.avgTemperature,"Cº")
        print("-------------------------------------------------------------------------------------------------")
        
            

    
        

