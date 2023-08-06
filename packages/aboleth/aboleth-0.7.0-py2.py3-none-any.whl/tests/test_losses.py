"""Test the layers module."""

import pytest
import numpy as np
import tensorflow as tf
from scipy.stats import norm

import aboleth as ab
from aboleth.losses import _sum_likelihood


def test_elbo_likelihood(make_graph):
    """Test for expected output dimensions from loss ."""
    x, y, N, X_, Y_, N_, layers = make_graph
    nn, kl = layers(X=X_)
    like = tf.distributions.Normal(nn, scale=1.)

    loss = ab.elbo(like, Y_, N, kl)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()

        L = loss.eval(feed_dict={X_: x, Y_: y, N_: float(N)})
        assert np.isscalar(L)


def test_map_likelihood(make_graph):
    """Test for expected output dimensions from deepnet."""
    x, y, _, _, _, _, layers = make_graph
    nn, reg = layers(X=x.astype(np.float32))
    like = tf.distributions.Normal(nn, scale=1.)

    loss = ab.max_posterior(like, y.astype(np.float32), reg)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()

        L = loss.eval()
        assert np.isscalar(L)


def test_categorical_likelihood(make_data):
    """Test aboleth with a tf.distributions.Categorical likelihood.

    Since it is a bit of an odd half-multivariate case.
    """
    x, y, _, = make_data
    N, K = x.shape

    # Make two classes (K = 2)
    Y = np.zeros(len(y), dtype=np.int32)
    Y[y[:, 0] > 0] = 1

    layers = ab.stack(
        ab.InputLayer(name='X', n_samples=10),
        lambda X: (X, 0.0)   # Mock a sampling layer, with 2-class output
    )

    nn, reg = layers(X=x.astype(np.float32))
    like = tf.distributions.Categorical(logits=nn)

    ELBO = ab.elbo(like, Y, N, reg)
    MAP = ab.max_posterior(like, Y, reg)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()

        assert like.probs.eval().shape == (10, N, K)
        assert like.prob(Y).eval().shape == (10, N)

        L = ELBO.eval()
        assert np.isscalar(L)

        L = MAP.eval()
        assert np.isscalar(L)


def test_sum_likelihood():
    """Test we can do weighted sums of likelihoods."""
    n_samples = 2
    N = 5
    Y = np.ones(N, dtype=np.float32)
    Net = np.ones((n_samples, N), dtype=np.float32) * .5
    like = tf.distributions.Bernoulli(probs=Net)
    lp = np.log(0.5)

    def weight_fn(Y):
        return Y * tf.range(N, dtype=tf.float32)

    unweighted = _sum_likelihood(like, Y, None)
    value = _sum_likelihood(like, Y, np.arange(N))
    call = _sum_likelihood(like, Y, weight_fn(Y))

    with pytest.raises(AssertionError, message='Expecting broadcasting error'):
        # contrive non-sensical weight that would be
        # accepted due to broadcasting rules
        _sum_likelihood(like, Y, np.random.randn(20, 2, 5))

    tc = tf.test.TestCase()
    with tc.test_session():
        sumll = unweighted.eval()
        assert np.allclose(sumll, lp * n_samples * N)

        sumll = value.eval()
        assert np.allclose(sumll, np.sum(lp * n_samples * np.arange(N)))

        sumll = call.eval()
        assert np.allclose(sumll, np.sum(lp * n_samples * np.arange(N)))
