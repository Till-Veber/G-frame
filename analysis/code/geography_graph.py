import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график географического распределения трафика конкурентов"""
    # Чтение данных для графика
    path = directory / "geography.csv"
    df = pd.read_csv(path, sep=';')
    df_1 = df[df["Site"] == "Warframebuilder"].copy() # География Warframebuilder
    df_1 = pd.concat([df_1[df_1['Country'] == 'Russia'], # "Сортируем", чтобы Россия была в начале
                      df_1[df_1['Country'] != 'Russia']],
                     ignore_index=True)
    df_2 = df[df["Site"] == "Overframe"].copy() # География Overframe
    df_2 = pd.concat([df_2[df_2['Country'] == 'Russia'], # "Сортируем", чтобы Россия была в начале
                      df_2[df_2['Country'] != 'Russia']],
                     ignore_index=True)

    # Готовим данные для объединённого графика географии с учётом трафика сайтов
    path = directory / "warframebuilder.csv"
    df_wb = pd.read_csv(path, sep=';') # Трафик Warframebuilder
    path = directory / "overframe.csv"
    df_of = pd.read_csv(path, sep=';') # Трафик Overframe
    total_wb_users = df_wb['Total'].iloc[-1] # Берём самые последние данные о трафике
    df_1["Absolute_Users"] = (df_1["Percentage"] / 100) * total_wb_users # Высчитываем абсолютные показатели географии
    total_of_users = df_of['Total'].iloc[-1] # Берём самые последние данные о трафике
    df_2["Absolute_Users"] = (df_2["Percentage"] / 100) * total_of_users # Высчитываем абсолютные показатели географии

    # Делаем комбинированные данные для объединённого графика
    total_combined_users = total_wb_users + total_of_users
    df_merged = pd.merge(df_1[["Country", "Absolute_Users"]],
                         df_2[["Country", "Absolute_Users"]],
                         on="Country",
                         how="outer",
                         suffixes=('_WB', '_OF'))
    df_merged = df_merged.fillna(0)
    df_merged["Total_Users"] = df_merged["Absolute_Users_WB"] + df_merged["Absolute_Users_OF"]
    df_merged["Final_Percentage"] = (df_merged["Total_Users"] / total_combined_users) * 100
    df_merged = df_merged.sort_values(by="Final_Percentage", ascending=False)
    threshold = 2.0  # Порог в процентах для попадания на график
    df_merged["Display_Country"] = df_merged.apply(
        lambda row: row["Country"] if row["Final_Percentage"] >= threshold else "Other", axis=1
    )
    df_final = df_merged.groupby("Display_Country")["Final_Percentage"].sum().reset_index()
    df_final = df_final.sort_values(by="Final_Percentage", ascending=False)
    df_final = pd.concat([df_final[df_final["Display_Country"] == 'Russia'], # "Сортируем", чтобы Россия была в начале
                      df_final[df_final["Display_Country"] != 'Russia']],
                     ignore_index=True)

    # Построение графика
    fig, axes = plt.subplots(1, 3, figsize=(14, 7))
    explode_wb = [0.1 if country == 'Russia' else 0 for country in df_1['Country']]
    axes[0].pie(df_1['Percentage'], labels=df_1['Country'], explode=explode_wb, autopct='%1.1f%%', startangle=90)
    explode_of = [0.1 if country == 'Russia' else 0 for country in df_2['Country']]
    axes[1].pie(df_2['Percentage'], labels=df_2['Country'], explode=explode_of, autopct='%1.1f%%', startangle=90)
    explode_final = [0.1 if country == 'Russia' else 0 for country in df_final['Display_Country']]
    wedges, texts, autotexts = axes[2].pie(
        df_final['Final_Percentage'],
        labels=df_final['Display_Country'],
        autopct='%1.1f%%',
        explode=explode_final,
        textprops={'fontsize': 10},
        startangle=90
    )

    # Настройка графика
    fig.suptitle("Competitors traffic geography")
    axes[0].set_title("Warframebuilder")
    axes[1].set_title("Overframe")
    axes[2].set_title("Total")
    plt.tight_layout()

    # Отображение графика
    plt.show()