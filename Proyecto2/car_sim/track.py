import random

class Track:
    
    def __init__(self,name,trackLaps,avgTemperature) -> None:
        self.name=name
        self.rain=self.rain_probability()
        self.trackLaps=trackLaps
        self.avgTemperature=avgTemperature
        if self.rain:
            self.typeRain = random.choice(["Heavy Rain" , "Light Rain"])
        else:
            self.typeRain = None
    
    def rain_probability(self):
        if self.name == "Suzuka" :
            probabilities = [0.2 , 0.8]
            opciones = [True, False]
            return random.choices(opciones, weights=probabilities, k=1)[0]
    
    def showTrackInfo(self):
        if self.typeRain == None:
            print("Weather: Clear")
        else:
            print("Weather:",self.typeRain)
        
        print("Track Name:",self.name)
        print("Average Temperature:",self.avgTemperature,"Cº")
        print()
        
            

    
        

