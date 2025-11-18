import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график трафика сайта WarframeBuilder"""
    # Чтение данных для графика
    path = directory / "warframebuilder.csv"
    df_1 = pd.read_csv(path, sep=';')
    df_1["DateTime"] = pd.to_datetime(df_1["DateTime"])

    path = directory / "overframe.csv"
    df_2 = pd.read_csv(path, sep=';')
    df_2["DateTime"] = pd.to_datetime(df_2["DateTime"])


    # Построение графика
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    axes[0].bar(df_1['DateTime'], df_1['Mobile Users'], label='Mobile Users', color='blue', linewidth=1)
    axes[0].bar(df_1['DateTime'], df_1['Desktop Users'], label='Desktop Users', color='red', linewidth=1, bottom=df_1['Mobile Users'])
    axes[1].bar(df_2['DateTime'], df_2['Mobile Users'], label='Mobile Users', color='blue', linewidth=1)
    axes[1].bar(df_2['DateTime'], df_2['Desktop Users'], label='Desktop Users', color='red', linewidth=1, bottom=df_2['Mobile Users'])

    # Настройка графика
    fig.suptitle("Competitors traffic (aug-oct 2025)")
    axes[0].set_title("Warframebuilder")
    axes[1].set_title("Overframe")
    axes[0].set_xlabel('Date')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_ylabel('Total number of unique users')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].set_xlabel('Date')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_ylabel('Total number of unique users')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()

    # Отображение графика
    plt.show()
