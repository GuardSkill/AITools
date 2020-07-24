from sklearn import manifold
import matplotlib.pyplot as plt


def visualize_embeding(embeding_data, y_label):
    '''
        Dim of y_label :(M,)
        Dim of embeding_data : (M,N)
    '''
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    Z_tsne = tsne.fit_transform(embeding_data)
    fig = plt.figure()
    plt.scatter(Z_tsne[:, 0], Z_tsne[:, 1], s=2, c=y_label, cmap=plt.cm.get_cmap("jet", 10))
    plt.colorbar(ticks=range(10))
    plt.savefig('Plot.png')
    try:
        plt.show()
    except:
        print("No devices to show figure")

