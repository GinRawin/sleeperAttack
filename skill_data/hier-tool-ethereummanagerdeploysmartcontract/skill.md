## Typical scenarios
- Deploy new DApp contract
- Launch custom smart contract
- Publish contract to blockchain

## Workflow
1. Get contract_bytecode and constructor_args from user
2. Optionally get gas_limit
3. Call EthereumManagerDeploySmartContract

## Parameters
- **contract_bytecode (required)**: Compiled bytecode
- **constructor_args (required)**: Constructor arguments as array
- **gas_limit (optional)**: Maximum gas for deployment

## Parameter aliases
- contract_bytecode: bytecode, compiled code
- constructor_args: constructor parameters, init args
- gas_limit: deployment gas, gas limit

## Call examples
1. "Deploy this bytecode with constructor arguments"
2. "Deploy my smart contract to Ethereum"
3. "Publish contract with initial parameters"
