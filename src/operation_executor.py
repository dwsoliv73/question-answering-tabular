import pandas as pd


def execute_operation(template, dataframe, column, value=None, group_a=None, group_b=None):
    """
    Executa a operação pandas com base no template reconhecido.
    """
    if template == "calculate average of column":
        return dataframe[column].mean()

    elif template == "get maximum of column":
        return dataframe[column].max()

    elif template == "check if maximum equals value":
        return dataframe[column].max() == value

    elif template == "check if maximum is negative":
        return dataframe[column].max() < 0

    elif template == "get most common value of column":
        return dataframe[column].value_counts().idxmax()

    elif template == "check if all values in column are equal":
        return dataframe[column].nunique() == 1

    elif template == "compare size of group A vs group B":
        count_a = dataframe[dataframe[column] == group_a].shape[0]
        count_b = dataframe[dataframe[column] == group_b].shape[0]
        return count_a > count_b

    elif template == "check if average is greater than value":
        return dataframe[column].mean() > value

    else:
        raise ValueError("Template não reconhecido.")
