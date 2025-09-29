import pandas as pd

def calculate_demographic_data(print_data=True):
    # Cargar dataset (coloca adult.data.csv en la misma carpeta)
    df = pd.read_csv('adult.data.csv', header=None, na_values=' ?', skipinitialspace=True)

    # Asignar nombres de columnas estándar del dataset 'adult'
    df.columns = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
        'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
        'hours-per-week', 'native-country', 'salary'
    ]

    # 1) Conteo por raza
    race_count = df['race'].value_counts()

    # 2) Edad promedio de hombres
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3) % con Bachelors
    total_count = len(df)
    percentage_bachelors = round((df['education'] == 'Bachelors').sum() / total_count * 100, 1)

    # 4) Porcentajes de riqueza según educación
    higher_edu_mask = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_edu = df[higher_edu_mask]
    lower_edu = df[~higher_edu_mask]

    # Evitar división por cero comprobando tamaños
    higher_education_rich = 0.0
    if len(higher_edu) > 0:
        higher_education_rich = round((higher_edu[higher_edu['salary'] == '>50K'].shape[0] / len(higher_edu)) * 100, 1)

    lower_education_rich = 0.0
    if len(lower_edu) > 0:
        lower_education_rich = round((lower_edu[lower_edu['salary'] == '>50K'].shape[0] / len(lower_edu)) * 100, 1)

    # 5) Horas mínimas trabajadas por semana
    min_work_hours = int(df['hours-per-week'].min())

    # 6) % de ricos entre los que trabajan el mínimo
    min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = 0.0
    if len(min_workers) > 0:
        rich_percentage = round((min_workers[min_workers['salary'] == '>50K'].shape[0] / len(min_workers)) * 100, 1)

    # 7) País con mayor % de personas que ganan >50K
    # Calculamos porcentaje por país de personas >50K
    country_counts = df.groupby('native-country').size()
    country_rich_counts = df[df['salary'] == '>50K'].groupby('native-country').size()
    # Evitar países que no aparecen en uno u otro
    percent_by_country = (country_rich_counts / country_counts * 100).dropna()
    if not percent_by_country.empty:
        highest_earning_country = percent_by_country.idxmax()
        highest_earning_country_percentage = round(percent_by_country.max(), 1)
    else:
        highest_earning_country = None
        highest_earning_country_percentage = 0.0

    # 8) Ocupación más común entre los que ganan >50K en India
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    if len(india_rich) > 0:
        top_IN_occupation = india_rich['occupation'].value_counts().idxmax()
    else:
        top_IN_occupation = None

    if print_data:
        print("Número de cada raza:\n", race_count, "\n")
        print("Edad promedio de los hombres:", average_age_men, "\n")
        print("Porcentaje con Bachelors:", percentage_bachelors, "\n")
        print("Porcentaje con educación avanzada que ganan >50K:", higher_education_rich, "\n")
        print("Porcentaje con educación no avanzada que ganan >50K:", lower_education_rich, "\n")
        print("Horas mínimas trabajadas por semana:", min_work_hours, "\n")
        print("Porcentaje de los que trabajan las horas mínimas y ganan >50K:", rich_percentage, "\n")
        print("País con mayor porcentaje de personas que ganan >50K:", highest_earning_country, "\n")
        print("Porcentaje en ese país:", highest_earning_country_percentage, "\n")
        print("Ocupación más común en India para >50K:", top_IN_occupation, "\n")

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

# Si querís probar el script directamente
if __name__ == "__main__":
    calculate_demographic_data(print_data=True)
