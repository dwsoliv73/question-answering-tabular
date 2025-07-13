import pandas as pd
import pyarrow.parquet as pq

from templates.ibm_hr import hr_ibm_to_json
from train import train
from prediction import pipeline_qa

table = pq.read_table("../../data/raw/competition/066_IBM_HR/all.parquet")
df_data = table.to_pandas()
df_questions = pd.read_csv("../../data/raw/competition/test_qa.csv")
df_questions = df_questions[df_questions.iloc[:, 1].str.contains("066_IBM_HR", na=False)]

context = hr_ibm_to_json(df_data, df_questions)
train('dataset_qa_066.json')
pipeline_qa("./meu-modelo",context)