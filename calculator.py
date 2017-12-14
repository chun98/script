import math,sys
def cal(k):
    k=k.replace(' ','')
    k=k.replace('^', '**')
    k=k.replace('=', '')
    k=k.replace('?', '')
    k=k.replace('%', '/100')
    k=k.replace('rad', 'radians')
    k=k.replace('mod', '%')

    functions = ['sin', 'cos', 'tan', 'sqrt', 'pi', 'radians', 'e']
    for i in functions:
        if i in k.lower():
            trans='math.'+i
            k=k.replace(i,trans)
    try:
        k = eval(k)
    except ZeroDivisionError:
        print("Can't divide by 0")
        exit()
    except NameError:
        print('Invalid input')
        exit()
    except AttributeError:
        print('Check usage method')
        exit()
    return k

def result(k):
    print("\n"+str(cal(k)))


def main():
    print("\nCalculator\nEg: sin(rad(90)) + 50% * (sqrt(16)) + round(1.42^2) - 12mod3\nEnter quit to exit")
    if sys.version_info.major >= 3:
        while True:
            k = input("\n ")
            if k == 'quit':
                break
            result(k)
    else:
        while True:
            k = input("\n")
            if k == 'quit':
                break
            result(k)
if __name__ == '__main__':
    main()