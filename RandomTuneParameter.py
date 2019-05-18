import numpy as np
experiments = 25
for i in range(experiments):
    # sample from a Uniform distribution on a log-scale
    learning_rate = 10 ** np.random.uniform(-1, -4)  # Sample learning rate candidates in the range (0.1 to 0.0001)
    regularization = 10 ** np.random.uniform(-2, -5)  # Sample regularization candidates in the range (0.01 to 0.00001)

    # do your thing with the hyper-parameters