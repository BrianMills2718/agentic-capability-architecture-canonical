#!/usr/bin/env python3
"""Record a possible reusable behavior without prematurely promoting it."""
from pathlib import Path
import argparse
import yaml

ROOT=Path(__file__).resolve().parents[1]
LOG=ROOT/'reuse_candidates.yml'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--id', required=True, help='stable id, e.g. scheduling.duration_approval')
    parser.add_argument('--project', required=True)
    parser.add_argument('--description', required=True)
    parser.add_argument('--evidence', action='append', default=[])
    args=parser.parse_args()

    data=yaml.safe_load(LOG.read_text(encoding='utf-8')) or {'schema_version':1,'candidates':[]}
    if any(item.get('id') == args.id for item in data['candidates']):
        raise SystemExit(f"candidate already exists: {args.id}")

    data['candidates'].append({
        'id': args.id,
        'project': args.project,
        'description': args.description,
        'status': 'observed',
        'evidence': args.evidence,
    })
    LOG.write_text(yaml.safe_dump(data, sort_keys=False), encoding='utf-8')
    print(f"Recorded reuse observation: {args.id}")


if __name__ == '__main__':
    main()
