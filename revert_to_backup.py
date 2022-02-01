import pandas as pd
import numpy as np
import sys

backup_name = sys.argv[1]

backup = pd.read_excel(backup_name, engine='openpyxl', index_col=0)

backup = {x['giver']: x['recipient'] for x in backup.to_dict('records')}

past_ass = pd.read_pickle('past_ass.pkl')
past_ass = past_ass.drop(past_ass.shape[0] - 1).replace('', np.nan).dropna(axis=1)

past_ass = past_ass.append(backup, ignore_index=True)

past_ass.to_pickle('past_ass.pkl')