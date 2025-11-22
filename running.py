"""Run CollatzAntGlobalHeight for seeds in a range, compute H1 persistence,
and write a summary CSV with metrics per seed.

Outputs: summary.csv with columns
  Seed, H1_max, H1_avg, H1_count, height_max
"""
import csv
import sys
from time import time
import numpy as np

try:
    from ripser import ripser
except Exception as e:
    print("Missing dependency 'ripser'. Install with: pip install ripser")
    raise

try:
    from main import CollatzAntGlobalHeight
except Exception:
    # If the module is named differently, try importing from the file directly
    from importlib.machinery import SourceFileLoader
    mod = SourceFileLoader("main", "main.py").load_module()
    CollatzAntGlobalHeight = mod.CollatzAntGlobalHeight


def compute_h1_metrics(points_2d):
    """Compute H1 metrics (max length, avg length, count) for a 2D point cloud.

    Returns (h1_max, h1_avg, h1_count)
    """
    pts = np.asarray(points_2d, dtype=float)
    if pts.shape[0] < 3:
        return 0.0, 0.0, 0

    res = ripser(pts, maxdim=1)
    dgm1 = res['dgms'][1]
    if dgm1.size == 0:
        return 0.0, 0.0, 0

    # Consider only finite death times (exclude infinite bars)
    finite_mask = np.isfinite(dgm1[:, 1])
    finite_bars = dgm1[finite_mask]
    if finite_bars.size == 0:
        return 0.0, 0.0, 0

    lengths = finite_bars[:, 1] - finite_bars[:, 0]
    return float(lengths.max()), float(lengths.mean()), int(len(lengths))


def main(seed_min=1, seed_max=200, steps=5000, summary_out='summary.csv'):
    results = []
    start_time = time()
    total = seed_max - seed_min + 1
    for i, seed in enumerate(range(seed_min, seed_max + 1), start=1):
        t0 = time()
        ant = CollatzAntGlobalHeight(seed)
        path = ant.run(steps)

        # Build 2D point cloud from the recorded path (x,y)
        points = [(x, y) for (x, y, h, N) in path]


        # Basic height metric from path
        h_max = max((h for (_x, _y, h, _N) in path), default=0)

        # Extract Collatz values sequence from the recorded path
        seq = [entry[3] for entry in path]

        # total_steps: number of steps until reaching 1 (exclude initial)
        total_steps = max(len(seq) - 1, 0)

        # stopping_time: first time the sequence dips below the starting n
        stopping_time = ''
        for idx, val in enumerate(seq):
            if idx == 0:
                continue
            if val < seed:
                stopping_time = idx
                break

        max_value = max(seq) if seq else 0
        odd_steps = int(sum(1 for v in seq if int(v) % 2 == 1))

        # longest consecutive odd-run
        max_consec = 0
        cur = 0
        for v in seq:
            if int(v) % 2 == 1:
                cur += 1
                if cur > max_consec:
                    max_consec = cur
            else:
                cur = 0

        sum_of_values = float(sum(seq))
        peak_ratio = float(max_value) / float(seed) if seed != 0 else 0.0

        h1_max, h1_avg, h1_count = compute_h1_metrics(points)

        results.append((seed, h1_max, h1_avg, h1_count, h_max,
                        total_steps, stopping_time, max_value,
                        odd_steps, max_consec, sum_of_values, peak_ratio))

        t1 = time()
        print(f"[{i}/{total}] Seed={seed}  points={len(points)}  H1_count={h1_count}  H1_max={h1_max:.6g}  height_max={h_max}  time={t1-t0:.2f}s")
        sys.stdout.flush()

    # Write summary CSV
    with open(summary_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Seed', 'H1_max', 'H1_avg', 'H1_count', 'height_max',
                         'total_steps', 'stopping_time', 'max_value',
                         'odd_steps', 'max_consecutive_odds', 'sum_of_values', 'peak_ratio'])
        writer.writerows(results)

    print(f"Wrote {summary_out} (processed {total} seeds in {time()-start_time:.1f}s)")


if __name__ == '__main__':
    # default range 1..n
    main(1, 5000, steps=5000, summary_out='summary.csv')
