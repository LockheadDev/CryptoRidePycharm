
import json
import os
from web3 import Web3

# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abiFile = open(os.path.dirname(__file__).replace("\\","/")+"/bin/CryptoRide.abi","r")
abi = json.loads(abiFile.read())
abiFile.close()
binaryFile = open(os.path.dirname(__file__).replace("\\","/")+"/bin/CryptoRide.bin","r")
bytecode = binaryFile.read()
binaryFile.close()

web3.eth.defaultAccount = web3.eth.accounts[0]
CryptoRide = web3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = CryptoRide.constructor().transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi,
)

with open('contractAddress.txt','w') as addressFile:
    addressFile.write(tx_receipt.contractAddress)
    addressFile.close()
    
print("Successful deployment!")