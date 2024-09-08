import pandas as pd

preds = pd.read_csv('preds (12).csv', encoding='utf32')
preds = preds.drop(columns="Unnamed: 0")
preds['date'] = pd.to_datetime(preds['date']).dt.normalize()
preds = preds.set_index('date')
preds = preds.sort_index(inplace=False)
preds = preds.drop_duplicates(subset=['text'])
preds = preds.resample('D').mean()
preds = preds.fillna(0)

preds_val = pd.read_csv('preds_val (9).csv', encoding='utf32')
preds_val = preds_val.drop(columns="Unnamed: 0")
preds_val['date'] = pd.to_datetime(preds_val['date']).dt.normalize()
preds_val = preds_val.set_index('date')
preds_val = preds_val.sort_index(inplace=False)
preds_val = preds_val.drop_duplicates(subset=['text'])
preds_val = preds_val.resample('D').mean()
preds_val = preds_val.fillna(0)
print(preds_val)

preds = pd.concat([preds,preds_val])
print(preds.tail())

moex_data = pd.read_csv('returns.csv')

moex_data['date'] = pd.to_datetime(moex_data['<DATE>'].astype(str),yearfirst=True,infer_datetime_format=True)

test_data = moex_data.merge(preds,how="inner",on='date')
test_data = test_data.dropna()
test_data = test_data.set_index('date')
test_data = test_data.sort_index(inplace=False) 
test_data[['log_ret','prob_1']].to_csv('test_data.csv',index=False)
