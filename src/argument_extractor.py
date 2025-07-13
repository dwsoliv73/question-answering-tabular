import re

def extract_all_args(question, df):
    question_lower = question.lower()
    columns = df.columns.tolist()

    column = extract_column_from_keywords(question_lower, columns)
    filter_column, filter_value = extract_filter_conditions(question_lower)
    group_a = extract_group(question_lower, group="a")
    group_b = extract_group(question_lower, group="b")

    # Regras contextuais específicas
    column, filter_column = apply_contextual_rules(question_lower, column, filter_column, columns)

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
        "group_a": group_a,
        "group_b": group_b,
    }

def extract_column_from_keywords(question_lower, columns):
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
        "promotion": "YearsSinceLastPromotion",
        "helpful votes": "num_helpful_votes",
        "review text": "text",
        "room rating": "ratings",
        "performance": "PerformanceRating",
        "grade": "PerformanceRating",
        "review source": "via_mobile",
        "source": "via_mobile",
        "overall rating": "ratings",
        "review rating": "ratings",
        "review": "text",
        "date stayed": "date_stayed",
        "date": "date",
        "centenarian": "age",
        "older": "age",
        "years old": "age",
        "age": "age",
        "child": "children",
        "children": "children",
        "location": "region",
        "region": "region",




    }
    return next((col for key, col in keyword_map.items() if key in question_lower and col in columns), None)

def extract_filter_conditions(question_lower):
    if "research dept" in question_lower:
        return "Department", "Research"
    if "sales dept" in question_lower:
        return "Department", "Sales"
    return None, None

def apply_contextual_rules(question_lower, column, filter_column, columns):
    if "highest average" in question_lower:
        if "department" in question_lower:
            return "YearsAtCompany", "Department"
        if "travel" in question_lower:
            return "MonthlyIncome", "BusinessTravel"
    if "satisfied" in question_lower and "gender" in question_lower:
        return "JobSatisfaction", "Gender"
    if "most frequent field of education" in question_lower:
        return "EducationField", filter_column
    if "longest time" in question_lower and "promotion" in question_lower:
        return "YearsSinceLastPromotion", filter_column
    if "labelled helpful" in question_lower or "marked helpful" in question_lower:
        return "num_helpful_votes", filter_column

    return column, filter_column

def extract_best_column_match(question_lower, columns):
    normalized_columns = {col: col.lower().replace("_", " ").replace("(", "").replace(")", "") for col in columns}
    for col, norm_col in normalized_columns.items():
        words = norm_col.split()
        if all(word in question_lower for word in words):
            return col
    for col, norm_col in normalized_columns.items():
        if any(word in question_lower for word in norm_col.split()):
            return col
    # Se nenhuma palavra-chave direta for encontrada, procure por categorias genéricas
    if "attractions" in question_lower or "automotive" in question_lower:
        for col in columns:
            if "tier" in col.lower() or "name" in col.lower():
                return col
    return None

def extract_number(text):
    match = re.search(r"\d+\.?\d*", text)
    return float(match.group()) if match else None

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
