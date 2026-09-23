# Exercises — Week 03 (Python II)

> Open-ended practice for control flow. The [Week 03 checkpoints](/Lecture/Lecture_03/README.md#checkpoints)
> are the graded-style version; these are for exploring. `uv run your_script.py`.

## 1. Asterisk diamond

Print a symmetric pattern whose height is given by the user — grow, then shrink:

```
please input a number: 5
*
**
***
****
*****
****
***
**
*
```

Then try: centre it into a pyramid; use a character other than `*`; make the
width grow by twos.

## 2. Guess the number

The program picks a secret number (`random.randint`); the player guesses.
After each wrong guess, print "higher" or "lower". End with a win message.

Extend it: cap the number of guesses; count how many they used; use
`random.seed()` so you can replay the exact same game while debugging (this is
the same reproducibility idea as the `roll_dice` checkpoint).

## 3. Factorial

Compute the factorial of a number the user enters. Print an error for negative
input; treat a missing/zero input as `0! = 1`. Write it with a loop here — then,
in **Week 08**, you will write it again with recursion and can compare.

## 4. Palindrome

Check whether a string reads the same forwards and backwards, ignoring spaces
and capitalisation (`"A man a plan a canal Panama"` → yes). This is checkpoint
`is_palindrome` in Week 03; here, extend it to also ignore punctuation, and to
report *where* the mismatch is when it is not a palindrome.
