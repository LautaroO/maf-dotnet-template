"""Shared documentary coverage validation and stable source-audit identities."""
from __future__ import annotations
import hashlib
import json
import re
from datetime import date
from pathlib import Path


def release_key(tag: str) -> tuple[int, int, int]:
    if not isinstance(tag, str) or not re.fullmatch(r'dotnet-\d+\.\d+\.\d+', tag):
        raise ValueError(f'invalid .NET release tag: {tag!r}')
    return tuple(map(int, tag.removeprefix('dotnet-').split('.')))


def coverage_errors(data: object, root: Path) -> list[str]:
    errors = []
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        return ['coverage: expected object with schema_version 1']
    def record(value, field):
        if not isinstance(value, dict):
            errors.append(f'coverage.{field}: expected object'); return None
        try:
            key = release_key(value.get('release'))
        except ValueError as exc:
            errors.append(f'coverage.{field}: {exc}'); key = None
        raw = value.get('date')
        try:
            if not isinstance(raw, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw): raise ValueError()
            date.fromisoformat(raw)
        except ValueError:
            errors.append(f'coverage.{field}: invalid ISO date {raw!r}')
        evidence = value.get('evidence')
        if not isinstance(evidence, str) or not evidence:
            errors.append(f'coverage.{field}: missing evidence path')
        else:
            p = Path(evidence)
            if p.is_absolute() or not (root / p).resolve().is_relative_to(root.resolve()) or not (root / p).is_file():
                errors.append(f'coverage.{field}: evidence must be an existing contained file: {evidence}')
        return key
    full = record(data.get('full_verification'), 'full_verification')
    assessed = record(data.get('last_assessed_release'), 'last_assessed_release')
    if full and assessed and assessed < full: errors.append('coverage: assessed release precedes full verification')
    if isinstance(data.get('full_verification'),dict) and isinstance(data.get('last_assessed_release'),dict):
        if str(data['last_assessed_release'].get('date','')) < str(data['full_verification'].get('date','')):
            errors.append('coverage: assessed date precedes full verification')
    areas = data.get('areas')
    if not isinstance(areas, list) or not areas: return errors + ['coverage.areas: expected nonempty list']
    ids = set()
    for i, area in enumerate(areas):
        if not isinstance(area, dict): errors.append(f'coverage.areas[{i}]: expected object'); continue
        ident = area.get('id')
        if not isinstance(ident,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',ident) or ident in ids:
            errors.append(f'coverage.areas[{i}]: invalid/duplicate id')
        else: ids.add(ident)
        area_full = record(area.get('full_verification'), f'areas[{i}].full_verification')
        if area_full and full and area_full < full:
            errors.append(f'coverage.areas[{i}]: global full verification exceeds this area')
        if area_full and assessed and area_full > assessed: errors.append(f'coverage.areas[{i}]: unassessed full release')
        area_date=area.get('full_verification',{}).get('date') if isinstance(area.get('full_verification'),dict) else None
        assessed_date=data.get('last_assessed_release',{}).get('date') if isinstance(data.get('last_assessed_release'),dict) else None
        if isinstance(area_date,str) and isinstance(assessed_date,str) and area_date > assessed_date:
            errors.append(f'coverage.areas[{i}]: full verification date exceeds assessment')
        deltas=area.get('delta_reviews')
        if not isinstance(deltas,list): errors.append(f'coverage.areas[{i}].delta_reviews: expected list'); continue
        for j, delta in enumerate(deltas):
            field=f'areas[{i}].delta_reviews[{j}]'
            if not isinstance(delta,dict): errors.append(f'coverage.{field}: expected object'); continue
            end=record(delta | {'release':delta.get('to_release')},field)
            try: start=release_key(delta.get('from_release'))
            except ValueError as exc: errors.append(f'coverage.{field}: {exc}'); start=None
            if start and end and (start >= end or (area_full and start < area_full)):
                errors.append(f'coverage.{field}: invalid delta range')
            if end and assessed and end > assessed: errors.append(f'coverage.{field}: delta exceeds assessed release')
            delta_date=delta.get('date')
            if isinstance(delta_date,str) and isinstance(area_date,str) and isinstance(assessed_date,str) and not area_date <= delta_date <= assessed_date:
                errors.append(f'coverage.{field}: delta date outside assessed window')
            if not isinstance(delta.get('scope'),str) or not delta['scope'].strip(): errors.append(f'coverage.{field}: missing scope')
    return errors


def load_coverage(path: Path) -> dict:
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,ValueError) as exc:
        raise ValueError(f'coverage {path}: {exc}') from exc
    root=next((p for p in path.resolve().parents if (p/'plugin.json').is_file()),path.parent)
    errors=coverage_errors(data,root)
    if errors: raise ValueError('; '.join(errors))
    return data


def audit_fingerprint(findings: list[dict], assessed_release: str) -> str:
    """Dates, response order and transient diagnostics are deliberately excluded."""
    unique=sorted({json.dumps(f,sort_keys=True,separators=(',',':')) for f in findings})
    value=json.dumps({'assessed_release':assessed_release,'findings':unique},sort_keys=True,separators=(',',':'))
    return hashlib.sha256(value.encode()).hexdigest()
