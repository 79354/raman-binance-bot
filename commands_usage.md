Markdown
# 📘 CLI Trader Command Usage Guide

This guide covers real-world trading scenarios tested on the Binance Testnet. Use these commands to execute specific strategies.

**Note:** For scripts located in the `src/advanced/` folder, we prepend `PYTHONPATH=src` to ensure the tool can find the necessary utility modules.

---

## 1. The "Buy the Dip" Order (Limit Buy)
**Goal:** You think the price is too high right now (e.g., $90,100). You want to buy only if it drops to **$89,500**.

**What to look for:** After running this, look at the **"Open Orders"** tab on your screen. It will sit there waiting for the price to drop.

```bash
uv run python src/limit_orders.py BTCUSDT BUY 0.002 89500
2. The "Take Profit" Order (Limit Sell)
Goal: Imagine you already bought some Bitcoin. You want to sell it automatically if the price jumps up to $90,800 to secure a profit.

What to look for: This will also appear in "Open Orders" with a "Sell" side.

Bash
uv run python src/limit_orders.py BTCUSDT SELL 0.002 90800
3. The "Safety Net" (Stop-Limit)
Goal: You want to protect yourself. If the price crashes below the 24h low ($87,900), you want to sell immediately to stop losing money.

Stop Price ($87,900): The trigger. "If price touches this..."

Limit Price ($87,800): The execution. "...sell my coins at this price."

Bash
PYTHONPATH=src uv run python src/advanced/stop_limit.py BTCUSDT SELL 0.002 87900 87800
4. The "Market Noise" Catcher (Grid Trading)
Goal: The price is bouncing between $89,000 and $91,000. You want to place automatic buy/sell orders across this range to profit from the wiggles.

Range: $89,500 to $90,500

Levels: 5 (It will create 5 orders spaced out)

Bash
PYTHONPATH=src uv run python src/advanced/grid.py BTCUSDT 89500 90500 5 0.002
5. Bonus: OCO (One-Cancels-the-Other)
Goal: You have an open position and want to set a Take Profit and Stop Loss simultaneously.

Take Profit: $89,840 (Profit target)

Stop Loss: $89,740 (Safety stop)

Bash
PYTHONPATH=src uv run python src/advanced/oco.py BTCUSDT 0.005 89840 89740