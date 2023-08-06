import os
import numpy as np
import xml.etree.ElementTree as ET
import itertools
import pandas as pd


def parse_mvnx(fn):
    mvnx = MVNX(fn)
    return mvnx.parse_mvnx()


class MVNX(object):
    def __init__(self, fn):
        self.tree, self.root = read_mvnx(fn)

    def parse_mvnx(self):
        D, tree, root = {}, self.tree, self.root
        prefix = '{http://www.xsens.com/mvn/mvnx}'
        joints = root[2].findall(prefix + 'joints')[0]
        joint_labels = [s.attrib['label'] for s in joints.getchildren()]
        D['jointIndices'] = {j: range(3*i, 3*(i+1))
                            for (i, j) in enumerate(joint_labels)}
        tags = [e.tag for e in root.getchildren()[2][-1][100].getchildren()]
        for s in tags:
            all_data = tree.findall('.//' + s)
            # TODO: this should be avoided. possibly best to read directly into
            # DataFrame
            x = np.array([to_float(o.text) for o in all_data])
            s = s.split('}', 1)[1]
            D[s] = x
        times = [i.get('ms') for i in root[2][-1]]
        D['times'] = times
        D['jointAngle'] = remove_discontinuities(D['jointAngle'])
        return D


def read_mvnx(fn):
    tree = ET.parse(fn)
    root = tree.getroot()
    return tree, root


def to_float(s):
    # TODO: slow, speed up!
    return np.array([float(x) for x in s.split(' ')])


def remove_discontinuities(arr):
    jump_x, jump_joint = np.where(abs(np.diff(arr, axis=0)) > 180)
    gaps = zip(jump_x[:-1:2], jump_x[1::2], jump_joint[1::2])
    for i, j, w in gaps:
        arr[i+1:j+1, w] += 360.
    return arr


def load_accelerations(fp='data/indoor.mvnx'):
    rf_name = 'right_foot_acceleration.pkl'
    lf_name = 'left_foot_acceleration.pkl'

    if not os.path.isfile(rf_name):
        # Load data
        mvnx = MVNX(fp)
        data = mvnx.parse_mvnx()
        # prepare multiindex
        sensors = mvnx.root[2][2].getchildren()
        sensor_names = [s.attrib['label'] for s in sensors]
        dat = data['sensorAcceleration']
        idx = list(itertools.product(sensor_names, ['x', 'y', 'z']))
        midx = pd.MultiIndex.from_tuples(idx, names=['sensor', 'coord'])
        # convert to DataFrame
        df = pd.DataFrame(data=dat.T, index=midx)
        left_foot_acc = df.loc['LeftFoot']
        right_foot_acc = df.loc['RightFoot']
        # save as pickle to save time (in class FootAcceleration)
        pd.to_pickle(left_foot_acc, lf_name)
        pd.to_pickle(right_foot_acc, rf_name)
    else:
        print('loading from pkl (reminder: switch to json).')
        left_foot_acc = pd.read_pickle(lf_name)
        right_foot_acc = pd.read_pickle(rf_name)
    return right_foot_acc, left_foot_acc
