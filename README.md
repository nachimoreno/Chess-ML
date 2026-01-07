# Nachi's Chess ML Bot
This is a chess ML project started in order to gain experience in machine learning.

The initial idea is to create an ML bot which plays like an average human (1000ish elo).

# Phase 1 - Data Collection & Filtering

1. Choose a target average elo
2. Get classical chess games
3. Filter out:
   4. Games where players are not in the target rating band
   5. Games with lots of early blunders
   5. Games that are too short (<20 plies)
   6. Obvious junk games (early resign / abort)
   
Output format:
* Position encoding
* Side to move
* Potential legal moves
* Move chosen

Ideal output: 5-20 million moves