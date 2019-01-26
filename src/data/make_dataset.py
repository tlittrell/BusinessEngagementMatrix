import pandas as pd


def read_and_merge_data(*, base_path="../../data/raw/"):
    df = pd.read_excel(base_path + 'RVMS_Current_Property_and_BIZ_Owner_List - vCurrent (1).xlsx',
                       sheet_name='Biz & Prop Owner MAIN list')

    naics = pd.read_excel(base_path + 'raw/2-6 digit_2017_Codes.xlsx')

    # Merge business and NAICS data
    df['NAICS Code'] = df['NAICS Code'].astype(object)
    df = df.merge(naics, left_on='NAICS Code', right_on='2017 NAICS US   Code', how='inner')

    # Clean up data
    df = df[pd.notnull(df['NAICS Code'])]
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df['NAICS_2_digit'] = df['NAICS_Code'].astype(str).str[:2]
