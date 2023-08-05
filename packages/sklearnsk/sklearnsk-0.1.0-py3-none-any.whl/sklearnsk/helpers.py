from sklearn import ensemble, svm, tree, naive_bayes, dummy, linear_model
from sklearn import model_selection
from sklearn import metrics

import numpy as np


def initialize_algorithm(name, config):
    algorithmClass = None
    for module in [ensemble, svm, tree, naive_bayes, dummy, linear_model]:

        try:
            algorithmClass = getattr(module, name)
            break
        except AttributeError:
            pass

    if algorithmClass is None:
        raise AttributeError('could not locate algorithm {}'.format(name))

    return algorithmClass(**config)


def get_score(y_true, y_pred, scorer_name, scorer_config):

    scorer = getattr(metrics, scorer_name)

    return scorer(y_true, y_pred, **scorer_config)


def merge_configs(configA, configB):
    config = {}

    for key, value in configA.items():
        config[key] = value

    for key, value in configB.items():

        if key not in config:
            config[key] = value

    return config


class Dataset():
    def __init__(self, items, labels=None, scores=None):
        """
        Initializes the dataset

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        """

        if labels is None and scores is None:
            raise ValueError('You must specify either labels or scores')

        if labels is not None and scores is not None:
            raise ValueError('You must specify either labels or scores, but not both')

        self.items = np.array(items)

        self.labels = None if labels is None else np.array(labels)
        self.scores = None if scores is None else np.array(scores)

        self.type = 'c' if labels is not None else 'r'

    def build_folds(self, n_folds):

        if self.labels is not None:
            skf = model_selection.StratifiedKFold(n_splits=n_folds, shuffle=True)
            return skf.split(self.items, self.labels)

        if self.scores is not None:
            kf = model_selection.KFold(n_splits=n_folds, shuffle=True)
            return kf.split(self.items, self.scores)

    def for_classification(self):
        return self.labels is not None

    def for_regression(self):
        return self.scores is not None

    def is_binary(self):

        if not self.for_classification():
            return False

        return len(set(self.labels)) == 2