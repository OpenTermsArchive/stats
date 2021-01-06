#!/usr/bin/env python3

from datetime import datetime
import json
import logging
from pathlib import Path
import os

import click

from lib.cgus import CGUsDataset, CGU
logging.basicConfig(level=logging.INFO)

debug_mode = os.getenv("PY_DEBUG")

@click.command()
@click.option('-p', '--path', default="../CGUs/cgus-dataset/", help="Path to your local cgus-dataset folder.")
@click.option('-o', '--outdir', default="./reports", help="Output folder for the generated statistics.")
def cli(path, outdir):
    return main(path, outdir)

def main(path, outdir):
    logging.info(f"Generating stats for cgus dataset in {path}")
    dataset = CGUsDataset(path)

    all_stats = dict()

    index = 1
    for file_path in dataset.yield_all_md(ignore_rootdir=True):
        if debug_mode:
            logging.info(f"{index} - Handling: {file_path}")
        cgu = CGU(file_path, is_historical=True)
        all_stats[cgu.fullname] = cgu.to_dict()
        index += 1

    fileout = f"historical_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    _save_to_file(all_stats, outdir, fileout)

    logging.info(f"Saved stats in {outdir}/{fileout}")

def _save_to_file(data: dict, outdir, filename):
    out_path = Path(outdir)
    # create destination folder if it does not exist
    out_path.mkdir(parents=True, exist_ok=True)
    # save data
    full_path = out_path / filename
    full_path.write_text(json.dumps(data))

if __name__ == "__main__":
    cli()