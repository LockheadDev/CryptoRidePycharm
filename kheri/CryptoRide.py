def changeActAccount():
    num = 0
    print("\n")
    num = input("Account (0-9): ")
    return num

def intInput():
    valid = False
    num = 0
    while(not valid):
        try:
            num = int(input("Option: "))
            valid=True
        except ValueError:
            print('Error: Introduce a valid option')
    return num
    
def printMenu():
    print("\n****CryptoRide****\n------------------")
    print("Active account: ",activeAccount,"\n------------------\n")
    print("1. Change active account")
    print("2. Publish ride")
    print("3. Bid")
    print("4.  ")
    print("5. End")
    return

end = False
ans = 0
activeAccount = 0
 
while not end:
    printMenu()   
 
    ans = intInput()
 
    if ans == 1:
        activeAccount = changeActAccount()
    elif ans == 2:
        print ("Opcion 2")
    elif ans == 3:
        print("Opcion 3")
    def changeActAccount():
    num = 0
    print("\n")
    num = input("Account (0-9): ")
    return num

def intInput():
    valid = False
    num = 0
    while(not valid):
        try:
            num = int(input("Option: "))
            valid=True
        except ValueError:
            print('Error: Introduce a valid option')
    return num
    
def printMenu():
    print("\n****CryptoRide****\n------------------")
    print("Active account: ",activeAccount,"\n------------------\n")
    print("1. Change active account")
    print("2. Publish ride")
    print("3. Bid")
    print("4. End ride")
    print("5. End")
    return

end = False
ans = 0
activeAccount = 0
 
while not end:
    printMenu()   
    ans = intInput()
    if ans == 1:
        activeAccount = changeActAccount()
    elif ans == 2:
        print ("Publish ride")
    elif ans == 3:
        print("Bid")
    elif ans == 4:
        print("End ride")
    elif ans == 5:
        end = True
    else:
        print ("Error: Introduce a valid option")
        
print ("End")