"""Exercise lifecycle behavior using the actual packaged query and catalog."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def verify_lifecycle_queries(script: Path) -> None:
    env = dict(os.environ)
    env.pop('PEPLINK_DATA_PATH', None)

    def query(*args):
        result = subprocess.run(
            [sys.executable, str(script), *args], cwd=script.parent,
            env=env, check=True, capture_output=True, text=True,
        )
        return json.loads(result.stdout)

    legacy = query('show', 'Balance 310 5G')
    if not legacy['specifications'] or legacy['lifecycle']['new_solution_eligible']:
        raise SystemExit('Legacy specifications must remain available but ineligible for new solutions.')

    candidates = query('list', '--new-solutions')
    names = {device['name'] for device in candidates}
    if names & {'Balance 310 5G', 'Balance 580X', 'AP One Enterprise (HW2)', 'AP Pro AC'}:
        raise SystemExit('Legacy hardware leaked into packaged recommendation candidates.')
    if not {'Balance 310 5G (HW3)', 'Balance 580X (HW2)', 'AP One Enterprise'} <= names:
        raise SystemExit('Current hardware revisions were incorrectly excluded.')
    if not all(device['lifecycle']['new_solution_eligible'] for device in candidates):
        raise SystemExit('Ineligible candidate in packaged new-solution query.')

    variants = query('skus', '--new-solutions', 'BR1 Pro 5G')['sku_variants']
    if {v['sku'] for v in variants} != {'MAX-BR1-PRO-5GK-T-PRM', 'MAX-BR1-PRO-5GN-T-PRM'}:
        raise SystemExit('Packaged BR1 Pro 5G filtering did not respect radio variants.')
    legacy_sku = query('skus', '--find', 'MAX-BR1-PRO-5GH-T-PRM')
    if not legacy_sku.get('matches'):
        raise SystemExit('Legacy SKU lookup must remain available.')

    # These similar names previously mixed legacy and current SKU ownership.
    expected_owners = {
        'APO-ENTR': ('AP One Enterprise', True),
        'APO-RUG': ('AP One Rugged Legacy', False),
        'APP-AGN3': ('AP Pro AC', False),
        'BPL-580X-PRM': ('Balance 580X (HW2)', True),
        'MAX-BR1-PRO-GLTE-S-T-PRM': ('BR1 Pro (CAT-20)', True),
        'MAX-BR1-PRO-LTEA-W-T': ('BR1 Pro', False),
        'MAX-BR1-PRO-LTE-US-T': ('BR1 Pro', False),
        'MAX-ADP-5GH': ('MAX Adapter 5G (5GH)', False),
        'MAX-ADP-5GH-T': ('MAX Adapter 5G (5GH)', False),
        'ADP-5GY-T-PRM': ('5G Adapter', True),
        'APO-AGN2-IW-US': ('APO-AGN2-IW-US', False),
    }
    for sku, (name, eligible) in expected_owners.items():
        record = query('show', sku)
        if record['product_name'] != name or record['lifecycle']['new_solution_eligible'] != eligible:
            raise SystemExit(f'Packaged SKU mapping or lifecycle is incorrect for {sku}.')

    mini = query('skus', '--new-solutions', 'BR1 Mini')
    if not mini['sku_variants'] or any(
        v['sku'] in {'MAX-BR1-MINI-LTEA-W-T', 'MAX-BR1-MINI-LTE-US-T',
                     'MAX-BR1-MINI-LTEA-W', 'MAX-BR1-MINI-LTE-US'}
        for v in mini['sku_variants']
    ):
        raise SystemExit('Unresolved BR1 Mini hardware leaked into packaged SKU recommendations.')
