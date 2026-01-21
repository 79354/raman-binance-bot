import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import get_client, setup_logger
from utils.validation import validate_side, validate_positive_float, validate_symbol
from binance.error import ClientError

logger = setup_logger("limit_order")

def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Executes a Limit Order.
    """
    try:
        client = get_client()
        
        # Validation
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_positive_float(quantity, "Quantity")
        price = validate_positive_float(price, "Price")

        logger.info(f"Initiating LIMIT {side} order for {quantity} {symbol} @ {price}")

        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC", # Good Till Cancel
            quantity=quantity,
            price=price
        )
        
        logger.info(f"Order Placed: ID {response['orderId']} | Status: {response['status']}")
        logger.debug(f"Full API Response: {response}")
        return response

    except ClientError as error:
        logger.error(f"Binance API Error: {error.error_code} - {error.error_message}")
    except Exception as e:
        logger.error(f"System Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a Limit Order on Binance Futures")
    parser.add_argument("symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order Quantity")
    parser.add_argument("price", type=float, help="Limit Price")

    args = parser.parse_args()
    place_limit_order(args.symbol, args.side, args.quantity, args.price)