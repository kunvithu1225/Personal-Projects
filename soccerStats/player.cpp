// This is the cpp file that takes information from the player.h file it displays and updates the information from player.h

#include "player.h"

// Constructor implementation
Player::Player(const std::string& playerName, const std::string& playerPosition)
    : name(playerName), position(playerPosition), goalsScored(0), assists(0), yellowCards(0), redCards(0) {}


// Function to display player information
void Player::displayingInfo() const {
    std::cout << "Name: " << name << "\n"
              << "Position: " << position << "\n"
              << "Goals Scored: " << goalsScored << "\n"
              << "Assists: " << assists << "\n"
              << "Yellow Cards: " << yellowCards << "\n"
              << "Red Cards: " << redCards << std::endl;
}

// Function to update player statistics
void Player::updateStats(int goals, int assists, int yellow, int red) {
    goalsScored += goals;
    this->assists += assists;
    yellowCards += yellow;
    redCards += red;
}


