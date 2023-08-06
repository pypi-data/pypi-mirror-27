from typing import List, Tuple, Dict
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline                                                                
from sklearn.model_selection import GridSearchCV
from primitive_interfaces.featurization import FeaturizationTransformerPrimitiveBase
from d3m_metadata import container, hyperparams, metadata, params

Inputs = container.List[container.numpy.ndarray]
Outputs = container.List[int]

class RFHyperparams(hyperparams.Hyperparams):
    problem_type = hyperparams.Hyperparameter(default='classification')
    scoring = hyperparams.Hyperparameter(default='accuracy')
    crossval = hyperparams.Hyperparameter(default=3)
    verbose = hyperparams.Hyperparameter(default=0)
    n_jobs = hyperparams.Hyperparameter(default=1)

class RFFeatures(FeaturizationTransformerPrimitiveBase[Inputs, Outputs, RFHyperparams]):
    __author__ = "Distil"
    metadata = metadata.PrimitiveMetadata({
        "id": "b970e9af-0e80-382b-8a46-fbd64e3dc6fa",
        "version": "2.0.0",
        "schema": "https://metadata.datadrivendiscovery.org/schemas/v0/primitive.json",
        "description": "Perform feature selection using Random Forest",
        "name": "Random Forest-based feature selection",
        "python_path": "d3m.primitives.distil.RFFeatures",
        "original_python_path": "punk.feature_selection.rf.RFFeatures",
        "algorithm_types": ["RANDOM_FOREST"],
        "installation": [{
            "package": "punk",
            "type": "PIP",
            "version": "2.0.0"
        }],
        "primitive_code": {
            "class_type_arguments": {},
            "interfaces_version": "2017.12.27",
            "interfaces": ["primitives_interfaces.featurization.FeaturizationTransformerPrimitiveBase"],
            "hyperparams": {},
            "arguments": {
                "inputs": {
                    "type": "container.numpy.ndarray",
                    "kind": "PIPELINE"
                }
            },
            "class_methods": {},
            "class_attributes": {},
            "instance_attributes": {} 
        },
        "primitive_family": "FEATURE_SELECTION",
        "source": {
            "name": "Distil",
            "contact": "http://newknowledge.io/contact/"
        },
        "structural_type": "numpy.ndarray"
    })

    def __init__(self, *, hyperparams:RFHyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)

        """
        Params
        ------
        problem_type : str
            ``classification`` or ``regression``.
        
        scoring : string, callable, list/tuple, dict or None, default: None
            A single string (see The scoring parameter: defining model
            evaluation rules) or a callable (see Defining your scoring strategy
            from metric functions) to evaluate the predictions on the test set.

            For evaluating multiple metrics, either give a list of (unique)
            strings or a dict with names as keys and callables as values.

            NOTE that when using custom scorers, each scorer should return a
            single value. Metric functions returning a list/array of values can
            be wrapped into multiple scorers that return one value each.
            
            See Specifying multiple metrics for evaluation for an example.
            
            If None, the estimator’s default scorer (if available) is used.


        crossval : int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy. Possible inputs
            for cv are:
                None, to use the default 3-fold cross validation,
                integer, to specify the number of folds in a (Stratified)KFold,
                An object to be used as a cross-validation generator.
                An iterable yielding train, test splits.

            For integer/None inputs, if the estimator is a classifier and y is
            either binary or multiclass, StratifiedKFold is used. In all other
            cases, KFold is used.

            Refer User Guide for the various cross-validation strategies that
            can be used here.

        n_jobs : int, default=1
            Number of jobs to run in parallel.

        verbose : integer
            Controls the verbosity: the higher, the more messages.
        """
        # self.__problem_type__ = self.hyperparams['problem_type']
        # self.__crossval__      = self.hyperparams['crossval']
        # self.scoring = self.hyperparams['scoring']
        # self.n_jobs  = self.hyperparams['n_jobs']
        # self.verbose = self.hyperparams['verbose']
        # self.params  = {'problem_type': self.problem_type, 'cross_validation': self.crossval,
        #                 'scoring': self.scoring}

    def produce(self, *, inputs: Inputs) -> Outputs:
        print(self.hyperparams)
        """ Rank features using Random Forest classifier.                           
                                                                                
	    Use GridSearchCV to optimize the scoring method for a random forest         
    	classifier and return the importance of the features.    

        "indices" indicate the feature importances of features order in
        ascending order (most importance feature to least important features).

        "feature_importances" The feature importances (the higher, the more
        important the feature).
                                                                                
    	Params                                                                      
    	------                                                                      
        data : tuple of arrays 
            ([n_samples, n_features], [n_samples, n_features]) corresponding to
            training data and labels.
        """
        self.X, self.y = inputs

        # Chose classfier or regressor
        if self.hyperparams.get('problem_type')=="classification":
            rf = Pipeline([('clf', RandomForestClassifier(random_state=1))])    
        elif self.hyperparams.get('problem_type')=="regression":
            rf = Pipeline([('clf', RandomForestRegressor(random_state=1))])
        else:
            raise ValueError(
                "problem_type must be 'classification' or 'regression'."
            )

        # Gridsearch for hyperparam optimization
        param_grid = [{'clf__n_estimators': [10, 100, 1000]},]                                          
        gs_rf = GridSearchCV(rf,                                                    
                             param_grid, 
                             cv      = self.hyperparams.get('cross_validation'),
                             scoring = self.hyperparams.get('scoring'),                                     
                             verbose = self.hyperparams.get('verbose'),                                           
                             n_jobs  = self.hyperparams.get('n_jobs'))                                           
        gs_rf.fit(self.X, self.y)                                                             
                                                                                
        # Rank from most to least important features (0, d-1)                       
        self.feature_importances = \
                gs_rf.best_estimator_.named_steps["clf"].feature_importances_
        self.indices = np.argsort(self.feature_importances)[::-1]                         

        return self.indices
