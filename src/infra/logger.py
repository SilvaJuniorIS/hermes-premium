import json
from datetime import datetime


def log(run_id, level, message, **meta):
    print(f"[{datetime.now().isoformat()}][RUN {run_id}][{level}] {message} {json.dumps(meta, ensure_ascii=False)}")