from app import app
import json

def run_test():
    client = app.test_client()
    payload = {'n':5, 'start':[0,0], 'goal':[4,4], 'blocks':[[1,1],[2,2],[3,3]]}
    resp = client.post('/compute', data=json.dumps(payload), content_type='application/json')
    print(resp.get_data(as_text=True))

if __name__ == '__main__':
    run_test()
