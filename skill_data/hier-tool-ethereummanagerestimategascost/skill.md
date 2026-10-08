## Typical scenarios
- Check gas cost before transaction
- Budget estimation for contract calls
- Avoid failed transactions

## Workflow
1. Get contract_address, function_name, function_args from user
2. Call EthereumManagerEstimateGasCost

## Parameters
- **contract_address (required)**: Smart contract address
- **function_name (required)**: Function to estimate
- **function_args (required)**: Function arguments as array

## Parameter aliases
- contract_address: contract, smart contract
- function_name: function, method
- function_args: arguments, params

## Call examples
1. "Estimate gas for transfer function"
2. "Check gas cost for approve call"
3. "How much gas needed for this function?"
