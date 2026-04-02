def state_START_STATE(input: list):
    if input[0] == '__none':
        state_Still(input[1:])


def state_Still(input: list):
    if input[0] == '__none':
        state_END_STATE(input[1:])
    if input[0] == '__none':
        state_Moving(input[1:])


def state_Moving(input: list):
    if input[0] == '__none':
        state_Still(input[1:])
    if input[0] == '__none':
        state_Crash(input[1:])


def state_Crash(input: list):
    if input[0] == '__none':
        state_END_STATE(input[1:])


def state_END_STATE(input: list):
    print("done")


if __name__ == '__main__':
    import sys
    state_START_STATE(sys.argv[1:])
