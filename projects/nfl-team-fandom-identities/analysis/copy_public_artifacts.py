#!/usr/bin/env python3
"""Copy selected aggregate artifacts after rendering the Quarto book."""
from pathlib import Path
import shutil

project = Path(__file__).resolve().parents[1]
public = project.parents[1] / 'website/projects/nfl-team-fandom-identities/report/artifacts'
public.mkdir(parents=True, exist_ok=True)
for name in (
    'rq1_zenodo_20260911.json', 'rq1_weighted_zenodo_20260911.json',
    'acquisition_20260911.json', 'rq1_retrieved_20260911.json',
    'acs_target_check_20260911.json',
):
    shutil.copy2(project / 'results' / name, public / name)
