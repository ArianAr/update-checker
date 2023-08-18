
prorgrams = ["type1", "type2", "type3", "type4", "type5", "type6", "type7", "type8", "type9", "type10"]

def list_type1():
    # for range
    for i in range(len(prorgrams)):
        if i % 2 == 0:
            print(prorgrams[i])

    # for in
    for program in prorgrams:
        print(program)
        
    # while
    index = 0 
    while index < len(prorgrams):
        print(prorgrams[index])
        index += 1
    


# -------- Math Operations
# % = Modulo
# * = Multiplication
# - = Subtraction
# + = Addition
# ** = Exponentiation
# / = Division


# -------- type of loops
# for loop
# for i in range(len(prorgrams), step=2):
#         print(prorgrams[i])



# -------- type of function call
# list_type1()
# list_type2(1,2,3)
# list_type3(taghi=1, naghi=2, jafar=3)


# -------- string functions 
# print("hello".capitalize())
# print("hello".upper())
# print("hello".lower())