# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  When I first ran the app, the game immediately looked off — I could open the "Developer Debug Info" tab to see the secret number, but every time I clicked Submit, the number changed, making it literally impossible to win. Two concrete bugs stood out right away: first, the secret number regenerated on every button click instead of staying fixed for the round; second, the "Higher" and "Lower" hints were completely backwards — if my guess was too low, the game told me to guess lower, and vice versa. The app ran without crashing, which made the bugs sneaky because nothing looked visually broken.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Copilot (in VS Code) and ChatGPT for this project. For a correct suggestion, when fixing the state reset bug, I asked ChatGPT: "How do I keep a variable from resetting in Streamlit when I click a button?" It correctly explained Streamlit's rerun behavior and suggested using `if "secret" not in st.session_state` to initialize once. I verified by running the app, opening the debug tab, and confirming the secret stayed fixed across submits. For an incorrect/misleading suggestion, when asking Copilot to refactor the hint logic, it initially generated code that kept the original backwards directions (e.g., "Go HIGHER!" for too high guesses). I verified this was wrong by manually testing the logic and running pytest, which failed until I corrected the messages to match the outcomes.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by running both automated tests (pytest) and manual testing in the live Streamlit app. For example, after fixing the hint directions, I ran pytest on the new test_check_guess_string_secret, which passed and confirmed the logic handled both numeric and string comparisons correctly. I also played the game manually, guessing numbers and checking that hints like "Go LOWER!" appeared for too-high guesses, and that the secret didn't change on submits. Copilot helped design tests by generating the initial test cases for parse_guess and update_score, which I then expanded; it also suggested the string secret test to cover the glitchy fallback behavior.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit works differently from most frameworks: every time a user interacts with the app — clicking a button, typing in a field — the entire Python script reruns from top to bottom. That means any variable you define normally (secret = random.randint(1, 100)) gets reset to a fresh value on every interaction. Session state is Streamlit's fix for this: st.session_state is a dictionary that persists across reruns within a session, so values you store there survive button clicks. If I were explaining it to a friend, I'd say: imagine your code is a whiteboard that gets erased and redrawn every time someone clicks anything — session state is a sticky note on the side of the whiteboard that doesn't get erased.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
One habit I want to carry forward is running tests before declaring a fix done — I thought I'd fixed the hint logic the first time, but pytest immediately proved me wrong. Without it, I would have shipped the same bug in different clothes. One thing I'd do differently next time is prompt AI with the actual broken code and a specific expected behavior upfront, rather than asking a general question and then trying to adapt the answer; that's where the misleading suggestion came from. This project genuinely shifted how I think about AI-generated code — it's a strong starting point but it can confidently reproduce the exact bug you're trying to fix, so treating every AI output as something that still needs to be read and tested is now non-negotiable for me.

---

## 6. Challenge 5: AI Model Comparison

For this challenge, I selected the "hints pointing the wrong way" bug from Phase 1, where the game showed "Go HIGHER!" for too-high guesses and vice versa. I asked for fixes from Copilot (in VS Code) and ChatGPT.

**Copilot's Response:** It provided a direct code fix, suggesting to swap the messages: `return "Too High", "📉 Go LOWER!"` for `guess > secret`. It explained that the original logic was inverted, and the fix ensures messages match the outcome. The code was readable and included comments for clarity.

**ChatGPT's Response:** It also suggested swapping the messages but added more context: "The issue is that 'Too High' should prompt going lower, not higher. Here's the corrected code with an explanation of why the comparison works." It emphasized the logic behind `if guess > secret` and included a note on potential edge cases like equal values.

**Comparison:** ChatGPT gave a more readable fix with better explanation of the "why" (detailing the comparison logic and edge cases), making it easier for beginners. Copilot's fix was concise and directly actionable but less explanatory. Overall, ChatGPT explained the "why" more clearly, while Copilot was quicker for implementation.
