import pandas as pd
import matplotlib.pyplot as plt

def make_chart(directory):
    """Строит график PAM-TAM-SAM модели рынка"""
    # Чтение данных для графика
    path_pam = directory / "steamdb_chart.csv"
    df_pam = pd.read_csv(path_pam, sep=';')
    df_pam["DateTime"] = pd.to_datetime(df_pam["DateTime"])
    path_tam_of = directory / "overframe.csv"
    df_tam_of = pd.read_csv(path_tam_of, sep=';')
    df_tam_of["DateTime"] = pd.to_datetime(df_tam_of["DateTime"])
    path_tam_wb = directory / "warframebuilder.csv"
    df_tam_wb = pd.read_csv(path_tam_wb, sep=';')
    df_tam_wb["DateTime"] = pd.to_datetime(df_tam_wb["DateTime"])
    path_sam = directory / "geography.csv"
    df_sam =pd.read_csv(path_sam, sep=';')

    # Вычисляем средний показатель PAM
    df_pam = df_pam[df_pam["DateTime"].dt.year == 2025]
    df_pam = df_pam.dropna(subset=['Players'])
    pam = df_pam["Players"].sum() / df_pam.shape[0]

    # Вычисляем средний показатель TAM
    tam_of = df_tam_of["Total"].sum() / df_tam_of.shape[0]
    tam_wb = df_tam_wb["Total"].sum() / df_tam_wb.shape[0]
    tam = min(pam, tam_of + tam_wb)

    # Вычисляем средний показатель SAM
    countries = ["Russia", "United Kingdom", "United States", "Canada"]

    geo_of = df_sam[df_sam["Site"] == "Overframe"]
    geo_of = geo_of[geo_of["Country"].isin(countries)]
    tam_of = tam_of * geo_of["Percentage"].sum() / 100
    geo_wb = df_sam[df_sam["Site"] == "Warframebuilder"]
    geo_wb = geo_wb[geo_wb["Country"].isin(countries)]
    tam_wb = tam_wb * geo_wb["Percentage"].sum() / 100
    sam = tam_of + tam_wb

    sam = round(sam)
    tam = round(tam)
    pam = round(pam)

    # Построение графика
    sizes = [sam, tam - sam, pam - tam]
    labels = [f'SAM ~ {sam} users/day', f'TAM-SAM ~ {tam - sam} users/day', f'PAM-TAM ~ {pam - tam} users/day']
    plt.figure(figsize=(8, 3))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')

    # Настройка графика
    plt.title(f'PAM-TAM-SAM model, PAM ~ {pam} users/day')
    plt.axis('equal')
    plt.tight_layout()

    # Отображение графика
    plt.show()