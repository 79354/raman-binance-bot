from typing import Literal, Tuple

def validate_side(side: str) -> str:
    """Validates and normalizes order side."""
    upper_side = side.upper()
    if upper_side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
    return upper_side

def validate_positive_float(value: float, name: str) -> float:
    """Ensures a numerical value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0. Received: {value}")
    return value

def validate_symbol(symbol: str) -> str:
    """Basic symbol validation."""
    if not symbol.isalnum():
        raise ValueError(f"Invalid symbol format: {symbol}")
    return symbol.upper()

def get_symbol_precision(client, symbol: str) -> Tuple[int, int]:
    """
    Fetches price and quantity precision from exchange info.
    
    Args:
        client: Binance futures client instance
        symbol: Trading pair (e.g., BTCUSDT)
    
    Returns:
        Tuple[int, int]: (price_precision, quantity_precision)
    
    Raises:
        ValueError: If symbol not found in exchange info
    """
    try:
        exchange_info = client.exchange_info()
        
        for sym_info in exchange_info['symbols']:
            if sym_info['symbol'] == symbol:
                price_precision = sym_info['pricePrecision']
                quantity_precision = sym_info['quantityPrecision']
                return (price_precision, quantity_precision)
        
        # If symbol not found
        raise ValueError(f"Symbol {symbol} not found in exchange info")
    
    except Exception as e:
        # Fallback to default precisions if API call fails
        # BTCUSDT typical: price=2, qty=3
        print(f"Warning: Could not fetch precision for {symbol}, using defaults: {e}")
        return (2, 3)  # Conservative defaults