//This is a budget calculator used to manage finances 

#include <stdio.h>

int main() {

	//Declaration of variables
	float paycheck, needs, wants, savings;



	//prompt and user input
	printf("Enter paycheck amount: $");
	scanf("%f", &paycheck);

	//logic
	needs = 0.5 * paycheck;
	wants - 0.3 * paycheck;
	savings = 0.2 * paycheck;

	//reads user input
	printf("\nBudget Breakdown:\n");
    	printf("Needs: $%.2f\n", needs);
    	printf("Wants: $%.2f\n", wants);
    	printf("Savings: $%.2f\n", savings);

		

	return 0;
}










