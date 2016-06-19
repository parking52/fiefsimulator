import random
LOG = False

class Side:

    def __init__(self, n_soldiers, n_knights, n_lords, bonus_dice=0, bonuses=0):
        self.n_soldiers = n_soldiers
        self.n_knights = n_knights
        self.n_lords = n_lords
        self.bonus_dice = bonus_dice
        self.bonuses = bonuses
        self.sum = 0
        self.n_dice = 0
        self.compute_sum()
        self.compute_dice()

    def compute_dice(self):
        if self.sum <= 6:
            self.n_dice = 1
        if self.sum > 7:
            self.n_dice = 2
        if self.sum > 13:
            self.n_dice = 3
        if self.bonus_dice:
            self.n_dice += self.bonus_dice
        self.n_dice = max(self.n_dice, 1)

    def compute_sum(self):
        self.sum = self.n_knights * 3 + self.n_soldiers + self.n_lords

    def is_able_to_fight(self):

        is_able = True
        if self.n_knights == 0 and self.n_soldiers == 0:
            is_able = False
        return is_able

    def apply_losses(self, n_losses):

        n_triplet, rest = n_losses // 3, n_losses % 3

        # Taking the max triples of soldiers out
        soldiers_triplet_loss = 3*(min(n_triplet, self.n_soldiers//3))
        self.n_soldiers -= soldiers_triplet_loss
        n_triplet -= soldiers_triplet_loss//3

        # Now taking horses out
        knights_triplet_loss = min(n_triplet, self.n_knights)
        self.n_knights -= knights_triplet_loss
        n_triplet -= knights_triplet_loss

        # Then we take remaining (1 or 2) soldiers, adding triplets if all horses died
        rest += n_triplet*3
        n_triplet = 0
        soldiers_rest_loss = min(self.n_soldiers, rest)
        self.n_soldiers -= soldiers_rest_loss
        rest -= soldiers_rest_loss

        # remove remaining soldiers if horses were not enough
        if rest != 0:
            assert self.n_soldiers == 0

        if rest >= 3:
            assert self.n_knights == 0

        # Removing lords if no others fighters are left
        if self.n_soldiers == 0 and self.n_knights == 0:
            self.n_lords -= (n_triplet*3 + rest)
            self.n_lords = max(self.n_lords, 0)

        self.compute_sum()
        self.compute_dice()


class Dice:

    def __init__(self):
        self.dice_results = [0, 1, 1, 2, 2, 3]

    def roll_dice(self, side):
        total_rolls = 0
        for i in range(side.n_dice):
            total_rolls += random.choice(self.dice_results)
        return total_rolls


def resolve_fight(side1, side2):
    while side1.is_able_to_fight() and side2.is_able_to_fight():
        resolve_exchange(side1, side2)

    return analyse_result(side1, side2)


def resolve_exchange(side1, side2):

    dice = Dice()

    roll_side1 = dice.roll_dice(side1)
    roll_side2 = dice.roll_dice(side2)

    if LOG:
        print("side 1 got " + str(side1.n_soldiers) + " soldiers " + str(side1.n_knights) + " knights " +
              str(side1.n_lords) + " lords and will run " + str(side1.n_dice) + " dices and sum " + str(side1.sum))
        print("side 2 got " + str(side2.n_soldiers) + " soldiers " + str(side2.n_knights) + " knights " +
              str(side2.n_lords) + " lords and will run " + str(side2.n_dice) + " dices and sum " + str(side2.sum))
        print("side 1 has a loss of " + str(roll_side2))
        print("side 2 has a loss of " + str(roll_side1))

    side1.apply_losses(roll_side2)
    side2.apply_losses(roll_side1)

    if LOG:
        print("After the loss, side 1 got " + str(side1.n_soldiers) + " soldiers " + str(side1.n_knights) + " knights " +
              str(side1.n_lords) + " lords and sum " + str(side1.sum))
        print("After the loss, side 2 got " + str(side2.n_soldiers) + " soldiers " + str(side2.n_knights) + " knights " +
              str(side2.n_lords) + " lords and sum " + str(side2.sum))
        print("-------------------------------------------------------")


def analyse_result(side1, side2):
    if not side1.is_able_to_fight():
        if not side2.is_able_to_fight():
            # print("unexpected draw for the fight")
            return 0

        else:
            # print("side 2 won")
            return 2

    else:
        # print("side 1 won")
        return 1


