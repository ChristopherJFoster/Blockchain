import hashlib
import requests  # pylint: disable=F0401
from uuid import uuid4

import sys


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    # Get miner_id from my_id file, or create one if needed
    try:
        with open('my_id', 'r+') as f:
            miner_id = f.read()
            # if my_id is empty...
            if miner_id == '':
                # ...generate a uuid and remove the '-'s
                miner_id = ''.join(str(i)
                                   for i in [x for x in list(str(uuid4())) if x != '-'])
                # write the uuid to my_id
                f.write(miner_id)
        f.closed
    # If no my_id file...
    except FileNotFoundError:
        # ...create one
        with open('my_id', 'w') as f:
            # generate a uuid and remove the '-'s
            miner_id = ''.join(str(i)
                               for i in [x for x in list(str(uuid4())) if x != '-'])
            # write the uuid to my_id
            f.write(miner_id)
        f.closed

    print('miner_id: ', miner_id)

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof, "miner_id": miner_id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
