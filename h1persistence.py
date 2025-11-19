import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ripser import ripser
from persim import plot_diagrams

df = pd.read_csv("points.csv")
points = df[['x','y']].to_numpy(dtype=float)

result = ripser(points, maxdim=1)
diagrams = result['dgms']

lengths = diagrams[1][:,1] - diagrams[1][:,0]
print("H1 bars:")
for (b,d), L in zip(diagrams[1], lengths):
    print(f"birth={b:.3f}, death={d:.3f}, length={L:.3f}")

plot_diagrams(diagrams, show=False)
plt.savefig('h1_diagrams.png')
print('Wrote h1_diagrams.png')