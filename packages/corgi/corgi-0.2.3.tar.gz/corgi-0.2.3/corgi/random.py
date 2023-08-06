import numpy as np
from scipy.stats import gaussian_kde


# TODO want to do this via multiple columns
# https://gist.github.com/spacelis/6088623
# https://stackoverflow.com/questions/15838733/stratified-sampling-in-numpy
# https://stackoverflow.com/questions/45486782/how-do-you-take-a-stratified-random-sample-from-a-pandas-dataframe-that-stratifi
def samplestrat(df, stratifying_column_name, num_to_sample, maxrows_to_est=10000, bw_per_range=50, eval_points=1000):
    '''
    Take a sample of dataframe df stratified by stratifying_column_name

    Source: https://stackoverflow.com/questions/45486782/how-do-you-take-a-stratified-random-sample-from-a-pandas-dataframe-that-stratifi
    '''
    strat_col_values = df[stratifying_column_name].values
    samplcol = (df.sample(maxrows_to_est) if df.shape[0] > maxrows_to_est else df)[stratifying_column_name].values
    vmin, vmax = min(samplcol), max(samplcol)
    pts = np.linspace(vmin,vmax, eval_points)
    kernel = gaussian_kde(samplcol, bw_method=float((vmax - vmin) / bw_per_range))
    density_estim_full = np.interp(strat_col_values, pts, kernel.evaluate(pts))
    return df.sample(n=num_to_sample, weights = 1 / (density_estim_full))
