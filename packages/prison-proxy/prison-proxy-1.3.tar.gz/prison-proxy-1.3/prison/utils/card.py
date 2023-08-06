# aa
# kk
# qq
# jj
# 1010
# 99
# 88
# 77

CHANGE_LEFT = 0
CHANGE_RIGHT = 1
CHANGE_ANY = 2
DO_NOT_CHANGE = 3


def which_change(left, right, wanna):
    left_card_type = left[1]
    right_card_type = right[1]

    # wanna: kk
    # left: bk
    # right: pk
    if left_card_type in wanna and right_card_type in wanna:
        return DO_NOT_CHANGE

    # wanna: kk
    # left: bk
    # right: p7
    if left_card_type in wanna:
        return CHANGE_RIGHT

    # wanna: kk
    # left: bk
    # right: p7
    if right_card_type in wanna:
        return CHANGE_LEFT

    # wanna: kk
    # left: b10
    # right: p7
    return CHANGE_ANY
