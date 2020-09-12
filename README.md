# Minesweeper-solver-AI
AI that deduces safe spots and mines in a Minesweeper game

## About
Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" without detonating any of them, with help from clues about the number of neighboring mines in each field.

## Description
This AI is able to deduce mines and safe spots by using combinations of different already known "knowledge". It makes use of mulitple known statements to infer more true statements which is used to infer even more true statements that is all added to it's knowledge base. 

## Inference Engine
This AI implements Inference Engine
Minimax is an AI strategy that applies logical rules to a knowledge base to deduce new information.
The AI basically uses it's current knowledge base and "logical rules" added to infer new statements to add to it's knowledge base, in turn making it "smarter" and able to infer more statements, which would also make it also add to it's knowledeg base and make it able to infer even more statements. This allows the AI some form of self-learning capabilities.

This however means that the AI would need to have some form of knowledge before it can infer more knowledge, and so at the beginning of the minesweeper game, the Ai knows nothing about the mines or the safe spots so it is to "Guess", and if it is lucky and didn't hit a mine, it would add the new statement it has learnt to it's knowledge base (the new statement in this case could be "there are 3 mines around cell-[row 3, column 5]" )

## TODO:
### Smarter Guessing
Currently, if the AI can't infer anything from the knowledge base, it would have to guess; but I believe this guessing can be optimized. I noticed that AI can better infer new statements with old statements that are closely related.
For example, if the AI knows "This week, it will only rain on Tuesday or Thursday", and "a boy went to play football yesterday". The AI can't infer anything from these two pieces of information.
Maybe it can use the first statement with some other statement to infer something, but the two statements it has aren't closely related so it can't work with them.
In another case, if the second statement was "Tomorrow is Tuesday", the two statements are related so it could infer things like "It did not rain today".

In this case, guessing the values of cells that are far away from each other is almost useless as they are very independent of each other. 
So in the beginning when the AI has to guess, the first guess could be at random, but the second guess should be a cell close to the first guess, so that the chances that the statements work together is higher. This would allow the AI infer new statements faster, making it a smarter guesser.

## Installing 
Run `pip3 install -r requirements.txt` to install the required Python package (pygame) for the project. Then run `Python3 runner.py` to start the game

