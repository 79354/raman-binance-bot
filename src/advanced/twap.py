import argparse
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import get_client, setup_logger
from utils.validation import validate_side, validate_positive_float, validate_symbol, get_symbol_precision
from binance.error import ClientError

logger = setup_logger("twap_algo")

def execute_twap(symbol: str, side: str, total_quantity: float, duration_minutes: int, chunks: int):
    """
    Executes a Time-Weighted Average Price (TWAP) strategy.
    Splits a large order into smaller market orders executed at regular intervals.
    """
    try:
        client = get_client()
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        
        if chunks <= 0: 
            raise ValueError("Chunks must be > 0")
        
        # Get symbol precision from exchange
        price_precision, qty_precision = get_symbol_precision(client, symbol)
        
        chunk_size = round(total_quantity / chunks, qty_precision)
        interval_seconds = (duration_minutes * 60) / chunks

        logger.info(f"Starting TWAP: {total_quantity} {symbol} over {duration_minutes}m in {chunks} chunks.")
        logger.info(f"Execution Plan: {chunk_size} {symbol} every {interval_seconds:.1f} seconds.")
        logger.info(f"Using quantity precision: {qty_precision} decimals")

        executed_qty = 0.0

        for i in range(chunks):
            # For the last chunk, use remaining quantity to handle rounding
            if i == chunks - 1:
                chunk_size = round(total_quantity - executed_qty, qty_precision)

            logger.info(f"Executing Chunk {i+1}/{chunks}: {chunk_size} {symbol}")
            
            # Execute Market Order for chunk
            try:
                response = client.new_order(
                    symbol=symbol, 
                    side=side, 
                    type="MARKET", 
                    quantity=chunk_size
                )
                executed_qty += chunk_size
                logger.info(f"Chunk {i+1} filled. Order ID: {response['orderId']}")
            except ClientError as e:
                logger.error(f"Chunk {i+1} failed: {e.error_message}")
                # Continue with remaining chunks
            
            if i < chunks - 1:
                logger.info(f"Sleeping for {interval_seconds:.1f}s...")
                time.sleep(interval_seconds)
        
        logger.info(f"TWAP Strategy Completed. Total executed: {executed_qty}/{total_quantity}")

    except ClientError as error:
        logger.error(f"API Error: {error.error_message}")
    except KeyboardInterrupt:
        logger.warning("TWAP Interrupted by User.")
        logger.info(f"Partial execution: {executed_qty}/{total_quantity}")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute TWAP Strategy")
    parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, help="BUY or SELL")
    parser.add_argument("total_qty", type=float, help="Total quantity to execute")
    parser.add_argument("duration_min", type=int, help="Total duration in minutes")
    parser.add_argument("chunks", type=int, help="Number of split orders")
    
    args = parser.parse_args()
    execute_twap(args.symbol, args.side, args.total_qty, args.duration_min, args.chunks)