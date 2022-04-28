import asyncio
import logging
from websockets.exceptions import ConnectionClosedOK
from typing import Optional, List, Union
from fastapi import FastAPI, Request, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastbtc.rpc import BitcoinRPC, RPC_USER, RPC_PASS, RPC_HOST, RPC_PORT

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

rpc = BitcoinRPC(RPC_USER, RPC_PASS, RPC_HOST, RPC_PORT)

######## RENDERED PAGES ########
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", 
        context={
            "request": request,
            "peer_info": await rpc.getpeerinfo(),
        }
    )

######## WSS ENDPOINTS ########
@app.websocket("/ws/peerinfo")
async def ws_peerinfo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(await rpc.getpeerinfo())
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        logging.debug("ws client disconnected")

######## API ENDPOINTS ########
@app.get("/rpc/addnode")
@app.post("/rpc/addnode")
async def addnode(node:str, command:str="onetry"):
    return await rpc.addnode(node, command)

@app.get("/rpc/getaddednodeinfo/{node}")
@app.post("/rpc/getaddednodeinfo")
async def getaddednodeinfo(node:str):
    return await rpc.getaddednodeinfo(node)

@app.get("/rpc/connectioncount")
async def connectioncount():
    return await rpc.getconnectioncount()

@app.get("/rpc/getnetworkinfo")
async def getnetworkinfo():
    return await rpc.getnetworkinfo()

@app.get("/rpc/getnettotals")
async def getnettotals():
    return await rpc.getnettotals()

@app.get("/rpc/getnodeaddresses")
async def getnodeaddresses(count:int=None, network:str=None):
    return await rpc.getnodeaddresses(count, network)

@app.get("/rpc/getpeerinfo")
async def getpeerinfo():
    return await rpc.getpeerinfo()

@app.get("/rpc/getmininginfo")
async def getmininginfo():
    return await rpc.getmininginfo()

@app.get("/rpc/getnetworkhashps")
async def getnetworkhashps(nblocks:Optional[int]=None, height:Optional[int]=None):
    return await rpc.getnetworkhashps(nblocks, height)

@app.get("/rpc/getmemoryinfo")
async def getmemoryinfo():
    return await rpc.getmemoryinfo()

@app.get("/rpc/uptime")
async def uptime():
    return await rpc.uptime()

@app.get("/rpc/getblockchaininfo")
async def getblockchaininfo():
    return await rpc.getblockchaininfo()

@app.get("/rpc/getdifficulty")
async def getdifficulty():
    return await rpc.getdifficulty()

@app.get("/rpc/getbestblockhash")
async def getbestblockhash():
    return await rpc.getbestblockhash()

@app.get("/rpc/getblockchainsize")
async def getblockchainsize():
    return await rpc.getblockchainsize()

@app.get("/rpc/getblockcount")
async def getblockcount():
    return await rpc.getblockcount()

@app.get("/rpc/getblockhash/{block}")
async def getblockhash(block:int):
    return await rpc.getblockhash(block)

@app.get("/rpc/getblockheader/{blockhash}")
async def getblockheader(blockhash:str, verbose:Optional[bool]=None):
    return await rpc.getblockheader(blockhash, verbose)

@app.get("/rpc/getblock/{blockhash}")
async def getblock(blockhash:str, verbosity:Optional[int]=None):
    return await rpc.getblock(blockhash, verbosity)

@app.post("/rpc/getblockstats")
async def getblockstats(hash_or_height:Union[str, int], stats:list=[]):
    return await rpc.getblockstats(hash_or_height, stats)

@app.get("/rpc/getaddressinfo/{address}")
async def getaddressinfo(address:str):
    return await rpc.getaddressinfo(address)

@app.get("/rpc/getchaintips")
async def getchaintips():
    return await rpc.getchaintips()

@app.get("/rpc/getchaintxstats")
async def getchaintxstats(nblocks:int=1, blockhash:Optional[str]=None):
    return await rpc.getchaintxstats(nblocks, blockhash)

@app.get("/rpc/getrawtransaction/{txid}")
async def getrawtransaction(txid:str, verbose:Optional[bool]=None, blockhash:Optional[str]=None):
    return await rpc.getrawtransaction(txid, verbose, blockhash)

@app.get("/rpc/gettxout")
async def gettxout(txid:str, n:int, include_mempool:Optional[bool]=None):
    return await rpc.gettxout(txid, n, include_mempool)

@app.post("/rpc/gettxoutproof")
async def gettxoutproof(txids:List[str], blockhash:Optional[str]=None):
    return await rpc.gettxoutproof(txids, blockhash)

@app.get("/rpc/verifytxoutproof")
async def verifytxoutproof(proof:str):
    return await rpc.verifytxoutproof(proof)

@app.get("/rpc/verifychain")
async def verifychain(checklevel:Optional[int]=None, nblocks:Optional[int]=None):
    if nblocks <= 0 or 100 < nblocks:
        logging.warning("Operation will take a long time to complete, limiting result to the last 100 blocks instead.")
        nblocks = 100
    return await rpc.verifychain(checklevel, nblocks)

@app.get("/rpc/getblockinfo/{height}")
async def getblockinfo(height:int, verbosity:Optional[int]=None):
    return await rpc.getblockinfo(height, verbosity)

@app.get("/rpc/validateaddress/{address}")
async def validateaddress(address:str):
    return await rpc.validateaddress(address)

@app.get("/rpc/verifymessage")
async def verifymessage(address:str, signature:str, message:str):
    return await rpc.verifymessage(address, signature, message)

@app.get("/rpc/signmessagewithprivkey")
async def signmessagewithprivkey(privkey:str, message:str):
    return await rpc.signmessagewithprivkey(privkey, message)

@app.get("/rpc/decodescript/{hexstring}")
async def decodescript(hexstring:str):
    return await rpc.decodescript(hexstring)

@app.get("/rpc/decoderawtransaction/{hexstring}")
async def decoderawtransaction(hexstring:str, is_witness:Optional[bool]=None):
    return await rpc.decoderawtransaction(hexstring, is_witness)

@app.get("/rpc/getmempoolinfo")
async def getmempoolinfo():
    return await rpc.getmempoolinfo()

@app.get("/rpc/getrawmempool")
async def getrawmempool():
    return await rpc.getrawmempool()

@app.get("/rpc/getmempoolentry/{txid}")
async def getmempoolentry(txid:str):
    return await rpc.getmempoolentry(txid)

@app.get("/rpc/getmempoolancestors/{txid}")
async def getmempoolancestors(txid:str, verbose:Optional[bool]=None):
    return await rpc.getmempoolancestors(txid, verbose)

@app.get("/rpc/getmempooldescendants/{txid}")
async def getmempooldescendants(txid:str, verbose:Optional[bool]=None):
    return await rpc.getmempooldescendants(txid, verbose)

@app.get("/rpc/getsatoshis/{address}")
async def getsatoshis(address:str):
    return await rpc.getsatoshis(address)

if __name__ == "__main__":
    rpc.close()