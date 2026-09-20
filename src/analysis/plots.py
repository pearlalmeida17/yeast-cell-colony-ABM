import matplotlib.pyplot as plt


def plot_colony(cells, title):
    fig, ax = plt.subplots()

    for cell in cells:

        color = plt.cm.tab20(cell.subcolony_id % 20)
        circle = plt.Circle(cell.pos, cell.radius, color=color, alpha=0.7)
        
        ax.add_patch(circle)

    ax.set_aspect('equal')
    ax.autoscale()
    ax.set_title(title)
    plt.show()    


def plot_growth_curve(time_history, cell_count_history):
    
    fig, ax = plt.subplots()

    plt.plot(time_history, cell_count_history)

    ax.set_xlabel("Time (mins)")
    ax.set_ylabel("Number of cells")
    ax.set_title("Colony Growth Curve")

    plt.show()