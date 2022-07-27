import pandas as pd

def normalize_df(df:pd.DataFrame)->pd.DataFrame:
	"""
	Note: modifies in-place
	"""
	for column in df.columns:
		df[column] = df[column]/df[column].max()

	return df