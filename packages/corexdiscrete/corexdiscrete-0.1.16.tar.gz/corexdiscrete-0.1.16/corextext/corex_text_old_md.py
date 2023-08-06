from sklearn import preprocessing
#import primitive
import sys
import os
#sys.path.append('corex_topic/')
from corextext.corextext.corex_topic import Corex
#import corex_topic.corex_topic as corex_text
from collections import defaultdict, OrderedDict
from scipy import sparse
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np

import d3m_metadata.container as container
import d3m_metadata.hyperparams as hyperparams
import d3m_metadata.params as params
from d3m_metadata.metadata import PrimitiveMetadata

from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from primitive_interfaces.base import CallResult
#from primitive_interfaces.params import Params
from d3m_metadata.hyperparams import Uniform, UniformInt, Union

from typing import NamedTuple,Optional, Sequence

import inspect
import typing

import git  # type: ignore
import typing_inspect  # type: ignore
from pytypes import type_util  # type: ignor


Input = container.DataFrame
Output = container.DataFrame

class CorexText_Params(params.Params):
    model: Corex
    bow: TfidfVectorizer
    get_text: bool
    data_path: str
    fitted: bool
    training_inputs: Input
    # add support for resuming training / storing model information


# class CorexText_HyperParams(hyperparams.Hyperparams):
#     max_df : Uniform(lower = .10, upper = 1, default = .9, q = .05, semantic_types = None, description = 'max percent document frequency of analysed terms')
#     min_df : Union(OrderedDict([('int df' , Uniform(lower = 1, upper = 20, default = 2, q = 1, semantic_types = int, description = 'min integer document frequency of analysed terms')),
#         ('pct df' , Uniform(lower = 0, upper = .10, default = .01, q = .01, semantic_types = float, description = 'min percent document frequency of analysed terms'))]), 
#         default = 'int df')
#     n_hidden : Uniform(lower = 0, upper = 100, default = 10, q = 1, description = 'number of topics')
#     max_features : Uniform(lower = 1000, upper = 50000, default = None, q = 1000, description = 'max number of terms to use')



class TFIDF: #(Primitive):
    def __init__(self, replace_df = True, raw_data_path = None, **kwargs):
        '''TO DO:  Add functionality to analyze multiple columns together'''
        self.cls = 'corex_primitives.tfidf' 
        #super().__init__(name = 'TFIDF', cls = 'corex_primitives.tfidf')

        self.bow = TfidfVectorizer(decode_error='ignore', **kwargs)
        
        self.replace_df = True #necessary?
        self.raw_data_path = raw_data_path


    def fit(self, X, y = None):
        self.columns = list(X)
        if len(self.columns) > 1:
            self.columns = self.columns[0] if self.columns[0] != X.index.name else self.columns[1]
            print ('WARNING: Only first column being analyzed', self.columns)
            # TO DO: handle multiple? naming in transform... modify read_text

        if self.raw_data_path is not None:
            #for col in self.columns: #multiple columns?
            self.idf_ = self.bow.fit_transform(self._read_text(X, self.columns, self.raw_data_path))
        else: #data frame contains raw text
            #for col in self.columns:
            self.idf_ = self.bow.fit_transform(X[col].values)
        return self

    def transform(self, X, y = None):
        # just let X be new dataframe of single column
        self.idf_df = pd.DataFrame(columns = str(self.columns+'_tfidf'), index = X.index) 
        self.idf_df.fillna()
        self.idf_df= self.idf_df.astype('object')
        
        for i, _ in self.idf_df.iterrows():
            #for col in self.columns:
            self.idf_df.loc[i, self.columns] = self.idf_[i, :]
        
        # returns dataframe in order to put array rows in each index
        return self.idf_df
                
        # returns matrix (n_samples, n_vocab) instead of a single pandas df
        # return self.idf_

    def fit_transform(self, X, y = None):
        #only set up for one column... last column will be stored / returned if multiple given
        self.fit(X, y)
        return self.transform(X, y)

    def _read_text(self, df, columns, data_path):
        column = columns # still takes column just in case want to switch back
        df = pd.DataFrame(df)
        #for col in columns:
        for i, _ in df.iterrows():
            file = df.loc[i, column]
            #legacy check for faulty one-hot encoding
            file = file if not isinstance(file, int) else str(file)+'.txt' 
            with open(os.path.join(data_path, file), 'r') as myfile:
                    yield myfile.read()

    def annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'TFIDF'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'NA'
        self._annotation.ml_algorithm = 'NA'
        self._annotation.tags = ['feature_extraction', 'text']
        return self._annotation

    def _get_feature_names(self):
        return ['tfidf'] # col + '_' + 'tfidf' in L2 execution


class CorexText(UnsupervisedLearnerPrimitiveBase[Input, Output, CorexText_Params]):  #(Primitive):
    """
    Learns latent factors / topics which explain the most multivariate information in bag of words representations of documents. Returns learned topic scores for each document. Also supports hierarchical models and 'anchoring' to encourage topics to concentrate around desired words.
    """
    metadata = PrimitiveMetadata({
          "schema": "v0",
          "id": "18e63b10-c5b7-34bc-a670-f2c831d6b4bf",
          "version": "0.2.0",
          "name": "CorexText",
          "description": "Learns latent factors / topics which explain the most multivariate information in bag of words representations of documents. Returns learned topic scores for each document. Also supports hierarchical models and 'anchoring' to encourage topics to concentrate around desired words.",
          "python_path": "d3m.primitives.corextext.corex_text:CorexText",
          "original_python_path": "corextext.corex_text.CorexText",
          "source": {
              "name": "Rob Brekelmans",
              "contact": "brekelma@usc.edu",
              "uris": ["https://github.com/brekelma/corextext.git"]
              },

          "installation": {
              "type":"PIP",
              "package":"corextext",
              "version":"0.2.0"
          },
          "algorithm_types": ["EXPECTATION_MAXIMIZATION_ALGORITHM", "LATENT_DIRICHLET_ALLOCATION"],
          "primitive_family": "FEATURE_CONSTRUCTION",
          "preconditions": [],
          "effects": [],
          "hyperparams_to_tune": ["n_hidden", "max_df", "min_df"]
        })

    #def __init__(self, hyperparams : CorexText_HyperParams, get_text : bool = False, data_path : str= None, iterations: int = 200, count: str ='binarize', eps: float = 1e-5, random_seed : int =None, verbose : bool =False,  **kwargs) -> None:
    def __init__(self, n_hidden : int = 10, max_df: float = 0.9, min_df: float = 2, max_features: int = None, 
        get_text : bool = False, data_path : str= None, iterations: int = 200, count: str ='binarize', eps: float = 1e-5, random_seed : int =None, verbose : bool =False,  **kwargs) -> None:

        super().__init__()
        #self.n_hidden = hyperparams['n_hidden']
        #self.max_df = hyperparams['max_df']
        #self.min_df = hyperparams['min_df']
        #self.max_features = hyperparams['max_features']
        self.n_hidden = n_hidden #DEFAULT = 10 topics (no latent_pct equivalent)
        self.max_df = max_df
        self.min_df = min_df #note: float = %, int = count of document frequencies
        self.max_features = max_features

        self.max_iter = iterations # defer to runtime
        self.get_text = get_text
        self.data_path = data_path
        
        self.fitted = False
        self.training_inputs = None

        # no real need to pass extra Corex parameters.  kwargs used for TFIDF
        self.model = Corex(n_hidden= self.n_hidden, max_iter = self.max_iter, eps = eps, seed = random_seed, verbose= verbose, count = count)#, **kwargs)

        if not self.get_text:
            self.bow = TfidfVectorizer(input = 'content', decode_error='ignore', max_df = self.max_df, min_df = self.min_df, max_features = self.max_features, **kwargs)
        else:
            self.bow = TfidfVectorizer(input = 'filename', max_df = self.max_df, min_df = self.min_df, max_features = self.max_features, binary = True, use_idf = False, norm = None, **kwargs)
            #self.bow = TfidfVectorizer(input = 'filename', max_df = self.max_df, min_df = self.min_df, max_features = self.max_features, binary = True, use_idf = False, norm = None, **kwargs)
        #if max_factors not None and n_hidden is None:
       #    self.n_hidden = int(max_factors/len(self.columns))
        #else:
         
    def fit(self, timeout : float = None, iterations : int = None) -> CallResult[None]: #X : Sequence[Input]): 
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed
        if self.fitted:
            return

        if not hasattr(self, 'training_inputs'):
            raise ValueError("Missing training data.")

        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter

        #print('****Raw inputs **** ', self._get_raw_inputs()[0:10])
        bow = self.bow.fit_transform(self.training_inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs())
        self.latent_factors = self.model.fit_transform(bow)
        self.fitted = True
        return CallResult(None, True, self.max_iter)


    def produce(self, inputs : Input, timeout : float = None, iterations : int = None) -> CallResult[Output]: # TAKES IN DF with index column
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed
        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter

        if not self.fitted:
            bow = self.bow.fit_transform(inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs(inputs = inputs, data_path = self.data_path))
            self.latent_factors = self.model.fit_transform(bow).astype(float)
            self.fitted = True
        else:
            bow = self.bow.transform(inputs.values.ravel()) if not self.get_text else self.bow.transform(self._get_raw_inputs(inputs = inputs, data_path = self.data_path))
            self.latent_factors = self.model.transform(bow).astype(float)

        # TO DO : Incorporate timeout, max_iter
        return CallResult(self.latent_factors, True, self.max_iter)

    def _fit_transform(self, inputs : Input, timeout : float = None, iterations : int = None) -> Sequence[Output]: # TAKES IN DF with index column
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed


        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter

        bow = self.bow.fit_transform(inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs(inputs = inputs))
        self.latent_factors = self.model.fit_transform(bow)
        self.fitted = True
        return self.latent_factors

    def _get_raw_inputs(self, inputs : Input = None, data_path = None) -> np.ndarray:
        print_ = True
        raw_inputs = self.training_inputs.values if inputs is None else inputs.values
        inp = self.training_inputs.values if inputs is None else inputs.values
        if data_path is not None:
            for idx, val in np.ndenumerate(inp):
                raw_inputs[idx] = os.path.join(data_path, val)
        elif self.data_path is not None:
            for idx, val in np.ndenumerate(inp):
                raw_inputs[idx] = os.path.join(self.data_path, val)
        else:
            print('Warning: data_path not passed')
        
        return raw_inputs.ravel()
    

    def set_training_data(self, inputs : Input) -> None:
        self.training_inputs = inputs
        self.fitted = False

    def get_params(self) -> CorexText_Params:
        return CorexText_Params(model = self.model, bow = self.bow, get_text = self.get_text, data_path = self.data_path, 
                                fitted = self.fitted, training_inputs = self.training_inputs)

    def set_params(self, params: CorexText_Params) -> None:
        self.model = params.model
        self.bow = params.bow
        self.get_text = params.get_text
        self.data_path = params.data_path
        self.fitted = params.fitted
        self.training_inputs = params.training_inputs

    def annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'CorexText'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'UnsupervisedLearning'
        self._annotation.ml_algorithm = ['Dimension Reduction']
        self._annotation.tags = ['feature_extraction', 'text']
        return self._annotation

    def get_feature_names(self):
        return ['CorexText_'+ str(i) for i in range(self.n_hidden)]