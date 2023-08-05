#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Energy-based voice activity detection for speaker recognition"""

import numpy
import bob.ap
import math
from .. import utils
import logging
import scipy.io.wavfile
import sys

from bob.bio.spear.preprocessor.Base import Base
from bob.bio.base.preprocessor import Preprocessor

logger = logging.getLogger("bob.paper.taslp_2017")


class Energy_2Gauss_Remove_Head_Tail(Base):
  """Extracts the Energy"""
  def __init__(
      self,
      max_iterations=10,
      convergence_threshold=0.0005,
      variance_threshold=0.0005,
      win_length_ms=20.,
      win_shift_ms=10.,
      smoothing_window=10,  # 10 frames (i.e. 100 ms)
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Preprocessor.__init__(
        self,
        max_iterations=max_iterations,
        convergence_threshold=convergence_threshold,
        variance_threshold=variance_threshold,
        win_length_ms=win_length_ms,
        win_shift_ms=win_shift_ms,
        smoothing_window=smoothing_window,
    )
    # copy parameters
    self.max_iterations = max_iterations
    self.convergence_threshold = convergence_threshold
    self.variance_threshold = variance_threshold
    self.win_length_ms = win_length_ms
    self.win_shift_ms = win_shift_ms
    self.smoothing_window = smoothing_window


  def _voice_activity_detection(self, energy_array):
    # Initialisation part

    n_samples = len(energy_array)
    # Add an epsilon small Gaussian noise to avoid numerical issues (mainly due to artificial silence).
    energy_array = numpy.array(math.pow(10, -6) * numpy.random.randn(len(energy_array))) + energy_array
    # Normalize the energy array
    normalized_energy = utils.normalize_std_array(energy_array)

    # Apply k-means
    kmeans = bob.learn.em.KMeansMachine(2, 1)
    m_ubm = bob.learn.em.GMMMachine(2, 1)
    kmeans_trainer = bob.learn.em.KMeansTrainer()
    bob.learn.em.train(kmeans_trainer, kmeans, normalized_energy, self.max_iterations, self.convergence_threshold)
    [variances, weights] = kmeans.get_variances_and_weights_for_each_cluster(normalized_energy)
    means = kmeans.means

    if numpy.isnan(means[0]) or numpy.isnan(means[1]):
      logger.warn("Skip this file since it contains NaN's")
      return numpy.array(numpy.zeros(n_samples), dtype=numpy.int16)
    # Initializes the GMM
    m_ubm.means = means

    m_ubm.variances = variances
    m_ubm.weights = weights
    m_ubm.set_variance_thresholds(self.variance_threshold)

    trainer = bob.learn.em.ML_GMMTrainer(True, True, True)
    bob.learn.em.train(trainer, m_ubm, normalized_energy, self.max_iterations, self.convergence_threshold)
    means = m_ubm.means
    weights = m_ubm.weights

    if means[0] < means[1]:
      higher = 1
      lower = 0
    else:
      higher = 0
      lower = 1

    label = numpy.array(numpy.ones(n_samples), dtype=numpy.int16)
    higher_mean_gauss = m_ubm.get_gaussian(higher)
    lower_mean_gauss = m_ubm.get_gaussian(lower)

    for i in range(n_samples):
      if higher_mean_gauss.log_likelihood(normalized_energy[i]) < lower_mean_gauss.log_likelihood(normalized_energy[i]):
        label[i] = 0
      else:
        label[i] = label[i] * 1
    return label

  def _compute_energy(self, rate_wavsample):
    """retreive the speech / non speech labels for the speech sample given by the tuple (rate, wave signal)"""

    e = bob.ap.Energy(rate_wavsample[0], self.win_length_ms, self.win_shift_ms)
    energy_array = e(rate_wavsample[1])
    labels = self._voice_activity_detection(energy_array)
    # discard isolated speech a number of frames defined in smoothing_window
    labels = utils.smoothing(labels, self.smoothing_window)

    logger.info("After 2 Gaussian Energy-based VAD there are %d frames remaining over %d", numpy.sum(labels), len(labels))
    return labels

  def __call__(self, input_signal, annotations=None):
    """labels speech (1) and non-speech (0) parts of the given input wave file using 2 Gaussian-modeled Energy
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal
        """
    labels = self._compute_energy(input_signal)
    rate = input_signal[0]
    data = input_signal[1]

    labels_1 = numpy.where(labels == 1)[0]

    # if there is at least one samples classified as 'speech', then we remove the silence at the beginning and end of the utterance.
    if(len(labels_1) > 0):
      idx0 = labels_1[0]
      idx1 = labels_1[-1]
    else:
      idx0 = 0
      idx1 = len(labels)-1
    idx0_data = idx0*self.win_shift_ms*rate/1000
    idx1_data = (idx1*self.win_shift_ms+self.win_length_ms)*rate/1000
    data = data[int(idx0_data):int(idx1_data)]
    labels = labels[int(idx0_data):int(idx1_data)]
    return rate, data, labels
