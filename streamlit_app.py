import streamlit as st
from app import value_iteration

st.set_page_config(page_title="Grid MDP - Streamlit", layout='centered')
st.title("Grid MDP — Clickable Grid")

def init_state(n):
    if 'n' not in st.session_state or st.session_state.n != n:
        st.session_state.n = n
        st.session_state.start = [0, 0]
        st.session_state.goal = [n-1, n-1]
        st.session_state.blocks = [[1,1],[2,2],[3,3]] if n==5 else []
        st.session_state.V = None
        st.session_state.policy = None
        st.session_state.path = None
        st.session_state.mode = 'block'

def cell_label(r, c):
    if [r,c] == st.session_state.start:
        return 'S'
    if [r,c] == st.session_state.goal:
        return 'G'
    if [r,c] in st.session_state.blocks:
        return 'X'
    # if policy exists, show arrow
    if st.session_state.policy:
        a = st.session_state.policy[r][c]
        return {'U':'↑','D':'↓','L':'←','R':'→','T':'★'}.get(a, '')
    return ''

def on_cell_click(r, c):
    mode = st.session_state.mode
    if mode == 'start':
        # prevent placing start on a block
        if [r,c] in st.session_state.blocks:
            st.warning('Cannot set start on a block')
            return
        st.session_state.start = [r,c]
    elif mode == 'goal':
        if [r,c] in st.session_state.blocks:
            st.warning('Cannot set goal on a block')
            return
        st.session_state.goal = [r,c]
    else:  # block
        if [r,c] == st.session_state.start or [r,c] == st.session_state.goal:
            st.warning('Cannot block start/goal')
            return
        if [r,c] in st.session_state.blocks:
            st.session_state.blocks.remove([r,c])
        else:
            if len(st.session_state.blocks) < st.session_state.n - 2:
                st.session_state.blocks.append([r,c])
            else:
                st.warning(f'Max {st.session_state.n-2} blocks allowed')

def run_value_iteration():
    V, policy, path = value_iteration(st.session_state.n, st.session_state.start, st.session_state.goal, st.session_state.blocks)
    st.session_state.V = V
    st.session_state.policy = policy
    st.session_state.path = path


n = st.sidebar.slider('Grid size n', 5, 9, st.session_state.get('n',5))
init_state(n)

st.sidebar.markdown('---')
st.sidebar.radio('Mode', ['block','start','goal'], key='mode', index=['block','start','goal'].index(st.session_state.mode))
if st.sidebar.button('Run Value Iteration'):
    run_value_iteration()

st.sidebar.markdown('Blocks:')
st.sidebar.write(st.session_state.blocks)

st.subheader('Click a cell to set start/goal/toggle block')

cols = []
for r in range(n):
    row_cols = st.columns(n, gap='small')
    for c, col in enumerate(row_cols):
        key = f'cell_{r}_{c}_{n}'
        label = cell_label(r,c)
        if col.button(label or ' ', key=key, help=f'Cell {r},{c}'):
            on_cell_click(r,c)
            st.experimental_rerun()

if st.session_state.V:
    st.subheader('State Values V(s)')
    import pandas as pd
    df = pd.DataFrame([[f"{v:.2f}" for v in row] for row in st.session_state.V])
    st.table(df)

    st.subheader('Planned Path')
    st.write(st.session_state.path)

    st.success('Value iteration completed')
else:
    st.info('No computed policy yet. Click "Run Value Iteration".')
