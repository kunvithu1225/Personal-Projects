// This file takes information from the team.h file

#include "team.h"

// Constructor implementation
Team::Team(const std::string& name, const std::string& coach)
    : teamName(name), coachName(coach), totalGoals(0), totalWins(0), totalLosses(0) {}

// Function to add a player to the team
void Team::addPlayer(const Player& player) {
    players.push_back(player);
}

// Function to display team information
void Team::displayTeamInfo() {
    std::cout << "Team Name: " << teamName << "\n"
              << "Coach Name: " << coachName << "\n"
              << "Total Goals: " << totalGoals << "\n"
              << "Total Wins: " << totalWins << "\n"
              << "Total Losses: " << totalLosses << "\n"
              << "Players: " << std::endl;

    for (const auto& player : players) {
        player.displayingInfo();
        std::cout << std::endl;
    }
}

// Function to update team statistics
void Team::updateTeamStats(int goals, int wins, int losses) {
    totalGoals += goals;
    totalWins += wins;
    totalLosses += losses;
}
 
