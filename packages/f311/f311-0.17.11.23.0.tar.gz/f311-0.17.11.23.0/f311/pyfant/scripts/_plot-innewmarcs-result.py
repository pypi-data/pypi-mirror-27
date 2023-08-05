#!/usr/bin/env python
"""
Plots interpolated atmospheric model curve (hopefully) in the middle of the curves
used by innewmarcs for interpolation.

The file containing which files and records innewmarcs chose is assumed to be called
'innewmarcs_explain.txt'

This file can be generated by invoking the Fortran binary like this:
  > innewmarcs --explain
"""


import argparse
import matplotlib.pyplot as plt
import re
import numpy as np
from itertools import cycle
from mpl_toolkits.mplot3d import Axes3D  # yes, required
import a99
import logging


a99.logging_level = logging.INFO
a99.flag_log_file = True


def parse_explain_file(filename):
    """Extracts information from "explain" file created by innewmarcs."""
    tokens = {}
    with open(filename) as h:
        while True:
            s = h.readline().strip()
            if not s:
                break
            m = re.match(r"(.+):\s*(.*)", s)
            if not m:
                raise RuntimeError('Error parsing file "%s"' % filename)
            token, s_data = m.groups()
            tokens[token] = eval(s_data)
    return tokens


FN_EXPLAIN = 'innewmarcs_explain.txt'
VARS = ['nh', 'teta', 'pe', 'pg', 'log_tau_ross']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
     description=__doc__,
     formatter_class=a99.SmartFormatter
     )
    parser.add_argument('--inum', type=int, default=1, help='Record number (>= 1)')
    parser.add_argument('--var', type=str, help='Variable to plot', default=VARS[0], choices=VARS)

    args = parser.parse_args()

    tokens = parse_explain_file(FN_EXPLAIN)
    fn_grid = tokens['innewmarcs grid file']
    fn_output = tokens['innewmarcs output file']
    indexes = np.array(np.matrix(tokens['innewmarcs indexes'])).flatten()
    records = []  # ModRecord, name
    m = ft.FileModBin()
    m.load(fn_grid)
    for i in indexes:
        record_name = '%s#%d' % (fn_grid, i)
        records.append((m.records[i-1], record_name))

    mod = ft.FileModBin()
    mod.load(fn_output)
    rm = mod.records[0]

    print_record = lambda record, name: print(name, '; teff=', record.teff, '; glog=', record.glog, '; asalog=', record.asalog)

    # Figure
    plt.figure()
    for record, name in records:
        print_record(record, name)
        plt.plot(record.log_tau_ross, record.__getattribute__(args.var), label=name)
    name = fn_output
    v = rm.__getattribute__(args.var)
    if any(np.isnan(v)):
        print("NaN ALERT!!!")
    print_record(rm, name)
    plt.plot(rm.log_tau_ross, v, label=name, linewidth=2, linestyle='--')
    plt.xlabel('log_tau_ross')
    plt.title(args.var)
    plt.legend(loc=0)

    # Scatter figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    markers = cycle("ov^<>p*+x")
    for r, name in records:
        ax.scatter([r.teff], [r.glog], [r.asalog],
                   c=next(ax._get_lines.color_cycle), s=60,
                   label=name, marker=next(markers))
    ax.scatter([rm.teff], [rm.glog], [rm.asalog],
               c=next(ax._get_lines.color_cycle), s=60,
               label=fn_output, marker=next(markers))
    ax.set_xlabel('teff')
    ax.set_ylabel('glog')
    ax.set_zlabel('asalog')
    fig.canvas.set_window_title('teff-glog-asalog scatterplot')
    plt.legend(loc=0)

    # Another figure
    fig = plt.figure()
    y_var_names = ["teff", "glog", "asalog"]
    for i, y_var_name in enumerate(y_var_names):
        ax = fig.add_subplot(len(y_var_names), 1, i+1, projection='3d')
        x = None
        for record, name in records:
            print_record(record, name)
            v = record.__getattribute__(args.var)
            x = record.log_tau_ross
            y_var = record.__getattribute__(y_var_name)
            y = np.ones((len(x),))*y_var
            ax.plot(x, y, v, label=name)

        name = fn_output
        v = rm.__getattribute__(args.var)
        x = rm.log_tau_ross
        y_var = rm.__getattribute__(y_var_name)
        y = np.ones((len(x),))*y_var
        print_record(rm, name)
        plt.plot(x, y, v, label=name, linewidth=2, linestyle='--')

        plt.xlabel('log_tau_ross')
        plt.ylabel(y_var_name)
        plt.gca().set_zlabel(args.var)
        plt.title("Layer X %s X %s" % (y_var_name, args.var))
        plt.legend(loc=0)

    plt.show()

