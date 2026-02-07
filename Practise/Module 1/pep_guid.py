
import math
import sys


def area_of_circle(radius: float) -> float:
 
 
    pi = math.pi
    area = pi * radius**2

  
    return area

DEFAULT_RADIUS = 5.0

def main():
    circle_radius = DEFAULT_RADIUS
   
    calculated_area = area_of_circle(circle_radius)

   
    print(f"The area of a circle with radius {circle_radius} is: {calculated_area:.2f}")

if __name__ == "__main__":
    main()
