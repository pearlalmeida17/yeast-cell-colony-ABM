from __future__ import annotations

import matplotlib.pyplot as plt


def plot_colony(records, title="Yeast colony", ax=None):
    if ax is None:
        _, ax = plt.subplots()

    subcolony_ids = sorted({
        record["subcolony_id"]
        for record in records
        if record.get("subcolony_id") is not None
    })

    # Provides up to 20 visually distinct categorical colors
    color_map = {
        subcolony_id: plt.cm.tab20(index % 20)
        for index, subcolony_id in enumerate(subcolony_ids)
    }

    for record in records:
        subcolony_id = record.get("subcolony_id")

        if subcolony_id is None:
            color = "black"
        else:
            color = color_map[subcolony_id]

        ax.add_patch(
            plt.Circle(
                (record["x"], record["y"]),
                record["R"],
                color=color,
                alpha=0.8,
                linewidth=0.2
            )
        )

    ax.set_aspect("equal")
    ax.autoscale()
    ax.set_title(title)
    ax.set_xlabel("x (µm)")
    ax.set_ylabel("y (µm)")

    return ax

def plot_metric_history(metrics, field, ylabel=None, ax=None):
    if ax is None:
        _, ax = plt.subplots()
    ax.plot([row["time"] for row in metrics], [row[field] for row in metrics], marker="o")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel(ylabel or field.replace("_", " ").title())
    ax.grid(alpha=0.25)
    return ax


def plot_growth_curve(metrics, ax=None):
    return plot_metric_history(metrics, "cell_count", "Number of cells", ax)


def plot_paper_metrics(metrics):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    plot_growth_curve(metrics, axes[0, 0])
    plot_metric_history(metrics, "expanse", "Expanse (µm)", axes[0, 1])
    plot_metric_history(metrics, "sparsity", "Sparsity", axes[1, 0])
    plot_metric_history(metrics, "connectivity", "Colony connectivity", axes[1, 1])
    fig.tight_layout()
    return fig
