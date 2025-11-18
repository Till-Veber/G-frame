import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график игровой активности по данным SteamDB"""
    # Чтение данных для графика
    path = directory / "steamdb_chart.csv"
    df = pd.read_csv(path, sep=';')
    df = df.dropna(subset=['Players'])
    df = df.dropna(subset=['Average Players'])
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df_2025 = df[df["DateTime"].dt.year == 2025].copy()

    # Построение графика
    plt.figure(figsize=(14, 7))
    plt.plot(df_2025['DateTime'], df_2025['Players'], label='Total number of players', color='blue', linewidth=1)
    plt.plot(df_2025['DateTime'], df_2025['Average Players'], label='Average number of players', color='red', linewidth=1)

    # Настройка графика
    plt.title('Active players in 2025')
    plt.xlabel('Date')
    plt.ylabel('Number of players')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Дополнительные подписи
    max_idx = df_2025['Players'].idxmax()
    max_date = df_2025.loc[max_idx, 'DateTime']
    max_players = df_2025.loc[max_idx, 'Players']
    plt.annotate(
        'Update 39',
        xy=(max_date, max_players),
        xytext=(max_date + pd.Timedelta(hours=12), max_players + 1000),
        fontsize=8,
        fontweight='bold',
        color='darkblue',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7)
    )

    target_date = pd.Timestamp('2025-10-10 00:00:00')
    target_value = 85000
    plt.annotate(
        'Update 40',
        xy=(target_date, target_value),
        xytext=(target_date + pd.Timedelta(days=5), target_value + 3000),
        fontsize=8,
        fontweight='bold',
        color='darkblue',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7)
    )

    target_date = pd.Timestamp('2025-06-20 00:00:00')
    target_value = 97000
    plt.annotate(
        'TennoCon 2025',
        xy=(target_date, target_value),
        xytext=(target_date + pd.Timedelta(days=5), target_value + 3000),
        fontsize=8,
        fontweight='bold',
        color='darkblue',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7)
    )

    target_date = pd.Timestamp('2025-03-14 00:00:00')
    target_value = 100000
    plt.annotate(
        'Update 38.5',
        xy=(target_date, target_value),
        xytext=(target_date + pd.Timedelta(days=5), target_value + 3000),
        fontsize=8,
        fontweight='bold',
        color='darkblue',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7)
    )

    # Отображение графика
    plt.show()
