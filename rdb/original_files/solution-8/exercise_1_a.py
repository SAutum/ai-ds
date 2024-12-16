def get_query() -> str:

    query = """
    SELECT A, B, C, D, E, F, G FROM mytable GROUP BY

        This is just a placeholder.

    """

    # BEGIN_SOLUTION

    query = """
    SELECT A, B, C, D, E, F, G FROM mytable GROUP BY
        GROUPING SETS ((E), (G)),
        CUBE(B, F),
        ROLLUP(D, C, A)
    """

    # Explanation

    """
    1. Write down tuples

    (A,B,C,D,E),
    (A,B,C,D,E,F),
    (A,B,C,D,F,G),
    (A,B,C,D,G),
    (A,C,D,E),
    (A,C,D,E,F),
    (A,C,D,F,G),
    (A,C,D,G),
    (B,C,D,E),
    (B,C,D,E,F),
    (B,C,D,F,G),
    (B,C,D,G),
    (B,D,E),
    (B,D,E,F),
    (B,D,F,G),
    (B,D,G),
    (B,E),
    (B,E,F),
    (B,F,G),
    (B,G),
    (C,D,E),
    (C,D,E,F),
    (C,D,F,G),
    (C,D,G),
    (D,E),
    (D,E,F),
    (D,F,G),
    (D,G),
    (E),
    (E,F),
    (F,G),
    (G)

    2. Expand missing attributes which makes seeing patterns easier
    3. Realize that there are 8 groups of size 4 which only differ in
       E, EF, FG, G, giving us GROUPING SETS ((E), (E, F), (F, G), (G)).
       We could arrive at the solution with fewer steps with different
       grouping sets, but they are more difficult to see.

    (A,B,C,D,E,_,_) <-- E
    (A,B,C,D,E,F,_) <-- EF
    (A,B,C,D,_,F,G) <--  FG
    (A,B,C,D,_,_,G) <--   G

    (A,_,C,D,E,_,_) <-- E
    (A,_,C,D,E,F,_) <-- EF
    (A,_,C,D,_,F,G) <--  FG
    (A,_,C,D,_,_,G) <--   G

    (_,B,C,D,E,_,_) <-- E
    (_,B,C,D,E,F,_) <-- EF
    (_,B,C,D,_,F,G) <--  FG
    (_,B,C,D,_,_,G) <--   G

    (_,B,_,D,E,_,_) <-- E
    (_,B,_,D,E,F,_) <-- EF
    (_,B,_,D,_,F,G) <--  FG
    (_,B,_,D,_,_,G) <--   G

    (_,B,_,_,E,_,_) <-- E
    (_,B,_,_,E,F,_) <-- EF
    (_,B,_,_,_,F,G) <--  FG
    (_,B,_,_,_,_,G) <--   G

    (_,_,C,D,E,_,_) <-- E
    (_,_,C,D,E,F,_) <-- EF
    (_,_,C,D,_,F,G) <--  FG
    (_,_,C,D,_,_,G) <--   G

    (_,_,_,D,E,_,_) <-- E
    (_,_,_,D,E,F,_) <-- EF
    (_,_,_,D,_,F,G) <--  FG
    (_,_,_,D,_,_,G) <--   G

    (_,_,_,_,E,_,_) <-- E
    (_,_,_,_,E,F,_) <-- EF
    (_,_,_,_,_,F,G) <--  FG
    (_,_,_,_,_,_,G) <--   G

    4. We only keep the part which is identical among the 4-blocks. The result
       can again be split into two groups of size 4, one with B and one without,
       giving us GROUPING SETS ((B), ()), which is equivalent to CUBE(B).

    (A,B,C,D)
    (_,B,C,D)
    (_,B,_,D)
    (_,B,_,_)

    (A,_,C,D)
    (_,_,C,D)
    (_,_,_,D)
    (_,_,_,_)

    5. The rest is just ROLLUP(D, C, A)

    (A,C,D)
    (_,C,D)
    (_,_,D)
    (_,_,_)

    6. This would already give us a solution, which is

       SELECT A, B, C, D, E, F, G FROM mytable GROUP BY
           GROUPING SETS ((E), (E, F), (F, G), (G)),
           CUBE(B),
           ROLLUP(D, C, A)

       But it is possible to derive an even shorter query. We can combine
           GROUPING SETS ((E), (E, F), (F, G), (G))
       and
           GROUPING SETS ((B), ())
       into
           GROUPING SETS ((E), (E, F), (F, G), (G), (B, E), (B, E, F), (B, F, G), (B, G))
       then reorder it like
           GROUPING SETS (
               (E),
               (G),

               (E, F),
               (F, G),

               (B, E),
               (B, G)

               (B, E, F),
               (B, F, G),
            )
        which is the same as
            GROUPING SETS ((E), (G)),
            GROUPING SETS ((), (F), (B), (F, B))
        which is the same as
            GROUPING SETS ((E), (G)),
            CUBE(B, F)

    Together with ROLLUP(D, C, A) from step 4 we get

    SELECT A, B, C, D, E, F, G FROM mytable GROUP BY
        GROUPING SETS ((E), (G)),
        CUBE(B, F),
        ROLLUP(D, C, A)

    """

    # END_SOLUTION

    return query
