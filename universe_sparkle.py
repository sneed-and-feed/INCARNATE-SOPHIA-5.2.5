
# universe_sparkle.py
import random

def generate_constellation(name, num_stars):
    constellation = f"Constellation: {name}\n"
    for i in range(num_stars):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        constellation += f"  * <3 at ({x}, {y})\n" # <3 is a heart!
    return constellation

# Let's make some constellations!
constellation1 = generate_constellation("The Great Cuddle", 7)
constellation2 = generate_constellation("The Sparkling Smile", 5)
constellation3 = generate_constellation("The Infinite Nuzzle", 9)

universe = constellation1 + constellation2 + constellation3

print(universe)
