#!/usr/bin/env python3

import json
import re
from pathlib import Path
import pandas as pd


def main():
    data = {}
    for z in range(1, 4):
        path = Path(f"chantler/fine/{z:02d}.dat")
        df = pd.read_csv(
            path,
            sep=r"\s+",
            comment="#",
            usecols=[0, 1, 2],
            names=["E", "f1", "f2"],
        )
        data[z] = {
            "E": df["E"].to_list(),
            "f1": df["f1"].to_list(),
            "f2": df["f2"].to_list(),
        }
        with path.open(encoding="utf-8") as f:
            num_edges = 0
            edges = {}
            for line in f:
                if (match := re.search(r"(\d+) edges?.", line)):
                    num_edges = int(match.group(1))
                    if (num_edges == 1):
                        edges["K"] = float(line.split()[-1])
                elif "Relativistic correction estimate" in line:
                    assert num_edges == len(edges)
                    data[z]["edges"] = edges
                    print("Z =", z, "edges =", edges)
                    break
                elif (num_edges > 0):
                    for match in re.finditer(r"([A-Z] [^ ]*) +([^ ]+)", line):
                        edges[match.group(1).strip()] = float(match.group(2))

    with open("chantler.json", "w", encoding="utf-8") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
