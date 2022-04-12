import sys
import operator
import math
with open("calclog.txt","w") as log:
    log.write("")
OPERATIONS = {
    "+":operator.add,
    "-":operator.sub,
    "*":operator.mul,
    "%":operator.truediv,
    "**":math.pow
    }

def test_function() -> None:
    assert calculate([2,"*",2,"*",2,"+",5,"+",5,"*",2,"*",2]) == 33
    assert calculate([8,"+",2,"**",3,"%",4,"-",33,"*",2]) == -56
    assert calculate(replacer(['1', '+', '5', '%', '6', '+', '7', '**', '2', '*', '2', '+', 'pi'])) == 102.97492598692313
    assert calculate([1,"+",8,"+",2]) == 11
    assert calculate([500,"-",80]) == 420
    assert calculate([70,"*",3,"*",7]) == 1470
    assert calculate([80,"%",4,"%",5]) == 4
    assert calculate([2,"**",3]) == 8
    assert calculate([10,"-",7,"%",2]) == 6.5
    assert calculate([20,"%",3]) == 6.666666666666666666666
    assert calculate([8]) == 8
    assert calculate(replacer(["pi"])) == math.pi
    assert calculate([10,"**",100]) == 1e+100

def file_opener(argument_list:list):
    if len(argument_list) == 1:
        with open(argument_list[0],"r") as file:
            argument_list = file.read().replace('\n',' ').split(' ')
    return argument_list

def replacer(argument_list):
    for i in range(len(argument_list)):
        if argument_list[i].isnumeric():
            argument_list[i] = int(argument_list[i])
        if argument_list[i] == "pi":
            argument_list[i] = math.pi
    return(argument_list)

def calculate(argument_list):
    
    def calculation(argument_list,index,item):
        temp = argument_list[index]
        argument_list[index] = OPERATIONS[item](argument_list[index-1],argument_list[index+1])
        with open("calclog.txt","a") as log:
            log.write(f"{argument_list[index-1]} {temp} {argument_list[index+1]} = {argument_list[index]}\n")
        argument_list.pop(index+1)
        argument_list.pop(index-1)
        return argument_list
    
    def operate(argument_list,operator,operator2=""):
        while operator in argument_list or operator2 in argument_list:
            for index,item in enumerate(argument_list):
                if item == operator or item == operator2:
                    argument_list = calculation(argument_list,index,item)
    
    operate(argument_list,"**")
    operate(argument_list,"%","*")
    operate(argument_list,"+","-")

    return argument_list[0]

def main():
    argument_list = file_opener(argument_list)
    argument_list = replacer(argument_list)
    print(argument_list)
    equation_result = calculate(argument_list)
    print(equation_result)
    return equation_result

def verify():
    incorrect = False
    with open(argument_list[1],"r") as verifier:
        for line in verifier:
            left_side = line.split(" ")[0:-2]
            left_side = " ".join(left_side)
            equation = line.split(" ")
            testresult = equation[-1].strip()
            equation = equation[0:-2]
            calcresult = calculate(replacer((equation)))

            if testresult != str(calcresult):
                print(f"{left_side} should equal {calcresult}, but equals {testresult} instead.")
                incorrect = True
    if not incorrect:
        print("Verified Successfully!")

if __name__ == "__main__":
    test_function()
    argument_list = sys.argv[1:]
    if argument_list[0] == "verify":
        verify() #TODO: add support for floats 
    else:
        main()