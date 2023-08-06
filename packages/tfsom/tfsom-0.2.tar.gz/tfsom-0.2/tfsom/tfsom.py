import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import scipy
import numpy as np


class SOM(object):
    """
    2-D Self-Organizing Map with Gaussian Neighbourhood function
    and linearly decreasing learning rate.
    """

    def __init__(self, m, n, dim, weightages, n_iterations=100,
                 alpha=None, sigma=None):
        """
        Initializes all necessary components of the TensorFlow
        Graph.

        m X n are the dimensions of the SOM. 'n_iterations' should
        should be an integer denoting the number of iterations undergone
        while training.
        'dim' is the dimensionality of the training inputs.
        'alpha' is a number denoting the initial time(iteration no)-based
        learning rate. Default value is 0.3
        'sigma' is the the initial neighbourhood value, denoting
        the radius of influence of the BMU while training. By default, its
        taken to be half of max(m, n).
        """

        self._m = m
        self._n = n
        self._dim = dim
        self._n_iterations = abs(int(n_iterations))
        self._alpha = alpha
        self._sigma = sigma
        self._weightages = weightages

        locations = []

        for i in range(m):
            for j in range(n):
                locations.append(np.array([i, j]))

        self._locations = locations

        centroid_grid = [[] for i in range(m)]

        for i, loc in enumerate(self._locations):
            centroid_grid[loc[0]].append(self._weightages[i])

        self._centroid_grid = centroid_grid

    @classmethod
    def load_trained_som(cls, filepath):
        with open(filepath, "r") as f:
            initparams = f.readline().split()
            m = int(initparams[1])
            n = int(initparams[2])
            dim = int(initparams[3])
            n_iter = int(initparams[4])
            alpha = float(initparams[5])
            sigma = float(initparams[6])

            weightages = []

            for line in f.readlines():
                weightages.append(np.array(
                    [float(x) for x in line.split()]))

        return SOM(m, n, dim, weightages, n_iter, alpha, sigma)

    @classmethod
    def train(cls, m, n, dim, input_vects, n_iterations=100,
              alpha=None, sigma=None):
        """
        Trains the SOM.
        'input_vects' should be an iterable of 1-D NumPy arrays with
        dimensionality as provided during initialization of this SOM.
        Current weightage vectors for all neurons(initially random) are
        taken as starting conditions for training.
        """

        if alpha is None:
            alpha = 0.3
        else:
            alpha = float(alpha)
        if sigma is None:
            sigma = max(m, n) / 2.0
        else:
            sigma = float(sigma)
# INITIALIZE GRAPH
        graph = tf.Graph()

# POPULATE GRAPH WITH NECESSARY COMPONENTS
        with graph.as_default():

            # VARIABLES AND CONSTANT OPS FOR DATA STORAGE

            # Randomly initialized weightage vectors for all neurons,
            # stored together as a matrix Variable of size [m*n, dim]
            weightage_vects = tf.Variable(tf.random_normal(
                [m*n, dim]))

            # Matrix of size [m*n, 2] for SOM grid locations
            # of neurons
            location_vects = tf.constant(np.array(
                list(SOM.neuron_locations(m, n))))

            # PLACEHOLDERS FOR TRAINING INPUTS
            # We need to assign them as attributes to self, since they
            # will be fed in during training

            # The training vector
            vect_input = tf.placeholder("float", [dim])
            # Iteration number
            iter_input = tf.placeholder("float")

            # CONSTRUCT TRAINING OP PIECE BY PIECE
            # Only the final, 'root' training op needs to be assigned as
            # an attribute to self, since all the rest will be executed
            # automatically during training

            # To compute the Best Matching Unit given a vector
            # Basically calculates the Euclidean distance between every
            # neuron's weightage vector and the input, and returns the
            # index of the neuron which gives the least value
            bmu_index = tf.argmin(tf.sqrt(tf.reduce_sum(
                tf.pow(tf.subtract(weightage_vects, tf.stack(
                    [vect_input for i in range(m*n)])), 2), 1
                                    )), 0)

            # This will extract the location of the BMU based on the BMU's
            # index
            slice_input = tf.pad(tf.reshape(bmu_index, [1]),
                                 np.array([[0, 1]]))
            bmu_loc = tf.reshape(tf.slice(location_vects, slice_input,
                                          tf.constant(np.array([1, 2]))),
                                 [2])

            # To compute the alpha and sigma values based on iteration
            # number
            learning_rate_op = tf.subtract(1.0, tf.div(iter_input,
                                                       n_iterations))
            _alpha_op = tf.multiply(alpha, learning_rate_op)
            _sigma_op = tf.multiply(sigma, learning_rate_op)

            # Construct the op that will generate a vector with learning
            # rates for all neurons, based on iteration number and location
            # wrt BMU.
            bmu_distance_squares = tf.reduce_sum(tf.pow(tf.subtract(
                location_vects, tf.stack(
                    [bmu_loc for i in range(m*n)])), 2), 1)
            neighbourhood_func = tf.exp(tf.negative(tf.div(tf.cast(
                bmu_distance_squares, "float32"), tf.pow(_sigma_op, 2))))
            learning_rate_op = tf.multiply(_alpha_op, neighbourhood_func)

            # Finally, the op that will use learning_rate_op to update
            # the weightage vectors of all neurons based on a particular
            # input
            learning_rate_multiplier = tf.stack([tf.tile(tf.slice(
                learning_rate_op, np.array([i]), np.array([1])), [dim])
                                            for i in range(m*n)])
            weightage_delta = tf.multiply(
                learning_rate_multiplier,
                tf.subtract(tf.stack([vect_input for i in
                            range(m*n)]), weightage_vects))
            new_weightages_op = tf.add(weightage_vects, weightage_delta)
            training_op = tf.assign(weightage_vects, new_weightages_op)

            # INITIALIZE SESSION
            sess = tf.Session()

            # INITIALIZE VARIABLES
            init_op = tf.global_variables_initializer()
            sess.run(init_op)

        # Training iterations
        for iter_no in range(n_iterations):
            # Train with each vector one by one
            for input_vect in input_vects:
                sess.run(training_op, feed_dict={vect_input: input_vect,
                                                 iter_input: iter_no})

        # Store a centroid grid for easy retrieval later on
        weightages = list(sess.run(weightage_vects))
        return SOM(m, n, dim, weightages, n_iterations, alpha, sigma)

    def save_trained_som(self, filepath):
        with open(filepath, "w") as f:
            f.write("SOM {} {} {} {} {} {}\n".format(self._m, self._n,
                    self._dim, self._n_iterations, self._alpha, self._sigma))
            for i in self._weightages:
                f.write(" ".join(map(str, i)) + "\n")

    @staticmethod
    def neuron_locations(m, n):
        """
        Yields one by one the 2-D locations of the individual neurons
        in the SOM.
        """
        # Nested iterations over both dimensions
        # to generate all 2-D locations in the map
        for i in range(m):
            for j in range(n):
                yield np.array([i, j])

    def get_centroids(self):
        """
        Returns a list of 'm' lists, with each inner list containing
        the 'n' corresponding centroid locations as 1-D NumPy arrays.
        """
        return self._centroid_grid

    def map_vects(self, input_vects):
        """
        Maps each input vector to the relevant neuron in the SOM
        grid.
        'input_vects' should be an iterable of 1-D NumPy arrays with
        dimensionality as provided during initialization of this SOM.
        Returns a list of 1-D NumPy arrays containing (row, column)
        info for each input vector(in the same order), corresponding
        to mapped neuron.
        """

        to_return = []
        for vect in input_vects:
            min_index = min([i for i in range(len(self._weightages))],
                            key=lambda x: np.linalg.norm(vect -
                                                         self._weightages[x]))
            to_return.append(self._locations[min_index])

        return to_return

    def get_umat(self):

        # Get output grid
        image_grid = self.get_centroids()

        # define the distance functions
        # the diagonal distance
        def dz(i, j):
            rows = len(image_grid)
            cols = len(image_grid[1])
            if ((i >= 0) & (j >= 0) & ((i + 1) < rows) & ((j + 1) < cols)):
                dxy = np.linalg.norm(image_grid[i][j] -
                                     image_grid[i + 1][j + 1])
                dyx = np.linalg.norm(image_grid[i][j + 1] -
                                     image_grid[i + 1][j])
                return(1/2 * (dxy + dyx))
            else:
                return(float('NaN'))

        # the distance on the x axis
        def dx(i, j):
            cols = len(image_grid[1])
            if ((i >= 0) & (j >= 0) & ((j + 1) < cols)):
                return(np.linalg.norm(image_grid[i][j] - image_grid[i][j + 1]))
            else:
                return(float('NaN'))

        # the distance on the y axis
        def dy(i, j):
            rows = len(image_grid)
            if ((i >= 0) & (j >= 0) & ((i + 1) < rows)):
                return(np.linalg.norm(image_grid[i][j] - image_grid[i + 1][j]))
            else:
                return(float('NaN'))

        # calculate the unified distance matrix
        # dimensions
        rows = len(image_grid)
        cols = len(image_grid[1])

        # intial matrix
        u_mat = np.array([[float(0) for x in range(2 * cols - 1)]
                          for y in range(2 * rows - 1)])

        # the distances
        for i in range(rows):
            for j in range(cols):
                if (((2 * i - 1) in range(2 * rows - 1)) &
                        ((2 * j - 1) in range(2 * cols - 1))):
                    u_mat[2 * i - 1][2 * j - 1] = dz(i - 1, j - 1)

                if (((2 * i - 1) in range(2 * rows - 1)) &
                        ((2 * j) in range(2 * cols - 1))):
                    u_mat[2 * i - 1][2 * j] = dy(i - 1, j)

                if (((2 * i - 1) in range(2 * rows - 1)) &
                        ((2 * j + 1) in range(2 * cols - 1))):
                    u_mat[2 * i - 1][2 * j + 1] = dz(i - 1, j)

                if (((2 * i) in range(2 * rows - 1)) & ((2 * j - 1) in
                                                        range(2 * cols - 1))):
                    u_mat[2 * i][2 * j - 1] = dx(i, j - 1)

                if (((2 * i) in range(2 * rows - 1)) & ((2 * j) in
                                                        range(2 * cols - 1))):
                    u_mat[2 * i][2 * j] = np.nanmean(np.array([
                        dz(i - 1, j - 1),
                        dy(i - 1, j),
                        dz(i - 1, j),
                        dx(i, j - 1),
                        dx(i, j),
                        dz(i, j - 1),
                        dy(i, j),
                        dz(i, j)]))

                if (((2 * i) in range(2 * rows - 1)) &
                        ((2 * j + 1) in range(2 * cols - 1))):
                    u_mat[2 * i][2 * j + 1] = dx(i, j)

                if (((2 * i + 1) in range(2 * rows - 1)) &
                        ((2 * j - 1) in range(2 * cols - 1))):
                    u_mat[2 * i + 1][2 * j - 1] = dz(i, j - 1)

                if (((2 * i + 1) in range(2 * rows - 1)) &
                        ((2 * j) in range(2 * cols - 1))):
                    u_mat[2 * i + 1][2 * j] = dy(i, j)

                if (((2 * i + 1) in range(2 * rows - 1)) &
                        ((2 * j + 1) in range(2 * cols - 1))):
                    u_mat[2 * i + 1][2 * j + 1] = dz(i, j)

        return(u_mat)

    def get_feat_grid(self, feat_num):
        image_grid = self.get_centroids()

        # dimentions
        cols = len(image_grid[1])
        rows = len(image_grid)

        # initial grid same size as the image_grid
        feat_grid = np.array([[float(0) for x in range(cols)]
                              for y in range(rows)])

        for i in range(cols):
            for j in range(rows):
                feat_grid[j][i] = image_grid[j][i][feat_num]

        return(feat_grid)

    def get_hit_grid(self, input_data):
        image_grid = self.get_centroids()
        mapped = self.map_vects(input_data)

        # dimentions
        cols = len(image_grid[1])
        rows = len(image_grid)
        model_vecs = np.unique(mapped, axis=False, return_counts=True)

        # initial matrix
        hit_grid = np.array([[0 for x in range(cols)] for y in range(rows)])
        for i, m in enumerate(model_vecs[0]):
            hit_grid[m[0], m[1]] = model_vecs[1][i]

        return(hit_grid)

    def get_sdh_grid(self, input_data, s=8):

        image_grid = self.get_centroids()

        # dimentions
        cols = len(image_grid[0])
        rows = len(image_grid)
        n = len(image_grid[0][0])

        sdh_mat = np.zeros(cols*rows)
        d_mat = scipy.spatial.distance.cdist(input_data, np.array(image_grid)
                                             .reshape(cols*rows, n))

        c = float(np.arange(1, s+1).sum())

        for x in d_mat:
            chosen_ind = np.argsort(x)[:s]

            for i, ind in enumerate(chosen_ind):
                sdh_mat[ind] += (s-i)/c

        sdh_mat = sdh_mat.reshape((rows, cols))
        return sdh_mat

    def get_activity_mat(self, model_vector_row, model_vector_col):

        image_grid = self.get_centroids()

        # dimentions
        cols = len(image_grid[0])
        rows = len(image_grid)
        n = len(image_grid[0][0])

        model_vec = image_grid[model_vector_row][model_vector_col]

        # initial mat
        activity_mat = np.array([])

        for i in np.array(image_grid).reshape(rows*cols, n):
            activity_mat = np.append(activity_mat,
                                     np.linalg.norm(model_vec - i))

        activity_mat = activity_mat.reshape(rows, cols)

        return(activity_mat)

    def plot_u_matrix(self, title="U-Matrix", colors='Greys'):
        plt.imshow(self.get_umat(), cmap=colors, interpolation='nearest')
        plt.title(title)
        plt.show()

    def plot_hit_histogram(self, input_data, title="Hit Histogram",
                           colors="coolwarm"):
        hit_grid = self.get_hit_grid(input_data)

        c_wr = mcolors.LinearSegmentedColormap.from_list(
            name='white_red',
            colors=[(1, 1, 1), (1, 0, 0)],
            N=len(np.unique(hit_grid)) - 1)

        fig1 = plt.figure(figsize=(10, 10))

        plot1 = fig1.add_subplot(1, 1, 1)
        plot1.imshow(hit_grid, cmap=c_wr, interpolation='nearest')

        for (j, i), label in np.ndenumerate(hit_grid):
            plt.text(i, j, int(label), ha='center', va='center')

        plt.title(title)
        plt.show()

    def plot_activity_matrix(self, model_vector_row, model_vector_col,
                             title="Activity Matrix", color="coolwarm"):
        plt.imshow(self.get_activity_mat(model_vector_row, model_vector_col),
                   cmap=color, interpolation='nearest')
        plt.title(title)
        plt.show()

    def plot_sdh_grid(self, input_data, s=8, title="SDH-Grid"):
        sdh_grid = self.get_sdh_grid(input_data, s)

        fig1 = plt.figure(figsize=(5, 5))
        plt.title(title)
        plot1 = fig1.add_subplot(1, 1, 1)
        plot1.contourf(scipy.ndimage.zoom(sdh_grid, 3))

        plt.show()
