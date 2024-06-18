Python program that gives suggestions for the solution word, keeping track of previous guesses and their results

How to Use:
- Run Python program and open terminal, this will be the communication method between you and the program
- Provide guess in lowercase letters only
- Provide the state of each letter in order using 0 (gray), 1 (yellow), and 2 (green)
-   For example, "crane" having the colors: green, green, yellow, gray, yellow, would translate to "22101" as input
- After providing the states, the program will give a list of potential solutions, and ask for the next word that was inputted
- The program will stop if there is only one possible solution (which will be given), or if the provided info doesn't match any of the words (likely impossible unless a misinput, in which case you have to restart the program)
