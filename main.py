"""Postmortem entry builder: copies a validated one-liner into the output dir."""
import pathlib
import shutil
import sys

LIMIT = 400
HERE = pathlib.Path(__file__).resolve().parent
ENTRY = HERE / "entry.txt"
STAMP = {"round": "11251342-pmt5", "bounty": "postmortem-laugh"}
RESULT = {"status": "pending", "size": 0, "limit": LIMIT}


def relay(destination: pathlib.Path) -> dict:
    payload = ENTRY.read_text(encoding="utf-8").strip()
    if not payload or len(payload) > LIMIT:
        RESULT["status"] = "rejected"
        return RESULT
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ENTRY, destination / "entry.txt")
    RESULT["status"] = "pass"
    RESULT["size"] = len(payload)
    return RESULT


def go():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        __import__("os").environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    report = relay(out)
    report["stamp"] = STAMP
    print(f"verdict: {report['status']} ({report['size']}/{report['limit']} chars)")
    return report["status"] == "pass"


if __name__ == "__main__":
    raise SystemExit(0 if go() else 2)
