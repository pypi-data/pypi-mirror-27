from sklearn import preprocessing
#import primitive
import sys
#sys.path.append('corexdiscrete/')
import corexdiscrete.corexdiscrete.corex as corex_disc
#import bio_corex.corex as corex_disc
from collections import defaultdict, OrderedDict
from scipy import sparse
import pandas as pd
import numpy as np
import typing

import d3m_metadata.container as container
import d3m_metadata.hyperparams as hyperparams
import d3m_metadata.params as params
from d3m_metadata.metadata import PrimitiveMetadata

from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from primitive_interfaces.base import CallResult
#from primitive_interfaces.params import Params
#from primitive_interfaces.hyperparams import HyperParameters

from typing import NamedTuple, Optional, Sequence, Any, OrderedDict

Input = container.DataFrame
Output = container.ndarray

class CorexDiscrete_Params(params.Params):
    model: typing.Union[corex_disc.Corex, None]
    #fitted: bool
    #training_inputs: Input

class CorexDiscrete_Hyperparams(hyperparams.Hyperparams):
    n_hidden = hyperparams.Union(OrderedDict([('n_hidden int' , hyperparams.Uniform(lower = 1, upper = 50, default = 2, q = 1, description = 'number of hidden factors learned')),
        ('n_hidden pct' , hyperparams.Uniform(lower = 0, upper = .50, default = .2, q = .05, description = 'number of hidden factors as percentage of # input columns'))]), 
        default = 'n_hidden pct')

class CorexDiscrete(UnsupervisedLearnerPrimitiveBase[Input, Output, CorexDiscrete_Params, CorexDiscrete_Hyperparams]):  #(Primitive):
    """
    Return components/latent factors that explain the most multivariate mutual information in the data. For comparison, PCA returns components explaining the most variance in the data.  Serves as DSBox wrapper for https://github.com/gregversteeg/bio_corex
    """
    metadata = PrimitiveMetadata({
      "schema": "v0",
      "id": "de2677d1-c48c-335e-ac55-6114a6bfd1be",
      "version": "0.2.0",
      "name": "CorexDiscrete",
      "description": "Return components/latent factors that explain the most multivariate mutual information in the data. For comparison, PCA returns components explaining the most variance in the data.  Serves as DSBox wrapper for https://github.com/gregversteeg/bio_corex",
      "python_path": "d3m.primitives.corexdiscrete.corex_discrete:CorexDiscrete",
      "original_python_path": "corexdiscrete.corex_discrete.CorexDiscrete",
      "source": {
          "name": "Rob Brekelmans",
          "contact": "mailto:brekelma@usc.edu",
          "uris": ["https://github.com/brekelma/corexdiscrete.git"]
          },

      "installation": [{
          "type":"PIP",
          "package":"corexdiscrete",
          "version":"0.2.0"
      }],
      "algorithm_types": ["EXPECTATION_MAXIMIZATION_ALGORITHM"],
      "primitive_family": "FEATURE_CONSTRUCTION",
      "preconditions": ["NO_MISSING_VALUES", "NO_CONTINUOUS_VALUES"],
      "hyperparams_to_tune": ["n_hidden"]
    })
    #      "effects": [],

    # def __init__(self, n_hidden: int = None, dim_hidden : int = 2, latent_pct : float = .2, max_iter : int = 100, 
    #             tol : float = 1e-5, n_repeat : int = 1, max_samples : int = 10000, n_cpu : int = 1, 
    #             smooth_marginals : bool = False, missing_values : float = -1, 
    #             seed : int = None, verbose : bool = False, **kwargs) -> None: 
    def __init__(self, *, hyperparams : CorexDiscrete_Hyperparams, random_seed : int =  0, docker_containers: typing.Dict[str, str] = None) -> None:
        super().__init__(hyperparams = hyperparams, random_seed = random_seed, docker_containers = docker_containers)



        # if n_hidden:
        #     self.n_hidden = n_hidden
        #     self.model = corex_disc.Corex(n_hidden= self.n_hidden, dim_hidden = self.dim_hidden,
        #         max_iter = self.max_iter, n_repeat = self.n_repeat, max_samples = self.max_samples,
        #         n_cpu = self.n_cpu, smooth_marginals= self.smooth_marginals, missing_values = self.missing_values, 
        #         verbose = self.verbose, seed = self.seed, **kwargs)
        # else:
        #     self.latent_pct = latent_pct # default = .20% of columns
        #     self.model = None
        #     self.n_hidden = None

    def fit(self, *, timeout: float = None, iterations : int = None) -> CallResult[None]:
        if self.fitted:
            return
        if not hasattr(self, 'training_inputs'):
            raise ValueError("Missing training data.")

        if iterations is not None:
            self.max_iter = iterations
        else:
            self.max_iter = 100
            
        self._fit_transform(self.training_inputs, timeout, iterations)
        self.fitted = True
        return CallResult(None, True, self.max_iter)

    def produce(self, *, inputs : Input, timeout : float = None, iterations : int = None) -> CallResult[Output]: 

        self.columns = list(inputs)
        X_ = inputs[self.columns].values # TO DO: add error handling for X[self.columns]?

        if iterations is not None:
            self.max_iter = iterations
        else:
            self.max_iter = 100

        if not self.fitted:
            raise ValueError('Please fit before calling produce')

        #if self.dim_hidden == 2:
        self.latent_factors = self.model.transform(X_, details = True)[0]
        self.latent_factors = np.transpose(np.squeeze(self.latent_factors[:,:,1])) if len(self.latent_factors.shape) == 3 else self.latent_factors # assuming dim_hidden = 2
        #else:
        #    self.latent_factors = self.model.transform(X_)

        return CallResult(self.latent_factors, True, self.max_iter)

    def _fit_transform(self, inputs : Input, timeout : float = None, iterations : int = None) -> CallResult[Output]:
        self.columns = list(inputs)
        if len(self.columns) == 1:
            return inputs.values
        X_ = inputs[self.columns].values

        if iterations is not None:
            self.max_iter = iterations

        if isinstance(self.hyperparams['n_hidden'], int):
            self.n_hidden = self.hyperparams['n_hidden']
        elif isinstance(self.hyperparams['n_hidden'], float):
            self.n_hidden = max(1,int(self.hyperparams['n_hidden']*len(self.columns)))

        if not hasattr(self, 'model') or self.model is None:
            self.model = corex_disc.Corex(n_hidden= self.n_hidden, max_iter = self.max_iter)

        self.model.fit(X_)
        self.latent_factors = self.model.transform(X_, details = True)[0]
        #print('*** LATENT FACTORS SHAPE ***', self.latent_factors.shape)
        self.latent_factors = np.transpose(self.latent_factors[:,:,1]) if len(self.latent_factors.shape) == 3 else self.latent_factors # assuming dim_hidden = 2

        self.fitted = True
        
        return self.latent_factors

    def set_training_data(self, *, inputs : Input) -> None:
        self.training_inputs = inputs
        self.fitted = False

    def get_params(self) -> CorexDiscrete_Params:
        return CorexDiscrete_Params(model = self.model)

    def set_params(self, *, params: CorexDiscrete_Params) -> None:
        self.model = params['model']


    def _annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'CorexDiscrete'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'UnsupervisedLearning'
        self._annotation.ml_algorithm = ['Dimension Reduction']
        self._annotation.tags = ['feature_extraction'] #'discrete'
        return self._annotation

    def _get_feature_names(self):
        return ['CorexDisc_'+ str(i) for i in range(self.n_hidden)]