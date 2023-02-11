def plot3d_cbar(X = [[1,2,3],[2,3,4],[1,2,3]], 
    ColorPoints = { 'Target': [0,1,2], 'Ticks': [0,1,2], 'TicksLabels' : ["setosa", "versicolor", "virgninica"]},
    Text = { 'Title': "First three PCA directions", 'XLabel': "1st eigenvector", 'YLabel': "2nd eigenvector", 'ZLabel': "3rd eigenvector" },
    Camera = { 'Elevation': -150, 'Azimuth': 100 }
    ):

    """
    Es importante que Target y X tengan la misma longitud, su longitud siendo la cantidad de muestras
    """
    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d", elev=Camera['Elevation'], azim=Camera['Azimuth'])
    
    # colors
    cmap = matplotlib.colors.ListedColormap(['red', 'orange', 'blue'])
    bounds=[0,1,2,3]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    # scatter plot
    scc = ax.scatter(
        X[:, 0],
        X[:, 1],
        X[:, 2],
        c=ColorPoints['Target'],
        cmap=cmap,
        edgecolor="k",
        s=40,
    )

    # creamos la color bar
    cbar = plt.colorbar(scc)
    cbar.set_ticks(ColorPoints['Ticks'])
    cbar.set_ticklabels(ColorPoints['TicksLabels'])
    ax.set_title(Text['Title'])
    ax.set_xlabel(Text['XLabel'])
    ax.xaxis.set_ticklabels([])
    ax.set_ylabel(Text['YLabel'])
    ax.yaxis.set_ticklabels([])
    ax.set_zlabel(Text['ZLabel'])
    ax.zaxis.set_ticklabels([])

    plt.show()


if __name__ == '__main__':
    import pandas as pd

    data = pd.read_csv('./iris.csv')
    data['class'] = data['class'].replace('setosa', 0)
    data['class'] = data['class'].replace('versicolor', 1)
    data['class'] = data['class'].replace('virginica', 2)

    X = data.values[:, :3] # tomamos las primeras 3 columnas para usar como features
    Target = data.values[:, 4] # tomamos la ultima columna para usar como labels (target)

    plot3d_cbar(X, 
        ColorPoints = { 'Target': Target, 'Ticks': [0,1,2], 'TicksLabels' : ["setosa", "versicolor", "virgninica"]},
        Text = { 'Title': "First three PCA directions", 'XLabel': "1st eigenvector", 'YLabel': "2nd eigenvector", 'ZLabel': "3rd eigenvector" },
        Camera = { 'Elevation': -150, 'Azimuth': 100 }
        )