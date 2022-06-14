from web3 import Web3
import json
import os
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abiFile = open(os.path.dirname(__file__).replace("\\","/")+"/bin/CryptoRide.abi","r")
abi = json.loads(abiFile.read())
abiFile.close()
addressFile = open(os.path.dirname(__file__).replace("\\","/")+"/contractAddress.txt","r")
address = web3.toChecksumAddress(addressFile.read())

contract = web3.eth.contract(address = address, abi= abi)

print("ID:")
_id= int(input())

print('Rider: {}'.format(
    contract.functions.getRider(_id).call()
))