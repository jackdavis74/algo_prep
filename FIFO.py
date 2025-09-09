
def calc_performance(input):
    #parse params
    n = input[0][0]
    s_rate, o_rate = input[1]
    #init return vars
    realized = 0
    inventory = []
    for data in input[2:-1]:
        #calc fees and realize
        fees = data[2] * s_rate + o_rate
        realized -= fees
        #update buy inventory
        if data[0] == 'BUY':
            inventory.append([data[1], data[2]])
        #update inventory and realized by matching sell
        elif data[0] == 'SELL':
            sell_q = data[2]
            while sell_q > 0:
                trade_q = min(sell_q, inventory[0][1])
                realized += (data[1] - inventory[0][0]) * trade_q
                #check if buy inventory needs to be removed
                inventory[0][1] -= trade_q
                if inventory[0][1] == 0:
                    inventory.pop(0)
                #update sell q
                sell_q -= trade_q
    #calc ending position, unreal, total pnl
    end_pos = 0
    unrealized = 0
    final = input[-1][1]
    for p,v in inventory:
        end_pos += v
        unrealized += (final - p) * v
    pnl = realized + unrealized
    return [end_pos, realized, unrealized, pnl]

tests = [
    # Base case
    {
        'input': [
            [7], [1, 10],
            ['BUY', 10000, 10],
            ['BUY', 9000, 5],
            ['SELL', 9500, 8],
            ['SELL', 12000, 3],
            ['BUY', 11000, 4],
            ['SELL', 11500, 2],
            ['FINAL', 10500]
        ],
        # From earlier calc: Realized = 8000 - 92 = 7908
        # Unrealized = 1000
        # Total = 8928
        'expected': [6, 7908, 1000, 8908]
    },

    # Multiple sells consuming FIFO lots (partial fill across boundary)
    {
        'input': [
            [5], [1,10],
            ['BUY', 100, 5],     # fee 15
            ['BUY', 200, 5],     # fee 15
            ['SELL', 150, 7],    # fee 17
            ['FINAL', 180]
        ],
        # No-fee realized = (5*(150-100)) + (2*(150-200)) = 250 - 100 = 150
        # Total fees = 15+15+17=47
        # Realized = 150 - 47 = 103
        # Remaining: 3@200 → cost 600, value 540 → -60
        # Unrealized = -60
        # Total = 43
        'expected': [3, 103, -60, 43]
    },

    # Large values, check 64-bit safety
    {
        'input': [
            [3], [1,10],
            ['BUY', 1_000_000, 1_000_000],   # fee 1,000,010
            ['SELL', 1_000_100, 500_000],    # fee 500,010
            ['FINAL', 1_000_050]
        ],
        # No-fee realized = 500k*(100) = 50,000,000
        # Fees = 1,000,010 + 500,010 = 1,500,020
        # Realized = 50,000,000 - 1,500,020 = 48,499,980
        # Remaining: 500k@1,000,000 cost=500,000,000; value=500,025,000 → +25,000,000
        # Unrealized = 25,000,000
        # Total = 73,499,980
        'expected': [500_000, 48_499_980, 25_000_000, 73_499_980]
    },

    # Zero fees vs non-zero fees
    {
        'input': [
            [4], [1,10],
            ['BUY', 100, 10],    # fee 20
            ['SELL', 110, 10],   # fee 20
            ['FINAL', 120]
        ],
        # No-fee realized = 10*(110-100)=100
        # Fees = 20+20=40
        # Realized = 60
        # Unrealized = 0
        # Total = 60
        'expected': [0, 60, 0, 60]
    },

    # No shorting: sells never exceed buys
    {
        'input': [
            [3], [1,10],
            ['BUY', 50, 5],      # fee 15
            ['SELL', 55, 5],     # fee 15
            ['FINAL', 60]
        ],
        # No-fee realized = 5*(55-50)=25
        # Fees = 15+15=30
        # Realized = -5
        # Unrealized = 0
        # Total = -5
        'expected': [0, -5, 0, -5]
    },

    # Final mark correctness
    {
        'input': [
            [3], [1,10],
            ['BUY', 200, 2],     # fee 12
            ['BUY', 150, 3],     # fee 13
            ['FINAL', 180]
        ],
        # No-fee realized=0
        # Fees=12+13=25
        # Basis= (400+12) + (450+13)=875
        # Value=5*180=900
        # Unrealized=25
        # Realized=0
        # Total=25-25=0 ? Check:
        # Actually: realized=0-25=-25 (fees hit realized P&L directly),
        # Unrealized=900-850=50 (lot cost only, excluding fees),
        # Total=-25+50=25
        'expected': [5, -25, 50, 25]
    }
]

for i,test in enumerate(tests):
    output = calc_performance(test['input'])
    if output == test['expected']:
        print(f'Passed test {i}')
    else:
        print(f'Failed test {i}')
        print(test['expected'])
        print(output)