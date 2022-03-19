import csv
import sys
import argparse
from .w3_scanner import PolygonScanner, DECIMALS


SAMPLE_ADDRESS = "0xCD6909C37CCEA877a5c8e9a3ffd69d9D9943409F"


def write_csv(events):
    fieldnames = ["block", "balance"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for block, balance in events:
        writer.writerow({"block": block, "balance": balance})
        sys.stdout.flush()


def main(
    account,
    precission=3,
    start_block=0,
    end_block=None,
    interpolation_step=0,
    scan_step=1
):
    scanner = PolygonScanner(account)
    write_csv(scanner.balance_history(start_block, end_block))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Account balance history.\n"
        f"Example: python -m bisect_scanner --account={SAMPLE_ADDRESS} --precission={DECIMALS}"
    )
    parser.add_argument("--account", help="address")
    parser.add_argument("--scan_step", type=int, default=1, help="scan step")
    parser.add_argument("--precission", type=int, default=3, help="precission")
    parser.add_argument(
        "--interpolation_step", type=int, default=0, help="interpolation step"
    )
    parser.add_argument(
        "--start_block", type=int, default=0, help="Start Block"
    )
    parser.add_argument("--end_block", type=int, help="End Block")
    parser.add_argument("--scanner", help="End Block")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(
        args.account,
        start_block=args.start_block,
        end_block=args.end_block,
        interpolation_step=args.interpolation_step,
        precission=args.precission,
        scan_step=args.scan_step,
    )
