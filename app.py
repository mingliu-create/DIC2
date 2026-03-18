from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


def value_iteration(n, start, goal, blocks, gamma=0.9, theta=1e-4):
    def in_bounds(r, c):
        return 0 <= r < n and 0 <= c < n

    # Initialize
    V = [[0.0 for _ in range(n)] for _ in range(n)]
    is_block = [[False for _ in range(n)] for _ in range(n)]
    for (r, c) in blocks:
        is_block[r][c] = True

    actions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def step(r, c, a):
        if (r, c) == tuple(goal) or is_block[r][c]:
            return r, c
        dr, dc = actions[a]
        nr, nc = r + dr, c + dc
        if not in_bounds(nr, nc) or is_block[nr][nc]:
            return r, c
        return nr, nc

    # Rewards: -1 per step, 0 at goal
    while True:
        delta = 0.0
        newV = [row[:] for row in V]
        for r in range(n):
            for c in range(n):
                if is_block[r][c] or (r, c) == tuple(goal):
                    continue
                best = -math.inf
                for a in actions:
                    nr, nc = step(r, c, a)
                    reward = 0.0 if (nr, nc) == tuple(goal) else -1.0
                    val = reward + gamma * V[nr][nc]
                    if val > best:
                        best = val
                newV[r][c] = best
                delta = max(delta, abs(V[r][c] - newV[r][c]))
        V = newV
        if delta < theta:
            break

    # Derive policy (greedy)
    policy = [['' for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if is_block[r][c]:
                policy[r][c] = ''
            elif (r, c) == tuple(goal):
                policy[r][c] = 'T'
            else:
                best = -math.inf
                best_a = ''
                for a in actions:
                    nr, nc = step(r, c, a)
                    reward = 0.0 if (nr, nc) == tuple(goal) else -1.0
                    val = reward + gamma * V[nr][nc]
                    if val > best:
                        best = val
                        best_a = a
                policy[r][c] = best_a

    # Compute path following policy from start
    path = []
    cur = tuple(start)
    seen = set()
    max_steps = n * n * 4
    steps = 0
    while cur != tuple(goal) and steps < max_steps:
        if cur in seen:
            break
        seen.add(cur)
        path.append(cur)
        a = policy[cur[0]][cur[1]]
        if a == '' or a == 'T':
            break
        cur = step(cur[0], cur[1], a)
        steps += 1
    if cur == tuple(goal):
        path.append(cur)

    return V, policy, path


@app.route('/')
def index():
    # Default scenario: 5x5 start (0,0), goal (4,4), blocks at (1,1),(2,2),(3,3)
    n = int(request.args.get('n', 5))
    n = max(5, min(9, n))
    start = [0, 0]
    goal = [n - 1, n - 1]
    default_blocks = []
    if n == 5:
        default_blocks = [[1, 1], [2, 2], [3, 3]]
    return render_template('index.html', n=n, start=start, goal=goal, blocks=default_blocks)


@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    n = int(data.get('n'))
    start = data.get('start')
    goal = data.get('goal')
    blocks = data.get('blocks', [])
    V, policy, path = value_iteration(n, start, goal, blocks)
    return jsonify({'V': V, 'policy': policy, 'path': path})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
