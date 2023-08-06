import numpy as np
import typing
from sklearn.decomposition import PCA
from typing import NamedTuple, List
from primitive_interfaces.featurization import FeaturizationTransformerPrimitiveBase
from d3m_metadata import container, hyperparams, metadata, params

Input = container.numpy.ndarray
Output = container.List[int]

class Hyperparams(hyperparams.Hyperparams):
    pass

class PCAFeatures(FeaturizationTransformerPrimitiveBase[Input, Output, Hyperparams]):
    __author__ = "Distil"
    metadata = metadata.PrimitiveMetadata({
        "id": "142c4056-ccd3-3530-9fcc-e9fa7052662f",
        "version": "2.0.0",
        "schema": "https://metadata.datadrivendiscovery.org/schemas/v0/primitive.json",
        "description": "Perform feature selection using PCA components",
        "name": "PCA-based feature selection",
        "python_path": "d3m.primitives.distil.PCAFeatures",
        "original_python_path": "punk.feature_selection.pca.PCAFeatures",
        "algorithm_types": ["PRINCIPAL_COMPONENT_ANALYSIS"],
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
            "instance_methods": {
                "produce": {
                    "kind": "PRODUCE",
                    "description": "Accept numpy array and return a list of column indices, sorted by feature significance",
                    "arguments": ["inputs"],
                    "returns": "container.List[int]"
                }
            },
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

    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: typing.Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)
        pass

    def produce(self, *, inputs: Input) -> Output:
        """ Perform PCA and return a list of the indices of the most important
        features, ordered by contribution to first PCA component
                                                                                
        The matrix M will correspond to the absolute value of the components of 
        the decomposiiton thus giving a matrix where each column corresponds to 
        a principal component and rows are the components that rescale each 
        feature.  
                                                                                
        For example, pca.components_.T could look like this:                        
                                                                                
        array([[ 0.52237162,  0.37231836, -0.72101681, -0.26199559],                
            [-0.26335492,  0.92555649,  0.24203288,  0.12413481],                 
            [ 0.58125401,  0.02109478,  0.14089226,  0.80115427],                 
            [ 0.56561105,  0.06541577,  0.6338014 , -0.52354627]])                
                                                                                
        So the most important feature with respect to the first principal 
        component would be the 3rd feature as this has an absolute value of 
        0.58125401 which is greater than all the entries in that column.                             
                                                                                
                                                                                
        "importance_on1stpc" corresponds to the indices of most important       
        features for the first principal. Component are in ascending order      
        (most important feature 0, least important feature n_features-1).       
                                                                                
        
        Params 
        ------- 
        data : np.ndarray, [n_samples, n_features]
            Training data.
        """

        pca = PCA()

        try:
            pca.fit_transform(inputs)

            M = np.absolute(pca.components_.T)

            # Rank features based on contribtuions to 1st PC
            self.importance_on1stpc = np.argsort(M[:,0], axis=0)[::-1]
        except:
            # If any error occurs, just return indices in original order
            # In the future we should consider a better error handling strategy
            self.importance_on1stpc = [i for i in range(inputs.shape[0])]

        return self.importance_on1stpc