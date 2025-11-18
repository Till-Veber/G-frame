import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def make_chart(directory):
    """Выводит png изображения рассматриваемых билдов"""
    # Чтение данных для графика
    path_empty = directory / "Empty_build.png"
    path_auto = directory / "Auto_build.png"
    path_overframe = directory / "Overframe_build.png"
    path_my = directory / "My_build.png"

    img_empty = mpimg.imread(path_empty)
    img_auto = mpimg.imread(path_auto)
    img_overframe = mpimg.imread(path_overframe)
    img_my = mpimg.imread(path_my)

    # Построение графика
    fig, axes = plt.subplots(2, 2, figsize=(14, 7))
    axes[0, 0].imshow(img_empty)
    axes[0, 1].imshow(img_auto)
    axes[1, 0].imshow(img_overframe)
    axes[1, 1].imshow(img_my)

    # Настройка графика
    fig.suptitle("Builds showcase")
    axes[0, 0].set_title("Empty build")
    axes[0, 1].set_title("Auto build")
    axes[1, 0].set_title("Overframe top build")
    axes[1, 1].set_title("My build")
    axes[0, 0].set_xticklabels([])
    axes[0, 0].set_yticklabels([])
    axes[0, 1].set_xticklabels([])
    axes[0, 1].set_yticklabels([])
    axes[1, 0].set_xticklabels([])
    axes[1, 0].set_yticklabels([])
    axes[1, 1].set_xticklabels([])
    axes[1, 1].set_yticklabels([])
    plt.tight_layout()

    # Отображение графика
    plt.show()