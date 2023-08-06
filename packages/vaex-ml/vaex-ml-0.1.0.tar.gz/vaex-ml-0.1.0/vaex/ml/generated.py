

import vaex.ml.transformations
import traitlets

def pca(self, features, n_components=2, prefix='PCA_'):
    obj = vaex.ml.transformations.PCA(n_components=n_components, prefix=prefix, features=features)
    obj.fit(self)
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add(pca=pca)

def __init__(self, n_components=2, prefix='PCA_', features=traitlets.Undefined):
    super(vaex.ml.transformations.PCA, self).__init__(n_components=n_components, prefix=prefix, features=features)

vaex.ml.transformations.PCA.__init__ = __init__
del __init__
    
