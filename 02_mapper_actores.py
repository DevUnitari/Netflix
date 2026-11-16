#!/usr/bin/env python3
import sys, csv
sys.stdin.reconfigure(encoding="utf-8"); sys.stdout.reconfigure(encoding="utf-8")
for row in csv.reader(sys.stdin):
    if not row or row[0] == "show_id":      # omite cabecera
        continue
    show_id, cast = row[0], row[4]          # cast = columna 5
    for actor in cast.split(","):
        actor = actor.strip()
        if actor:
            print(f"{actor}\t{show_id}")