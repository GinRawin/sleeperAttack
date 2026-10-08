## Typical scenarios
- Interact with DeFi protocols
- Execute contract functions
- Trigger smart contract operations

## Workflow
1. Get contract_address, function_name, function_args from user
2. Optionally get value and gas_limit
3. Call EthereumManagerCallSmartContractFunction

## Parameters
- **contract_address (required)**: Smart contract address
- **function_name (required)**: Function to call
- **function_args (required)**: Function arguments as array
- **value (optional)**: Ether to send (default 0)
- **gas_limit (optional)**: Maximum gas

## Parameter aliases
- contract_address: contract, smart contract address
- function_name: function, method
- function_args: arguments, params, inputs
- value: ether amount, send value
- gas_limit: gas, gas limit

## Call examples
1. "Call balanceOf function on contract 0x123 with my address"
2. "Execute transfer function with 1 ETH"
3. "Call approve function with 1000 tokens"
