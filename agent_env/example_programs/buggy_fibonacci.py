def fibonacci(n):
    """
    A buggy implementation of the Fibonacci sequence.
    The bug is that the base case is incorrectly defined,
    leading to negative index errors for certain inputs.
    """
    # Bug: Base case should handle n <= 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # This will cause an error for n <= 0
        return fibonacci(n - 1) + fibonacci(n - 2)

def print_fibonacci_sequence(n):
    """Print the Fibonacci sequence up to the nth term."""
    sequence = []
    for i in range(n):
        sequence.append(fibonacci(i))
    return sequence

if __name__ == "__main__":
    try:
        # This will work
        print("Fibonacci sequence up to 5th term:", print_fibonacci_sequence(5))
        
        # This will cause an error
        print("Fibonacci sequence for -1:", fibonacci(-1))
    except Exception as e:
        print(f"Error occurred: {e}")