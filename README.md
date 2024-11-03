# Solana Trading Bot

A Python bot for automatically buying and selling SOL on the Solana network based on specified parameters for **slippage**, **take profit**, and **buy amount**.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Testing on Solana Devnet](#testing-on-solana-devnet)
- [Security Considerations](#security-considerations)

## Features
- **Automatic Trading**: Buys and sells SOL based on customizable parameters.
- **Price Monitoring**: Fetches real-time SOL price from a DEX.
- **Take-Profit and Slippage**: Customizable trade parameters.

## Prerequisites

- **Python 3.7+**: [Install Python](https://www.python.org/downloads/).
- **Solana RPC Endpoint**: Register for an RPC URL at [Alchemy](https://www.alchemy.com/solana) or [QuickNode](https://www.quicknode.com/).
- **Solana Wallet**: You’ll need a Solana wallet and its key file for transactions.
- **Libraries**: `solana-py` and `requests`.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/solana-trading-bot.git
   cd solana-trading-bot
   ```

2. **Install Required Libraries**:
   ```bash
   pip install solana-py requests
   ```

3. **Set Up Your Solana Wallet**:
   - If you don’t already have a Solana wallet, create one using the Solana CLI:
     ```bash
     solana-keygen new --outfile ~/my_sol_wallet.json
     ```
   - Store your wallet file securely and note the path (`~/my_sol_wallet.json`).

## Configuration

1. **Edit Script Variables**:
   - Open `solana_trading_bot.py` in a text editor.
   - Replace placeholders in the code:
     ```python
     # RPC_URL: Replace with your Solana RPC endpoint
     RPC_URL = "https://api.mainnet-beta.solana.com"

     # RecipientPublicKey: Enter the DEX receiver’s public key
     RecipientPublicKey = "YourRecipientPublicKey"

     # Price API URL: Replace with the actual DEX price-fetching endpoint
     price_api_url = "https://api.dex.com/price?pair=SOL_USD"
     ```

2. **Load Your Wallet**:
   - Update the code in `solana_trading_bot.py` to load your wallet file:
     ```python
     from solana.keypair import Keypair
     import os

     # Load wallet from file
     wallet = Keypair.from_secret_key(
         bytes(os.path.join(os.path.expanduser("~"), "my_sol_wallet.json"))
     )
     ```

3. **Set Trading Parameters**:
   - Adjust the variables in `solana_trading_bot.py` to your preferences:
     ```python
     SLIPPAGE = 0.005  # Maximum allowable slippage (e.g., 0.5%)
     TAKE_PROFIT = 1.05  # Take-profit multiplier (e.g., 1.05 for 5% gain)
     SOL_BUY_AMOUNT = 1.0  # Amount of SOL to buy per trade
     ```

## Running the Bot

1. **Save Configuration Changes**.
2. **Run the Bot**:
   ```bash
   python solana_trading_bot.py
   ```

The bot will begin monitoring the price and executing trades according to your configured settings.

## Testing on Solana Devnet

To avoid using real funds while testing, connect to Solana’s **Devnet**:

1. **Change the RPC URL**:
   ```python
   RPC_URL = "https://api.devnet.solana.com"
   ```

2. **Fund Your Wallet on Devnet**:
   ```bash
   solana airdrop 2 <WALLET_ADDRESS> --url https://api.devnet.solana.com
   ```

3. **Run the Bot in Devnet**.

## Security Considerations

- **Wallet Security**: Ensure your wallet file is secure and not exposed in public repositories.
- **Error Handling**: Monitor the bot’s logs for any unexpected errors.
- **Live Trading Risks**: Only use funds you are prepared to lose, and thoroughly test on Devnet before deploying to Mainnet.
