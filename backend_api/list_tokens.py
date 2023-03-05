import json

import requests

KEY = 'ckey_abe5b7ee0d6d476cb68ab2f2e63'



def get_nft_metadata(contract_address):
    """ Get the metadata for all NFTs in a given contract using the Covalent API."""
    page = 0
    res = []
    base_url = "https://api.covalenthq.com/v1/{chainName}/nft/{contractAddress}/metadata/"
    while 1:
        headers = {
            "accept": "application/json",
            "x-api-key": KEY
        }

        url = base_url.format(chainName="eth-mainnet",
                              contractAddress=contract_address,
                              )

        if page > 0:
            url += "?page-number={}".format(page)

        response = requests.get(url, headers=headers, auth=(KEY, ''))
        data = response.json()
        if not data['data']['items'] or data.get('error'):
            break

        res.extend(data['items'])
        page += 1
    return res


def save_jsonl(data, filename):
    """ Save a list of JSON objects to a JSON Lines file."""
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def main():
    res = get_nft_metadata('0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d')
    save_jsonl(res, 'nft.jsonl')


if __name__ == '__main__':
    main()
