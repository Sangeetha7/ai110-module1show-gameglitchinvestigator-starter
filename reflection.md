# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

* The game did not work as I expected
* The difficult levels were not designed properly
* The design aspect was cool

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  1) Clicking on 'New Game' button did not start a new game.
  2) Changing difficulty level did not start a new game
  3) Had to refresh the page completely to load a new game
  4) Even after changing the difficulty levels, the instructions did not change in the main screen. It showed guess a number between 1 to 100 for all levels.
  5) The hints were wrong
  6) No errors when I typed an out of range number
  7) 'Hard' level difficult was easier than 'Normal' level
  8) Number of attempts seem wrong


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  
  * Copilot

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

* Copilot pointed out that the type flip was causing the secret number confusion. I checked the code and saw the secret was being treated as a string on some turns. After fixing that, guesses worked consistently.
  

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

* At first, AI focused mostly on the secret number bug. I still found other bugs like scoring and difficulty problems. I verified this by testing each feature and adding pytest cases.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  
  * I manually tested the feature that was broken by repeated the same steps I performed earlier and verified the function logic in code. After that, I used pytest to make sure the fix was stable.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  * Manually clicked on the 'New Game' button and checked the developer debug info if attempts, score, history, and status reset correctly.
  * I also changed difficulty and checked that the secret reset in the new range. 
  * For automated testing, I added pytest cases for bugs like wrong hints, out-of-range guesses, and scoring issues. Passing tests showed that those fixes were actually working and not breaking something else

- Did AI help you design or understand any tests? How?

 * Yes, AI helped me turn each bug into a test case. * It suggested testing the logic functions directly first, then adding flow-style tests for full game behavior


## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

* The secret didn’t literally change every time, but the comparison logic acted differently on even attempts. The code converted the secret to a string on some turns, so guesses were compared with mixed types, which caused weird high/low results. That made it feel like the secret was moving. Once I removed that type flip and always compared integers, the game became consistent.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

 * In Streamlit, almost every interaction reruns the whole script from top to bottom. If you use normal variables, they reset on each rerun. Session state is the place where values are remembered across reruns, like secret, score, and attempts. So session state acts like memory for your app while users click buttons and type guesses.


- What change did you make that finally gave the game a stable secret number?

* I removed the code that changed the secret to a string on even attempts and always passed st.session_state.secret as an integer into check_guess. That made comparisons consistent every time. I also made sure the secret only resets on New Game or when the difficulty changes. That gave the game stable behavior.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  * Understanding the core logic and essential behaviour of an app before trying to changing anything
  * Commit changes frequently after every successful change

- What is one thing you would do differently next time you work with AI on a coding task?

  * Trying fixing one bug at a time before fixing another
  * I would also ask for test cases immediately after each fix, not at the end

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  * Helped me realize the importance of verifying AI suggestions and use our own analytical thinking at every step
