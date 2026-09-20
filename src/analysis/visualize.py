import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config.base_config import simulparams
from simulation.engine import run_simulation


def animate_simulation(save_as: str | None = None):
    # 1. Run the simulation and get trajectories
    positions = run_simulation()  # dict: i -> array[t, 2]
    cell_ids = sorted(positions.keys())
    timesteps = positions[cell_ids[0]].shape[0]

    # 2. Extract positions to set axis limits nicely
    all_x = []
    all_y = []
    for i in cell_ids:
        all_x.extend(positions[i][:, 0])
        all_y.extend(positions[i][:, 1])

    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)

    pad = 1.0
    x_min -= pad
    x_max += pad
    y_min -= pad
    y_max += pad

    # 3. Figure + scatter
    fig, ax = plt.subplots()
    scat = ax.scatter(
        [positions[i][0, 0] for i in cell_ids],
        [positions[i][0, 1] for i in cell_ids],
        s=100
    )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("x (microns)")
    ax.set_ylabel("y (microns)")
    ax.set_title("Cell positions at t = 0.00000 min")

    # 4. Update per frame
    def update(frame: int):
        # Debug print: this should print 0, 1, 2, ..., 9 in your terminal
        print(f"Frame {frame}")

        xs = [positions[i][frame, 0] for i in cell_ids]
        ys = [positions[i][frame, 1] for i in cell_ids]
        scat.set_offsets(list(zip(xs, ys)))

        time_min = frame * simulparams.dt  # in minutes
        ax.set_title(f"Cell positions at t = {time_min:.5f} min")

        return scat,

    # 5. Animation – explicit list of frame indices, no blitting
    frame_indices = list(range(timesteps))
    anim = FuncAnimation(
        fig,
        update,
        frames=frame_indices,
        interval=500,
        blit=False,
        repeat=False
    )

    plt.show()


if __name__ == "__main__":
    animate_simulation()
