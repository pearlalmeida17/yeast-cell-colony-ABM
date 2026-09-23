from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.storage.loaders import load_run_records


def animate_run(run_dir, save_as=None, interval=250):
    data = load_run_records(run_dir)
    rows = data["snapshots"]
    times = sorted({float(row["time"]) for row in rows})
    by_time = {time: [row for row in rows if float(row["time"]) == time] for time in times}
    if not times:
        raise ValueError("No snapshots found for animation")
    fig, ax = plt.subplots(figsize=(7, 7))

    def update(frame):
        ax.clear()
        from src.analysis.plots import plot_colony
        plot_colony(by_time[times[frame]], f"Yeast colony at {times[frame]:.1f} minutes", ax)

    animation = FuncAnimation(fig, update, frames=len(times), interval=interval, repeat=False)
    if save_as:
        animation.save(save_as, dpi=120)
    else:
        plt.show()
    return animation


if __name__ == "__main__":
    animate_run("data/runs/run_0001")
