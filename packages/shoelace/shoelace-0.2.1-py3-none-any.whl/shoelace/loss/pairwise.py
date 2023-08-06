import chainer.functions as F
from chainer import cuda


def ranknet(x, t):
    """
    The RankNet loss as in Burges et al (2005), Learning to Rank using Gradient
    Descent

    :param x: The activation of the previous layer 
    :param t: The target labels
    :return: The loss
    """

    # Get the ground truth by sorting activations by the relevance labels
    xp = cuda.get_array_module(x, t)
    S = xp.transpose(t) * xp.ones(t.shape)


    mt = xp.reshape(t, (1, t.shape[0]))
    s1 = mt * xp.ones((mt.shape[1], mt.shape[0]))
    s2 = xp.ones((mt.shape[0], mt.shape[1])) * mt.T
    s = s1 - s2
    s = 1.0 * (s > 0) - 1.0 * (s < 0)

    mx = xp.reshape(x, (1, x.shape[0]))
    sigma1 = mx * xp.ones((mx.shape[1], mx.shape[0]))
    sigma2 = xp.ones((mt.shape[0], mt.shape[1])) * mt.T
    sigma = sigma1 - sigma2

    loss = xp.mean(0.5*(-s + 1) * sigma + xp.log(xp.exp(-sigma) + 1), 0)


