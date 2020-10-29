#!/usr/bin/env python3

import json
import logging
from pathlib import Path
from datetime import datetime

import click

from lib.cgus import CGUsDataset, CGU

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('-p', '--path', default="../CGUs-versions", help="Path to your local CGUs-versions repository.")
@click.option('-o', '--outdir', default="./reports", help="Output folder for the generated statistics.")
def cli(path, outdir):
    return main(path, outdir)

def main(path, outdir):
    logging.info(f"Generating stats for data in {path}")
    dataset = CGUsDataset(path)

    all_stats = dict()

    for file_path in dataset.yield_all_md(ignore_rootdir=True):
        cgu = CGU(file_path)
        all_stats[cgu.fullname] = cgu.to_dict()

    fileout = f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
