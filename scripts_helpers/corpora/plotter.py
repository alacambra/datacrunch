from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def s():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for c, z in zip(['r', 'g', 'b', 'y'], [70, 20, 10, 0]):
        xs = np.arange(50)
        ys = np.random.rand(50)

        # You can provide either a single color or an array. To demonstrate this,
        # the first bar of each set will be colored cyan.
        cs = [c] * len(xs)
        cs[0] = 'c'

        #Add 2D bar(s).
        #def bar(self, left, height, zs=0, zdir='z', *args, **kwargs):
        #==========  ================================================
        #Argument    Description
        #==========  ================================================
        #*left*      The x coordinates of the left sides of the bars.
        #*height*    The height of the bars.
        #*zs*        Z coordinate of bars, if one value is specified
        #            they will all be placed at the same z.
        #*zdir*      Which direction to use as z ('x', 'y' or 'z')
        #            when plotting a 2D set.
        #==========  ================================================
        #
        #Keyword arguments are passed onto :func:`~matplotlib.axes.Axes.bar`.
        #
        #Returns a :class:`~mpl_toolkits.mplot3d.art3d.Patch3DCollection`

    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


x = np.arange(-6.0, 6.0, 0.01)
plt.plot(x, [x**2 for x in x])
plt.show()
