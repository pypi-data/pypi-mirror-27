# -*- coding: utf-8 -*-
"""A simple probabilistic counter."""

from probcount import metadata
from .probcounterlib import ProbCounter, MockCounter

__all__ = ["ProbCounter", "MockCounter"]

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

