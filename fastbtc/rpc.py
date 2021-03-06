import os
import orjson
import aiohttp
from typing import List, Union


RPC_USER = os.getenv("BTC_RPC_USER")    # rpcuser from bitcoin.conf
RPC_PASS = os.getenv("BTC_RPC_PASS")    # rpcpassword from bitcoin.conf
RPC_HOST = "127.0.0.1"                  # rpcbind from bitcoin.conf
RPC_PORT = 8332                         # rpcport from bitcoin.conf
RPC_SCHEME = 'http'                     # currently only HTTP is supported
RPC_URL = f"{RPC_SCHEME}://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}"


class BitcoinRPC:
    def __init__(self, username:str, password:str, host:str, port:int, scheme:str='http') -> None:
        self.session = aiohttp.ClientSession(trust_env=True, json_serialize=orjson.dumps)
        self.url = f"{scheme}://{username}:{password}@{host}:{port}"

    async def __aenter__(self) -> 'BitcoinRPC':
        '''Upon entry if being used as context manager'''
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        '''Upon exit if being used as context manager'''
        await self.close()

    async def close(self):
        '''Close the ClientSession'''
        await self.session.close()

    async def __rpc__(self, method:str, params:list=None):
        '''Sends formatted RPC to server and returns JSON reply'''
        command = {
            "method": method,
            "params": params if params else [],
        }
        async with self.session.post(self.url, data=orjson.dumps(command)) as reply:
            return (await reply.json())
  
    async def call(self, method:str, params:list=None):
        '''Returns the result from the RPC server using the given method and params'''
        reply = await self.__rpc__(method, params)
        return reply['error'] if reply['error'] else reply['result']

    ######## NODE AND NETWORK ########
    async def addnode(self, node:str, command:str) -> Union[None, dict]:
        '''Attempts to add or remove a node from the addnode list. Or try a connection to a node once.'''
        method = "addnode"
        assert command.lower() in ["add", "remove", "onetry"]
        params = [node, command,]
        return await self.call(method, params)

    async def clearbanned(self) -> None:
        '''Clear all banned IPs.'''
        method = "clearbanned"
        return await self.call(method)

    async def listbanned(self) -> list:
        '''Returns all banned IPs.'''
        method = "listbanned"
        return await self.call(method)

    async def getaddednodeinfo(self, node:str) -> dict:
        '''Returns information about the given added node, or all added nodes (note that onetry addnodes are not listed here)'''
        method = "getaddednodeinfo"
        params = [node,]
        return await self.call(method, params)

    async def getconnectioncount(self) -> int:
        '''Returns the number of connections to other nodes'''
        method = "getconnectioncount"
        return await self.call(method)

    async def getnetworkinfo(self) -> dict:
        '''Returns an object containing various state info regarding P2P networking.'''
        method = "getnetworkinfo"
        return await self.call(method)

    async def getnettotals(self) -> dict:
        '''Returns information about network traffic, including bytes in, bytes out, and current time.'''
        method = "getnettotals"
        return await self.call(method)

    async def getnodeaddresses(self, count:int=1, network:str=None) -> List[dict]:
        '''Return known addresses which can potentially be used to find new nodes in the network'''
        method = "getnodeaddresses"
        params = [count, network,]
        return await self.call(method, params)

    async def getpeerinfo(self) -> list:
        '''Returns list of information about peer nodes'''
        method = "getpeerinfo"
        return await self.call(method)

    async def getmemoryinfo(self) -> dict:
        '''Returns general statistics about memory usage in the daemon.'''
        method = "getmemoryinfo"
        return await self.call(method)

    async def uptime(self) -> int:
        '''Returns the total number of seconds that the server has been running'''
        method = "uptime"
        return await self.call(method)

    ######## BLOCKCHAIN AND MINING ########
    async def getmininginfo(self) -> dict:
        '''Returns a json object containing mining-related information.'''
        method = "getmininginfo"
        return await self.call(method)

    async def getnetworkhashps(self, nblocks:int=120, height:int=-1) -> float:
        '''Returns the estimated network hashes per second based on the last n blocks.'''
        method = "getnetworkhashps"
        params = [nblocks, height,]
        return await self.call(method, params)

    async def getblockchaininfo(self) -> dict:
        method = "getblockchaininfo"
        return await self.call(method)

    async def getdifficulty(self) -> float:
        '''Returns the proof-of-work difficulty as a multiple of the minimum difficulty'''
        method = "getdifficulty"
        return await self.call(method)

    async def getbestblockhash(self) -> str:
        '''version 0.9 Returns the hash of the best (tip) block in the longest block chain.'''
        method = "getbestblockhash"
        return await self.call(method)

    async def getblockcount(self) -> int:
        '''Returns the number of blocks in the longest block chain.'''
        method = "getblockcount"
        return await self.call(method)

    async def getblockhash(self, block:int) -> str:
        '''Returns hash for specified block {0..N}'''
        method = "getblockhash"
        params = [block,]
        return await self.call(method, params)

    async def getblockheader(self, blockhash:str, verbose:bool=True) -> Union[dict, str]:
        '''If verbose is false, returns a string that is serialized, hex-encoded data for blockheader 'hash'.
        If verbose is true, returns an Object with information about blockheader <hash>.'''
        method = "getblockheader"
        params = [blockhash, verbose]
        return await self.call(method, params)

    async def getblock(self, blockhash:str, verbosity:int=1) -> dict:
        '''
            Returns information about the block with the given hash
            If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'.
            If verbosity is 1, returns an Object with information about block <hash>.
            If verbosity is 2, returns an Object with information about block <hash> and information about each transaction. 
        '''
        method = "getblock"
        params = [blockhash, verbosity,]
        return await self.call(method, params)

    async def getblockstats(self, hash_or_height:Union[str, int], stats:List[str]=None) -> dict:
        '''Compute per block statistics for a given window. All amounts are in satoshis. It won't work for some heights with pruning.'''
        if hash_or_height.isnumeric():
            hash_or_height = int(hash_or_height)
        method = "getblockstats"
        params = [hash_or_height, stats,]
        return await self.call(method, params)

    async def getchaintips(self) -> list:
        '''Return information about all known tips in the block tree, including the main chain as well as orphaned branches.'''
        method = "getchaintips"
        params = []
        return await self.call(method, params)

    async def getchaintxstats(self, nblocks:int=1, blockhash:str=None) -> dict:
        '''Return information about all known tips in the block tree, including the main chain as well as orphaned branches.'''
        method = "getchaintxstats"
        params = [nblocks, blockhash,]
        return await self.call(method, params)

    async def getaddressinfo(self, address:str) -> dict:
        '''Returns information about the given address'''
        method = "getaddressinfo"
        params = [address,]
        return await self.call(method, params)

    async def getrawtransaction(self, txid:str, verbose:bool=False, blockhash:str=None) -> dict:
        '''Returns information about the transaction with the given txid'''
        method = "getrawtransaction"
        params = [txid, verbose,]
        if blockhash:
            params.append(blockhash)
        return await self.call(method, params)

    async def gettxout(self, txid:str, n:int, include_mempool:bool=True):
        '''Returns details about an unspent transaction output (UTXO)'''
        method = "gettxout"
        params = [txid, n,]
        return await self.call(method, params)

    async def gettxoutproof(self, txids:List[str], blockhash:str=None):
        '''Returns a hex-encoded proof that "txid" was included in a block.'''
        method = "gettxoutproof"
        params = [txids, blockhash,]
        return await self.call(method, params)

    async def verifytxoutproof(self, proof:str) -> List[str]:
        '''Verifies that a proof points to a transaction in a block, returning the transaction
        it commits to and throwing an RPC error if the block is not in our best chain'''
        method = "verifytxoutproof"
        params = [proof,]
        return await self.call(method, params)

    async def verifychain(self, checklevel:int=3, nblocks:int=6) -> bool:
        '''Verifies blockchain database.'''
        method = "verifychain"
        params = [checklevel, nblocks,]
        return await self.call(method, params)

    ######## UTILITIES ########
    async def validateaddress(self, address:str) -> dict:
        '''Returns information about the validity of the given address'''
        method = "validateaddress"
        params = [address,]
        return await self.call(method, params)

    async def verifymessage(self, address:str, signature:str, message:str) -> bool:
        '''Verify a signed message'''
        method = "verifymessage"
        params = [address, signature, message,]
        verified = await self.call(method, params)
        return True if verified else False

    async def signmessagewithprivkey(self, privkey:str, message:str) -> str:
        ''' Sign a message with the private key of an address'''
        method = "signmessagewithprivkey"
        params = [privkey, message,]
        return await self.call(method, params)

    async def decodescript(self, hexstring:str) -> dict:
        '''Decode a hex-encoded script'''
        method = "decodescript"
        params = [hexstring,]
        return await self.call(method, params)

    async def decoderawtransaction(self, hexstring:str, is_witness:bool) -> dict:
        ''''''
        method = "decoderawtransaction"
        params = [hexstring, is_witness,]
        return await self.call(method, params)

    ######## MEMORY POOL ########
    async def getmempoolinfo(self) -> dict:
        '''Returns information about the memory pool'''
        method = "getmempoolinfo"
        return await self.call(method)

    async def getrawmempool(self) -> list:
        '''Returns list of txids in memory pool'''
        method = "getrawmempool"
        return await self.call(method)

    async def getmempoolentry(self, txid:str) -> dict:
        '''Returns information about the given txid'''
        method = "getmempoolentry"
        params = [txid,]
        return await self.call(method, params)

    async def getmempoolancestors(self, txid:str, verbose:bool=False) -> list:
        '''Returns list containing mempool ancestors of the given txid'''
        method = "getmempoolancestors"
        params = [txid, verbose,]
        return await self.call(method, params)

    async def getmempooldescendants(self, txid:str, verbose:bool=False) -> list:
        '''Returns list containing mempool ancestors of the given txid'''
        method = "getmempooldescendants"
        params = [txid, verbose, ]
        return await self.call(method, params)

    ######## WALLET ########
    async def getwalletinfo(self) -> dict:
        '''Returns information about wallet'''
        method = "getwalletinfo"
        return await self.call(method)

    async def getbalance(self) -> float:
        '''Returns balance of node'''
        method = "getbalance"
        return await self.call(method)

    async def getbalances(self) -> dict:
        '''Returns a dictionary with all the balances'''
        method = "getbalances"
        return await self.call(method)

    ######## EXTERNAL QUERIES ########
    async def getsatoshis(self, wallet:str) -> int:
        '''Returns the satoshi balance of given wallet'''
        url = f"https://blockchain.info/q/addressbalance/{wallet}"
        reply = await self.session.get(url)
        if reply.status == 200:
            return int(await reply.text())

    ######## DERIVED ########
    async def getblockchainsize(self) -> float:
        '''Returns size of current blockchain in Giga Bytes'''
        reply = await self.getblockchaininfo()
        return round(reply['size_on_disk'] / 2**30, 2) if reply else reply

    async def getblockinfo(self, block:int, verbosity:int=2) -> dict:
        '''Returns detailed info about given block height'''
        blockhash = await self.getblockhash(block)
        return await self.getblock(blockhash, verbosity)


if __name__ == "__main__":
    raise RuntimeError("Module is not meant to be called directly")
