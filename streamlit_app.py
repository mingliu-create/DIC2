import streamlit as st
from app import value_iteration

st.set_page_config(page_title="Grid MDP - Streamlit", layout='centered')

st.title("Grid MDP — Value Iteration")

n = st.sidebar.slider('Grid size n', 5, 9, 5)

# prepare cell labels
cells = [f"{r},{c}" for r in range(n) for c in range(n)]

start_label = st.sidebar.selectbox('Start cell', cells, index=0)
goal_label = st.sidebar.selectbox('Goal cell', cells, index=len(cells)-1)

# default blocks: diagonal for n==5
default_blocks = []
if n == 5:
    default_blocks = ['1,1', '2,2', '3,3']

blocks_sel = st.sidebar.multiselect('Blocks (max n-2)', cells, default=default_blocks)
if len(blocks_sel) > n-2:
    st.sidebar.error(f'Max {n-2} blocks allowed')

if st.sidebar.button('Run Value Iteration'):
    start = [int(x) for x in start_label.split(',')]
    goal = [int(x) for x in goal_label.split(',')]
    blocks = [[int(x) for x in b.split(',')] for b in blocks_sel]

    V, policy, path = value_iteration(n, start, goal, blocks)

    arrows = {'U':'↑','D':'↓','L':'←','R':'→','T':'★','':''}

    # show values table
    st.subheader('State Values V(s)')
    import pandas as pd
    df = pd.DataFrame([[f"{v:.2f}" for v in row] for row in V])
    st.table(df)

    # show policy grid
    st.subheader('Policy (arrows)')
    html = ['<table style="border-collapse:collapse">']
    for r in range(n):
        html.append('<tr>')
        for c in range(n):
            cell_style = 'padding:10px; border:1px solid #999; text-align:center; width:48px;'
            classes = []
            if [r,c] == start:
                cell_style += ' background:#b7f0b7;'
            if [r,c] == goal:
                cell_style += ' background:#f0b7b7;'
            if [r,c] in blocks:
                cell_style += ' background:#d0d0d0;'
            arrow = arrows.get(policy[r][c], '')
            html.append(f"<td style='{cell_style}'>{arrow}<div style='font-size:10px'>{V[r][c]:.2f}</div></td>")
        html.append('</tr>')
    html.append('</table>')
    st.markdown(''.join(html), unsafe_allow_html=True)

    # show path
    st.subheader('Planned Path')
    st.write(path)

    st.success('Value iteration completed')

else:
    st.info('Configure parameters in the sidebar and click "Run Value Iteration"')
