import requests
import time
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.publickey import PublicKey
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair

# Configuration and trading parameters
RPC_URL = "https://api.mainnet-beta.solana.com"  # Replace with your Solana RPC endpoint
wallet = Keypair()  # Initialize or load your wallet keypair
client = Client(RPC_URL)

# Trading variables (adjust as needed)
SLIPPAGE = 0.005           # 0.5% slippage
TAKE_PROFIT = 1.05         # 5% increase for take-profit target
SOL_BUY_AMOUNT = 0.1       # Amount of SOL to buy per trade

# Function to get the current price of SOL from a DEX API
def get_sol_price():
    try:
        response = requests.get("https://api.dex.com/price?pair=SOL_USD")  # Replace with actual price API
        response.raise_for_status()
        price = response.json().get("price", None)
        if price:
            print(f"Current SOL price: ${price}")
        return price
    except requests.RequestException as e:
        print("Error fetching price:", e)
        return None

# Function to execute a buy order for SOL
def buy_sol(amount):
    price = get_sol_price()
    if price is None:
        print("Price data unavailable, cannot proceed with buy.")
        return None

    buy_price = price * (1 + SLIPPAGE)
    print(f"Buying {amount} SOL at {buy_price} USDC with slippage of {SLIPPAGE * 100}%")

    transaction = Transaction()
    transfer_params = TransferParams(
        from_pubkey=wallet.public_key,
        to_pubkey=PublicKey("RecipientPublicKey"),  # Replace with DEX receiver address
        lamports=int(amount * 1e9)
    )
    transaction.add(transfer(transfer_params))

    try:
        response = client.send_transaction(transaction, wallet)
        print("Buy transaction successful:", response)
        return response
    except Exception as e:
        print("Buy transaction failed:", e)
        return None

# Function to execute a sell order for SOL
def sell_sol(amount):
    price = get_sol_price()
    if price is None:
        print("Price data unavailable, cannot proceed with sell.")
        return None

    sell_price = price * TAKE_PROFIT
    print(f"Selling {amount} SOL at {sell_price} USDC for take profit target of {TAKE_PROFIT * 100}%")

    transaction = Transaction()
    transfer_params = TransferParams(
        from_pubkey=wallet.public_key,
        to_pubkey=PublicKey("RecipientPublicKey"),  # Replace with DEX receiver address
        lamports=int(amount * 1e9)
    )
    transaction.add(transfer(transfer_params))

    try:
        response = client.send_transaction(transaction, wallet)
        print("Sell transaction successful:", response)
        return response
    except Exception as e:
        print("Sell transaction failed:", e)
        return None

# Main trading loop
def trade_loop():
    print("Starting trading loop...")
    while True:
        price = get_sol_price()
        if price is None:
            print("Price fetch failed, retrying in 30 seconds...")
            time.sleep(30)
            continue

        # Example buy condition: Buy if the price drops below a specified threshold
        if price <= SOL_BUY_AMOUNT:
            print(f"Triggering buy for {SOL_BUY_AMOUNT} SOL.")
            buy_response = buy_sol(SOL_BUY_AMOUNT)

            if buy_response:
                # After a successful buy, monitor the price to reach take-profit level
                initial_price = price
                while True:
                    current_price = get_sol_price()
                    if current_price is None:
                        print("Waiting for price data...")
                        time.sleep(10)
                        continue

                    if current_price >= initial_price * TAKE_PROFIT:
                        print("Take-profit level reached, selling...")
                        sell_response = sell_sol(SOL_BUY_AMOUNT)
                        if sell_response:
                            break
                    time.sleep(10)  # Check every 10 seconds

        # Wait between main trading loop iterations
        time.sleep(30)

# Start the bot
if __name__ == "__main__":
    trade_loop()
