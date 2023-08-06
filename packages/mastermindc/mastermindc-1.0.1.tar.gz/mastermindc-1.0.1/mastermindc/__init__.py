import random
import time


# calculates every permutation of a list recursively, and of a specified length
def permute(a_list, codeLength):
    if codeLength == 1:
        return [[el] for el in a_list]
    else:
        out = []
        for i in range(0, len(a_list)):
            cOut = permute(a_list, codeLength - 1)
            for el in cOut:
                out.append([a_list[i]] + el)
        return out


# finds out whether or not two reponses are equal (in combination, permutation is not relevant)
def match(response1, response2):
    for el in response1:
        if response1.count(el) != response2.count(el):
            return False
    return True


# random guess
def a_guess(possibles):
    return random.choice(possibles)


# sketchy if repeats are allowed
def gradeGuess(guess, answerKey):
    res = []
    for g in range(0, len(guess)):
        if answerKey[g] == guess[g]:
            res.append('g')
        elif guess[g] in answerKey:
            res.append('b')
        else:
            res.append('r')
    return res


# makes sure none of the possibilities contradict our information basis
def eliminate_possibles_pro(possibles, guesses, answers):
    for guess in range(len(possibles)-1, -1, -1):
        for g in range(0, len(guesses)):
            tentativeAnswers = "".join(gradeGuess(guesses[g], possibles[guess])).lower()
            realCAnswers = "".join(answers[g]).lower()
            if not match(tentativeAnswers, realCAnswers):
                possibles.pop(guess)
                break
    return possibles

def game():
    nums = 5
    codeLength = 4
    done = "not yet"

    print("OK lets go I am going to play mastermind you are going to lose")
    print("If you do not know the rules google them or leave now")

    temp = input("what is the code length?\t")
    try:
        codeLength = int(temp)
    except:
        print("um ya I dunno man, I am going to set the code length to " + str(codeLength))

    temp = input("what is the number of numbers I can guess up to 1 less than but starting at 0?\t")
    try:
        nums = int(temp)
    except:
        print("Set to default value of " + str(nums))


    print("think of a " + str(codeLength) + " length number with numbers from 0 to " + str(nums - 1) + " inclusive")
    time.sleep(0.5)

    alphabet = list(range(0, nums))
    possibles = permute(alphabet, codeLength)

    # remove codes with more than 1 of a number
    for i in range(len(possibles) - 1, -1, -1):
        for c in possibles[i]:
            if possibles[i].count(c) > 1:
                possibles.pop(i)
                break


    guesses = []
    answers = []  # both of these lists are in order of occurence do not mess up the order


    print("I will guess and you will give me feedback")
    while done == "not yet":
        if len(possibles) == 0:
            print("I am relatively sure that you have given me incorrect information...")
            print("You have told me the following")
            qas = [str(guesses[i]) + "->" + str(answers[i]) for i in range(0, len(answers))]
            print("Q and A's\n" + "\n".join(qas))
            done = "user cheated"
        else:
            cur_guess = a_guess(possibles)

            print("My guess is " + str(cur_guess))
            print("I was guessing out of about {} possibilities".format(len(possibles)))
            print("How correct was I (1 R per number not in the code, 1B per correct number in incorrect place, and 1G per correct number in correct place)")
            feedback = []
            while len(feedback) != codeLength:
                feedback = input("Answer(space seperated):\t").lower().split(" ")
            guesses.append(cur_guess)
            answers.append(feedback)
            if feedback == ["g" for i in range(0, codeLength)]:
                done = "computer won"
            else:
                # all the brains
                possibles = eliminate_possibles_pro(possibles, guesses, answers)


    if done == "computer won":
        print("good game")
    elif done == "user cheated":
        print("cheaters never win")


def main():
    game()
