from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = 'bitcoin'
rpc_password = 'bitcoin'
rpc_host = '127.0.0.1'
rpc_port = '8332'

rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}')

last_scanned_block = 0

def listen_for_transactions():
    # Get the latest block height
    block_count = rpc_connection.getblockcount()

    # If it's an even block, scan
    if block_count % 2 == 0 and block_count != last_scanned_block:
        last_scanned_block = block_count

        # Look for Bitcooin messages in this block
        block_hash = rpc_connection.getblockhash(block_count)
        block = rpc_connection.getblock(block_hash)
        for tx in block['tx']:
            # Get the transaction details
            tx_details = rpc_connection.getrawtransaction(tx, 1)

            # Loop through the outputs
            for output in tx_details['vout']:
                # If the output is a data output
                if 'data' in output['scriptPubKey']:
                    # Decode the data
                    data = output['scriptPubKey']['data']
                    message = bytes.fromhex(data).decode('utf-8')
                    print(message)

if __name__ == '__main__':
    while True:
        listen_for_transactions()