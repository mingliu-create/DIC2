from app import value_iteration

def pretty_print(V, policy, path):
    print('Values:')
    for row in V:
        print(['{:.2f}'.format(x) for x in row])
    print('\nPolicy:')
    for row in policy:
        print(row)
    print('\nPath:')
    print(path)


if __name__ == '__main__':
    n = 5
    start = [0,0]
    goal = [4,4]
    blocks = [(1,1),(2,2),(3,3)]
    V, policy, path = value_iteration(n, start, goal, blocks)
    pretty_print(V, policy, path)
