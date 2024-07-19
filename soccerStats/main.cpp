// This is the main file that synthesizes all of the files into a primary display

#include <iostream>
#include "player.h"
#include "team.h"

int main() {
    // Create a team
    Team team("Santa Cruz FC", "John Doe");

    // Create players
    Player player1("Alice Smith", "Forward");
    Player player2("Bob Johnson", "Midfielder");
    Player player3("Charlie Brown", "Defender");

    // Add players to the team
    team.addPlayer(player1);
    team.addPlayer(player2);
    team.addPlayer(player3);

    // Update player stats
    player1.updateStats(5, 3, 1, 0); // Goals, Assists, Yellow Cards, Red Cards
    player2.updateStats(2, 4, 0, 1);
    player3.updateStats(0, 1, 2, 0);

    // Display individual player stats
    std::cout << "Player Stats:" << std::endl;
    player1.displayInfo();
    std::cout << std::endl;
    player2.displayInfo();
    std::cout << std::endl;
    player3.displayInfo();
    std::cout << std::endl;

    // Update team stats
    team.updateTeamStats(7, 2, 1); // Goals, Wins, Losses

    // Display team information
    std::cout << "Team Info:" << std::endl;
    team.displayTeamInfo();

    return 0;
}




