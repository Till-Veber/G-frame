import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график трафиков сайтов конкурентов"""
    # Загрузка данных
    path = directory / "builds_test.csv"
    df = pd.read_csv(path, sep=';')
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Уникальные билды
    builds = df['Build'].unique()

    # Подготовка данных для DPS (Damage per Second)
    # Группируем по Build и целой секунде
    df['Second'] = df['DateTime'].dt.floor('s')
    dps = df.groupby(['Build', 'Second'])['DamageHit'].sum().reset_index()

    # Подготовка данных для точечного графика (с распределением по Frame)
    # Для каждого Build и каждой секунды нормализуем Frame от 0 до 1 внутри секунды
    df['HitsInSecond'] = df.groupby(['Build', 'Second'])['Frame'].transform('count')
    df['HitOrderInSecond'] = df.groupby(['Build', 'Second']).cumcount()

    # Вычисляем точную позицию по оси X внутри секунды
    df['X'] = np.where(
        df['HitsInSecond'] == 1,
        df['Second'].astype('int64') / 1e9 + 0.5,  # середина секунды
        df['Second'].astype('int64') / 1e9 + (df['HitOrderInSecond'] + 0.5) / df['HitsInSecond']
    )

    # Построение графиков
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    axes = axes.flatten()

    for i, build in enumerate(builds):
        ax = axes[i]

        # Данные для текущего билда
        df_build = df[df['Build'] == build].copy()
        dps_build = dps[dps['Build'] == build].copy()

        # Точечный график: Damage Hits
        ax.scatter(df_build['X'], df_build['DamageHit'],
                   color='tab:red', s=20, alpha=0.7, label='Damage Hit')

        # Столбчатая диаграмма: DPS
        bar_x = dps_build['Second'].astype('int64') / 1e9 + 0.5  # центр столбца — середина секунды
        ax.bar(bar_x, dps_build['DamageHit'], width=0.9, alpha=0.3, color='tab:blue', label='Damage Per Second')

        # Аннотации киллов (где Kill == 1)
        kills_df = df_build[df_build['Kill'] == 1]
        for idx, row in kills_df.iterrows():
            ax.annotate('KILL',
                        xy=(row['X'], row['DamageHit']),
                        xytext=(row['X'] + 0.1, row['DamageHit'] + 500),
                        fontsize=8,
                        fontweight='bold',
                        color='darkblue',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', color='darkblue', lw=0.8),
                        ha='center')

        # Настройки осей
        ax.set_title(f'Build: {build}', fontsize=14)
        ax.set_xlabel('Time (seconds)', fontsize=10)
        ax.set_ylabel('Damage', fontsize=10)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

        # Форматирование оси X (время)
        if not dps_build.empty:
            start_sec = int(dps_build['Second'].iloc[0].timestamp())
            end_sec = int(dps_build['Second'].iloc[-1].timestamp()) + 1
            ax.set_xlim(start_sec - 0.5, end_sec + 0.5)
            ax.set_xticks(range(start_sec, end_sec + 1))
            ax.set_xticklabels(
                [pd.Timestamp.fromtimestamp(t).strftime('%H:%M:%S')
                 for t in range(start_sec, end_sec + 1)],
                rotation=45, ha='right'
            )

    plt.tight_layout()
    plt.suptitle('Damage analysis by build', fontsize=16, y=1.02)
    plt.show()