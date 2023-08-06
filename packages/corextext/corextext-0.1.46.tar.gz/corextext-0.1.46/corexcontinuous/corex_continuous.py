from sklearn import preprocessing
#import primitive
import sys
import os
import corexcontinuous.linearcorex.linearcorex.linearcorex as corex_cont
#import LinearCorex.linearcorex as corex_cont
from collections import defaultdict, OrderedDict
from scipy import sparse
import pandas as pd
import numpy as np

import d3m_metadata.container as container
import d3m_metadata.hyperparams as hyperparams
import d3m_metadata.params as params
from d3m_metadata.metadata import PrimitiveMetadata

from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
import primitive_interfaces.base
#from primitive_interfaces.params import Params
#from primitive_interfaces.hyperparams import HyperParameters

from typing import NamedTuple, Optional, Sequence, Any


Input = container.DataFrame
Output = container.ndarray

class CorexContinuous_Params(params.Params):
    model: corex_cont.Corex
    fitted: bool
    training_inputs: Input

    # add support for resuming training / storing model information


class CorexContinuous_HyperParams(hyperparams.Hyperparams):
    n_hidden : hyperparams.Union(OrderedDict([('n_hidden int' , hyperparams.Uniform(lower = 1, upper = 50, default = 2, q = 1, description = 'number of hidden factors learned')),
        ('n_hidden pct' , hyperparams.Uniform(lower = 0, upper = .50, default = .2, q = .05, description = 'number of hidden factors as percentage of # input columns'))], 
        default = 'n_hidden pct'), _structural_type = float)
    #max_df = hyperparams.Uniform(lower = .10, upper = 1, default = .9, q = .05, description = 'max percent document frequency of analysed terms', _structural_type = float)
    #min_df = hyperparams.Union(OrderedDict([('int df' , hyperparams.Uniform(lower = 1, upper = 20, default = 2, q = 1, description = 'min integer document frequency of analysed terms')),
    ##    ('pct df' , hyperparams.Uniform(lower = 0, upper = .10, default = .01, q = .01, description = 'min percent document frequency of analysed terms'))], 
    #   default = 'int df'), _structural_type = int)
    #max_features = hyperparams.Uniform(lower = 1000, upper = 50000, default = None, q = 1000, description = 'max number of terms to use')



class CorexContinuous(UnsupervisedLearnerPrimitiveBase[Input, Output, CorexContinuous_Params, CorexContinuous_HyperParams]):  #(Primitive):
    
    """
    Return components/latent factors that explain the most multivariate mutual information in the data under Linear Gaussian model. For comparison, PCA returns components explaining the most variance in the data.  Serves as DSBox 'wrapper' for https://github.com/gregversteeg/linearcorex"
    """
    metadata = PrimitiveMetadata({
      "schema": "v0",
      "id": "d2d4fefc-0859-3522-91df-7e445f61a69b",
      "version": "0.1.9",
      "name": "corexcontinuous.corex_continuous.CorexContinuous",
      "description": "Return components/latent factors that explain the most multivariate mutual information in the data under Linear Gaussian model. For comparison, PCA returns components explaining the most variance in the data.  Serves as DSBox 'wrapper' for https://github.com/gregversteeg/linearcorex",
      "python_path": "d3m.primitives.corexcontinuous.corex_continuous:CorexContinuous",
      "original_python_path": "corexcontinuous.corex_continuous:CorexContinuous",
      "source": {
          "name": "Rob Brekelmans",
          "contact": "brekelma@usc.edu",
          "uris": ["https://github.com/brekelma/corexcontinuous.git"]
          },

      "installation": {
          "type":"PIP",
          "package":"corexcontinuous",
          "version":"0.1.10"
      },
      "algorithm_types": ["EXPECTATION_MAXIMIZATION_ALGORITHM"],
      "primitive_family": "FEATURE_CONSTRUCTION",
      "preconditions": ["NO_MISSING_VALUES", "NO_CATEGORICAL_VALUES"],
      "effects": [],
      "hyperparams_to_tune": ["n_hidden"]
    })

    def __init__(self, n_hidden : Any = None, max_iter : int = 10000, 
            tol : float = 1e-5, anneal : bool = True, discourage_overlap : bool = True, gaussianize : str = 'standard',  
            gpu : bool = False, verbose : bool = False, seed : int = None, **kwargs) -> None:
        
        super().__init__()

        self.kwargs = kwargs
        self.max_iter = max_iter
        self.tol = tol
        self.anneal = anneal
        self.discourage_overlap = discourage_overlap
        self.gaussianize = gaussianize
        self.gpu = gpu
        self.verbose = verbose
        self.seed = seed

        #self.is_feature_selection = False
        #self.hyperparameters = {'n_hidden': None, 'latent_pct': .2} # NOT TRUE, default = latent pct
        
        if isinstance(n_hidden, int):
            self.n_hidden = n_hidden
            self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = max_iter, tol = tol, 
                anneal = anneal, discourage_overlap = discourage_overlap, gaussianize = gaussianize, 
                gpu = gpu, verbose = verbose, seed = seed, **kwargs)
        elif isinstance(n_hidden, float):
            self.latent_pct = n_hidden
            self.model = None
            self.n_hidden = n_hidden
        else:
            raise TypeError('n_hidden should be an int or zero-one float')

        # if latent_pct is not None and n_hidden is None:
        # 	self.n_hidden = int(len(self.columns)*latent_pct)
        # else:
        # 	self.n_hidden = 2 if n_hidden is None else n_hidden #DEFAULT = 2 

    def fit(self, timeout: float = None, iterations : int = None) -> CallResult[None]:
        if self.fitted:
            return
        if not hasattr(self, 'training_inputs'):
            raise ValueError("Missing training data.")

        self._fit_transform(self.training_inputs, timeout, iterations)
        self.fitted = True
        # add support for max_iter / incomplete
        return CallResult(None, True, self.max_iter)

    def produce(self, inputs : Input, timeout : float = None, iterations : int = None) -> CallResult[Output]: 

        self.columns = list(inputs)
        X_ = inputs[self.columns].values 
    	
        if iterations is not None:
            self.max_iter = iterations

        if not self.fitted:
            if self.model is None and self.latent_pct:
                self.n_hidden = max(1, int(self.latent_pct*len(self.columns)))
                self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = self.max_iter, tol = self.tol, 
                    anneal = self.anneal, discourage_overlap = self.discourage_overlap, gaussianize = self.gaussianize, 
                    gpu = self.gpu, verbose = self.verbose, seed = self.seed, **self.kwargs)

            self.latent_factors = self.model.fit_transform(X_)
        else:
            self.latent_factors = self.model.transform(X_)

        return CallResult(self.latent_factors, True, self.max_iter)

    def _fit_transform(self, inputs : Input, timeout: float = None, iterations : int = None) -> Sequence[Output]:
        
        self.columns = list(inputs)
        X_ = inputs[self.columns].values

        if self.model is None and self.latent_pct:
            self.n_hidden = max(1,int(self.latent_pct*len(self.columns)))

        if iterations is not None:
            self.max_iter = iterations


        if self.model is None and self.latent_pct:
        	self.model = corex_cont.Corex(n_hidden= self.n_hidden, max_iter = self.max_iter, tol = self.tol, 
                anneal = self.anneal, discourage_overlap = self.discourage_overlap, gaussianize = self.gaussianize, 
                gpu = self.gpu, verbose = self.verbose, seed = self.seed, **self.kwargs)

        self.latent_factors = self.model.fit_transform(X_)
        self.fitted = True
        return self.latent_factors

    def set_training_data(self, inputs : Input) -> None:
        self.training_inputs = inputs
        self.fitted = False

    def get_params(self) -> CorexContinuous_Params:
        return CorexContinuous_Params(model = self.model, fitted = self.fitted, training_inputs = self.training_inputs)

    def set_params(self, params: CorexContinuous_Params) -> None:
        self.model = params.model
        self.fitted = params.fitted
        self.training_inputs = params.training_inputs


    def annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'CorexContinuous'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'UnsupervisedLearning'
        self._annotation.ml_algorithm = ['Dimension Reduction']
        self._annotation.tags = ['feature_extraction', 'continuous']
        return self._annotation

    def get_feature_names(self):
    	return ['CorexContinuous_'+ str(i) for i in range(self.n_hidden)]

