import random

class Track:
    
    def __init__(self,name) -> None:
        self.name=name
        self.rain=self.rain_probability()
        if self.rain:
            self.typeRain = random.choice(["Heavy Rain" , "Light Rain"])
        else:
            self.typeRain = None
    
    
    def rain_probability(self):
        if self.name == "Suzuka" :
            probabilidades = [0.5 , 0.5]
            opciones = [True, False]
            return random.choices(opciones, weights=probabilidades, k=1)[0]
            


