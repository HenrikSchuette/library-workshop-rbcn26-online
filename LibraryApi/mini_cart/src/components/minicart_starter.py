"""
Contains a set of simple keyword implementations.
"""

def _ensure_valid_price(value):
    """
    Validate and normalize a price-like value to a non-negative
    float.

    Accepts ints, floats, and numeric strings. Raises ValueError for
    negative values or values that cannot be converted to float.
    """
    try:
        price = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid price: {value!r}") from exc
    if price < 0:
        raise ValueError(f"Price cannot be negative: {value!r}")
    return price


def add_line_item(price: float, quantity: int) -> float:
    """
    Calculate a single line item's total: price * quantity.
    """
    unit_price = _ensure_valid_price(price)
    qty = int(quantity)
    if qty < 0:
        raise ValueError(f"Quantity cannot be negative: {quantity!r}")
    return unit_price * qty


def sum_line_items(*line_totals):
    """
    Sum one or more line totals into a cart subtotal.
    """
    subtotal = 0.0
    for t in line_totals:
        subtotal += _ensure_valid_price(t)
    return subtotal


def apply_discount(subtotal, percent):
    """
    Apply a percentage discount to a subtotal.
    """
    base = _ensure_valid_price(subtotal)
    pct = float(percent)
    if pct < 0 or pct > 100:
        raise ValueError(
            f"Discount percent must be between 0 and 100: {percent!r}"
        )
    return base * (1.0 - (pct / 100.0))


def total_with_tax(total, tax_rate):
    """
    Apply a tax rate (percentage) to a total and return the new total.
    """
    base = _ensure_valid_price(total)
    rate = float(tax_rate)
    if rate < 0:
        raise ValueError(f"Tax rate cannot be negative: {tax_rate!r}")
    return base * (1.0 + (rate / 100.0))
