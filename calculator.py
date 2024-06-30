#Calculator program 

def add(x, y): 
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0: 
        return "Error: Divided by zero" 
    return x / y


#List of operations 

def main(): 
    
    print("Select operation:");
    print("1. Add");
    print("2. Subtract");
    print("3. Multiply");
    print("4. Divide");


    while True: 
        #prompting user input
        choice = input("Enter choice(1/2/3/4): ")

        #checking if choice is valid
        if choice in ['1', '2', '3', '4']
            num1 = float(input("Enter first number: "));
            num2 = float(input("Enter second number: "));


        if choice == '1':
            print("Result", add(num1, num2));
        elif choice == '2': 
            print("Result", subtract(num1, num2));
        elif choice == '3':
            print("Result", multiply(num1, num2));
        elif choice == '4':
            print("Result", divide(num1, num2));

    else: 
        print("Invalid input") 


    # Ask if the user wants to perform another calculation
    next_calculation = input("Would you like to perform another calculation? (yes/no): ")
    if next_calculation.lower() != 'yes':
        break;




if __name__ == "__main__": 
    main()










