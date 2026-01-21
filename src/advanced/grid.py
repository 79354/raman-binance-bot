import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import get_client, setup_logger
from utils.validation import validate_symbol, validate_positive_float, get_symbol_precision
from binance.error import ClientError

logger = setup_logger("grid_strategy")

def place_grid_orders(symbol: str, lower_price: float, upper_price: float, grid_levels: int, qty_per_grid: float):
    """
    Places a neutral grid of LIMIT orders.
    Buys below current price, Sells above current price.
    """
    try:
        client = get_client()
        symbol = validate_symbol(symbol)
        
        # Get symbol precision from exchange
        price_precision, qty_precision = get_symbol_precision(client, symbol)
        
        # Get current price
        ticker = client.ticker_price(symbol=symbol)
        current_price = float(ticker['price'])
        
        logger.info(f"Current Price: {current_price}. Grid Range: {lower_price} - {upper_price}")
        logger.info(f"Using precision: Price={price_precision}, Quantity={qty_precision}")
        
        price_step = (upper_price - lower_price) / grid_levels
        
        orders_placed = 0

        for i in range(grid_levels + 1):
            level_price = lower_price + (i * price_step)
            level_price = round(level_price, price_precision)
            
            if abs(level_price - current_price) < (price_step * 0.1):
                logger.info(f"Skipping level {i+1} @ {level_price} (too close to current price)")
                continue
                
            side = "BUY" if level_price < current_price else "SELL"
            
            try:
                logger.info(f"Placing Grid Level {i+1}: {side} {qty_per_grid} @ {level_price}")
                client.new_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=qty_per_grid,
                    price=level_price
                )
                orders_placed += 1
            except ClientError as e:
                logger.error(f"Failed to place level {level_price}: {e.error_message}")

        logger.info(f"Grid Setup Complete. Total Orders Placed: {orders_placed}")

    except Exception as e:
        logger.error(f"Grid Strategy Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place Static Grid Orders")
    parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("lower_price", type=float, help="Lower bound of grid")
    parser.add_argument("upper_price", type=float, help="Upper bound of grid")
    parser.add_argument("levels", type=int, help="Number of grid levels")
    parser.add_argument("qty_per_grid", type=float, help="Quantity per grid level")
    
    args = parser.parse_args()
    place_grid_orders(args.symbol, args.lower_price, args.upper_price, args.levels, args.qty_per_grid)