def get_version() -> str:
    from pathlib import Path
    try:
        return Path("VERSION").read_text().splitlines()[0]
    except:
        return "0.0"
