from pathlib import Path
from typing import List


def __try_cast_to_number(s: str):
    try:
        parent, stem = s.split("/")
        if stem.startswith("testcase") and stem[8:].isdigit():
            return parent + "/" + stem[:8] + stem[8:].zfill(4)
    except: pass
    return s


def get_list(path: str) -> List[Path]:
    return sorted(
        [name for name in Path(path).rglob("[ABC]/testcase*/")],
        key=lambda p: __try_cast_to_number(f"{p.parent.stem}/{p.stem}")
    )
