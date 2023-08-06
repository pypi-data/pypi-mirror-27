#! /usr/bin/env python
from __future__ import print_function
from bigsi.graph import BIGSI as Graph
import os.path
import sys
import logging
import json
logger = logging.getLogger(__name__)
from bigsi.utils import DEFAULT_LOGGING_LEVEL
logger.setLevel(DEFAULT_LOGGING_LEVEL)

from bigsi.tasks import run_insert


def insert(kmers, bloom_filter, async=False):
    if async:
        logger.debug("Inserting with a celery task")
        result = run_insert.delay(bloom_filter)
        result = result.get()
    else:
        logger.debug("Inserting without a celery task")
        result = run_insert(bloom_filter)
    return result
