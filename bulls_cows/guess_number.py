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
        # self.target = "1730"
        self.prev_guesses = []  # save guess, save response
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

    def prune(self, guess: str, response: str) -> None:
        num_a, num_b = int(response[0]), int(response[2])

        # if none of the digit matches:
        if num_a == 0 and num_b == 0:
            self.candidates = [
                cand for cand in self.candidates if len(set(guess) & set(cand)) == 0
            ]

        # prune the size of the solution space based on our guess and response
        self.candidates = [
            cand for cand in self.candidates if self.check(guess, cand) == response
        ]

        # # extra logic 1, check previous guesses, guess = '1A1B'
        # for i in range(len(self.prev_guesses)):
        #     prev_guess, prev_response = self.prev_guesses[i][0], self.prev_guesses[i][1]
        #     # check if 3 digits are the same
        #     if len(set(prev_guess) & set(guess)) == 3:
        #         prev_num_a_b = int(prev_response[0]) + int(prev_response[2])
        #         num_a_b = int(response[0]) + int(response[2])

        #         new_num = (set(guess) - set(prev_guess)).pop()
        #         old_num = (set(prev_guess) - set(guess)).pop()

        #         if num_a_b + 1 == prev_num_a_b:
        #             # exclude new number and include old number
        #             self.candidates = [
        #                 num
        #                 for num in self.candidates
        #                 if new_num not in num and old_num in num
        #             ]

        #         elif num_a_b - 1 == prev_num_a_b:
        #             # include new number and exclude old number
        #             self.candidates = [
        #                 num
        #                 for num in self.candidates
        #                 if new_num in num and old_num not in num
        #             ]

        # main logic
        self.candidates = self.process_a(num_a, num_b, guess)
        return

    def process_a(self, num_a, num_b, guess):
        lst = []
        if num_a == 0:
            lst_a = self.candidates
            a_pos = []
            lst += self.process_b(a_pos, num_b, guess, lst_a)
            lst = list(set(lst))

        # when num_a = 1
        elif num_a == 1:
            for i in range(4):  # try a at different positions
                lst_a = []
                a_pos = [i]
                for num in self.candidates:
                    if num[i] == guess[i]:  # since a = 1, we just need 1 digit to match
                        lst_a.append(num)

                lst += self.process_b(a_pos, num_b, guess, lst_a)
            lst = list(set(lst))

        # when num_a = 2
        elif num_a == 2:
            for i in range(4):
                for j in range(i + 1, 4):
                    lst_a = []
                    a_pos = [i, j]
                    for num in self.candidates:
                        if num[i] == guess[i] and num[j] == guess[j]:
                            lst.append(num)
                    lst += self.process_b(a_pos, num_b, guess, lst_a)
            lst = list(set(lst))

        # when num_a = 3
        elif num_a == 3:
            for i in range(4):
                for j in range(i + 1, 4):
                    for k in range(j + 1, 4):
                        a_pos = [i, j, k]
                        lst_a = []
                        for num in self.candidates:
                            if (
                                num[i] == guess[i]
                                and num[j] == guess[j]
                                and num[k] == guess[k]
                            ):
                                lst_a.append(num)
                        lst += self.process_b(a_pos, num_b, guess, lst_a)
            lst = list(set(lst))
        return lst

    def process_b(self, a_pos, num_b: int, guess: str, lst_a):
        lst_b = []

        if num_b == 0:
            return lst_a

        guess_digits = set([guess[i] for i in range(4) if i not in a_pos])
        for candidate in lst_a:
            is_valid = True
            candidate_digits = set([candidate[i] for i in range(4) if i not in a_pos])
            if len(candidate_digits & guess_digits) == num_b:
                for i in range(4):
                    if (
                        i not in a_pos and guess[i] == candidate[i]
                    ):  # cannot match position
                        is_valid = False
                        break
                if is_valid:
                    lst_b.append(candidate)
        return lst_b

    def play_game(self) -> int:
        while True:
            print(f"Target number: {self.target}")
            # return a guess
            if self.guess_cnt == 0:  # our first guess is always fixed
                # guess = "0123"
                guess = random.sample(self.candidates, 1)[0]
            else:
                print(
                    "Random 10 candidates: ",
                    random.sample(self.candidates, min(10, len(self.candidates))),
                )
                # guess = input("Your guess: ")
                guess = random.sample(self.candidates, 1)[0]
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


# g = Game()
# g.play_game()
bench_mark(num_iter=10001)
