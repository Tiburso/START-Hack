from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time

rpc_user = 'bitcoin'
rpc_password = 'bitcoin'
rpc_host = '127.0.0.1'
rpc_port = '8332'

rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}')

global last_scanned_block
last_scanned_block: int = 0

def scan_block(block_hash: str):
    # Look for Bitcooin messages in this block
    block = rpc_connection.getblock(block_hash)
    print(f"<#> Block Height {block['height']} --------------- <#>")

    for tx in block['tx']:
        
        messages: list[str] = []
        
        # Get the transaction details
        tx_details = rpc_connection.getrawtransaction(tx, 1)

        # Loop through the outputs
        for output in tx_details['vout']:
            
            # If the output is a data output
            if 'asm' in output['scriptPubKey']:
                
                # Decode the data
                data = output['scriptPubKey']['asm'].split(' ')
                for d in data:
                    try:
                        messages.append(bytes.fromhex(d).decode('utf-8'))
                    except Exception: pass
        if messages:
            print(f"    Transaction {tx_details['txid']} contains messages:")

            for message in messages:
                print(f"        > {message}")

def listen_for_transactions():

    global last_scanned_block

    # Get the latest block height
    block_count = rpc_connection.getblockcount()

    # If it's an even block, scan
    if block_count != last_scanned_block:
        last_scanned_block = block_count

        # Look for Bitcooin messages in this block
        block_hash = rpc_connection.getblockhash(block_count)
        scan_block(block_hash)

    time.sleep(1)

if __name__ == '__main__':
        
    print("\nStarting from 10 blocks behind...\n")

    latestBlock = rpc_connection.getblockcount()

    # Scan for messages in the last 10 blocks
    for i in range(latestBlock-10, latestBlock-1):
        
        block_hash = rpc_connection.getblockhash(i)
        scan_block(block_hash)

    # Start listening for new blocks
    while True:
        listen_for_transactions()