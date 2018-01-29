import argparse
import libethereumcpuminer

root_parser = argparse.ArgumentParser()
root_parser.add_argument('ETHEREUM_URL')
root_parser.add_argument('-n', '--num-blocks', type=int, default=1)

args = root_parser.parse_args()

miner = libethereumcpuminer.EthereumCpuMiner(args.ETHEREUM_URL)
miner.mine_n_blocks(args.num_blocks)
