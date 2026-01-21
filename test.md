# 🎮 Complete Testing & CLI Usage Guide

Let me walk you through **exactly** how to test your bot and use the CLI from scratch.

---

## 📦 **STEP 1: Initial Setup (First Time Only)**

### 1.1 Install Dependencies

Open your terminal in the project folder:

```bash
# Check if you're in the right folder
ls
# Should see: src/, README.md, requirements.txt, etc.

# Install required packages
pip install -r requirements.txt
```

**What this installs:**
- `binance-connector` - Talks to Binance API
- `python-dotenv` - Reads your .env file securely

---

### 1.2 Get Testnet Account & API Keys

**Why testnet?** It's a practice environment with **fake money** but **real API**. You can't lose actual money!

**Get your keys:**

1. **Go to testnet website:**
   ```
   https://testnet.binancefuture.com
   ```

2. **Create account** (use any email, even fake ones work)

3. **Get free test money:**
   - After login, click "Get Test Funds" or similar button
   - You'll receive fake USDT (like $10,000)

4. **Generate API keys:**
   - Click your profile → API Management
   - Create New Key
   - **Copy both:**
     - API Key (looks like: `abc123def456...`)
     - Secret Key (looks like: `xyz789uvw012...`)

---

### 1.3 Configure Your .env File

Create the `.env` file in your project root:

```bash
# Create the file
touch .env

# Open in editor (choose one)
nano .env
# OR
code .env
# OR
vim .env
```

**Paste this inside `.env`:**

```env
BINANCE_API_KEY=paste_your_actual_api_key_here
BINANCE_SECRET_KEY=paste_your_actual_secret_key_here
USE_TESTNET=True
```

**Example with real keys:**
```env
BINANCE_API_KEY=K7jN9mP4qR2sT8vW1xY5zB3cD6eF0gH
BINANCE_SECRET_KEY=A1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU
USE_TESTNET=True
```

**Save and close** (Ctrl+X if using nano)

---

## 🧪 **STEP 2: Testing Each Order Type**

### Test 1: Market Order (Simplest)

**What it does:** Buys Bitcoin RIGHT NOW at whatever the current price is.

```bash
python src/market_orders.py BTCUSDT BUY 0.001
```

**Breaking down the command:**
- `python` - Run Python
- `src/market_orders.py` - The script to execute
- `BTCUSDT` - Trading pair (Bitcoin vs USDT)
- `BUY` - Direction (could be SELL)
- `0.001` - Quantity (0.001 Bitcoin = very small amount)

**What you'll see:**

```
2025-01-21 15:30:15 - INFO - Initiating MARKET BUY order for 0.001 BTCUSDT
2025-01-21 15:30:16 - INFO - Order Success: ID 12345678 | AvgPrice: 50000.00
```

**What happened:**
1. Bot connected to Binance testnet
2. Placed buy order for 0.001 BTC
3. Order filled instantly at ~$50,000
4. You now own 0.001 BTC (fake, in testnet)

**Verify it worked:**

**Option A - Check logs:**
```bash
cat bot.log
# Should show your order details
```

**Option B - Check testnet website:**
1. Go to https://testnet.binancefuture.com
2. Click "Orders" or "Positions"
3. You'll see your 0.001 BTC position

---

### Test 2: Limit Order

**What it does:** Places an order that ONLY executes if price reaches your target.

```bash
python src/limit_orders.py BTCUSDT BUY 0.001 45000
```

**Breaking it down:**
- `BTCUSDT BUY 0.001` - Same as before
- `45000` - **NEW**: Only buy if price drops to $45,000

**Current scenario:**
- Bitcoin is at $50,000
- You placed limit at $45,000
- Order is **waiting** (not filled yet)

**What you'll see:**

```
2025-01-21 15:35:20 - INFO - Initiating LIMIT BUY order for 0.001 BTCUSDT @ 45000
2025-01-21 15:35:21 - INFO - Order Placed: ID 87654321 | Status: NEW
```

**Status = NEW means:**
- Order is active
- Waiting for price to reach $45,000
- Will auto-execute when/if price drops

**Verify:**

```bash
# Check testnet website → "Open Orders"
# You'll see your limit order waiting
```

**To cancel it:**
- Go to testnet website → Open Orders → Cancel
- (Or write a cancel script, but manual is fine for testing)

---

### Test 3: TWAP (Time-Weighted Average Price)

**What it does:** Splits ONE large order into MANY small orders over time.

```bash
python src/advanced/twap.py BTCUSDT BUY 0.01 5 3
```

**Breaking it down:**
- `BTCUSDT BUY` - Standard
- `0.01` - **Total amount** to buy (0.01 BTC)
- `5` - **Duration** (5 minutes)
- `3` - **Chunks** (split into 3 pieces)

**What happens:**
```
Minute 0:00 → Buy 0.00333 BTC (chunk 1/3)
Minute 1:40 → Buy 0.00333 BTC (chunk 2/3)
Minute 3:20 → Buy 0.00334 BTC (chunk 3/3)
Total: 0.01 BTC over 5 minutes
```

**What you'll see:**

```
2025-01-21 15:40:00 - INFO - Starting TWAP: 0.01 BTCUSDT over 5m in 3 chunks
2025-01-21 15:40:00 - INFO - Executing Chunk 1/3: 0.00333 BTCUSDT
2025-01-21 15:40:00 - INFO - Sleeping for 100.0s...
2025-01-21 15:41:40 - INFO - Executing Chunk 2/3: 0.00333 BTCUSDT
2025-01-21 15:41:40 - INFO - Sleeping for 100.0s...
2025-01-21 15:43:20 - INFO - Executing Chunk 3/3: 0.00334 BTCUSDT
2025-01-21 15:43:20 - INFO - TWAP Strategy Completed. Total executed: 0.01/0.01
```

**Watch it in real-time:**

Open a second terminal window and run:
```bash
tail -f bot.log
```
This shows logs as they happen (live feed)

---

### Test 4: Grid Trading

**What it does:** Creates a ladder of buy/sell orders in a price range.

```bash
python src/advanced/grid.py BTCUSDT 48000 52000 5 0.001
```

**Breaking it down:**
- `48000` - Lower price ($48k)
- `52000` - Upper price ($52k)
- `5` - Number of grid levels
- `0.001` - Quantity per level

**Assuming current price is $50,000:**

**Bot will create:**
```
SELL @ $52,000 (level 5) - 0.001 BTC
SELL @ $51,000 (level 4) - 0.001 BTC
--- Current price: $50,000 ---
BUY @ $49,000 (level 2) - 0.001 BTC
BUY @ $48,000 (level 1) - 0.001 BTC
```

**What you'll see:**

```
2025-01-21 16:00:00 - INFO - Current Price: 50000. Grid Range: 48000 - 52000
2025-01-21 16:00:01 - INFO - Placing Grid Level 1: BUY 0.001 @ 48000
2025-01-21 16:00:02 - INFO - Placing Grid Level 2: BUY 0.001 @ 49000
2025-01-21 16:00:03 - INFO - Skipping level 3 @ 50000 (too close to current price)
2025-01-21 16:00:04 - INFO - Placing Grid Level 4: SELL 0.001 @ 51000
2025-01-21 16:00:05 - INFO - Placing Grid Level 5: SELL 0.001 @ 52000
2025-01-21 16:00:06 - INFO - Grid Setup Complete. Total Orders Placed: 4
```

**Verify on testnet:**
- Go to Open Orders
- You'll see 2 buy orders + 2 sell orders
- They're all waiting for their price levels

---

### Test 5: OCO (One-Cancels-the-Other)

**What it does:** Places take-profit AND stop-loss simultaneously.

**First, you need a position:**

```bash
# Step 1: Buy Bitcoin to create position
python src/market_orders.py BTCUSDT BUY 0.01

# Step 2: Place OCO to manage that position
python src/advanced/oco.py BTCUSDT 0.01 52000 48000
```

**Breaking down OCO command:**
- `BTCUSDT` - Pair
- `0.01` - Position size (must match what you own)
- `52000` - Take profit price (+4% from $50k)
- `48000` - Stop loss price (-4% from $50k)

**What you'll see:**

```
2025-01-21 16:10:00 - INFO - Setting up OCO bracket for BTCUSDT | Qty: 0.01
2025-01-21 16:10:01 - INFO - Placing Take Profit Limit @ 52000
2025-01-21 16:10:02 - INFO - Placing Stop Loss Market @ 48000
2025-01-21 16:10:03 - INFO - OCO Bracket Placed Successfully.
2025-01-21 16:10:03 - INFO - TP Order ID: 11111111 | SL Order ID: 22222222
```

**Now what happens:**
- If price rises to $52,000 → Take profit sells, stop-loss cancels (you win)
- If price drops to $48,000 → Stop-loss sells, take profit cancels (limited loss)

---

### Test 6: Stop-Limit Order

**What it does:** Triggers a limit order when price hits a stop price.

```bash
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 49000 48900
```

**Breaking it down:**
- `SELL 0.01` - Close 0.01 BTC position
- `49000` - **Stop price** (trigger point)
- `48900` - **Limit price** (actual sell price)

**Scenario:**
```
Current price: $50,000
Your stop-limit: Stop @ $49k, Limit @ $48.9k

Price drops to $49,000 → Order activates
Now tries to sell at $48,900 (limiting your loss)
```

**What you'll see:**

```
2025-01-21 16:20:00 - INFO - Placing STOP-LIMIT: Trigger @ 49000, Limit @ 48900
2025-01-21 16:20:01 - INFO - Stop-Limit Registered: ID 33333333
```

---

## 🔍 **How to Monitor & Debug**

### Check What's Happening

**1. Live log monitoring:**
```bash
tail -f bot.log
```
Shows logs as they happen (Ctrl+C to stop)

**2. View all logs:**
```bash
cat bot.log
```

**3. Find errors only:**
```bash
grep ERROR bot.log
```

**4. Last 20 lines:**
```bash
tail -20 bot.log
```

---

### Verify on Testnet Website

**Check positions:**
1. Go to https://testnet.binancefuture.com
2. Click "Positions" tab
3. See all your open trades

**Check orders:**
1. Click "Orders" → "Open Orders"
2. See waiting limit/grid orders

**Check history:**
1. Click "Orders" → "Order History"
2. See all filled orders

---

## 🎯 **Practice Test Sequence**

Run these commands in order to see everything work:

```bash
# Test 1: Quick market buy
python src/market_orders.py BTCUSDT BUY 0.001

# Test 2: Place a limit order (won't fill immediately)
python src/limit_orders.py BTCUSDT BUY 0.001 40000

# Test 3: Small TWAP (3 minutes)
python src/advanced/twap.py BTCUSDT BUY 0.01 3 3

# Test 4: Tiny grid (5 levels)
python src/advanced/grid.py BTCUSDT 48000 52000 5 0.001

# Test 5: Check logs
cat bot.log

# Test 6: Check testnet website
# Go to browser and verify orders
```

---

## ❌ **Common Errors & Solutions**

### Error: "API credentials not found"

**Fix:**
```bash
# Check if .env exists
ls -la .env

# If not, create it
touch .env

# Add your keys
nano .env
```

### Error: "Invalid symbol format"

**Fix:** Use uppercase
```bash
# Wrong
python src/market_orders.py btcusdt BUY 0.001

# Correct
python src/market_orders.py BTCUSDT BUY 0.001
```

### Error: "Insufficient balance"

**Fix:** Get testnet funds
1. Go to https://testnet.binancefuture.com
2. Click "Get Test Funds"
3. Wait 1 minute
4. Try again

### Error: "Module not found: binance"

**Fix:**
```bash
pip install -r requirements.txt
```

---

## 🎮 **CLI Command Cheat Sheet**

### Basic Syntax
```bash
python src/[script_name].py [ARGS]
```

### Market Orders
```bash
# Buy
python src/market_orders.py BTCUSDT BUY 0.001

# Sell
python src/market_orders.py BTCUSDT SELL 0.001
```

### Limit Orders
```bash
# Buy at price
python src/limit_orders.py BTCUSDT BUY 0.001 45000

# Sell at price
python src/limit_orders.py BTCUSDT SELL 0.001 55000
```

### TWAP
```bash
# Buy [amount] over [minutes] in [chunks]
python src/advanced/twap.py BTCUSDT BUY 0.01 10 5
```

### Grid
```bash
# [low_price] [high_price] [levels] [qty_per_level]
python src/advanced/grid.py BTCUSDT 45000 55000 10 0.001
```

### OCO
```bash
# [qty] [take_profit] [stop_loss]
python src/advanced/oco.py BTCUSDT 0.01 52000 48000
```

### Stop-Limit
```bash
# [side] [qty] [stop_price] [limit_price]
python src/advanced/stop_limit.py BTCUSDT SELL 0.01 49000 48900
```

---

## 📸 **Taking Screenshots for Report**

**What to capture:**

1. **Terminal output** (use your OS screenshot tool)
2. **Testnet UI showing orders**
3. **bot.log file contents**

**Example process:**

```bash
# Run a command
python src/market_orders.py BTCUSDT BUY 0.001

# Screenshot 1: Terminal output
# (Press PrtScn or Cmd+Shift+4)

# Screenshot 2: Open testnet website
# Go to Orders → Order History
# (Screenshot showing filled order)

# Screenshot 3: View logs
cat bot.log
# (Screenshot log entries)
```

---

## 🎓 **You're Ready!**

**Practice workflow:**
1. Run each command once
2. Check logs after each
3. Verify on testnet website
4. Take screenshots
5. Add screenshots to report.pdf

**Time estimate:** 30 minutes to test everything

You've got this! 🚀