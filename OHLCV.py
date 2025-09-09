import numpy as np

def detect_new_period(last_x:int, k:int, t:int):
    if t > (last_x+1) * (k) - 1:
        return True
    else:
        return False
    

def agg_candles(input):
    #init storage
    all_bars = []
    #init params
    n, k = input[0]
    last_x = -1
    #init return vars
    open = None
    close = None
    high = -np.inf
    low = np.inf
    volume = 0
    #collect and agg
    for data in input[1:]:
        t, p, q = data
        #detect x (period)
        x = t // k
        if x > last_x:
            if open:
                s_time = last_x * k
                e_time = (last_x+1) * k - 1
                all_bars.append([s_time, e_time, open, high, low, close, volume])
            #track open
            open = p
            #reset vars
            close = None
            high = -np.inf
            low = np.inf
            volume = 0
        #update data
        close = p
        if p > high:
            high = p
        if p < low:
            low = p
        volume += q
        last_x = x
    
    if close:
        s_time = x * k
        e_time = (x+1) * k - 1
        all_bars.append([s_time, e_time, open, high, low, close, volume])
    
    return all_bars


tests = [

    # 1. Sample case from prompt
    {
        "input": [
            (7, 60),
            (0, 100, 5),
            (5, 101, 1),
            (30, 99, 2),
            (60, 102, 3),
            (61, 103, 1),
            (119, 98, 10),
            (121, 100, 1),
        ],
        "expected": [
            [0, 59, 100, 101, 99, 99, 8],
            [60, 119, 102, 103, 98, 98, 14],
            [120, 179, 100, 100, 100, 100, 1],
        ],
    },

    # 2. Trades only in one interval (interval 0)
    {
        "input": [
            (3, 60),
            (5, 200, 10),
            (20, 195, 5),
            (59, 210, 1),
        ],
        "expected": [
            [0, 59, 200, 210, 195, 210, 16],
        ],
    },

    # 3. Many empty intervals in between (jump from t=5 to t=400)
    {
        "input": [
            (2, 60),
            (5, 50, 1),
            (400, 55, 2),
        ],
        "expected": [
            [0, 59, 50, 50, 50, 50, 1],
            [360, 419, 55, 55, 55, 55, 2],
        ],
    },

    # 4. Multiple trades at the exact same timestamp
    {
        "input": [
            (4, 60),
            (10, 100, 1),
            (10, 105, 2),
            (10, 95, 3),
        ],
        "expected": [
            [0, 59, 100, 105, 95, 95, 6],
        ],
    },

    # 5. Very large prices/volumes (check 64-bit safety)
    {
        "input": [
            (2, 60),
            (0, 1_000_000_000, 5_000_000_000),
            (30, 2_000_000_000, 4_000_000_000),
        ],
        "expected": [
            [0, 59, 1_000_000_000, 2_000_000_000, 1_000_000_000, 2_000_000_000, 9_000_000_000],
        ],
    },

]

for i,test in enumerate(tests):
    output = agg_candles(test['input'])
    if output == test['expected']:
        print(f'Passed {i}')
        print(test['expected'])
        print(output)
    else:
        print(f'Failed {i}')
        print(test['expected'])
        print(output)
    