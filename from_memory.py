import pandas as pd

last_year = {
    "Zac": ["Crystal"],
    "Lyd": ["TC"],
    "Em": ["Lyd"],
    "Nic": ["Jake"],
    "TC": ["Zac"],
    "Jon": ["Steph"],
    "Crystal": ["Nic"],
    "Jake": ["Em"],
    "Steph": ["Jon"]
}

pd.DataFrame(last_year).to_pickle("past_ass.pkl")