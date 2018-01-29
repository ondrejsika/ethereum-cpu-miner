import binascii
from web3 import Web3, HTTPProvider
from ethereum.pow.ethpow import get_cache, hashimoto_light, TT64M1
from ethereum import utils


def hex_to_bin(data_hex):
    return binascii.unhexlify(data_hex[2:])


def bin_to_hex(data_bin):
    return '0x' + binascii.hexlify(data_bin)


class EthereumCpuMiner(object):
    def __init__(self, ethereum_url):
        self._conn = Web3(HTTPProvider(ethereum_url))

        self._mining_hash_hex = None
        self._mining_hash_bin = None
        self._target_bin = None
        self._block_number_int = None
        self._nonce_bin = None
        self._mix_digest_bin = None

    def get_work(self):
        self._mining_hash_hex, _, target_hex, block_number_hex = self._conn.eth.getWork()
        self._mining_hash_bin, self._target_bin, self._block_number_int = \
            hex_to_bin(self._mining_hash_hex), hex_to_bin(target_hex), int(block_number_hex, 16)

    def mine(self, start_nonce=0):
        cache = get_cache(self._block_number_int)
        nonce = start_nonce
        i = 0
        while True:
            i += 1
            bin_nonce = utils.zpad(utils.int_to_big_endian((nonce + i) & TT64M1), 8)
            o = hashimoto_light(self._block_number_int, cache, self._mining_hash_bin, bin_nonce)
            if o[b'result'] <= self._target_bin:
                assert len(bin_nonce) == 8
                assert len(o[b'mix digest']) == 32

                self._nonce_bin = bin_nonce
                self._mix_digest_bin = o[b'mix digest']
                return

    def submit_work(self):
        nonce_hex, mix_digest_hex = bin_to_hex(self._nonce_bin), bin_to_hex(self._mix_digest_bin)
        self._conn.manager.request_blocking("eth_submitWork", [nonce_hex, self._mining_hash_hex, mix_digest_hex])

    def mine_n_blocks(self, n=1):
        for _ in range(n):
            self.get_work()
            self.mine()
            self.submit_work()

