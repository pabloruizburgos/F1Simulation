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
    
   


    def showTrackInfo(self):
        print("-------------------------------------------------------------------------------------------------")
        if self.typeRain == None:
            print("Weather: Clear")
        else:
            print("Weather:",self.typeRain)
        
        print("Track Name:",self.name)
        print("Average Temperature:",self.avgTemperature,"Cº")
        print("-------------------------------------------------------------------------------------------------")
        
            

    
        

