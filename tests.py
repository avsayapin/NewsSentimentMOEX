import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

def symmetric_mape(A, F):
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))

realized_vol = pd.read_csv('HF_data/realized_vol.csv')
realized_vol['date'] = pd.to_datetime(realized_vol['date'])
realized_vol = realized_vol.rename(columns={'squared_log_ret':'realized_vol'})


preds_val = pd.read_csv('preds_val (9).csv', encoding='utf32')
preds_val = preds_val.drop(columns="Unnamed: 0")
preds_val['date'] = pd.to_datetime(preds_val['date']).dt.normalize()
preds_val = preds_val.set_index('date')
preds_val = preds_val.sort_index(inplace=False)
preds_val = preds_val.drop_duplicates(subset=['text'])
preds_val = preds_val.resample('D').mean()
preds_val = preds_val.fillna(0)
print(preds_val)

moex_data = pd.read_csv('returns.csv')

moex_data['date'] = pd.to_datetime(moex_data['<DATE>'].astype(str),yearfirst=True,infer_datetime_format=True)

test_data = moex_data.merge(preds_val,how="inner",on='date')
test_data = test_data.dropna()

test_data = test_data.merge(realized_vol,how='inner',on='date')

garch = pd.read_csv('garch.csv')
garchx = pd.read_csv('garchx.csv')

print(test_data.head())
print(realized_vol.head())
print("REALIZED")
rmse = root_mean_squared_error(test_data['realized_vol'], garch['Sigma'])
mape = mean_absolute_percentage_error(test_data['realized_vol'],garch['Sigma'])
smape = symmetric_mape(test_data['realized_vol'],garch['Sigma'])

print("GARCH")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.4f}")
print(f"SMAPE: {smape:.4f}")

rmse = root_mean_squared_error(test_data['realized_vol'], garchx['Sigma'])
mape = mean_absolute_percentage_error(test_data['realized_vol'],garchx['Sigma'])
smape = symmetric_mape(test_data['realized_vol'],garchx['Sigma'])

print("GARCHX")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.4f}")
print(f"SMAPE: {smape:.4f}")


print("LOG_RET")
rmse = root_mean_squared_error(test_data['log_ret'], garch['Sigma'])
mape = mean_absolute_percentage_error(test_data['log_ret'],garch['Sigma'])


print("GARCH")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.4f}")

rmse = root_mean_squared_error(test_data['log_ret'], garchx['Sigma'])
mape = mean_absolute_percentage_error(test_data['log_ret'],garchx['Sigma'])

print("GARCHX")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.4f}")