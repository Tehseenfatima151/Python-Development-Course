def calculate_bmi(weight, height):
    """
    Calculates the Body Mass Index (BMI).

    Parameters:
    weight (float): Weight in kilograms
    height (float): Height in meters

    Returns:
    float: The calculated BMI rounded to 2 decimal places
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)
print(calculate_bmi(70, 1.75))  # Example usage