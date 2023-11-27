import random


class Game:
    def __init__(self) -> None:
        self.candidates = []
        # generate 0123 to 0987
        self.candidates += ["0" + str(i) for i in range(100, 999)]
        # generate 1234 to 9876
        self.candidates += [str(i) for i in range(1000, 9999)]
        # remove numbers with duplicated digits 
        self.candidates = [s for s in self.candidates if len(set(s)) == 4]
        # generate random number to use as our target 
        self.ans = random.sample(self.candidates, 1)[0]
        # self.ans = '2035'
        self.prev_guesses = []  # save guess, save clue 

    def check(self, guess:str, target: str) -> str:
        num_a = 0
        num_b = 0
        for i in range(len(guess)):
            if guess[i] == target[i]:
                num_a += 1
            elif guess[i] in target and guess[i] != target[i]:
                num_b += 1
        return f"{num_a}A{num_b}B"

    def learn(self, guess: str, clue: str) -> None:
        num_a, num_b = int(clue[0]), int(clue[2])

        # if none of the digit matches:
        if num_a == 0 and num_b == 0:
            lst = []
            for num in self.candidates:
                if (
                    len(set(guess) & set(num)) == 0
                ):  # only keep those that do NOT overlap
                    lst.append(num)
            self.candidates = lst
            return lst
        
        # extra logic 2, check that our current guess is consistent with previous guess 
        candidate_remove = set()
        for candidate in self.candidates: 
            for prev_guess, prev_clue in self.prev_guesses:
                if self.check(candidate, prev_guess) != prev_clue:
                    candidate_remove.add(candidate)
                    break 
        self.candidates = [num for num in self.candidates if num not in candidate_remove]
        

        # extra logic 1, check previous guesses, guess = '1A1B'
        for i in range(len(self.prev_guesses)):
            prev_guess, prev_clue = self.prev_guesses[i][0], self.prev_guesses[i][1] 
            # check if 3 digits are the same 
            if len(set(prev_guess) & set(guess)) == 3:
                prev_num_a_b = int(prev_clue[0]) + int(prev_clue[2])
                num_a_b = int(guess[0]) + int(guess[2])

                if num_a_b + 1 == prev_num_a_b:
                    # exclude new number 
                    new_num = set(guess) - set(prev_guess)
                    assert len(new_num) == 1 and type(new_num) == str
                    new_num = new_num.pop() 
                    self.candidates = [num for num in self.candidates if new_num not in num]

                elif num_a_b - 1 == prev_num_a_b:
                    # include old number 
                    old_num = set(prev_guess) - set(guess)
                    assert len(old_num) == 1 and type(old_num) == str
                    old_num = old_num.pop() 
                    self.candidates = [num for num in self.candidates if old_num in num]

        self.candidates = [
            num for num in self.candidates if num != guess
        ]  # remove the previous guess
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

    def play_game(self):
        guess = ""
        print("num ", self.ans)
        guess_cnt = 0
        while True:
            guess = input("Your guess: ")
            if guess == "tell me":
                print("correct number", self.ans)
                continue
            if guess not in self.candidates:
                if not guess_cnt < 2:
                    print('Bad guess, guess is not in candidate list')
                    continue 

            if guess == self.ans:
                print("YOU WINNN!!!")
                break
            print("actual number", self.ans)

            clue = self.check(guess, self.ans)
            # clue = input("clue is ")
            print("clue: ", clue)

            # learn and prune candidates
            self.learn(guess, clue)

            # save guess and clue
            print("Previous guesses", self.prev_guesses)
            self.prev_guesses.append([guess, clue])

            print("Number of candidates", len(self.candidates))
            print(
                "Random 10 candidates: ",
                random.sample(self.candidates, min(10, len(self.candidates))),
            )
            guess_cnt += 1
            if guess_cnt > 100:
                print("you lost, more than 100 guesses is not allowed")
                break
            print("Number of gueses ", guess_cnt)
            print()

    def bench_mark(self, num_iter=10000):
        num_guesses = [] 
        for i in range(num_iter):
            g = Game() 
            guess_cnt = 0 
            while True:
                if guess_cnt == 0:
                    guess = '0123'
                elif guess_cnt == 1:
                    guess = '4567'
                else:
                    guess = random.sample(g.candidates, 1)[0]
                guess_cnt += 1 
                if guess == g.ans:
                    num_guesses.append(guess_cnt)
                    print(f'Finished {i} run. Took {guess_cnt} gueses')
                    break 
                clue = g.check(guess, g.ans)
                g.learn(guess, clue)
        print('Average number of guesses: ', 1.0 * sum(num_guesses) / len(num_guesses))


# num_to_guess = input('Number to guess: ')
g = Game()
# g.play_game()
g.bench_mark(5000)
