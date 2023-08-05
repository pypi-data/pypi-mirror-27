import os
import time
import pickle
import json
import scipy
import tqdm
import math

import numpy as np
import matplotlib.pyplot as plt

from sklearn import model_selection, metrics

from abc import ABC, abstractmethod

from . import helpers

class ParameterSearchRecord():
    """
    Saves the results of a parameter search to file, so it can be resumed
    """

    def __init__(self, path, direction=None):

        if direction is None:
            direction = 'max'

        self.path = path

        if os.path.isfile(path):
            with open(path, "rb") as f:
                data = pickle.load(f)

                self.allConfigsAndScores = data.get('allConfigsAndScores', [])
                self.randomSeed = data.get('randomSeed', int(time.time()))
                self.direction = data.get('direction', 'max')

            f.close()
        else:
            self.allConfigsAndScores = []
            self.randomSeed = int(time.time())
            self.direction = direction

        self.scoresByConfigKey = {}

        self.bestConfig = None
        self.bestScore = None

        for (config, score) in self.allConfigsAndScores:
            key = self.__get_config_key(config)

            self.scoresByConfigKey[key] = score

            if self.__is_best(score):
                self.bestConfig = config
                self.bestScore = score

        print(' - recovered {} previously searched parameter permutations'.format(len(self.allConfigsAndScores)))
        print(' - best score so far is {}'.format(self.bestScore))

    def __is_best(self, score):

        if self.bestScore is None:
            return True

        if self.direction == 'max':
            return score > self.bestScore
        else:
            return score < self.bestScore

    def __get_config_key(self, config):

        return json.dumps(config, sort_keys=True)

    def update(self, config, score):

        self.allConfigsAndScores.append((config, score))

        if self.__is_best(score):
            self.bestConfig = config
            self.bestScore = score

        with open(self.path, "wb") as f:
            pickle.dump(
                {
                    'allConfigsAndScores': self.allConfigsAndScores,
                    'randomSeed': self.randomSeed,
                    'direction': self.direction
                }
                , f)

        f.close()

    def getScore(self, config):
        key = self.__get_config_key(config)
        return self.scoresByConfigKey.get(key)


class GridParameterSearcher(ABC):
    """
    This provides a tool to exhaustively evaluate different combinations of parameters.
    """

    @abstractmethod
    def initialize_algorithm(self, config):
        """
        Initializes an algorithm (which must extend ConfigurableAlgorithm) with the given configuration

        :param config: a configuration for the algorithm
        :param runs: the number of seperate runs to perform
        :return the initialized, configured algorithm
        """

        pass

    def __init__(self, items, labels=None, scores=None, scorer=None, scorer_config=None):
        """
        Initializes the GridSearcher, with the given dataset of items and labels

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        """

        self.dataset = helpers.Dataset(items, labels, scores)

        if scorer is None:
            if self.dataset.for_classification():
                self.scorer = 'f1_score'
            else:
                self.scorer = 'r2_score'
        else:
            self.scorer = scorer

        if scorer_config is None:
            if self.dataset.for_classification() and not self.dataset.is_binary():
                self.scorer_config = {'average': 'micro'}
            else:
                self.scorer_config = {}
        else:
            self.scorer_config = scorer_config

    def do_search(self, configs, record, n_runs=5, n_folds=5):

        grid = model_selection.ParameterGrid(configs)

        print("{} distinct configurations to test".format(len(grid)))

        with tqdm.tqdm_notebook(total=len(grid) * n_runs * n_folds) as progress:

            for config in grid:

                score = record.getScore(config)

                # skip this set of parameters if we already have a record of it
                if (score is not None):
                    progress.update(n_runs * n_folds)
                    continue

                scores = []

                for run in range(0, n_runs):

                    folds = self.dataset.build_folds(n_folds)

                    gold = []
                    pred = []

                    for train_index, test_index in folds:

                        X_train, X_test = self.dataset.items[train_index], self.dataset.items[test_index]

                        if self.dataset.type == 'c':
                            y_train, y_test = self.dataset.labels[train_index], self.dataset.labels[test_index]
                        else:
                            y_train, y_test = self.dataset.scores[train_index], self.dataset.scores[test_index]

                        gold = np.concatenate((gold, y_test))

                        alg = self.initialize_algorithm(config)
                        alg.fit(X_train, y_train)

                        pred = np.concatenate((pred, alg.predict(X_test)))

                        progress.update(1)

                    scores.append(helpers.get_score(gold, pred, self.scorer, self.scorer_config))

                record.update(config, np.mean(scores))

        return record.bestConfig, record.bestScore


class RandomParameterSearcher(ABC):
    """
    This provides a tool to randomly search for the best combinations of parameters.
    """

    @abstractmethod
    def initialize_algorithm(self, config):
        """
        Initializes an algorithm (which must extend ConfigurableAlgorithm) with the given configuration

        :param config: a configuration for the algorithm
        :return the initialized, configured algorithm
        """

        pass

    def __init__(self, items, labels=None, scores=None, scorer=None, scorer_config=None):
        """
        Initializes the GridSearcher, with the given dataset

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        """

        self.dataset = helpers.Dataset(items, labels, scores)

        if scorer is None:
            if self.dataset.for_classification():
                self.scorer = 'f1_score'
            else:
                self.scorer = 'r2_score'
        else:
            self.scorer = scorer

        if scorer_config is None:
            if self.dataset.for_classification() and not self.dataset.is_binary():
                self.scorer_config = {'average': 'micro'}
            else:
                self.scorer_config = {}
        else:
            self.scorer_config = scorer_config

    def do_search(self, param_distributions, record, budget=100, n_runs=3, n_folds=5, verbose=False):

        with tqdm.tqdm_notebook(total=budget * n_runs * n_folds) as progress:

            configs = list(model_selection.ParameterSampler(param_distributions, budget, record.randomSeed))
            for c in configs:

                config = self.__get_rounded_config(c)

                score = record.getScore(config)

                # skip this set of parameters if we already have a record of it
                if (score is not None):
                    if verbose:
                        print(config, score)

                    progress.update(n_runs * n_folds)
                    continue

                scores = []

                for run in range(0, n_runs):

                    folds = self.dataset.build_folds(n_folds)

                    gold = []
                    pred = []

                    for train_index, test_index in folds:

                        X_train, X_test = self.dataset.items[train_index], self.dataset.items[test_index]

                        if self.dataset.type == 'c':
                            y_train, y_test = self.dataset.labels[train_index], self.dataset.labels[test_index]
                        else:
                            y_train, y_test = self.dataset.scores[train_index], self.dataset.scores[test_index]

                        gold = np.concatenate((gold, y_test))

                        alg = self.initialize_algorithm(config)
                        alg.fit(X_train, y_train)

                        pred = np.concatenate((pred, alg.predict(X_test)))

                        progress.update(1)

                    scores.append(helpers.get_score(gold, pred, self.scorer, self.scorer_config))

                score = np.mean(scores)
                record.update(config, score)

                if verbose:
                    print(config, score)

        return record.bestConfig, record.bestScore

    def __get_rounded_config(self, config):

        rounded = {}
        for (key, value) in config.items():

            if isinstance(value, (float, complex)):
                rounded[key] = self.__round_to_n(value, 3)
            else:
                rounded[key] = value

        return rounded

    def __round_to_n(self, x, n):
        return round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))


class ParameterSearchVisualizer():

    def __is_num(self, val):


        try:
            float(val)
            return True
        except ValueError:
            return False
        except TypeError:
            return False


    def __matches_filter(self, config, filter_by):

        for (key, val) in filter_by.items():

            configVal = config.get(key)

            if self.__is_num(configVal) and isinstance(val, (list, tuple)) and len(val) == 2:
                if configVal < val[0]:
                    return False

                if configVal > val[1]:
                    return False
            else:
                if not config.get(key) == val:
                    return False

        return True

    def visualize_grid_search(self, record, x_axis, y_axis, filter_by={}, figsize=(8, 6)):

        x_vals = []
        y_vals = []

        scores = {}

        for (config, score) in record.allConfigsAndScores:

            if score == 0:
                continue

            if not self.__matches_filter(config, filter_by):
                continue

            x = config.get(x_axis)
            y = config.get(y_axis)

            if x is None or y is None:
                continue

            if x not in x_vals:
                x_vals.append(x)

            if y not in y_vals:
                y_vals.append(y)

            scores['{}_{}'.format(x, y)] = score

        x_vals = sorted(x_vals)
        y_vals = sorted(y_vals)

        score_grid = []
        for y in y_vals:
            score_grid.append([scores.get('{}_{}'.format(x, y), np.nan) for x in x_vals])

        plt.figure(figsize=figsize)
        # plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)

        masked_scores = np.ma.array(score_grid, mask=np.isnan(score_grid))

        cmap = plt.cm.jet
        cmap.set_bad('white', 1.)
        # ax.imshow(masked_array, interpolation='nearest', cmap=cmap)



        plt.imshow(masked_scores, interpolation='nearest', cmap=cmap)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.colorbar()
        plt.xticks(np.arange(len(x_vals)), x_vals, rotation=45)
        plt.yticks(np.arange(len(y_vals)), y_vals)
        plt.show()

    def visualize_random_search(self, record, x_axis, y_axis, x_range=None, y_range=None, filter_by=None, figsize=None):

        if filter_by is None:
            filter_by = {}

        if figsize is None:
            figsize = (8, 6)

        xs = []
        ys = []
        points = []
        scores = []

        for (config, score) in record.allConfigsAndScores:

            if score == 0:
                continue

            if not self.__matches_filter(config, filter_by):
                continue

            x = config.get(x_axis)
            y = config.get(y_axis)

            if x is None or y is None:
                continue

            xs.append(x)
            ys.append(y)
            points.append((x, y))
            scores.append(score)

        if x_range is None:
            x_range = (min(xs), max(xs))

        if y_range is None:
            y_range = (min(ys), max(ys))

        grid_x, grid_y = np.mgrid[x_range[0]:x_range[1]:100j, y_range[0]:y_range[1]:100j]
        grid = scipy.interpolate.griddata(points, scores, (grid_x, grid_y), method='linear')

        plt.figure(figsize=figsize)

        plt.contour(grid_x, grid_y, grid, 15, linewidths=0.5, colors='k')
        plt.contourf(grid_x, grid_y, grid, 15, cmap=plt.cm.jet)

        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.colorbar()

        plt.scatter(*zip(*points),marker='o',c='black',s=5)
        # plt.xticks(np.arange(len(x_vals)), x_vals, rotation=45)
        # plt.yticks(np.arange(len(y_vals)), y_vals)
        plt.show()
