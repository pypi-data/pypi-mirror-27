import os
from typing import NamedTuple, Union, List, Sequence, Any, Optional
from typing import TypeVar
import scipy.io
import numpy as np
from d3m_types.sequence import ndarray
from primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase
import rpi_feature_selection_toolbox


Inputs = ndarray
Outputs = ndarray
Params = NamedTuple('Params', [
    ('index', ndarray),
])



class IPCMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False

    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.IPCMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass



class JMIplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.JMIplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class STMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.STMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class aSTMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.aSTMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class sSTMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.sSTMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class pSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.pSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class F_STMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_STMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class F_aSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_aSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class F_sSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_sSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass




class JMIp_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self) -> None:
        super().__init__()

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.JMIp()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> Params:
        return Params(index = self.index)


    def set_params(self):
        pass


















