"""
Number to Words Converter
Converts numeric monetary amounts into professional English words.
Supports South Asian (Lakhs / Crores) as seen in the reference invoice ("One Lac Fifty One Thousand Five Hundred")
as well as standard Western International format (Millions / Billions).
"""
from decimal import Decimal, ROUND_HALF_UP

ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen"]

TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def _two_digits(n: int) -> str:
    if n == 0:
        return ""
    if n < 20:
        return ONES[n]
    tens_digit = n // 10
    ones_digit = n % 10
    if ones_digit:
        return f"{TENS[tens_digit]} {ONES[ones_digit]}"
    return TENS[tens_digit]


def _three_digits(n: int) -> str:
    hundreds = n // 100
    remainder = n % 100
    parts = []
    if hundreds:
        parts.append(f"{ONES[hundreds]} Hundred")
    if remainder:
        parts.append(_two_digits(remainder))
    return " ".join(parts)


def convert_south_asian(number: int, use_lac_spelling: bool = True) -> str:
    """
    Converts an integer to South Asian numbering format (Crore, Lac/Lakh, Thousand, Hundred).
    Example: 151500 -> "One Lac Fifty One Thousand Five Hundred"
    """
    if number == 0:
        return "Zero"

    lac_word = "Lac" if use_lac_spelling else "Lakh"
    parts = []

    crores = number // 10000000
    number %= 10000000

    lacs = number // 100000
    number %= 100000

    thousands = number // 1000
    number %= 1000

    hundreds = number // 100
    remainder = number % 100

    if crores:
        parts.append(f"{convert_south_asian(crores, use_lac_spelling)} Crore")
    if lacs:
        parts.append(f"{_two_digits(lacs)} {lac_word}")
    if thousands:
        parts.append(f"{_two_digits(thousands)} Thousand")
    if hundreds:
        parts.append(f"{ONES[hundreds]} Hundred")
    if remainder:
        parts.append(_two_digits(remainder))

    return " ".join(filter(None, parts))


def convert_western(number: int) -> str:
    """
    Converts an integer to Western numbering format (Billion, Million, Thousand, Hundred).
    """
    if number == 0:
        return "Zero"

    parts = []
    billions = number // 1000000000
    number %= 1000000000

    millions = number // 1000000
    number %= 1000000

    thousands = number // 1000
    number %= 1000

    if billions:
        parts.append(f"{_three_digits(billions)} Billion")
    if millions:
        parts.append(f"{_three_digits(millions)} Million")
    if thousands:
        parts.append(f"{_three_digits(thousands)} Thousand")
    if number:
        parts.append(_three_digits(number))

    return " ".join(filter(None, parts))


def amount_to_words(amount, currency_name: str = "", system: str = "south_asian", suffix: str = "") -> str:
    """
    Converts a numeric or Decimal amount to words.
    
    Args:
        amount: float, int, str, or Decimal.
        currency_name: e.g. "Rupees", "USD", "Dollars" or ""
        system: "south_asian" (Crore/Lac) or "western" (Million/Billion)
        suffix: e.g. "Only"
    
    Returns:
        String in words matching reference invoice format.
    """
    if amount is None:
        return ""
    
    try:
        dec = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception:
        return str(amount)

    integer_part = int(abs(dec))
    fraction_part = int((abs(dec) - integer_part) * 100)

    if system == "south_asian":
        words = convert_south_asian(integer_part)
    else:
        words = convert_western(integer_part)

    result_parts = []
    if currency_name:
        result_parts.append(currency_name)
    
    result_parts.append(words)

    if fraction_part > 0:
        sub_words = _two_digits(fraction_part)
        result_parts.append(f"and {sub_words} Paisa" if "Rupee" in currency_name or not currency_name else f"and {sub_words} Cents")

    if suffix:
        result_parts.append(suffix)

    # Clean double spaces
    return " ".join(" ".join(result_parts).split())
