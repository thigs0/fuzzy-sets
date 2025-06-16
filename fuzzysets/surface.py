import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Necessário para 3D
from alive_progress import alive_bar

def Surface(inference, X, Y, universe, out) -> None:
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    M = np.zeros([len(X), len(Y)])
    with alive_bar(len(X)*len(Y)) as bar:
        for i, value_x in enumerate(X):
            for j, value_y in enumerate(Y):
                M[i,j] = inference.infer([value_x, value_y], universe)#, universe)
                bar()
    ax.plot_surface(X, Y, M, cmap='viridis')

    # Adicione rótulos
    ax.set_title('Gráfico da superfície z = f(x, y)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ax




