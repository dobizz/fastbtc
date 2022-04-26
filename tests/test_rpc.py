import pytest
from fastbtc.rpc import BitcoinRPC, RPC_USER, RPC_PASS, RPC_HOST, RPC_PORT


@pytest.mark.asyncio
class TestClassNode:

    async def test_getconnectioncount(self):
        pass

    async def test_getpeerinfo(self):
        pass
    
    
@pytest.mark.asyncio
class TestClassBlockchain:

    async def test_getmininginfo(self):
        pass
    
    async def test_getblockchaininfo(self):
        pass
    
    async def test_getdifficulty(self):
        pass

    async def test_getbestblockhash(self):
        pass

    async def test_getblockcount(self):
        pass

    async def test_getblockhash(self):
        pass
    
    async def test_getblock(self):
        pass

    async def test_getblockstats(self):
        pass

    async def test_getaddressinfo(self):
        pass

    async def test_getrawtransaction(self):
        pass

    async def test_gettxout(self):
        pass


@pytest.mark.asyncio
class TestClassUtils:
    async def test_validateaddress(self):
        pass

    async def test_verifymessage(self):
        pass

    async def test_signmessagewithprivkey(self):
        pass

    async def test_decodescript(self):
        pass

    async def test_decoderawtransaction(self):
        pass


@pytest.mark.asyncio
class TestClassMemoryPool:

    async def test_getmempoolinfo(self):
        pass
    
    async def test_getrawmempool(self):
        pass
    
    async def test_getmempoolentry(self):
        pass

    async def test_getmempoolancestors(self):
        pass

    async def test_getmempooldescendants(self):
        pass


@pytest.mark.asyncio
class TestClassWallet:

    async def test_getwalletinfo(self):
        pass

    async def test_getbalance(self):
        pass

    async def test_getbalances(self):
        pass


@pytest.mark.asyncio
class TestClassDerived:

    async def test_getblockchainsize(self):
        pass

    async def test_getblockinfo(self):
        pass


@pytest.mark.asyncio
class TestClassExternal:

    async def test_getsatoshis(self):
        pass


if __name__ == "__main__":
    raise RuntimeError("Module is not meant to be called directly")