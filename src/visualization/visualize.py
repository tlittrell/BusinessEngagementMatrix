import numpy as np
from bokeh.models.tickers import FixedTicker
from bokeh.palettes import viridis
from bokeh.plotting import figure, ColumnDataSource


def make_dataset(df, business_types=None, *, noise_low=0.25, noise_high=0.75, naics_digits=2, dot_radius=0.05):
    df = df.copy()

    if business_types is None:
        pass
    else:
        df = df[df['2017_NAICS_US_Title'].isin(business_types)]

    # Calculate score
    n_rows = df.shape[0]
    df['R2B_score'] = df.filter(like='R2B').apply('sum', axis=1)
    df['B2R_score'] = df.filter(like='B2R').apply('sum', axis=1)
    df['R2B_score_noise'] = df['R2B_score'] + np.random.uniform(low=noise_low, high=noise_high, size=n_rows)
    df['B2R_score_noise'] = df['B2R_score'] + np.random.uniform(low=noise_low, high=noise_high, size=n_rows)

    # Add color
    naics_categories = df['NAICS_Code'].astype(str).str[:naics_digits]
    colors = viridis(len(naics_categories.unique()))
    colormap = {val: colors[i] for i, val in enumerate(naics_categories.unique())}
    df['color'] = [colormap[x] for x in naics_categories]

    # Add circle radius
    df['radius'] = dot_radius

    return ColumnDataSource(df)

def make_plot(src):
    tooltips = [
        ("index", "$index"),
        ("Business", "@Business_Name"),
        ("R2B: Email sponsorship/promotion", "@R2B_email_sponsorship_promotion"),
        ("R2B: Provide Resources", "@R2B_provide_resources"),
        ("R2B: Liason", "@R2B_liason"),
        ("B2R: Event participation", "@B2R_event_participation"),
        ("B2R: Sponsorship/donation", "@B2R_sponsorship_donation"),
        ("B2R: Share info", "@B2R_share_business_information"),
        ("B2R: Volunteer", "@B2R_volunteer"),
        ("Use RVMS resources", "@B2R_use_RVMS_resources"),
        ("Industry", "@2017_NAICS_US_Title"),
        ("NAICS Code", "@NAICS_Code"),
    ]

    p = figure(title="Business Engagement Matrix", x_axis_label='Business to RVMS', y_axis_label='RVMS to Business',
               x_range=(0, 6), y_range=(0, 4), tooltips=tooltips)

    # Ticks
    p.xaxis.ticker = FixedTicker(ticks=[1, 2, 3, 4, 5])
    p.yaxis.ticker = FixedTicker(ticks=[1, 2, 3, 4])

    # Grid lines
    p.xgrid.ticker = FixedTicker(ticks=[1, 2, 3, 4, 5])
    p.ygrid.ticker = FixedTicker(ticks=[1, 2, 3, 4])

    p.scatter(x='B2R_score_noise', y='R2B_score_noise', fill_color='color', radius='radius',
              source=src)

    return p
