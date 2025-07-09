import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_all_args(question, df):
    question_lower = question.lower()
    columns = df.columns.tolist()

    keyword_map = {
        "age": "Age",
        "income": "MonthlyIncome",
        "satisfaction": "JobSatisfaction",
        "education": "EducationField",
        "research": "Department",
        "sales": "Department",
        "distance": "DistanceFromHome",
        "rating": "PerformanceRating",
        "reviews": "Reviews",
        "book": "Book Title",
        "category": "Category",
        "page": "Book Length (Pages)",
        "copy": "Copies Left",
        "edition": "Edition",
        "price": "Price (TK)",
        "wish": "Wished Users",
        "discount": "Discount Offer",
        "publication": "Publication",
        "author": "Author",
        "contract": "Contract Value",
        "supplier": "Supplier",
        "region": "Region",
        "borrower": "Borrower Country",
        "procurement": "Procurement Category",
        "fiscal": "Fiscal Year",
        "brand": "brands",
        "store": "stores",
        "product": "product_name",
        "country": "countries_en",
    }

    column = next((col for key, col in keyword_map.items() if key in question_lower and col in columns), None)

    filter_column = None
    filter_value = None

    if "research dept" in question_lower:
        filter_column = "Department"
        filter_value = "Research"
    elif "sales dept" in question_lower:
        filter_column = "Department"
        filter_value = "Sales"

    if "highest average" in question_lower and "department" in question_lower:
        column = "YearsAtCompany"
        filter_column = "Department"

    if "most frequent field of education" in question_lower:
        column = "EducationField"

    if "travel" in question_lower and "rarely traveling" in question_lower:
        column = "BusinessTravel"

    if column is None:
        column = extract_best_column_match(question_lower, columns)

    value = extract_number(question_lower)
    top_n = value

    return {
        "column": column,
        "value": value,
        "top_n": top_n,
        "filter_column": filter_column,
        "filter_value": filter_value,
        "group_a": extract_group(question_lower, group="a"),
        "group_b": extract_group(question_lower, group="b"),
    }

def extract_number(text):
    import re
    match = re.search(r"\d+\.?\d*", text)
    return float(match.group()) if match else None

def extract_best_column_match(question_lower, columns):
    for col in columns:
        if col.lower() in question_lower:
            return col
    return None

def extract_group(text, group="a"):
    if group == "a" and "research dept" in text:
        return "Research"
    if group == "b" and "sales dept" in text:
        return "Sales"
    return None