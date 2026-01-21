# Complete Testing & CLI Usage Guide

This document describes the setup, testing process, and practical CLI usage of the Binance Futures Trading Bot. It is intended to be used both as a testing manual and as reference material for demonstrations or reports.

---

## Step 1: Initial Setup (First Time Only)

### 1.1 Install Dependencies

This project uses `uv` for Python package management.

From the project root, run:

```bash
uv sync
```

This installs all dependencies defined in `pyproject.toml`.

---

### 1.2 Create a Binance Futures Testnet Account

**Purpose**  
The testnet provides a simulated trading environment with fake funds but real Binance APIs.

**Steps**

1. Visit the Binance Futures Testnet website.
2. Log in and click **Get Test Funds** to receive test USDT.
3. Go to **Profile → API Management**.
4. Create a new API key.
5. Copy the **API Key** and **Secret Key**.

---

### 1.3 Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following values:

```env
BINANCE_API_KEY=your_actual_api_key
BINANCE_SECRET_KEY=your_actual_secret_key
USE_TESTNET=True
```

---

## Step 2: Testing Each Order Type

All commands are executed using `uv run`.

For advanced strategies, `PYTHONPATH=src` is required so Python can locate shared utility modules.

---

### Test 1: Market Order

**Description**  
Executes immediately at the current market price.

**Command**

```bash
uv run python src/market_orders.py BTCUSDT BUY 0.002
```

**Note**  
Binance Testnet enforces a minimum notional value of 100 USDT.
Using `0.002 BTC` ensures this requirement is met.

---

### Test 2: Limit Order

**Description**  
Executes only when the market reaches the specified price.

**Command**

```bash
# Buy 0.002 BTC if price drops to 45,000
uv run python src/limit_orders.py BTCUSDT BUY 0.002 45000
```

**Verification**

* Check the **Open Orders** tab on the Binance Testnet website.

---

### Test 3: TWAP (Time-Weighted Average Price)

**Description**  
Splits a large order into smaller chunks executed over time.

**Command**

```bash
# Buy 0.01 BTC total, over 5 minutes, in 3 chunks
PYTHONPATH=src uv run python src/advanced/twap.py BTCUSDT BUY 0.01 5 3
```

---

### Test 4: Grid Trading

**Description**  
Places multiple buy and sell orders across a defined price range.

**Command**

```bash
# Grid between 89,500 and 90,500 with 5 levels
PYTHONPATH=src uv run python src/advanced/grid.py BTCUSDT 89500 90500 5 0.002
```

---

### Test 5: OCO (One-Cancels-the-Other)

**Description**  
Places a take-profit and stop-loss order simultaneously.
Requires an active open position.

**Command**

```bash
# Take profit at 89,840 and stop loss at 89,740
PYTHONPATH=src uv run python src/advanced/oco.py BTCUSDT 0.005 89840 89740
```

---

## Real-World Command Cheat Sheet

These scenarios are suitable for demonstrations and reports.

---

### 1. Buy the Dip (Limit Buy)

**Goal**  
Buy only if price drops to 89,500.

```bash
uv run python src/limit_orders.py BTCUSDT BUY 0.002 89500
```

**Expected Result**

* Order appears in **Open Orders**.

---

### 2. Take Profit (Limit Sell)

**Goal**  
Sell automatically if price reaches 90,800.

```bash
uv run python src/limit_orders.py BTCUSDT SELL 0.002 90800
```

---

### 3. Safety Net (Stop-Limit Order)

**Goal**  
Protect downside risk during a price crash.

```bash
PYTHONPATH=src uv run python src/advanced/stop_limit.py BTCUSDT SELL 0.002 87900 87800
```

* Trigger Price: 87,900
* Execution Price: 87,800

---

### 4. Market Noise Capture (Grid Strategy)

**Goal**  
Profit from small price fluctuations within a range.

```bash
PYTHONPATH=src uv run python src/advanced/grid.py BTCUSDT 89500 90500 5 0.002
```

---

### 5. Advanced OCO Management

**Goal**  
Simultaneously manage profit targets and downside risk.

```bash
PYTHONPATH=src uv run python src/advanced/oco.py BTCUSDT 0.005 89840 89740
```

---

## Monitoring and Debugging

### 1. Live Log Monitoring

Open a second terminal:

```bash
tail -f bot.log
```

This displays real-time execution and decision logs.

---

### 2. Binance Website Verification

* **Positions Tab**: View current BTC positions
* **Open Orders Tab**: View pending limit, grid, or OCO orders
* **Order History**: Verify executed market orders

---

### 3. Common Errors and Fixes

| Error Message                   | Cause                | Fix                                                |
| ------------------------------- | -------------------- | -------------------------------------------------- |
| Order Notional must be > 100    | Order size too small | Increase quantity (e.g., 0.002 BTC)                |
| ModuleNotFoundError: utils      | PYTHONPATH missing   | Use `PYTHONPATH=src`                               |
| Order would immediately trigger | Invalid stop price   | Ensure stop is on the correct side of market price |

---

## Conclusion

The system is now fully tested and ready for controlled trading experiments.
