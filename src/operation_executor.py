import pandas as pd

def execute_operation(template, df, column, value=None, top_n=None,
                      filter_column=None, filter_value=None,
                      group_a=None, group_b=None):
    try:
        if template == "calculate average of column":
            return df[column].mean()

        elif template == "get maximum of column":
            return df[column].max()

        elif template == "get minimum of column":
            return df[column].min()

        elif template == "calculate median of column":
            return df[column].median()

        elif template == "calculate range of column":
            return df[column].max() - df[column].min()

        elif template == "sum column":
            return df[column].sum()

        elif template == "check if maximum equals value":
            return df[column].max() == value

        elif template == "check if maximum is negative":
            return df[column].max() < 0

        elif template == "get most common value of column":
            return df[column].mode().iloc[0] if not df[column].mode().empty else "Invalid"

        elif template == "get least common value of column":
            counts = df[column].value_counts()
            return counts.idxmin() if not counts.empty else "Invalid"

        elif template == "check if all values in column are equal":
            return df[column].nunique() == 1

        elif template == "compare size of group A vs group B":
            if not group_a or not group_b or not filter_column:
                return "Invalid"
            count_a = df[df[filter_column] == group_a].shape[0]
            count_b = df[df[filter_column] == group_b].shape[0]
            return count_a > count_b

        elif template == "check if average is greater than value":
            if value is None:
                return "Invalid"
            return df[column].mean() > value

        elif template == "list values in column":
            return str(df[column].tolist())

        elif template == "list top-n values in column":
            if top_n is None:
                return "Invalid"
            return str(df[column].dropna().value_counts().head(int(top_n)).index.tolist())

        elif template == "filter then get top-n":
            if filter_column and filter_value and top_n:
                filtered = df[df[filter_column].astype(str).str.contains(str(filter_value), case=False, na=False)]
                sorted_df = filtered.sort_values(by=column, ascending=False)
                return str(sorted_df[column].head(int(top_n)).tolist())
            return "Invalid"

        elif template == "count distinct values of column":
            return df[column].nunique()

        else:
            return "Invalid"

    except Exception as e:
        return f"Error: {e}"
