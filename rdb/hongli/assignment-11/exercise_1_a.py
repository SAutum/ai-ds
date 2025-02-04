from test_exercise_1 import Node
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_tree(root: Node, filename: str) -> None:
    """
    Draw the tree and save the plot as the given filename.

    Parameters
    ----------
    root : Node
        Root node of the tree.
    filename : str
        Filename to save the plot.
    """

    plt.figure(figsize=(10, 10))
    draw_node(root)
    plt.savefig(filename)


def draw_node(node):

    # plot the bounds
    bounds = node.bounds
    x = bounds[0][0]
    y = bounds[0][1]
    width = bounds[1][0] - bounds[0][0]
    height = bounds[1][1] - bounds[0][1]
    rect = patches.Rectangle((x, y), width, height, linewidth=3,
                             edgecolor='black', facecolor=('gray', 0.3))
    plt.gca().add_patch(rect)

    # plot the points
    if node.children is not None:
        for child in node.children:
            draw_node(child)
    else:
        points = node.points
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        plt.scatter(x, y, edgecolor='black')
