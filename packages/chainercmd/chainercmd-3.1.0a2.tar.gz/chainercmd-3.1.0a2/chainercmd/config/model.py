import os
import shutil
from importlib import import_module
from importlib.machinery import SourceFileLoader

from chainercmd.config.base import ConfigBase

import chainer


class Model(ConfigBase):

    def __init__(self, **kwargs):
        required_keys = [
            'file',
            'name',
        ]
        optional_keys = [
            'args'
        ]
        super().__init__(
            required_keys, optional_keys, kwargs, self.__class__.__name__)


class Loss(ConfigBase):

    def __init__(self, **kwargs):
        required_keys = [
            'file',
            'name',
        ]
        optional_keys = [
            'args',
        ]
        super().__init__(
            required_keys, optional_keys, kwargs, self.__class__.__name__)


def get_model(
        result_dir, model_file, model_name, model_args,
        loss_file, loss_name, loss_args):
    model_fullname = model_file.replace('/', '.').replace('.py', '')
    model_fullname += '.{}'.format(model_name)
    loader = SourceFileLoader(model_fullname, model_file)
    mod = loader.load_module()
    model = getattr(mod, model_name)

    # Copy model file
    if chainer.config.train:
        dst = '{}/{}'.format(result_dir, os.path.basename(model_file))
        if not os.path.exists(dst):
            shutil.copy(model_file, dst)

    # Initialize
    if model_args is not None:
        model = model(**model_args)
    else:
        model = model()

    # Wrap the model with loss class
    if chainer.config.train and loss_name is not None:
        loader = SourceFileLoader(loss_name, loss_file)
        mod = loader.load_module()
        loss = getattr(mod, loss_name)
        if loss_args is not None:
            model = loss(model, **loss_args)
        else:
            model = loss(model)

        if loss_file is not None:
            # Copy loss file
            dst = '{}/{}'.format(result_dir, os.path.basename(loss_file))
            if not os.path.exists(dst):
                shutil.copy(loss_file, dst)
    return model


def get_model_from_config(config):
    model = Model(**config['model'])
    loss = Loss(**config['loss'])
    return get_model(
        config['result_dir'], model.file, model.name, model.args,
        loss.file, loss.name, loss.args)
