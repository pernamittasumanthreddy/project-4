from decimal import Decimal, ROUND_HALF_UP

CURRENCY_QUANTIZE = Decimal('0.01')
FOUR_DECIMALS_QUANTIZE = Decimal('0.0001')

def to_decimal(val) -> Decimal:
    """Safely converts numeric or string input to Decimal without floating-point inaccuracies."""
    if val is None or val == '':
        return Decimal('0.00')
    if isinstance(val, Decimal):
        return val
    # Convert float via string representation to avoid 0.1000000000000000055511...
    return Decimal(str(val))

def quantize_currency(val) -> Decimal:
    """Rounds an amount to two decimal places using standard ROUND_HALF_UP."""
    d = to_decimal(val)
    return d.quantize(CURRENCY_QUANTIZE, rounding=ROUND_HALF_UP)

def calculate_tax(base_amount, rate_percentage) -> Decimal:
    """Computes tax amount from base amount and rate percentage."""
    b = to_decimal(base_amount)
    r = to_decimal(rate_percentage)
    tax = (b * r) / Decimal('100.00')
    return quantize_currency(tax)
