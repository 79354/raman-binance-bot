import argparse
import sys
import os

# Adjust path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import get_client, setup_logger
from utils.validation import validate_side, validate_positive_float, validate_symbol
from binance.error import ClientError

logger = setup_logger("market_order")

def place_market_order(symbol: str, side: str, quantity: float):
    """
    Executes a Market Order.
    """
    try:
        client = get_client()
        
        # Validation
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_positive_float(quantity, "Quantity")

        logger.info(f"Initiating MARKET {side} order for {quantity} {symbol}")

        response = client.new_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        
        logger.info(f"Order Success: ID {response['orderId']} | AvgPrice: {response.get('avgPrice', 'N/A')}")
        logger.debug(f"Full API Response: {response}")
        return response

    except ClientError as error:
        logger.error(f"Binance API Error: {error.error_code} - {error.error_message}")
    except Exception as e:
        logger.error(f"System Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a Market Order on Binance Futures")
    parser.add_argument("symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order Quantity")

    args = parser.parse_args()
    place_market_order(args.symbol, args.side, args.quantity)