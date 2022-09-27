from web3 import web3, Web3
import time
import json
import asyncio
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pyfiglet
from config import*





infura = infura_mainnet #imported from config
web3 = Web3(Web3.HTTPProvider(infura))

# uniswap address and abi
eth_contract = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" #WETH
Token_address = buy_token_contract #imported from config
sender_address = my_eth_public_address #imported from config
eth_value = float(eth_buy_value) #imported from config
amount_tokens_min = int(amount_ofmin_tokensto_recieve)
uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)

def check_connection():
    return web3.isConnected() #boolean output

def balance():

    balance = web3.eth.get_balance(sender_address)
    format_balance = web3.fromWei(balance,'ether') #only to view readable, use balance for further functions
    return format_balance

def try_buy_uni(): #uniswap buy setup
    contract = web3.eth.contract(address=uniswap_router, abi=uniswap_factory_abi)

    nonce = web3.eth.get_transaction_count(sender_address)

    start = time.time()

    txn = contract.functions.swapExactETHForTokens(
        amount_tokens_min,  #amoubt of tokens to recieve (min)
        [eth_contract, Token_address],
        sender_address,
        (int(time.time()) + 10000)
    ).buildTransaction({
        'from': sender_address,
        'value': web3.toWei(eth_value, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("SNIPED !!!!, bought >> " + web3.toHex(tx_token))



def handle_event(event):
    print("PLEASE DO NOT CLOSE THE WINDOW,ALLOW BOT TO RUN")
    print(Web3.toJSON(event))
    t_0 = str(Web3.toJSON(event['args']['token1']))
    t_1 = str(Web3.toJSON(event['args']['token0']))
    print("Token0: " + t_0)
    print("Token1: " + t_1)


    weth_format = eth_contract.upper()
    buy_token_format = Token_address.upper()
    if (t_0.upper().strip('"') == weth_format and t_1.upper().strip('"') == buy_token_format):
        print("FOUND PAIR")
        try_buy_uni()
    elif (t_0.upper().strip('"') == buy_token_format and t_1.upper().strip('"') == weth_format):
        print("FOUND PAIR")
        try_buy_uni()
    else:
        print("<<<<-------------------------------------->>>>")
        print("PLEASE DO NOT CLOSE THE WINDOW,ALLOW BOT TO RUN")
        print("<<<<-------------------------------------->>>>")
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)



def main():
    event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))

    finally:

        loop.close()

ascii_banner = pyfiglet.figlet_format("SNIPE-BALL")
print(ascii_banner)
print("<Bot by SHAHEN B>")
print("PLEASE MAKE SURE CONFIG.PY FILE IS CORRECTLY FILLED!!")
print("___Refer to the README file for detailed discription on how-to setup config file___")
print(f"CURRENT ETH BALANCE : {balance()}")
if check_connection() == True:
    print("Sucessfull Connection with HTTP-Provider")
start_bot = input("Type ( launch ) if config setup is done:  ")
if start_bot == "launch":
    print("PLEASE WAIT WHILE BOT SCANS NEW PAIRS CREATED......")
    main()
elif start_bot != "launch":
     print("sorry WRONG command")
     start_bot2 = input("Type (launch) to restart or ( exit ) to exit:  ")
     if start_bot2 == "launch":
        print("PLEASE WAIT WHILE BOT SCANS NEW PAIRS CREATED......")
        main()
     else:
         print("---Program closing.............")
         print(ascii_banner)
         print("<Bot by SHAHEN B>")
         time.sleep(3)
         quit()













