import os
import warnings
import numpy as np

import vaex
import vaex.dataset
from vaex.utils import InnerNamespace

from .pipeline import Pipeline
from .transformations import PCA, StandardScaler, MinMaxScaler


def iris():
    dirname = os.path.dirname(__file__)
    return vaex.open(os.path.join(dirname, 'iris.hdf5'))


def pca(self, n_components=2, features=None, progress=False):
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    pca = PCA(n_components=n_components, features=features)
    pca.fit(self, progress=progress)
    return pca


def standard_scaler(self, features=None, with_mean=True, with_std=True):
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    standard_scaler = StandardScaler(features=features, with_mean=with_mean, with_std=with_std)
    standard_scaler.fit(self)
    return standard_scaler


def minmax_scaler(self, features=None, feature_range=[0, 1]):
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    minmax_scaler = MinMaxScaler(features=features, feature_range=feature_range)
    minmax_scaler.fit(self)
    return minmax_scaler


def xgboost_model(self, label, num_round, features=None, copy=False, **param):
    from .xgboost import XGBModel
    dataset = self
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    xg = XGBModel(num_round=num_round, features=features, **param)
    xg.fit(dataset, label, copy=copy)
    return xg


def state_transfer(self):
    from .transformations import StateTransfer
    return StateTransfer(state=self.state_get())


def one_hot_encoding(self, expression, prefix=None, numeric=True, zero=None, one=None):
    prefix = prefix or expression
    uniques = self.unique(expression)
    uniques = np.sort(uniques)  # gives consistent results

    if numeric:
        if zero is None:
            zero = 0
        if one is None:
            one = 1
    else:
        if zero is None:
            zero = False
        if one is None:
            one = True
    # add a virtual column for each unique value
    for value in uniques:
        column_name = prefix + "_" + str(value)
        self.add_virtual_column(column_name, 'where({expression} == {value}, {one}, {zero})'.format(
            expression=expression, value=repr(value), one=one, zero=zero))


def train_test_split(self, test_size=0.2, strings=True, virtual=True):
    """Will split the dataset in train and test part.

    TODO:
     * see to_copy, we now copy virtual columns
     * maybe respect initial active_range
    """
    warnings.warn('make sure the dataset is shuffled')
    initial = None
    try:
        assert self.filtered is False, 'filtered dataset not supported yet'
        # full_length = len(self)
        self = self.trim()
        initial = self.get_active_range()
        self.set_active_fraction(test_size)
        test = self.trim()
        __, end = self.get_active_range()
        self.set_active_range(end, self.length_original())
        train = self.trim()
    finally:
        if initial is not None:
            self.set_active_range(*initial)
    return train, test


def add_namespace():
    vaex.dataset.Dataset.ml = InnerNamespace({})
    # try:
    #     from . import generated
    # except ImportError:
    #     print("importing generated code failed")
    vaex.dataset.Dataset.ml._add(train_test_split=train_test_split)

    def to_xgboost_dmatrix(self, label, features=None, selection=None, blocksize=1000 * 1000):
        """

        label: ndarray containing the labels
        """
        from . import xgboost
        return xgboost.VaexDMatrix(self, label, features=features, selection=selection, blocksize=blocksize)

    vaex.dataset.Dataset.ml._add(to_xgboost_dmatrix=to_xgboost_dmatrix, xgboost_model=xgboost_model,
                                 state_transfer=state_transfer,
                                 one_hot_encoding=one_hot_encoding,
                                 pca=pca,
                                 standard_scaler=standard_scaler,
                                 minmax_scaler=minmax_scaler)
    del to_xgboost_dmatrix

    # named_objects.update({ep.name: ep.load()})
