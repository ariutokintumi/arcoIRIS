import requests
import json


def list_abi_clones(abi_filename):
    """ List all contracts that have the same ABI as the given one. """
    # Set up the request parameters
    # Read the ABI from a local file
    with open(abi_filename) as f:
        abi = json.load(f)

    url = 'https://api.thegraph.com/subgraphs/name/'
    subgraph = 'graphprotocol/ethereum-mainnet'
    query = '''
        query {
            contracts(where: {abi: "%s"}) {
                address
            }
        }
    ''' % json.dumps(abi)

    # Send the request to The Graph API
    response = requests.post(url + subgraph, json={'query': query})
    response.raise_for_status()

    # Parse the response and extract the contract addresses
    data = response.json()
    contract_addresses = [contract['address'] for contract in data['contracts']]

    return contract_addresses


def list_children_contracts(contract_address):
    """ List all contracts that are children of the given contract. """
    # Set up the request parameters
    url = 'https://api.thegraph.com/subgraphs/name/'
    subgraph = 'ethereum-mainnet'
    query = '''
        query {
            contracts(where: {parent: "%s"}) {
                address
            }
        }
    ''' % contract_address

    # Send the request to The Graph API
    response = requests.post(url + subgraph, json={'query': query})
    response.raise_for_status()

    # Parse the response and extract the contract addresses
    data = response.json()
    contract_addresses = [contract['address'] for contract in data['contracts']]

    return contract_addresses

def main():
    contract_addresses = list_children_contracts('0xC6387E937Bcef8De3334f80EDC623275d42457ff')
    print(contract_addresses)


if __name__ == '__main__':
    main()
