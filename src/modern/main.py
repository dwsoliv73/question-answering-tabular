import pandas as pd
import pyarrow.parquet as pq

from templates.ibm_hr import hr_ibm_to_json
from train import train
from answer import pipeline_qa

# table = pq.read_table("../../data/raw/competition/066_IBM_HR/all.parquet")
# df_data = table.to_pandas()
# df_questions = pd.read_csv("../../data/raw/competition/test_qa.csv")

# hr_ibm_to_json(df_data, df_questions)
# train()
pipeline_qa("./meu-modelo-distilbert-finetuned")