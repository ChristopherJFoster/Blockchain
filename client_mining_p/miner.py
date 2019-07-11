import hashlib
import requests  # pylint: disable=F0401
import time

import sys


# TODO: Implement functionality to search for a proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted

    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if guess_hash[:6] == "000000":
            print('client guess: ', guess)
            print('client guess_hash: ', guess_hash)
        return guess_hash[:6] == "000000"

    def proof_of_work(last_proof):
        proof = 0
        while valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(f'{node}/last_proof').json()['last_proof']
        print('last_proof: ', last_proof)
        print('Looking for new proof...')
        start = time.time()
        new_proof = proof_of_work(last_proof)
        end = time.time()
        print(
            f'...success! Time taken find new proof: {round((end - start), 2)} seconds')
        # TODO: When found, POST it to the server {"proof": new_proof}
        server_response = requests.post(
            f'{node}/mine', json={'sender': 'chris', 'proof': new_proof}).json()
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        print(server_response['message'])
        if server_response['message'] == 'New Block Forged':
            coins_mined += 1
            print('coins_mined:', coins_mined)
