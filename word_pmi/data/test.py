def calculate_series(N):
    """
    Calculate the alternating series 1 - 3 + 5 - 7 +9 ... up to N.
    N: positive integer
    Returns the calculated result.
    """
    result = 0
    sign = 1  # Start with a positive sign

    for i in range(1, N + 1, 2):  # Iterate over odd numbers up to N
        result += sign * i
        sign *= -1  # Alternate the sign

    return result


# Test the function with an example input
N = 9
print(calculate_series(N))
