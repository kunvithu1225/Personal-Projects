// This is a budget calculator used to manage finances
// Update made on July 13, 2024

#include <stdio.h>
#include <string.h>
#include <ctype.h> // Required for tolower()

int main() {

    // Declaration of variables
    float paycheck, savings, checking, investment;
    char response[4]; // To hold 'yes' or 'no' input

    // Prompt and user input
    printf("Enter paycheck amount: $");
    scanf("%f", &paycheck);

    // Confirming user input
    printf("You entered: $%.2f\n", paycheck); // Displaying the value of paycheck

    // Asking if it's a summer paycheck
    printf("Is this a summer paycheck? (yes/no): ");
    scanf("%3s", response); // Input for response (max 3 chars + '\0')

    // Lower-case conversion
    for (int i = 0; response[i]; i++) {
        response[i] = tolower(response[i]);
    }

    // Checking if response is 'yes' or 'no'
    if (strcmp(response, "yes") == 0) {
        printf("Here is the summer budget breakdown:\n");

        // Summer budget logic
        savings = 0.7 * paycheck;
        checking = 0.2 * paycheck;
        investment = 0.1 * paycheck;

    } else if (strcmp(response, "no") == 0) {
        printf("Here is the standard budget breakdown:\n");

        // Standard budget logic
        savings = 0.5 * paycheck;
        checking = 0.3 * paycheck;
        investment = 0.2 * paycheck;

    } else {
        // Edge case for invalid input
        printf("Invalid input. Please enter 'yes' or 'no'.\n");
        return 1; // Exit with an error code
    }

    // Displaying budget breakdown
    printf("\nBudget Breakdown:\n");
    printf("Savings: $%.2f\n", savings);
    printf("Checking: $%.2f\n", checking);
    printf("Investment: $%.2f\n", investment);

    return 0;
}
