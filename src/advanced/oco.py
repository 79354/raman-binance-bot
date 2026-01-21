import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import get_client, setup_logger
from utils.validation import validate_positive_float, validate_symbol
from binance.error import ClientError

logger = setup_logger("oco_order")

def place_oco_strategy(symbol: str, quantity: float, take_profit_price: float, stop_loss_price: float, side: str = "SELL"):
    """
    Simulates an OCO (One-Cancels-the-Other) strategy for an open position.
    
    In Futures, this is achieved by placing two orders with 'reduceOnly=True':
    1. A Limit Order (Take Profit)
    2. A Stop Market/Limit Order (Stop Loss)
    
    Note: In a true production engine, you would need a websocket listener to cancel 
    the other order if one fills. This script places the initial structure.
    """
    try:
        client = get_client()
        symbol = validate_symbol(symbol)
        quantity = validate_positive_float(quantity, "Quantity")
        
        logger.info(f"Setting up OCO bracket for {symbol} | Qty: {quantity}")

        # 1. Place Take Profit (Limit Order)
        logger.info(f"Placing Take Profit Limit @ {take_profit_price}")
        tp_response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=take_profit_price,
            timeInForce="GTC",
            reduceOnly="true"
        )

        # 2. Place Stop Loss (Stop Market)
        logger.info(f"Placing Stop Loss Market @ {stop_loss_price}")
        sl_response = client.new_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            quantity=quantity,
            stopPrice=stop_loss_price,
            reduceOnly="true"
        )
        
        logger.info(f"OCO Bracket Placed Successfully.")
        logger.info(f"TP Order ID: {tp_response['orderId']} | SL Order ID: {sl_response['orderId']}")

    except ClientError as error:
        logger.error(f"API Error during OCO setup: {error.error_message}")
        logger.error("Critial: Check open orders. One leg might have executed while the other failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place OCO Bracket (TP and SL) for an existing position")
    parser.add_argument("symbol", type=str)
    parser.add_argument("quantity", type=float)
    parser.add_argument("tp_price", type=float, help="Take Profit Price")
    parser.add_argument("sl_price", type=float, help="Stop Loss Trigger Price")
    parser.add_argument("--side", type=str, default="SELL", help="Direction to close (default SELL for long close)")
    
    args = parser.parse_args()
    place_oco_strategy(args.symbol, args.quantity, args.tp_price, args.sl_price, args.side)