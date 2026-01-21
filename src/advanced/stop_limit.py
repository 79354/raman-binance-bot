import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import get_client, setup_logger
from utils.validation import validate_side, validate_positive_float, validate_symbol
from binance.error import ClientError

logger = setup_logger("stop_limit")

def place_stop_limit(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    """
    Executes a Stop-Limit Order.
    """
    try:
        client = get_client()
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_positive_float(quantity, "Quantity")
        stop_price = validate_positive_float(stop_price, "Stop Price")
        limit_price = validate_positive_float(limit_price, "Limit Price")

        logger.info(f"Placing STOP-LIMIT: Trigger @ {stop_price}, Limit @ {limit_price}")

        response = client.new_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price,
            timeInForce="GTC"
        )
        
        logger.info(f"Stop-Limit Registered: ID {response['orderId']}")
        return response

    except ClientError as error:
        logger.error(f"API Error: {error.error_message}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a Stop-Limit Order")
    parser.add_argument("symbol", type=str)
    parser.add_argument("side", type=str)
    parser.add_argument("quantity", type=float)
    parser.add_argument("stop_price", type=float)
    parser.add_argument("limit_price", type=float)
    
    args = parser.parse_args()
    place_stop_limit(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price)