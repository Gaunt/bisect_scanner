import csv
import sys
import argparse
from .w3_scanner import PolygonScanner, EtherScanner, DECIMALS
from .base_scanner import SlowedDownScanner
from .plot import with_plot


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
    scan_step=1,
    scanner="Ethereum",
    contract_address=None,
    plot=False,
):
    assert account
    if scanner == "Polygon":
        scanner = PolygonScanner()
    elif scanner == "fake":
        scanner = SlowedDownScanner(delay=1)
    else:
        scanner = EtherScanner(contract_address=contract_address)
    if not end_block:
        end_block = scanner.last_block()
    balances = scanner.balance_history(
        account=account, start_block=start_block, end_block=end_block
    )
    if plot:
        balances = with_plot(balances, end_block)
    write_csv(balances)
    if plot:
        input("Press Enter to continue...")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="python -m bisecect_scanner",
        description="Outputs account balance history on stdout in the csv format,"
        " also can plot a chart with --plot switch.\n"
        f"Example: python -m bisect_scanner --account={SAMPLE_ADDRESS}",
    )
    parser.add_argument("--account", help="address")
    parser.add_argument("--contract_address", help="ERC20 contract address")

    parser.add_argument("--scan_step", type=int, default=1, help="scan step")
    parser.add_argument("--precission", type=int, default=3, help="precission")
    parser.add_argument(
        "--interpolation_step", type=int, default=0, help="interpolation step"
    )
    parser.add_argument(
        "--start_block", type=int, default=0, help="Start Block"
    )
    parser.add_argument("--end_block", type=int, help="End Block")
    parser.add_argument(
        "--polygon", action="store_true", help="Polygon (MATIC native Token)"
    )
    parser.add_argument(
        "--ethereum", action="store_true", help="Ethereum (default)"
    )
    parser.add_argument(
        "--fake",
        action="store_true",
        help="fake chain for testing purposes only",
    )
    parser.add_argument("--plot", action="store_true", help="plot chart")
    return parser.parse_args(argv)


if __name__ == "__main__":  # pragma: no cover
    args = parse_args(sys.argv[1:])
    main(
        args.account,
        start_block=args.start_block,
        end_block=args.end_block,
        interpolation_step=args.interpolation_step,
        precission=args.precission,
        scan_step=args.scan_step,
        scanner="Ethereum" if not args.polygon else "Polygon",
        contract_address=args.contract_address,
        plot=args.plot,
    )
