# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
   *  The game is a number guessing app where the player tries to guess a secret number in a limited number of attempts. The app gives hints after each guess and tracks score. Different difficulty levels change the number range and attempts.

- [ ] Detail which bugs you found.

   * The secret number behavior felt inconsistent because of a type issue in comparisons. Hints were giving the wrong direction in some cases. New Game and difficulty switching did not always reset state correctly at first. Hard mode was not truly harder than Normal, out-of-range inputs were accepted, and attempt limit behavior was confusing.

- [ ] Explain what fixes you applied.

* I fixed guess comparisons to always use the integer secret and corrected hint direction logic. I added proper input range validation and adjusted difficulty ranges so Hard is actually harder. I centralized game state reset logic for New Game and difficulty changes, then added pytest tests to confirm all fixes. I also improved comments and organized logic into helper modules for cleaner code.


## 📸 Demo

- ![Screenshot from browser](images\browser.png)
- ![pytest screenshot](images\pytest.png)
## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
