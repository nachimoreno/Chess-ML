# Nachi's Chess ML Bot
This is a chess ML project started in order to gain experience in machine learning.

The idea is to create an ML bot which plays like an average human (1500ish elo in Lichess rapid).

# Phase 1 - Data Collection & Filtering

1. Choose a target average elo
2. Get classical chess games
3. Filter out:
   * Games where players are not in the target rating band 
   * Games with lots of early blunders 
   * Games that are too short (<20 plies)
   * Obvious junk games (early resign / abort)
   
Output format:
* Position encoding
* Side to move
* Potential legal moves
* Move chosen

Ideal output: 5-20 million moves