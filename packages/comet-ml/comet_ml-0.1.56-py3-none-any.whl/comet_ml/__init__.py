"""comet"""
from pkg_resources import get_distribution, DistributionNotFound

from .comet import Experiment


try:
    __version__ = get_distribution('comet_ml').version
except DistributionNotFound:
    __version__ = 'Please install comet with `pip install comet_ml`'


__author__ = 'Gideon <Gideon@comet.ml>'
__all__ = ['Experiment']
