from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import bz2
import gzip
import ast
import glob

# import numpy as np
import pandas as pd

"""TrackML dataset loading"""

__authors__ = ['Moritz Kiehn', 'Sabrina Amrouche']


def read_hits(filename, separated_pixels=False):
    if filename.endswith(".gz"):
        fp = gzip.open(filename, 'rt')
    elif filename.endswith(".bz2"):
        fp = bz2.open(filename, 'rt')
    else:
        fp = open(filename)

    if fp is not None:
        header = [x.strip() for x in fp.readline().split(',')]
        if not separated_pixels:
            parsed_line = []
            for line in fp:
                if line.strip():
                    pline = ast.literal_eval(line)
                    features = list(pline[:8])
                    clusters = list(pline[8:])
                    features.append( [list(clusters[i:i+3]) for i in range(0, len(clusters), 3)] )
                    parsed_line.append(features)
            df_data = pd.DataFrame(parsed_line)
        else:
            df_data = pd.DataFrame( [ast.literal_eval(line) for line in fp if line.strip()] )
            df_data.columns = header
        fp.close()
    header[8] = "pixels"
    df_data.columns = header[:9]
    return df_data

def read_truth(filename):
    if filename.endswith(".gz"):
        fp = gzip.open(filename, 'rt')
    elif filename.endswith(".bz2"):
        fp = bz2.open(filename, 'rt')
    else:
        fp = open(filename)

    if fp is not None:
        header = [x.strip() for x in fp.readline().split(',')]
        df_data = pd.DataFrame( [ast.literal_eval(line) for line in fp if line.strip()] )
        df_data.columns = header
        fp.close()
    return df_data


def load_hit_generator(data_path, **kw):
    """
    Provide an iterator over all events in a dataset directory.

    For each event it returns the event_id and the output of `load_event`
    concatenated as a single tuple.
    """
    file_list = glob.glob(os.path.join(data_path, 'event*-hits*'))
    name_list = set(os.path.basename(file).split('-', 1)[0] for file in file_list)
    name_list = sorted(name_list)
    for name in name_list:
        event_id = int(name[5:])
        file = os.path.join(data_path, name + "-hits.csv.bz2")
        yield event_id, read_hits(file, **kw)

        
def load_hit_truth_generator(data_path, **kw):
    """
    Provide an iterator over all events in a dataset directory.

    For each event it returns the event_id and the output of `load_event`
    concatenated as a single tuple.
    """
    file_list = glob.glob(os.path.join(data_path, 'event*-hits*'))
    name_list = set(os.path.basename(file).split('-', 1)[0] for file in file_list)
    name_list = sorted(name_list)
    for name in name_list:
        event_id = int(name[5:])
        file = os.path.join(data_path, name + "-hits.csv.bz2")
        truth_file = os.path.join(data_path, name + "-truth.csv.bz2")
        yield event_id, read_hits(file, **kw), read_truth(truth_file)
        
        
def load_hit_particle_generator(data_path, **kw):
    """
    Provide an iterator over all events in a dataset directory.

    For each event it returns the event_id and the output of `load_event`
    concatenated as a single tuple.
    """
    file_list = glob.glob(os.path.join(data_path, 'event*-hits*'))
    name_list = set(os.path.basename(file).split('-', 1)[0] for file in file_list)
    name_list = sorted(name_list)
    for name in name_list:
        event_id = int(name[5:])
        file = os.path.join(data_path, name + "-hits.csv.bz2")
        particle_file = os.path.join(data_path, name + "-particles.csv.bz2")
        yield event_id, read_hits(file, **kw), read_truth(particle_file)


def load_hits(data_path):
    hit_list = []
    for event_id, hit in load_hit_generator(data_path):
        hit['event_id'] = event_id
        hit_list.append(hit)
    data = pd.concat(hit_list)
    return data


def load_hits_truth(data_path):
    hit_list = []
    truth_list = []
    for event_id, hit, truth in load_hit_truth_generator(data_path):
        hit['event_id'] = event_id
        truth['event_id'] = event_id
        hit_list.append(hit)
        truth_list.append(truth)
    data = pd.concat(hit_list)
    truth = pd.concat(truth_list)
    return data, truth