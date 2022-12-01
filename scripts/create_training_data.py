import pandas as pd
import numpy as np
df_data_final  = pd.read_pickle('data/data_labels_final.pkl')
df_data_final= df_data_final[df_data_final.label != 'None']
df_data_final['double_conf'] = 1*(df_data_final['label']  == df_data_final['label_transformer'] )
df_contat = []
for label in np.unique(df_data_final.label.values):
    df_l_ = df_data_final[df_data_final.label == label]
    df_l_dc =  df_l_[df_l_['double_conf'] == 1]
    df_l_nc =  df_l_[df_l_['double_conf'] == 0]
    if len(df_l_dc) > 1000:
        df_c = df_l_dc.sample(1000)
    else:
        df_c = pd.concat([df_l_dc, df_l_nc.sample(min(len(df_l_nc),1000-len(df_l_dc)))])
    df_contat.append(df_c)
df_contat = pd.concat(df_contat)
df_contat.to_pickle('/data/training_data.pkl')