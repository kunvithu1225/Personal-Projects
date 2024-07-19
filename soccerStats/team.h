// This is a file for the stats of a team. In this file we are using information from player.h 
#ifndef TEAM_H
#define TEAM_H


#include <iostream>
#include <vector>
#include "player.h"

class Team {
public:
    std::string teamName;
    std::string coachName;
    std::vector<Player> players; // Vector to store Player objects
    int totalGoals;
    int totalWins;
    int totalLosses;

    // Constructor
    Team(const std::string& name, const std::string& coach);

    // Function to add a player to the team
    void addPlayer(const Player& player);

    // Function to display team information
    void displayTeamInfo();

    // Function to update team statistics
    void updateTeamStats(int goals, int wins, int losses);
};

#endif // TEAM_H


