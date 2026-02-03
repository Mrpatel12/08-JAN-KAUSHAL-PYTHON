# n = int(input("Enter number rows for the pattern :"))    

# for i in range(1, n + 1):
#         for j in range(1, i + 1):
#             print(" * ", end="")
#         print("")


# REVERSE PATTERN
 
rows = int(input("Enter number of rows for the pattern:"))

rows = 5
i = rows
while i >= 1:
    j = 1
    while j <= i:
        print(" * ", end="")
        j += 1
    print()  
    i -= 1
 