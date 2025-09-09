import math

def has_arb(input:list):
    #unpack
    n, m = input[0]
    all_edges = input[1:]
    #init dist vector
    d = [0.0] * (n + 1)
    #loop through combinations
    for i in range(0, n):
        update = False
        for u,v,r in all_edges:
            d[v] = d[u] + -math.log(r)
            update = True
        if not update:
            break
    #check for negative combination (arb)
    for u,v,r in all_edges:
        if d[u] + -math.log(r) < d[v]:
            print('YES')
            return 'YES'

    print('NO')
    return 'NO'

tests = [
    # Test 1: Sample (arbitrage exists)
    ([(3, 3),
      (1, 2, 0.9),
      (2, 3, 120),
      (3, 1, 0.0093)], "YES"),

    # Test 2: Graph with no cycle
    ([(2, 1),
      (1, 2, 5.0)], "NO"),

    # Test 3: Cycle with product = 1 (boundary case)
    ([(2, 2),
      (1, 2, 2.0),
      (2, 1, 0.5)], "NO"),

    # Test 4: Multiple components; arbitrage in non-1 component
    ([(4, 4),
      (1, 2, 2.0),
      (2, 1, 0.5),
      (3, 4, 0.8),
      (4, 3, 1.3)], "YES"),

    # Test 5: Very small and very large rates (numeric stability)
    ([(3, 3),
      (1, 2, 1e-6),
      (2, 3, 1e6),
      (3, 1, 1.0000001)], "YES"),

    # Test 6: Larger no-arbitrage cycle
    ([(3, 3),
      (1, 2, 0.5),
      (2, 3, 0.5),
      (3, 1, 3.0)], "NO"),
]

for i, test in enumerate(tests):
    case = test[0]
    answer = test[1]
    print(case)
    print(answer)
    output = has_arb(case)
    if answer == output:
        print(f'Passed {i}')
    else:
        print(f'Failed {i}')
        print(answer)
        print(output)

