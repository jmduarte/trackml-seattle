from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import numpy as np
import pandas as pd

__authors__ = ['Sabrina Amrouche', 'David Rousseau', 'Moritz Kiehn']

"""
scores a dataset using the TrackML custom metric
"""


def compute_score(submission, solution, verbose=0):
    # combine to get the true and reconstructed particle id for each hit
    # validate checks that each key exist once and there are no duplicates
    dataset = merge_solution_submission(solution, submission)

    score_mean, score_std, n_purity_reco, n_purity_truth = score_dataset(dataset, verbose=verbose)
    return score_mean, score_std, n_purity_reco, n_purity_truth


def merge_solution_submission(solution, submission):
    dataset = pd.merge(solution, submission,
                       on=['event_id', 'hit_id'],
                       how='left', validate='one_to_one')
    return dataset


def score_dataset(dataset, verbose=1):
    scores = []
    # split dataset into events
    for event_id, event in dataset.groupby('event_id', sort=False):
        score_event = 0
        n_purity_reco = 0
        n_purity_truth = 0

        # split hits into reconstructed tracks
        for track_id, track in event.groupby('track_id', sort=False):
            # find contributing particles sorted by occurence
            particles = track['particle_id'].value_counts()
            # the particles contributing the most hits
            major_id = particles.index[0]
            major_nhits_matched = particles.iloc[0]

            # need at least half (wrt to the reco track) of hits matched
            purity_reco = major_nhits_matched / len(track)
            if purity_reco < 0.51:
                n_purity_reco += 1
                continue

            # need at least half  (wrt to the reco track) of hits matched
            # count number of true hits of the major
            major_nhits = len(event.loc[event['particle_id'] == major_id])
            purity_truth = major_nhits_matched / major_nhits
            if purity_truth < 0.51:
                n_purity_truth += 1
                continue

            # track score is the sum of the reco hit weights that belong to the major particle
            # this is the intersection between the reco and the truth
            score_track = track['weight'].where(track['particle_id'] == major_id).sum()
            score_event += score_track

        # normalize wrt total weight. A perfect reco algorithm should get score 1.
        score_event /= event['weight'].sum()
        scores.append(score_event)

    # normalize to the number of events
    score_mean = np.mean(scores)
    score_median = np.median(scores)
    score_std = np.std(scores)
    if verbose:
        print('score mean:   {:f}'.format(score_mean))
        print('score median: {:f}'.format(score_median))
        print('score stddev: {:f}'.format(score_std))
        print('purity_reco: {:d}'.format(n_purity_reco))
        print('purity_truth: {:d}'.format(n_purity_truth))
    return score_mean, score_std, n_purity_reco, n_purity_truth


def check_event(tracks, truth):
    """
    Check that the event and solution are consistent
    """
    # check for duplicates
    dup_mask = tracks.duplicated('hit_id')
    if np.any(dup_mask):
        dup = sorted(truth[dup_mask]['hit_id'])
        raise Exception('Tracks contain duplicated hits: {}'.format(dup))
    dup_mask = truth.duplicated('hit_id')
    if np.any(dup_mask):
        dup = sorted(truth[dup_mask]['hit_id'])
        raise Exception('Truth contains duplicated hits: {}'.format(dup))


def main(submission_file, solution_file):
    solution_dtypes = {
        'event_id': 'i4',
        'hit_id': 'i4',
        'particle_id': 'i8',
        'weight': 'f4', }
    solution = pd.read_csv(solution_file, header=0, dtype=solution_dtypes)
    submission_dtypes = {
        'event_id': 'i4',
        'hit_id': 'i4',
        'track_id': 'i4', }
    submission = pd.read_csv(submission_file, header=0, dtype=submission_dtypes)
    compute_score(submission, solution, verbose=1)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description='score a solution')
    parser.add_argument('submission_file')
    parser.add_argument('solution_file')
    args = parser.parse_args()

    main(**vars(args))
