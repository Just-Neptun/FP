import torch
import matplotlib.pyplot as plt


def show_galaxy(image: torch.Tensor, ax, title: str = "") -> None:
    # permute image shape: (C, H, W) -> (H, W, C) for matplotlib
    img = image.permute(1, 2, 0)

    # normalize to [0, 1]
    if img.max() > 1.0:
        img = img / 255

    # display
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")
    return


def show_first_galaxies_of_class(
    N: int, images: torch.Tensor, label_name: str, cols: int = 3
) -> None:
    rows: int = (N - 1) // cols + 1

    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 3 * rows))
    axes = axes.flatten()

    fig.suptitle(f"Class: {label_name}")
    for i in range(N):
        show_galaxy(images[i], axes[i])
    for j in range(N, len(axes)):
        axes[j].set_visible(False)

    plt.show(fig)

    return
