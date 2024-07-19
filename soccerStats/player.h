// This is a header file that stores information on the player class
// We will include information like an individual players stats here

#ifndef PLAYER_H
#define PLAYER_H


#include <iostream> 
#include <string>


class Player {
public: 
	std::string name; 
	std::string position;
	int goalsScored;
	int assists;
	int yellowCards;
	int redCards;


	Player(const std::string& playerName, const std::string& playerPosition);

	void displayingInfo();
	
	void updateStats(int goals, int assists, int yellow, int red); 
	};

#endif // PLAYER_H

