def calculate_payments(amount, int_rate, duration):
    """
    Calculates the monthly payments for a given loan amount, interest
    rate and duration

    Args:
        amount (float): amount of the loan
        int_rate (float): interest rate for the loan
        duration (int): duration of the loan in months

    Returns:
        float: monthly payment
    """
    #Compute monthly interest rate
    int_rate /= 1200
    
    r1 = int_rate * (1 + int_rate)**duration
    r2 = (1+int_rate)**duration - 1
    r3 = r1 / r2

    return round(amount * r3,2)


def calculate_total_paid(amount, int_rate, duration):
    """
    Calculates the total amount paid for the loan

    Args:
        amount (float): amount of the loan
        int_rate (float): interest rate for the loan
        duration (int): duration of the loan in months

    Returns:
        float: total amount paid for the loan
    """
    return calculate_payments(amount, int_rate, duration) * duration


def calculate_total_interest(amount, int_rate, duration):
    """
    Calculates the total amount of interest paid on the loan

    Args:
        amount (float): amount of the loan
        int_rate (float): interest rate for the loan
        duration (int): duration of the loan in months

    Returns:
        float: total amount of interest paid on the loan
    """
    return calculate_payments(amount, int_rate, duration)*duration - amount
