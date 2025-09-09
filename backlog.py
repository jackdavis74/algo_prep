import heapq

def process_orders(orders):
    sell_heap = []
    buy_heap = []
    for order in orders:
        price, qty, tp = order

        if tp == 0: #buy
            while qty > 0:
                if sell_heap:
                    sell_price, sell_qty, sell_tp = heapq.heappop(sell_heap)
                    if sell_price <= price:
                        trade_qty = min(qty, sell_qty)
                        qty -= trade_qty
                        sell_qty -= trade_qty
                        if sell_qty > 0:
                            heapq.heappush(sell_heap, (sell_price, sell_qty, sell_tp))
                    else:
                        heapq.heappush(sell_heap, (sell_price, sell_qty, sell_tp))
                        heapq.heappush(buy_heap, (-1 * price, qty, tp))
                        break
                else:
                    heapq.heappush(buy_heap, (-1 * price, qty, tp))
                    break


        elif tp == 1:   #sell
            while qty > 0:
                if buy_heap:
                    buy_price, buy_qty, buy_tp = heapq.heappop(buy_heap)
                    if abs(buy_price) >= price:
                        trade_qty = min(buy_qty, qty)
                        qty -= trade_qty
                        buy_qty -= trade_qty
                        if buy_qty > 0:
                            heapq.heappush(buy_heap, (buy_price, buy_qty, buy_tp))
                    else:
                        heapq.heappush(buy_heap, (buy_price, buy_qty, buy_tp))
                        heapq.heappush(sell_heap, (price, qty, tp))
                        break
                else:
                    heapq.heappush(sell_heap, (price, qty, tp))
                    break
        
    backlog = sum(qty for p,qty,t in sell_heap) + sum(qty for p,qty,t in buy_heap)
    print(buy_heap)
    print(sell_heap)
    return backlog % (10**9 + 7)

tests = [
    # 1. Provided sample
    ([(10, 5, 0),
      (15, 2, 1),
      (25, 1, 1),
      (30, 4, 0),
      (12, 1, 1),
      (40, 10, 0)], 15),

    # 2. All orders on one side only (no matches ever)
    ([(5, 3, 0), (6, 2, 0), (7, 1, 0)], 6),   # only buys
    ([(5, 3, 1), (6, 2, 1), (7, 1, 1)], 6),   # only sells

    # 3. Exact match, backlog zero
    ([(5, 5, 0), (3, 5, 1)], 0),  # buy 5@5, sell 5@3 → all consumed
    ([(3, 5, 1), (5, 5, 0)], 0),  # reversed order

    # 4. Partial match leaves residual
    ([(5, 10, 0), (4, 3, 1)], 7),  # leftover buy
    ([(3, 3, 0), (2, 10, 1)], 7),  # leftover sell

    # 5. No match due to price
    ([(5, 5, 0), (6, 5, 1)], 10),  # buy too low
    ([(6, 5, 1), (5, 5, 0)], 10),  # sell too high

    # 6. Multiple orders stacking
    ([(5, 5, 0), (5, 5, 0), (4, 8, 1)], 2),  # leftover buy
    ([(2, 4, 1), (3, 2, 1), (5, 10, 0)], 4), # chain of matches, leftover buy=4

    # 7. No orders at all
    ([], 0),

    # 8. Big sweep (one order clearing many)
    ([(2, 5, 1), (3, 5, 1), (4, 5, 1), (10, 20, 0)], 5),
    # buy 20@10 matches 15 sells, leftover buy=5 → backlog=5
]

for idx, (input, output) in enumerate(tests):
    a = process_orders(input)
    if a == output:
        print(f'Passed test {idx + 1}.')
    else:
        print(f'Failed test {idx + 1}.')
        print(a)
        print(output)