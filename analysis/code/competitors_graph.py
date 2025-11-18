import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график трафиков сайтов конкурентов"""
    # Чтение данных для графика
    path = directory / "overframe.csv"
    df_1 = pd.read_csv(path, sep=';')
    df_1["DateTime"] = pd.to_datetime(df_1["DateTime"])
    path = directory / "warframebuilder.csv"
    df_2 = pd.read_csv(path, sep=';')
    df_2["DateTime"] = pd.to_datetime(df_2["DateTime"])

    # Построение графика
    plt.figure(figsize=(14, 7))
    plt.plot(df_1['DateTime'], df_1['Total'], label='Total Overframe traffic', color='blue', linewidth=1)
    plt.plot(df_2['DateTime'], df_2['Total'], label='Total Warframebuilder traffic', color='red', linewidth=1)

    # Настройка графика
    plt.yscale('log')
    plt.title('Competitors traffic (aug-oct 2025)')
    plt.xlabel('Date')
    plt.ylabel('Total number of unique users')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Отображение графика
    plt.show()