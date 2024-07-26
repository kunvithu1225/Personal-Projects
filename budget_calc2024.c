//This is a budget calculator used to manage finances 
//Update made on July 13, 2024

#include <stdio.h>
#include <string.h>

int main() {

	//Declaration of variables
	float paycheck, needs, wants, savings;



	//prompt and user input
	printf("Enter paycheck amount: $");
	scanf("%f", &paycheck);
	
	// Confirming user input
	printf("You entered: paycheck");
	
	printf("Is this a summer paycheck? (yes/no)");
	scanf(%3s, response);

	//lower-case conversion
	for (int i = 0; response[i]; i++) {
		response[i] = tolower(response[i]);
	}

	if (strcmp(reposnse, "yes") == 0) {
		printf("Here is the summer budget breakdown: ");

		//logic
                savings = 0.7 * paycheck;
                checking = 0.2 * paycheck;
                investment = 0.1 * paycheck;

                //reads user input
                printf("\nBudget Breakdown:\n");
                printf("Savings: $%.2f\n", savings);
                printf("Checking: $%.2f\n", checking);
                printf("Investment: $%.2f\n", investment);	




	} else if (strcmp(response, "no") == 0) {
		printf("Here is the standard budget breakdown: ");

		//logic
		savings = 0.5 * paycheck;
		checking = 0.3 * paycheck;
		investment = 0.2 * paycheck;

		//reads user input
		printf("\nBudget Breakdown:\n");
    		printf("Savings: $%.2f\n", savings);
    		printf("Checking: $%.2f\n", checking);
    		printf("Investment: $%.2f\n", investment);

	
	} else {
		//Edge case
		printf("Invalid input"); 
	}

	return 0;
}










