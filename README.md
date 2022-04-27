## RPC Commands Coverage

**== Blockchain ==**
- [x] getbestblockhash
- [x] getblock "blockhash" ( verbosity )
- [x] getblockchaininfo
- [x] getblockcount
- [ ] getblockfilter "blockhash" ( "filtertype" )
- [x] getblockhash height
- [x] getblockheader "blockhash" ( verbose )
- [x] getblockstats hash_or_height ( stats )
- [x] getchaintips
- [x] getchaintxstats ( nblocks "blockhash" )
- [x] getdifficulty
- [x] getmempoolancestors "txid" ( verbose )
- [x] getmempooldescendants "txid" ( verbose )
- [x] getmempoolentry "txid"
- [x] getmempoolinfo
- [x] getrawmempool ( verbose mempool_sequence )
- [x] gettxout "txid" n ( include_mempool )
- [x] gettxoutproof - ["txid",...] ( "blockhash" )
- [ ] gettxoutsetinfo ( "hash_type" hash_or_height use_index )
- [ ] preciousblock "blockhash"
- [ ] pruneblockchain height
- [ ] savemempool
- [ ] scantxoutset "action" ( - [scanobjects,...] )
- [x] verifychain ( checklevel nblocks )
- [x] verifytxoutproof "proof"

**== Control ==**
- [x] getmemoryinfo ( "mode" )
- [ ] getrpcinfo
- [ ] help ( "command" )
- [ ] logging ( - ["include_category",...] - ["exclude_category",...] )
- [ ] stop
- [x] uptime

**== Generating ==**
- [ ] generateblock "output" - ["rawtx/txid",...]
- [ ] generatetoaddress nblocks "address" ( maxtries )
- [ ] generatetodescriptor num_blocks "descriptor" ( maxtries )

**== Mining ==**
- [ ] getblocktemplate ( "template_request" )
- [x] getmininginfo
- [ ] getnetworkhashps ( nblocks height )
- [ ] prioritisetransaction "txid" ( dummy ) fee_delta
- [ ] submitblock "hexdata" ( "dummy" )
- [ ] submitheader "hexdata"

**== Network ==**
- [ ] addnode "node" "command"
- [ ] clearbanned
- [ ] disconnectnode ( "address" nodeid )
- [ ] getaddednodeinfo ( "node" )
- [x] getconnectioncount
- [ ] getnettotals
- [ ] getnetworkinfo
- [ ] getnodeaddresses ( count "network" )
- [x] getpeerinfo
- [ ] listbanned
- [ ] ping
- [ ] setban "subnet" "command" ( bantime absolute )
- [ ] setnetworkactive state

**== Rawtransactions ==**
- [ ] analyzepsbt "psbt"
- [ ] combinepsbt - ["psbt",...]
- [ ] combinerawtransaction - ["hexstring",...]
- [ ] converttopsbt "hexstring" ( permitsigdata iswitness )
- [ ] createpsbt - [{"txid":"hex","vout":n,"sequence":n},...] - [{"address":amount,...},{"data":"hex"},...] ( locktime replaceable )
- [ ] createrawtransaction - [{"txid":"hex","vout":n,"sequence":n},...] - [{"address":amount,...},{"data":"hex"},...] ( locktime replaceable )
- [ ] decodepsbt "psbt"
- [x] decoderawtransaction "hexstring" ( iswitness )
- [x] decodescript "hexstring"
- [ ] finalizepsbt "psbt" ( extract )
- [ ] fundrawtransaction "hexstring" ( options iswitness )
- [x] getrawtransaction "txid" ( verbose "blockhash" )
- [ ] joinpsbts - ["psbt",...]
- [ ] sendrawtransaction "hexstring" ( maxfeerate )
- [ ] signrawtransactionwithkey "hexstring" - ["privatekey",...] ( - [{"txid":"hex","vout":n,"scriptPubKey":"hex","redeemScript":"hex","witnessScript":"hex","amount":amount},...] "sighashtype" )
- [ ] testmempoolaccept - ["rawtx",...] ( maxfeerate )
- [ ] utxoupdatepsbt "psbt" ( - ["",{"desc":"str","range":n or - [n,n]},...] )

**== Signer ==**
- [ ] enumeratesigners 

**== Util ==**
- [ ] createmultisig nrequired - ["key",...] ( "address_type" )
- [ ] deriveaddresses "descriptor" ( range )
- [ ] estimatesmartfee conf_target ( "estimate_mode" )
- [ ] getdescriptorinfo "descriptor"
- [ ] getindexinfo ( "index_name" )
- [x] signmessagewithprivkey "privkey" "message"
- [x] validateaddress "address"
- [x] verifymessage "address" "signature" "message"

**== Wallet ==**
- [ ] abandontransaction "txid"
- [ ] abortrescan
- [ ] addmultisigaddress nrequired - ["key",...] ( "label" "address_type" )
- [ ] backupwallet "destination"
- [ ] bumpfee "txid" ( options )
- [ ] createwallet "wallet_name" ( disable_private_keys blank "passphrase" avoid_reuse descriptors load_on_startup external_signer )
- [ ] dumpprivkey "address"
- [ ] dumpwallet "filename"
- [ ] encryptwallet "passphrase"
- [ ] getaddressesbylabel "label"
- [x] getaddressinfo "address"
- [x] getbalance ( "dummy" minconf include_watchonly avoid_reuse )
- [x] getbalances
- [ ] getnewaddress ( "label" "address_type" )
- [ ] getrawchangeaddress ( "address_type" )
- [ ] getreceivedbyaddress "address" ( minconf )
- [ ] getreceivedbylabel "label" ( minconf )
- [ ] gettransaction "txid" ( include_watchonly verbose )
- [ ] getunconfirmedbalance
- [x] getwalletinfo
- [ ] importaddress "address" ( "label" rescan p2sh )
- [ ] importdescriptors "requests"
- [ ] importmulti "requests" ( "options" )
- [ ] importprivkey "privkey" ( "label" rescan )
- [ ] importprunedfunds "rawtransaction" "txoutproof"
- [ ] importpubkey "pubkey" ( "label" rescan )
- [ ] importwallet "filename"
- [ ] keypoolrefill ( newsize )
- [ ] listaddressgroupings
- [ ] listdescriptors
- [ ] listlabels ( "purpose" )
- [ ] listlockunspent
- [ ] listreceivedbyaddress ( minconf include_empty include_watchonly "address_filter" )
- [ ] listreceivedbylabel ( minconf include_empty include_watchonly )
- [ ] listsinceblock ( "blockhash" target_confirmations include_watchonly include_removed )
- [ ] listtransactions ( "label" count skip include_watchonly )
- [ ] listunspent ( minconf maxconf - ["address",...] include_unsafe query_options )
- [ ] listwalletdir
- [ ] listwallets
- [ ] loadwallet "filename" ( load_on_startup )
- [ ] lockunspent unlock ( - [{"txid":"hex","vout":n},...] )
- [ ] psbtbumpfee "txid" ( options )
- [ ] removeprunedfunds "txid"
- [ ] rescanblockchain ( start_height stop_height )
- [ ] send - [{"address":amount,...},{"data":"hex"},...] ( conf_target "estimate_mode" fee_rate options )
- [ ] sendmany "" {"address":amount,...} ( minconf "comment" - ["address",...] replaceable conf_target "estimate_mode" fee_rate verbose )
- [ ] sendtoaddress "address" amount ( "comment" "comment_to" subtractfeefromamount replaceable conf_target "estimate_mode" avoid_reuse fee_rate verbose )
- [ ] sethdseed ( newkeypool "seed" )
- [ ] setlabel "address" "label"
- [ ] settxfee amount
- [ ] setwalletflag "flag" ( value )
- [ ] signmessage "address" "message"
- [ ] signrawtransactionwithwallet "hexstring" ( - [{"txid":"hex","vout":n,"scriptPubKey":"hex","redeemScript":"hex","witnessScript":"hex","amount":amount},...] "sighashtype" )
- [ ] unloadwallet ( "wallet_name" load_on_startup )
- [ ] upgradewallet ( version )
- [ ] walletcreatefundedpsbt ( - [{"txid":"hex","vout":n,"sequence":n},...] ) - [{"address":amount,...},{"data":"hex"},...] ( locktime options bip32derivs )
- [ ] walletdisplayaddress bitcoin address to display
- [ ] walletlock
- [ ] walletpassphrase "passphrase" timeout
- [ ] walletpassphrasechange "oldpassphrase" "newpassphrase"
- [ ] walletprocesspsbt "psbt" ( sign "sighashtype" bip32derivs )

**== Zmq ==**
- [ ] getzmqnotifications