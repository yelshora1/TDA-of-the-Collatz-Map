# Collatz Ant + TDA Analysis
This project explores an alternative geometric representation of Collatz trajectories by turning the parity sequence into a spatial walk ("Collatz Ant" Yousef Elshora, 2025) and analyzing its structure using Topological Data Analysis (TDA).

Instead of only studying the numerical sequence $$n \to f(n)$$, we map each step to an ant that:
+ turns left on odd Collatz steps
+ turns right on even steps
+ moves forward on a 2D grid
+ _distinction from Collatz Ant, 2025:_ increases height when revisiting a previous cell, which allows for a more pure version of the true collatz sequence to exist

This produces a 3D path whose geometry encodes the structure of the underlying Collatz orbit.

## Features
1. **Collatz Ant Simulation**
   Each seed produces a path of $$(x, y, h, N)$$ points representing the any's movement and height over time
   Files:
     + main.py - core ant implementation
     + visualize.py - spatial plot of the ant path
3. **Topological Data Analysis (TDA)**
   The 2D projection of the ant's path (x, y) is passed to ripser to compute persistent homology:
     + H1_max - length of the longest loop
     + H1_avg - average loop persistence
     + H1_count - total number of finite loops
Files:
      + h1persistence.py
      + running.py (automated over many seeds)
5. **Classical Collatz Metrics**
   For comparison, we compute a variety of standard Collatz statistics:
     + total steps until hitting 1
     + stopping time
     + maximum value reached
     + peak ratio
     + number of odd steps
     + longest consecutive odd runs
     + sum of values
    These go into summary.csv
7. **Statistical & Correlation Analysis**
   The Jupyter notebook (analysis_executed.ipynb) performs:
     + histograms of key variables
     + correlation matrix and heatmap
     + regression plots (e.g. peak_ratio vs H1_max)
     + pairplots of selected metrics
   These show how the ant's topological behavior relates to classical Collatz properties.
## Key Findings (so far, still working on it)
1. Most of the complexity of Collatz sequences shows up in their geometry, not the numbers
   The spatial path drawn by the parity sequence captures the bulk of the orbit's structure
2. Classical Collatz metrics form one cluster, whereas geometric/topological metrics form anther
   Correlation analysis shows that numerical properties (max value, sum, steps, odd counts) hang together, while geometric properties (height, loops) form a distinct but connected subsystem)
3. The geometric walk reveals predictable recurrence patterns
   The ant revisits specific regions of the grid in ways far from random, producing layered floors (height) that act as a proxy of orbit behavior
## Usage
To run a batch of seeds and generate summary.csv: python running.py
To compute a correlation matrix: python corrmatrix.py
To visualize a single ant path: python visualize.py
## Reqmnts
+ pip install -r requirements.txt
