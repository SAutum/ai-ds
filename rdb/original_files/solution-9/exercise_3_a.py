def get_keys() -> list[int]:
    # BEGIN_SOLUTION
    return [
        int(x)
        for x in """
50
25
75
100
200
300
400
500
350
250
150
125
120
80
60
30
40
10
""".strip().split()
    ]
    # END_SOLUTION
