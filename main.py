import json
import os
import pathlib
import sys

STORY = (
    "I asked the agent to delete dead code, and it removed the only script "
    "our nightly cron called, because nothing in the repo imported it. "
    "Six weeks of silent failures later, the sole person who noticed was a "
    "customer thanking support for the fix that no longer exists."
)
CEILING = 400
TAG = "pmt-1125"
ROUND = "nov-1125-a"


def check(story):
    body = story.strip()
    if len(body) < 1 or len(body) > CEILING:
        sys.exit("gate range 1..%d violated: %d" % (CEILING, len(body)))
    return body


def deliver():
    base = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    base.mkdir(parents=True, exist_ok=True)
    body = check(STORY)
    dest = base.joinpath("entry.txt")
    dest.write_bytes(body.encode("utf-8") + b"\n")
    print(json.dumps({"tag": TAG, "round": ROUND, "verdict": "written", "size": len(body), "dest": str(dest)}))


if __name__ == "__main__":
    deliver()
