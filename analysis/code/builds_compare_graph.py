import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def make_chart(directory):
    """
    Строит два графика: DPS по билдам и количество киллов по билдам.

    Args:
        data_directory_path (str or Path-like): Путь к директории, содержащей файл builds_test.csv
    """
    # Загрузка данных
    path = (directory) / "builds_test.csv"
    df = pd.read_csv(path, sep=';')
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Подготовка данных для DPS
    # Группируем по Build и DateTime (секунда), суммируем DamageHit -> DPS
    df['Second'] = df['DateTime'].dt.floor('s')
    dps_data = df.groupby(['Build', 'Second'])['DamageHit'].sum().reset_index()
    # Переименуем для ясности
    dps_data.rename(columns={'DamageHit': 'DPS'}, inplace=True)

    # Подготовка данных для Kill Count
    # Суммируем количество киллов (Kill == 1) по каждому билду
    kill_counts = df[df['Kill'] == 1].groupby('Build')['Kill'].count().reindex(df['Build'].unique(), fill_value=0)

    # Построение графиков
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 7))

    # Левый график: DPS
    builds_in_data = df['Build'].unique()  # Сохраняем порядок билдов из данных
    for build in builds_in_data:
        build_data = dps_data[dps_data['Build'] == build]
        axes[0].plot(build_data['Second'], build_data['DPS'], label=build, marker='o', markersize=3, linewidth=1)

    axes[0].set_title('Damage per second by build')
    axes[0].set_xlabel('Time (seconds)')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_ylabel('Damage per second')
    axes[0].legend(title="Build")
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # Правый график: Kill Count
    builds_list = kill_counts.index.tolist()
    kills_list = kill_counts.values.tolist()

    bars = axes[1].bar(builds_list, kills_list, color='skyblue', edgecolor='black')
    axes[1].set_title('Kills by build')
    axes[1].set_xlabel('Build')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_ylabel('Number of kills')
    axes[1].grid(axis='y', linestyle='--', alpha=0.6)

    # Добавим числовые значения над столбцами
    for bar, kill_count in zip(bars, kills_list):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                     f'{kill_count}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Финальные настройки
    plt.tight_layout()
    plt.show()