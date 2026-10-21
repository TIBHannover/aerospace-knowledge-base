"""Load the repository's synthetic configuration into the configured GraphDB repository."""
import json
from pathlib import Path

from main import import_coupled_kratos, save_onto

FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / 'examples'
    / 'synthetic'
    / 'coupled-system.json'
)


def main():
    with FIXTURE_PATH.open(encoding='utf-8') as fixture_file:
        data = json.load(fixture_file)

    import_coupled_kratos(data, 'Synthetic coupled system')
    save_onto()


if __name__ == '__main__':
    main()
