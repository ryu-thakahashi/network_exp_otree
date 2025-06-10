from pathlib import Path
import pandas as pd
import dtale

data_folder_path = Path().resolve() / "__temp_bots_Jun07_20h35m59.7s"
app_name = "network_pd.csv"

df = pd.read_csv(data_folder_path / app_name, index_col=0)
dtale.show(df)
