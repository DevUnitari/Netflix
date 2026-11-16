#!/usr/bin/env python3
import sys
sys.stdin.reconfigure(encoding="utf-8"); sys.stdout.reconfigure(encoding="utf-8")
actual, ids = None, set()
for line in sys.stdin:
    actor, sid = line.rstrip("\n").split("\t", 1)
    if actor != actual:
        if actual is not None:
            print(f"{actual}\t{len(ids)}")
        actual, ids = actor, set()
    ids.add(sid)
if actual is not None:
    print(f"{actual}\t{len(ids)}")