import matplotlib
matplotlib.use('Agg')    # non-interactive backend
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("points.csv")

plt.figure(figsize=(8,8))
plt.scatter(df.x, df.y, c=df.h, cmap="viridis", s=20)
plt.colorbar(label="Height (h)")
plt.title("Collatz Ant Spatial Path Colored by Height")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('collatz_path.png', dpi=150)
print('Wrote collatz_path.png')