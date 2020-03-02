class Greet:
    def __init__(self,country,greeting):
        self.country = country
        self.greeting = greeting
        self.full = self.country + ' ' + self. greeting
    
    def greet(self):
        return self.greeting + ' from ' + self.country

hi = Greet('france','hi')
print(hi.greet())
hi.country = 'germany'
print(hi.greet()) #python does not update derived attributes
