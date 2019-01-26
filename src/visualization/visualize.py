import pandas as pd


def make_dataset(df, *, noise_low=0.25, noise_high=0.75):
    n_rows = df.shape[0]

    # Calculate score
    df['R2B_score'] = df.filter(like='R2B').apply('sum', axis=1)
    df['B2R_score'] = df.filter(like='B2R').apply('sum', axis=1)
    df['R2B_score_noise'] = df['R2B_score'] + np.random.uniform(low=noise_low, high=noise_high, size=n_rows)
    df['B2R_score_noise'] = df['B2R_score'] + np.random.uniform(low=noise_low, high=noise_high, size=n_rows)

    # Add color
    cate = df['NAICS_Code'].astype(str).str[:2]
    colors = viridis(len(cats.unique()))
    colormap = {val: colors[i] for i, val in enumerate(cats.unique())}
    df['color'] = [colormap[x] for x in cats]