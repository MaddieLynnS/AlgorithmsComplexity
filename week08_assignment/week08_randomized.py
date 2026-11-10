from random import Random

def freivalds_check( 
    A: list[list[int]], 
    B: list[list[int]], 
    C: list[list[int]], 
    repetitions: int = 1,
    rng: Random | None = None
) -> bool:
    """Returns whether C is probably equal to A times B over GF(2).""" 
    """Return False immediately when a repetition finds unequal vectors."""
    """Return True only when every repetition agrees."""

    # Raise error if stuff is bad
    if not A or not B or not C:
        raise ValueError("Input matrices cannot be empty.")
    if len(A) != len(B) or len(B) != len(C):
        raise ValueError("Input matrices must have the same dimensions.")
    if len(A[0]) != len(A):
        raise ValueError("Input matrices must be square.")
    if len(B[0]) != len(B):
        raise ValueError("Input matrices must be square.")
    if len(C[0]) != len(C):
        raise ValueError("Input matrices must be square.")
    if any(i not in (0, 1) for row in A for i in row) or \
       any(i not in (0, 1) for row in B for i in row) or \
       any(i not in (0, 1) for row in C for i in row):
        raise ValueError("Input matrices must contain only 0s and 1s.")
    if repetitions <= 0:
        raise ValueError("Number of repetitions must be positive.")

    for i in range(repetitions):
        #Generate random vector w same length as matrix dimensions
        if rng is None:
            rng = Random()
        r = []
        for i in range(len(A)):
            r.append(rng.randint(0, 1))

        # Compute A * B * r and C * r
        # B*r first
        Br = []
        for i in range(len(B)):
            row_total = 0
            for j in range(len(r)):
                row_total += (B[i][j] * r[j])
            Br.append(row_total % 2)

        # A*(Br)
        ABr = []
        for i in range(len(A)):
            row_total = 0
            for j in range(len(Br)):
                row_total += (A[i][j] * Br[j])
            ABr.append(row_total % 2)

        # C*r
        Cr = []
        for i in range(len(C)):
            row_total = 0
            for j in range(len(r)):
                row_total += (C[i][j] * r[j])
            Cr.append(row_total % 2)

        if ABr != Cr:
            return False

    # return true if we made it through the repetitions without finding any
    # discrepancies between AB and C
    return True