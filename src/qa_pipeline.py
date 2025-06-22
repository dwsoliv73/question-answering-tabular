import pandas as pd
import os

from src.template_matcher import TemplateMatcher
from src.operation_executor import execute_operation


class QAPipeline:
    """
    Pipeline que conecta:
    Pergunta → Template → Execução no DataFrame → Resposta
    """

    def __init__(self, template_path):
        self.matcher = TemplateMatcher(template_path)

    def load_dataset(self, dataset_id):
        """
        Carrega o dataset parquet baseado no ID.
        """
        path = os.path.join("data", "raw", "competition", dataset_id, "all.parquet")
        df = pd.read_parquet(path)
        return df

    def answer_question(self, question, dataframe, column, value=None, group_a=None, group_b=None):
        """
        Recebe uma pergunta e retorna a resposta.
        """
        template = self.matcher.predict_template(question)
        print(f"\n🔍 Pergunta: {question}")
        print(f"🧠 Template identificado: {template}")

        result = execute_operation(
            template=template,
            dataframe=dataframe,
            column=column,
            value=value,
            group_a=group_a,
            group_b=group_b
        )

        print(f"✅ Resposta: {result}\n")
        return result


if __name__ == "__main__":
    dataset_id = "066_IBM_HR"
    pipeline = QAPipeline("src/templates.json")
    df = pipeline.load_dataset(dataset_id)
    print(df.head())

    pipeline.answer_question(
        question="Is our average employee older than 35?",
        dataframe=df,
        column="Age",
        value=35
    )
