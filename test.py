import fight


def test_dices_and_sum():
    side0 = fight.Side(1, 1, 1)
    assert side0.n_dice == 1
    assert side0.sum == 5
    side0 = fight.Side(1, 1, 1, bonus_dice=-1)
    assert side0.n_dice == 1
    assert side0.sum == 5
    side0 = fight.Side(2, 2, 1, bonus_dice=-1)
    assert side0.n_dice == 1
    assert side0.sum == 9

    side1 = fight.Side(2, 3, 1)
    assert side1.n_dice == 2
    assert side1.sum == 12

    side2 = fight.Side(1, 8, 2, bonus_dice=-1)
    assert side2.n_dice == 2
    assert side2.sum == 27

    side1.apply_losses(5)
    assert side1.n_knights == 2
    assert side1.n_soldiers == 0
    assert side1.n_dice == 2
    assert side1.sum == 7

    side2.apply_losses(5)
    assert side2.n_knights == 7
    assert side2.n_soldiers == 0
    assert side2.n_dice == 2
    assert side2.sum == 23


def test_able():
    side3 = fight.Side(0, 0, 1)
    assert side3.is_able_to_fight() is False
    side3 = fight.Side(1, 0, 1)
    assert side3.is_able_to_fight() is True

test_able()
test_dices_and_sum()

