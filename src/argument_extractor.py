import re

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
        "travel": "BusinessTravel",
        "role": "JobRole",
        "hours": "StandardHours",
        "marital": "MaritalStatus",
        "gender": "Gender",
        "life balance": "WorkLifeBalance",
        "years at ibm": "YearsAtCompany",
        "years": "TotalWorkingYears",
        "experience": "TotalWorkingYears",
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

    if "highest average" in question_lower and "travel" in question_lower:
        column = "MonthlyIncome"
        filter_column = "BusinessTravel"

    if "satisfied" in question_lower and "gender" in question_lower:
        column = "JobSatisfaction"
        filter_column = "Gender"

    if "most frequent field of education" in question_lower:
        column = "EducationField"

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
    match = re.search(r"\d+\.?\d*", text)
    return float(match.group()) if match else None

def extract_best_column_match(question_lower, columns):
    normalized_columns = {col: col.lower().replace("_", " ").replace("(", "").replace(")", "") for col in columns}

    for col, norm_col in normalized_columns.items():
        words = norm_col.split()
        if all(word in question_lower for word in words):
            return col

    for col, norm_col in normalized_columns.items():
        if any(word in question_lower for word in norm_col.split()):
            return col

    return None

def extract_group(text, group="a"):
    if group == "a" and "research" in text:
        return "Research"
    if group == "b" and "sales" in text:
        return "Sales"
    if group == "a" and "travel frequently" in text:
        return "Travel_Frequently"
    if group == "b" and "hr department" in text:
        return "Human Resources"
    return None
