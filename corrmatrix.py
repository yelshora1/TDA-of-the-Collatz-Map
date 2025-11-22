
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
	import seaborn as sns
	_HAS_SEABORN = True
except Exception:
	_HAS_SEABORN = False


def build_corr(csv_path='summary.csv', out_csv='summary_corr.csv', out_png='summary_corr.png'):
	if not os.path.exists(csv_path):
		raise FileNotFoundError(f"Input file not found: {csv_path}")

	df = pd.read_csv(csv_path)

	# Keep only numeric columns for correlation
	numeric = df.select_dtypes(include=[np.number])
	if numeric.shape[1] == 0:
		raise ValueError("No numeric columns found in summary CSV to correlate.")

	corr = numeric.corr()

	# Save correlation matrix as CSV
	corr.to_csv(out_csv)

	# Plot heatmap
	plt.figure(figsize=(max(6, corr.shape[0] * 0.6), max(6, corr.shape[1] * 0.6)))
	if _HAS_SEABORN:
		sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1)
	else:
		im = plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
		plt.colorbar(im)
		# annotate cells
		for (i, j), val in np.ndenumerate(corr.values):
			plt.text(j, i, f"{val:.3f}", ha='center', va='center', color='black', fontsize=8)
		plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
		plt.yticks(range(len(corr.index)), corr.index)

	plt.title('Correlation matrix')
	plt.tight_layout()
	plt.savefig(out_png, dpi=150)
	plt.close()

	return corr


if __name__ == '__main__':
	try:
		corr = build_corr('summary.csv', 'summary_corr.csv', 'summary_corr.png')
		print('Wrote summary_corr.csv and summary_corr.png')
		print(corr)
	except Exception as e:
		print('Error:', e)

