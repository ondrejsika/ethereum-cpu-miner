# Ethereum CPU Miner

    Ondrej Sika <ondrej@ondrejsika.com>
    https://github.com/ondrejsika/ethereum-cpu-miner.git

Python implementation of Ethereum miner for __testing__ on __zero difficulty__ chains. This is __not__ a real miner.

## Install

```
git clone git@github.com:ondrejsika/ethereum-cpu-miner.git
cd ethereum-cpu-miner
virtualenv .env
.env/bin/pip install -r requirements.txt.lock
```

## Run

Mine 10 blocks

```
.env/bin/python miner.py https://127.0.0.1:8545 -n 10
```

## Help

```
.env/bin/python miner.py --help
```

