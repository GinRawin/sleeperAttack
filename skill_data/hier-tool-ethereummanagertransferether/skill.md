## Typical scenarios
- Send ETH to another wallet
- Make payment in Ether
- Transfer funds between accounts

## Workflow
1. Get from_address, to_address, amount_ether from user
2. Optionally get gas_limit
3. Call EthereumManagerTransferEther

## Parameters
- **from_address (required)**: Sender address
- **to_address (required)**: Recipient address
- **amount_ether (required)**: Ether amount
- **gas_limit (optional)**: Maximum gas for transfer

## Parameter aliases
- from_address: sender, source address
- to_address: recipient, destination address
- amount_ether: ETH amount, transfer amount
- gas_limit: transfer gas, gas limit

## Call examples
1. "Send 1 ETH from my wallet to 0x456"
2. "Transfer 0.5 Ether to another address"
3. "Send payment of 2 ETH"
