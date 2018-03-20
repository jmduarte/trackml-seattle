from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import pandas as pd

from sklearn.base import BaseEstimator
from joblib import Parallel, delayed


class BaseTracker(BaseEstimator):
    def __init__(self):
        super().__init__()

    def fit_generator(self, event_generator):
        raise NotImplemented("The fit_generator method should be implemented")

    def predict_generator(self, event_generator):
        raise NotImplemented("The predict_generator method should be implemented")

    def predict_one_event(self, event_id, event):
        raise NotImplemented("The predict_one_event method should be implemented")


class ParallelPredictTracker(BaseTracker):
    """ Decorator that enable parralel prediction of events from generator.
    """
    def __init__(self, tracker, n_jobs=2, backend="multiprocessing"):
        super().__init__()
        self.tracker = tracker
        self.n_jobs = n_jobs
        if backend not in ("multiprocessing", "threading"):
            raise ValueError("backend should be multiprocessing or threading : {} found".format(backend))
        self.backend = backend

    def fit_generator(self, event_generator):
        self.tracker.fit(event_generator)

    def predict_generator(self, event_generator):
        sub_list = Parallel(n_jobs=self.n_jobs, backend=self.backend)(
                        delayed(self.tracker.predict_one_event)(event_id, event) 
                        for event_id, event in event_generator)
        submission = pd.concat(sub_list)
        return submission

    def predict_one_event(self, event_id, event):
        return self.tracker.predict_one_event(event_id, event)
