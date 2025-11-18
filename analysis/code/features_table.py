import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит таблицу фич в сравнении с конкурентами"""
    # Чтение данных для таблицы
    path = directory / "features.json"
    df = pd.read_json(path)
    # Транспонируем
    df = df.set_index('Name').T.reset_index()
    df = df.rename(columns={'index': 'Features'})

    # Построение таблицы
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_facecolor('#2E7D32')
            cell.set_text_props(color='white', weight='bold', size=12)
        elif key[1] == 0:
            cell.set_facecolor('#E8F5E8')
            cell.set_text_props(weight='bold')
        cell.set_edgecolor('gray')
        cell.set_linewidth(0.5)

    plt.title('Comparison of Warframe configurator functionality',
              pad=30, size=16, weight='bold')
    plt.tight_layout()
    plt.show()
