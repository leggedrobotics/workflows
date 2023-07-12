import argparse
from tqdm import tqdm
from time import time

import torch
from torch.utils.data.dataloader import DataLoader

parser = argparse.ArgumentParser("Benchmark a torch dataset by accessing its data through a torch dataloader.")
parser.add_argument("--num-workers", type=int, default=1, help="num_workers for dataloader")
parser.add_argument("--batch-size", type=int, default=32, help="batch size for dataloader")
args = parser.parse_args()


def main():
    dataset = None  # TODO: replace with your own dataset
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)
    bits = 0
    start = time()
    for x in tqdm(dataloader):
        for y in x:  # TODO: you might need to modify this to access all data (e.g. if x contains a dict)
            bits += y.numel() * torch.finfo(y.dtype).bits
    t = time() - start
    print(f"time: {t:.2f}s")
    print(f"data: {bits / 8 / 1024 / 1024 / 1024:.2f} GB")
    print(f"rate: {bits / 8 / 1024 / 1024 / 1024 / t:.3f} GB/s")


if __name__ == "__main__":
    main()
