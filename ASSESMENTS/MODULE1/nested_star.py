rows = int(input("Enter number of rows:"))

def pattern(n):
    
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print("* ", end="")
        print("")
