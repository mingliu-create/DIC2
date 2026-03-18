# HW1 Grid MDP


Run the Flask app and open http://127.0.0.1:5000/

Install:

```bash
python -m pip install -r requirements.txt
```

Run Flask app:

```bash
python app.py
```

Usage (Flask):
- Resize grid (n between 5 and 9)
- Click `Set Start` then click a cell to set start (green)
- Click `Set Goal` then click a cell to set goal (red)
- Click `Toggle Block` then click cells to toggle blocks (gray) up to n-2 blocks
- Click `Run Value Iteration` to compute V(s), policy arrows, and the path

Default scenario: 5x5 with start (0,0), goal (4,4), blocks (1,1),(2,2),(3,3)

Streamlit app:

The repo includes a `streamlit_app.py` so you can run the same value-iteration UI in Streamlit (useful for Streamlit Cloud deployment).

Run Streamlit locally:

```bash
streamlit run streamlit_app.py
```

Deploy to Streamlit Cloud:
1. Push this repository to GitHub (already done).
2. In Streamlit Cloud (https://share.streamlit.io), connect your GitHub account and select the `mingliu-create/DIC2` repo.
3. Set the main file to `streamlit_app.py` and deploy. Streamlit will install `requirements.txt` automatically.

