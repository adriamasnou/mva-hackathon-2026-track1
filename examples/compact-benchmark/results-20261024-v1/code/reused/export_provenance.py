"""Check copied configuration against the values bound by an execution receipt."""
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(root, execution):
    root = Path(root)
    required = {'properties_sha256', 'properties_text', 'batch_sha256',
                'log_sha256', 'pre_inference_addenda'}
    missing = required - execution.keys()
    if missing:
        raise ValueError('Execution provenance is incomplete: '+', '.join(sorted(missing)))
    for name, key in [('runtime.properties', 'properties_sha256'),
                      ('batch.txt', 'batch_sha256'), ('execution.log', 'log_sha256')]:
        if sha(root/name) != execution[key]:
            raise ValueError('Execution-bound file changed: '+name)
    if (root/'runtime.properties').read_text() != execution['properties_text']:
        raise ValueError('Execution-bound property text changed')
    for field in ('design_records', 'pre_inference_addenda'):
        if not isinstance(execution.get(field, {}), dict):
            raise ValueError('Execution provenance must be an object: '+field)
        for name, record in execution.get(field, {}).items():
            if not isinstance(record, dict) or not {'sha256','content'} <= record.keys():
                raise ValueError('Execution-bound record is incomplete: '+name)
            path = (root/name).resolve()
            if not path.is_relative_to(root.resolve()) or sha(path) != record['sha256']:
                raise ValueError('Execution-bound design/addendum changed: '+name)
            if json.loads(path.read_text()) != record['content']:
                raise ValueError('Execution-bound JSON content changed: '+name)
