import pandas as pd
import json

def responder_perguntas_hr(question, df):
  q_lower = question.lower()
  
  if 'average employee older than' in q_lower:
      val = int(q_lower.split('than ')[1].replace('?', ''))
      return "Yes" if df['Age'].mean() > val else "No"
  elif 'most frequent travel value rarely traveling' in q_lower:
      return "Yes" if df['BusinessTravel'].mode()[0] == 'Travel_Rarely' else "No"
  elif 'highest dailyrate equal to' in q_lower:
      value = int(q_lower.split('to ')[1].replace('?', ''))
      return "Yes" if int(df['DailyRate'].max()) == value else "No"
  elif 'highest dailyrate negative' in q_lower:
      return "Yes" if df['DailyRate'].max() < 0 else "No"
  elif 'research dept bigger than sales' in q_lower:
      research_count = df[df['Department'] == 'Research & Development'].shape[0]
      sales_count = df[df['Department'] == 'Sales'].shape[0]
      return "Yes" if research_count > sales_count else "No"
  elif 'highest rating given to any performance to 4' in q_lower:
      return "Yes" if df['PerformanceRating'].max() == 4 else "No"
  elif 'more employees who travel frequently than those who work in the hr department' in q_lower:
      freq_travel_count = df[df['BusinessTravel'] == 'Travel_Frequently'].shape[0]
      hr_dept_count = df[df['Department'] == 'Human Resources'].shape[0]
      return "Yes" if freq_travel_count > hr_dept_count else "No"
  elif 'average monthlyincome of employees affected by attrition less than those not affected' in q_lower:
      avg_income = df.groupby('Attrition')['MonthlyIncome'].mean()
      return "Yes" if avg_income['Yes'] < avg_income['No'] else "No"
  elif 'standard number of working hours the same across all employees' in q_lower:
      return "Yes" if df['StandardHours'].nunique() == 1 else "No"

  elif 'most common role' in q_lower:
      return df['JobRole'].mode()[0]
  elif 'department has the highest average yearsatcompany' in q_lower:
      return df.groupby('Department')['YearsAtCompany'].mean().idxmax()
  elif 'least common marital status' in q_lower:
      return df['MaritalStatus'].value_counts().idxmin()
  elif 'most frequent field of education' in q_lower:
      return df['EducationField'].mode()[0]
  elif 'travel category has the highest average income' in q_lower:
      return df.groupby('BusinessTravel')['MonthlyIncome'].mean().idxmax()
  elif 'gender is most satisfied with the job on average' in q_lower:
      return df.groupby('Gender')['JobSatisfaction'].mean().idxmax()
  elif 'most common score given work and life balance' in q_lower:
      return int(df['WorkLifeBalance'].mode()[0])
  elif 'educationfield do we employ the least' in q_lower:
      return df['EducationField'].value_counts().idxmin()
  elif 'average age of our employees' in q_lower:
      return float(round(df['Age'].mean(), 2))
  elif 'total number of different job roles' in q_lower:
      return int(df['JobRole'].nunique())
  elif 'maximum years someone has been at ibm' in q_lower:
      return int(df['YearsAtCompany'].max())
  elif 'median monthly income' in q_lower:
      return float(df['MonthlyIncome'].median())
  elif 'sum of the miles employees have to travel' in q_lower:
      return int(df['DistanceFromHome'].sum())
  elif 'average number of total working years for employees who are working in sales' in q_lower:
      return float(round(df[df['Department'] == 'Sales']['TotalWorkingYears'].mean(), 2))
  elif 'how many employees rate their satisfaction' in q_lower:
      score = int(q_lower.split('score of ')[1].replace('?', ''))
      return int(df[df['EnvironmentSatisfaction'] == score].shape[0])
  elif 'range (max - min) of yearsincelastpromotion' in q_lower.replace(" ", ""): 
      return int(df['YearsSinceLastPromotion'].max() - df['YearsSinceLastPromotion'].min())
  elif 'longest time someone has been without a promotion' in q_lower:
      return int(df['YearsSinceLastPromotion'].max())

  elif 'list the unique different grades received by anyone for their performance' in q_lower:
      return ", ".join([str(int(g)) for g in sorted(df['PerformanceRating'].unique())])
  elif 'list the amounts of the lowest 5 monthly incomes' in q_lower:
      return ", ".join([str(int(i)) for i in df['MonthlyIncome'].nsmallest(5).tolist()])
  elif 'list all the different education levels' in q_lower:
      return ", ".join([str(int(e)) for e in sorted(df['Education'].unique())])
  elif 'list the top 5 highest percentsalaryhike values' in q_lower:
      return ", ".join([str(int(h)) for h in df['PercentSalaryHike'].nlargest(5).tolist()])
  elif 'list the top 3 most common job roles' in q_lower:
      return ", ".join(df['JobRole'].value_counts().nlargest(3).index.tolist())
  elif 'list all the different (unique) values we use to classify the field of education' in q_lower:
      return ", ".join(df['EducationField'].unique().tolist())
  elif 'list the top 5 businesstravel categories' in q_lower:
      return ", ".join(df['BusinessTravel'].value_counts().nlargest(5).index.tolist())
  elif 'list all the unique possible values overtime can take' in q_lower:
      return ", ".join(df['OverTime'].unique().tolist())
  elif 'list the 4 most common joblevels' in q_lower:
      return ", ".join([str(int(l)) for l in df['JobLevel'].value_counts().nlargest(4).index.tolist()])
  elif 'list the 3 most common joblevels' in q_lower:
      return ", ".join([str(int(l)) for l in df['JobLevel'].value_counts().nlargest(3).index.tolist()])
      
  return None

def hr_ibm_to_json(df_data, df_questions):
  context = df_data.to_csv(index=False)
  questions_to_process = df_questions
  results = []

  for index, row in questions_to_process.iterrows():
    question = row['question']
    
    answer_text = str(responder_perguntas_hr(question, df_data))
    context = question + " " + answer_text
    answer_start = context.find(answer_text)
    # Pular perguntas sem lógica implementada
    # if answer_text is None or "não foi implementada" in answer_text:
    #     continue
    
    # --- ETAPA 3: ENCONTRAR O ÍNDICE DA RESPOSTA ---
    # Encontrar a posição inicial da resposta dentro do nosso contexto de texto


    # Apenas adicionar ao dataset se a resposta for encontrada no contexto
    if answer_start != -1:
      results.append({
          "context": context,
          "question": question,
          "answers": {
            "text": [answer_text],
            "answer_start": [answer_start]
          }
      })
    else:
      print(f"AVISO: A resposta '{answer_text}' para a pergunta '{question}' não foi encontrada no contexto CSV. O par será ignorado.")
      
  output_filename = 'dataset_qa_para_distilbert.json'
  
  final_output = {"data": results}
  
  with open(output_filename, 'w', encoding='utf-8') as f:
      json.dump(final_output, f, ensure_ascii=False, indent=4)

  print(f"\nProcesso concluído! Dataset salvo em '{output_filename}'.")
  print(f"Total de {len(results)} pares de QA válidos gerados.")