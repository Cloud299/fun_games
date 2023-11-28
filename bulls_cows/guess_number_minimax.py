import random
import collections


class Game:
    def __init__(self) -> None:
        self.guess_cnt = 0
        # generate 0123 to 0987
        self.candidates = ["0" + str(i) for i in range(100, 999)]
        # generate 1234 to 9876
        self.candidates += [str(i) for i in range(1000, 9999)]
        # remove numbers with duplicated digits
        self.candidates = [s for s in self.candidates if len(set(s)) == 4]
        # generate random number to use as our target
        self.target = random.sample(self.candidates, 1)[0]
        # self.target = '2035'
        self.prev_guesses = []  # save guess, save clue
        # generate a list of all possible outcomes
        self.responses = []
        for i in range(5):
            self.responses.append(f"{i}A{4-i}B")

    def check(self, guess: str, target: str) -> str:
        num_a = 0
        num_b = 0
        for i in range(len(guess)):
            if guess[i] == target[i]:
                num_a += 1
            elif guess[i] in target and guess[i] != target[i]:
                num_b += 1
        return f"{num_a}A{num_b}B"

    def learn(self) -> str:
        """
        Minimax algorithm:
        For every possible guess
            For all possible responses to the guess
                Consider the size of the solution space after the response acts on it
            Select the maximum solution space size after a response has been applied, i.e. worst case scenario
        Select the guess that results minimum size of the solution space
        """
        guess = ""
        candidate_min_size = float("inf")
        # For every possible guess
        for possible_guess in self.candidates:
            # For all possible responses to the guess
            response_size = [
                self.check(possible_guess, cand) for cand in self.candidates
            ]
            #  Consider the size of the solution space after the response acts on it
            response_size = collections.Counter(response_size)
            # Select the maximum solution space size after a response has been applied, i.e. worst case scenario
            response_max_size = max(response_size.values())
            if response_max_size < candidate_min_size:
                # Select the guess that results minimum size of the solution space
                guess = possible_guess
                candidate_min_size = response_max_size
        return guess

    def prune(self, guess: str, response: str) -> None:
        # prune the size of the solution space based on our guess and response
        self.candidates = [
            cand for cand in self.candidates if self.check(guess, cand) == response
        ]
        return

    def play_game(self) -> int:
        while True:
            print(f"Target number: {self.target}")
            # return a guess
            if self.guess_cnt == 0:  # our first guess is always fixed
                guess = "0123"
            # elif self.guess_cnt == 1:
            #     guess = '4567'
            else:
                guess = self.learn()
            self.guess_cnt += 1

            response = self.check(guess, self.target)
            print(f"Guess: {guess}, response = {response}")

            # prune the solution space size
            print(f"Previous size: {len(self.candidates)}")
            self.prune(guess, response)
            print(f"Current size: {len(self.candidates)}")

            # save guess and response
            self.prev_guesses.append([guess, response])
            print("Guesses history", self.prev_guesses)

            print(
                "Random 10 candidates: ",
                random.sample(self.candidates, min(10, len(self.candidates))),
            )

            print("Number of guesses ", self.guess_cnt)

            if guess == self.target:
                print("YOU WIN!!")
                break
            print()
        return self.guess_cnt



def bench_mark(num_iter=500):
    history = []
    for i in range(num_iter):
        g = Game()
        guess_cnt = g.play_game()
        print(f"Game {i}', {guess_cnt} guesses")
        print()
        history.append(guess_cnt)
    counter = collections.Counter(history)
    for num_guess in range(10):
        if num_guess in counter:
            count = counter[num_guess]
            print(
                f"# of guesses: {num_guess}, count: {count}, probability: {100. * count / num_iter:.2f}%"
            )
    print(f"Number of Games: {num_iter}")
    print(f"Average number of guesses: {sum(history) / num_iter:.2f}")


# num_to_guess = input('Number to guess: ')
# g = Game(); g.play_game()
bench_mark(51)
