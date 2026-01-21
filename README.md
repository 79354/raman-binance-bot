# Binance Futures Trading Bot

A production-grade CLI trading system for Binance USDT-M Futures with support for core and advanced order types, built with safety, modularity, and professional logging.

## Features

### Core Order Types
- **Market Orders**: Instant execution at current market price
- **Limit Orders**: Execute at specified price or better

### Advanced Strategies
- **TWAP (Time-Weighted Average Price)**: Split large orders into smaller chunks executed over time to minimize market impact
- **Grid Trading**: Automated buy-low/sell-high with multiple price levels
- **OCO (One-Cancels-the-Other)**: Simultaneous take-profit and stop-loss orders
- **Stop-Limit Orders**: Trigger limit orders when price reaches stop level

### Infrastructure
- Comprehensive input validation
- Structured logging (console + file)
- Environment-based configuration
- Testnet support for safe testing
- Error handling with detailed traces

---

## Prerequisites

- Python 3.8 or higher
- Binance Futures account (or testnet account)
- API key and secret from Binance

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/yourname-binance-bot.git
cd yourname-binance-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
USE_TESTNET=True
```

 **Important**: 
- Start with `USE_TESTNET=True` to test safely
- Get testnet credentials from: https://testnet.binancefuture.com
- Never commit `.env` to version control

---

## Usage

All commands should be run from the project root directory.

### Market Orders
Execute immediate buy/sell at current market price.

```bash
# Buy 0.001 BTC at market price
python src/market_orders.py BTCUSDT BUY 0.001

# Sell 0.5 ETH at market price
python src/market_orders.py ETHUSDT SELL 0.5
```

**Use Case**: Quick entries/exits, closing positions urgently

---

### Limit Orders
Place orders that execute only at your specified price or better.

```bash
# Buy 0.01 BTC when price reaches 45000
python src/limit_orders.py BTCUSDT BUY 0.01 45000

# Sell 1 ETH at 3200
python src/limit_orders.py ETHUSDT SELL 1.0 3200
```

**Use Case**: Patient trading, getting better prices, avoiding slippage

---

### Stop-Limit Orders
Trigger a limit order when price hits your stop level.

```bash
# Syntax: symbol side quantity stop_price limit_price
python src/advanced/stop_limit.py BTCUSDT SELL 0.1 49000 48900

# Stop-loss example: If BTC drops to 49000, sell at 48900
python src/advanced/stop_limit.py BTCUSDT SELL 0.05 48500 48400
```

**Use Case**: Stop-losses, breakout trading

---

### OCO (One-Cancels-the-Other)
Simultaneously place take-profit and stop-loss orders. When one executes, the other is cancelled.

```bash
# Syntax: symbol quantity take_profit_price stop_loss_price [--side]
python src/advanced/oco.py BTCUSDT 0.1 52000 48000

# For closing a long position with 2% profit and 1% loss targets
python src/advanced/oco.py ETHUSDT 0.5 3300 3100 --side SELL
```

**Use Case**: Risk management, automated exits

---

### TWAP (Time-Weighted Average Price)
Split large orders into smaller chunks executed at regular intervals.

```bash
# Syntax: symbol side total_quantity duration_minutes chunks
python src/advanced/twap.py BTCUSDT BUY 1.0 60 10

# Buy 1 BTC over 60 minutes in 10 equal chunks (0.1 BTC every 6 minutes)
python src/advanced/twap.py BTCUSDT BUY 0.5 30 5
```

**Use Case**: Minimize market impact for large orders, institutional trading

---

### Grid Trading
Create a ladder of buy and sell orders within a price range.

```bash
# Syntax: symbol lower_price upper_price grid_levels quantity_per_level
python src/advanced/grid.py BTCUSDT 45000 55000 10 0.01

# Create 10 grid levels between 45k-55k, each with 0.01 BTC
# Buys below current price, sells above current price
python src/advanced/grid.py ETHUSDT 2800 3200 8 0.1
```

**Use Case**: Range-bound markets, automated scalping, sideways price action

---

## 📊 Logging

All operations are logged to two destinations:

1. **Console Output** (INFO level): Real-time feedback
2. **bot.log file** (DEBUG level): Complete execution history

### Log Format
```
2025-01-21 10:30:15 - INFO - [market_orders.py:25] - Initiating MARKET BUY order for 0.001 BTCUSDT
2025-01-21 10:30:16 - INFO - [market_orders.py:35] - Order Success: ID 12345678 | AvgPrice: 50000.00
```

### Monitoring Logs
```bash
# Watch logs in real-time
tail -f bot.log

# Search for errors
grep ERROR bot.log

# View last 50 lines
tail -n 50 bot.log
```

---

## Project Structure

```
yourname-binance-bot/
│
├── src/
│   ├── market_orders.py          # Market order execution
│   ├── limit_orders.py            # Limit order execution
│   │
│   ├── advanced/                  # Advanced strategies
│   │   ├── __init__.py
│   │   ├── stop_limit.py          # Stop-limit orders
│   │   ├── oco.py                 # OCO bracket orders
│   │   ├── twap.py                # TWAP execution algorithm
│   │   └── grid.py                # Grid trading strategy
│   │
│   └── utils/                     # Core utilities
│       ├── __init__.py
│       ├── config.py              # API client & logger setup
│       └── validation.py          # Input validation functions
│
├── .env                           # Environment variables (not in git)
├── .env.example                   # Template for .env
├── requirements.txt               # Python dependencies
├── bot.log                        # Execution logs (generated)
├── report.pdf                     # Technical documentation
└── README.md                      # This file
```

---

## 🔒 Security Best Practices

1. **Use testnet first**: Set `USE_TESTNET=True` initially
2. **Start with small amounts**: Test with minimal quantities
3. **API Restrictions**: 
   - Enable only "Enable Futures" permission
   - Whitelist your IP address
   - Set withdrawal restrictions

---

## 🧪 Testing Workflow

1. **Get Testnet Credentials**
   - Visit: https://testnet.binancefuture.com
   - Create account and generate API keys

2. **Configure Testnet**
   ```env
   USE_TESTNET=True
   ```

3. **Test Basic Orders**
   ```bash
   python src/market_orders.py BTCUSDT BUY 0.001
   python src/limit_orders.py BTCUSDT BUY 0.001 40000
   ```

4. **Test Advanced Strategies**
   ```bash
   python src/advanced/twap.py BTCUSDT BUY 0.01 5 3
   ```

5. **Review Logs**
   ```bash
   cat bot.log
   ```

6. **Verify on Testnet UI**: Check orders at https://testnet.binancefuture.com

---

## Common Issues & Solutions

### Issue: "API credentials not found"
**Solution**: Ensure `.env` file exists with valid API keys

### Issue: "Invalid symbol format"
**Solution**: Use uppercase symbols (BTCUSDT, not btcusdt)

### Issue: "Insufficient balance"
**Solution**: On testnet, request test funds from faucet

### Issue: Orders not appearing
**Solution**: 
- Check `bot.log` for errors
- Verify API keys have Futures trading enabled
- Confirm correct testnet URL

---

## API Documentation

- **Binance Futures API**: https://binance-docs.github.io/apidocs/futures/en/
- **Testnet**: https://testnet.binancefuture.com
- **Python Connector**: https://github.com/binance/binance-connector-python


## Disclaimer

**This software is for educational purposes only.**

- Trading cryptocurrencies involves substantial risk
- Past performance does not guarantee future results
- The authors are not responsible for financial losses
- Always test on testnet before using real funds
- Never invest more than you can afford to lose

---

## Support

For issues or questions:
- Check `bot.log` for detailed error messages
- Review API documentation
- Contact: gillramansingh900@gmail.com

---

## License

This project is submitted as part of an academic assignment.

---

**Built for safe, modular, and professional trading automation**
