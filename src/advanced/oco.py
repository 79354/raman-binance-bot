import time
import sys
import os
import logging
import json
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import get_client, setup_logger, API_KEY
from utils.validation import validate_positive_float, validate_symbol
from binance.error import ClientError
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

logger = setup_logger("oco_ws_manager")

class OCOManager:
    def __init__(self, symbol, quantity, tp_price, sl_price, side="SELL"):
        self.client = get_client()
        self.symbol = validate_symbol(symbol)
        self.quantity = validate_positive_float(quantity, "Quantity")
        self.tp_price = validate_positive_float(tp_price, "Take Profit")
        self.sl_price = validate_positive_float(sl_price, "Stop Loss")
        self.side = side

        self.tp_order_id = None
        self.sl_order_id = None
        self.is_done = False
        self.listen_key = None
        self.ws_client = None

    def start(self):
        try:
            self._start_user_stream()
            self._place_orders()

            logger.info("Monitoring orders via WebSocket. Press Ctrl+C to stop manually.")
            while not self.is_done:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.warning("Manual interruption. Cancelling open orders...")
            self._cancel_all()
        except Exception as e:
            logger.error(f"Critical Error: {e}")
            self._cancel_all()
        finally:
            self._cleanup()

    def _start_user_stream(self):
        logger.info("Connecting to Binance WebSocket...")

        self.listen_key = self.client.new_listen_key()['listenKey']
        logger.info(f"Listen Key retrieved: {self.listen_key[:10]}...")

        self.ws_client = UMFuturesWebsocketClient(on_message=self._on_ws_message)

        is_testnet = os.getenv("USE_TESTNET", "False").lower() == "true"
        ws_url = "wss://stream.binancefuture.com" if is_testnet else "wss://fstream.binance.com"

        self.ws_client.user_data(
            listen_key=self.listen_key,
            id=1
        )
        logger.info("WebSocket connection started.")

    def _place_orders(self):
        logger.info(f"Placing OCO Orders for {self.quantity} {self.symbol}...")

        tp_order = self.client.new_order(
            symbol=self.symbol,
            side=self.side,
            type="LIMIT",
            quantity=self.quantity,
            price=self.tp_price,
            timeInForce="GTC",
            reduceOnly="true"
        )
        self.tp_order_id = tp_order['orderId']
        logger.info(f"TP Placed: ID {self.tp_order_id} @ {self.tp_price}")

        sl_order = self.client.new_order(
            symbol=self.symbol,
            side=self.side,
            type="STOP_MARKET",
            quantity=self.quantity,
            stopPrice=self.sl_price,
            reduceOnly="true"
        )
        self.sl_order_id = sl_order['orderId']
        logger.info(f"SL Placed: ID {self.sl_order_id} Trigger @ {self.sl_price}")

    def _on_ws_message(self, _, message):
        try:
            data = json.loads(message) if isinstance(message, str) else message

            if data.get('e') == 'ORDER_TRADE_UPDATE':
                order_data = data.get('o', {})
                order_id = order_data.get('i')
                status = order_data.get('X')

                if order_id in [self.tp_order_id, self.sl_order_id]:
                    logger.info(f"Update for Order {order_id}: {status}")

                    if status == 'FILLED':
                        logger.info(f"Order {order_id} FILLED. Cancelling sibling.")
                        self._handle_fill(filled_id=order_id)
        except Exception as e:
            logger.error(f"WS Parse Error: {e}")

    def _handle_fill(self, filled_id):
        try:
            target_to_cancel = self.sl_order_id if filled_id == self.tp_order_id else self.tp_order_id

            if target_to_cancel:
                logger.info(f"Cancelling Order ID {target_to_cancel}...")
                self.client.cancel_order(symbol=self.symbol, orderId=target_to_cancel)
                logger.info("Sibling cancelled. OCO complete.")

            self.is_done = True

        except ClientError as e:
            if -2011 not in [e.error_code]:
                logger.error(f"Cancel failed: {e}")
            self.is_done = True

    def _cancel_all(self):
        for oid in [self.tp_order_id, self.sl_order_id]:
            if oid:
                try:
                    self.client.cancel_order(symbol=self.symbol, orderId=oid)
                    logger.info(f"Cancelled {oid}")
                except:
                    pass

    def _cleanup(self):
        if self.ws_client:
            self.ws_client.stop()
        logger.info("Manager stopped.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-time WebSocket OCO Manager")
    parser.add_argument("symbol", type=str)
    parser.add_argument("quantity", type=float)
    parser.add_argument("tp_price", type=float)
    parser.add_argument("sl_price", type=float)
    parser.add_argument("--side", type=str, default="SELL")

    args = parser.parse_args()

    manager = OCOManager(
        args.symbol,
        args.quantity,
        args.tp_price,
        args.sl_price,
        args.side
    )
    manager.start()
