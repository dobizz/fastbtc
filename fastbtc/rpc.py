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
            if reply.status == 200: return (await reply.json())
        return {}

    async def call(self, method:str, params:list=None):
        '''Returns the result from the RPC server using the given method and params'''
        reply = await self.__rpc__(method, params)
        return reply['result'] if reply else reply

    ######## NODE AND NETWORK ########
    async def getconnectioncount(self) -> int:
        '''Returns the number of connections to other nodes'''
        method = "getconnectioncount"
        return await self.call(method)

    async def getpeerinfo(self) -> list:
        '''Returns list of information about peer nodes'''
        method = "getpeerinfo"
        return await self.call(method)

    ######## BLOCKCHAIN AND MINING ########
    async def getmininginfo(self) -> dict:
        method = "getmininginfo"
        return await self.call(method)

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

    async def getblockstats(self, height:int, fields:List[str]=None) -> dict:
        '''Compute per block statistics for a given window. All amounts are in satoshis. It won't work for some heights with pruning.'''
        method = "getblockstats"
        params = [height, fields,]
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
