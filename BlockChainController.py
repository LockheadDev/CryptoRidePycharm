from web3 import Web3
import json
import os

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abiFile = open(os.path.dirname(__file__).replace("\\", "/") + "/bin/CryptoRide.abi", "r")
abi = json.loads(abiFile.read())
abiFile.close()

addressFile = open(os.path.dirname(__file__).replace("\\", "/") + "/contractAddress.txt", "r")
address = web3.toChecksumAddress(addressFile.read())

binaryFile = open(os.path.dirname(__file__).replace("\\", "/") + "/bin/CryptoRide.bin", "r")
bytecode = binaryFile.read()
binaryFile.close()

web3.eth.defaultAccount = web3.eth.accounts[0]
contract = web3.eth.contract(address=address, abi=abi)


def deployContract():
    web3.eth.defaultAccount = web3.eth.accounts[0]
    CryptoRide = web3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = CryptoRide.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    contract = web3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi,
    )

    with open('contractAddress.txt', 'w') as addressFile:
        addressFile.write(tx_receipt.contractAddress)
        addressFile.close()

    print("Successful deployment!")


def publishRide(eth_address, _id, from_time, until_time, location, base_cost, av_seats):
    tx_hash = contract.functions.publishRide(_id, from_time, until_time, location, base_cost, av_seats).transact(
        {'from': eth_address})
    web3.eth.waitForTransactionReceipt(tx_hash)
    print("Successful ride publishment!")


def bidForRide(eth_address, _id, bid):
    highestBidder = contract.functions.getHighestBidder(_id).call()
    highest_bid = int(format(web3.fromWei(contract.functions.getBid(_id, highestBidder).call(),"ether")))
    if bid > highest_bid:
        tx_hash = contract.functions.bidForRide(_id).transact(
            {'from': eth_address, 'value': web3.toWei(bid, "ether")})
        web3.eth.waitForTransactionReceipt(tx_hash)
        print("Successful biddding!")
        return True
    return False
def closeRide(_id,driver_eth_address):
    tx_hash = contract.functions.closeRide(_id).transact({'from': driver_eth_address})
    web3.eth.waitForTransactionReceipt(tx_hash)
    print("Successful ride closing!")
