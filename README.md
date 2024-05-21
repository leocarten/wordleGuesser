## A wordle guessing game.
By: Leo Carten

## How to run this:

1. Clone the repository

```
git clone https://github.com/leocarten/wordleGuesser.git
```

2. Install program dependencies

```
pip install requests re enchant
```

3. Make sure you have the necesary C libraries for the enchant library. I am using MacOS, so I ran this to update dependencies:

```
brew update
brew install enchant
```

[More info can be found here for additional operating systems if you are using Windows or Linux](https://pyenchant.github.io/pyenchant/install.html)

## How to read the output:
`_____` represents all incorrect guesses.

A capital letter in the output string, such as `____P` represents a letter, `P`, which is in the string, but not in the correct place.

A lowercase letter in the output string, such as `y____` says that `y` is in the correct posiiton.