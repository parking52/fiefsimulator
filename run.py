import fight
import numpy as np


def test_run():

    side1 = fight.Side(n_soldiers=2, n_knights=3, n_lords=1)
    side2 = fight.Side(n_soldiers=1, n_knights=8, n_lords=2, bonus_dice=-1)
    fight_result = fight.resolve_fight(side1, side2)
    assert fight_result < 3
    return fight_result

test_run()

results = []
n_sample = 10000
for i in range(n_sample):
    results.append(test_run())

results = np.array(results)
victory_side1 = len(np.where(results == 1)[0]) / (n_sample / 100)
victory_side2 = len(np.where(results == 2)[0]) / (n_sample / 100)
draw = len(np.where(results == 0)[0]) / (n_sample / 100)


print("This fight has probability of " + str(victory_side1) + "% side 1 victory, " + str(victory_side2) +
      "% side 2 victory, and a draw for " + str(draw) + "%.")

