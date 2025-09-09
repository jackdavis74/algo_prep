
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

tests = []

for i,test in enumerate(tests):
    output = calc_performance(test['input'])
    if output == test['expected']:
        print(f'Passed test {i}')
    else:
        print(f'Failed test {i}')
        print(test['expected'])
        print(output)