#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from collections import OrderedDict, namedtuple
from fractions import Fraction
from contextlib import contextmanager

TagBox = namedtuple('TagBox', 'content tag')

def pack_boxes(list_of_content, tag):
    return [TagBox(content, tag) for content in list_of_content]

def get_numerator(ratio, max_denominator):
    fraction = Fraction.from_float(ratio).limit_denominator(max_denominator)
    return int(fraction.numerator * max_denominator / fraction.denominator)

def get_denominator(ratio, max_numerator):
    return get_numerator(1/ratio, max_numerator)

@contextmanager
def prplot(**argkw):
    import matplotlib.pyplot as plt
    import numpy as np

    def formula(p, f):
        r = f * p / (2 * p - f)
        r[r<0] = np.NAN
        return r
    size = argkw.get('size', 6)
    if 'ax' in argkw:
        ax = argkw['ax']
    else:
        fig, ax = plt.subplots(figsize=(size, size))
    ttl = ax.title
    ttl.set_position([.5, 1.05])

    for f in np.arange(0.1, 1, 0.1):
        p = np.arange(-1, 1.0, 0.00001)
        r = formula(p,f)
        ax.plot(p, r, color='lightgray', linewidth=1, zorder=-100)
        ax.annotate('  F={:.1f}'.format(f),
                    xy=(1-0.001, formula(np.array([1-0.001]), f)),
                    fontsize=size*1.7,
                    color='gray')

    plt.yticks(rotation='vertical')
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].set_visible(False)

    ax.grid(True, zorder=-99)
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
    for line in gridlines[1:]:
        line.set_linestyle('--')
        line.set_color('lightgray')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)

    ax.set_xlabel('Precision', labelpad=25, size=size*2.5)
    ax.set_ylabel('Recall', labelpad=25, size=size*2.5)
    ax.tick_params(axis='both', which='major', labelsize=size*2)

    # Plot the data
    yield ax

    title = ax.get_title()
    ax.set_title(title, fontsize=size*3)

class Report:
    """
    Holding the results of experiment, presenting the precision, recall,
    f1 score of the experiment.
    """
    def __init__(self, tp=[], fp=[], fn=[], title=None):
        """
        tp: the ture positive items
        fp: the false positive items
        fn: the false negative items
        title: the title of this report
        """
        self.tp = pack_boxes(tp, title)
        self.fp = pack_boxes(fp, title)
        self.fn = pack_boxes(fn, title)
        self.title = title

    def precision(self):
        try:
            return float(len(self.tp)) / (len(self.tp) + len(self.fp))
        except ZeroDivisionError:
            return 0.0

    def recall(self):
        try:
            return float(len(self.tp)) / (len(self.tp) + len(self.fn))
        except ZeroDivisionError:
            return 0.0

    def f1(self):
        r = self.recall()
        p = self.precision()
        try:
            return float(2 * r * p) / (r + p)
        except ZeroDivisionError:
            return 0.0

    def __repr__(self):
        r = self.recall()
        p = self.precision()
        f = self.f1()
        syntax = 'Report<P{p:.3f} R{r:.3f} F{f:.3f} {t!r}>'
        return syntax.format(p=p, r=r, f=f, t=self.title)

    def update(self, report):
        """
        Add the items from the given report.
        """
        self.tp.extend(pack_boxes(report.tp, self.title))
        self.fp.extend(pack_boxes(report.fp, self.title))
        self.fn.extend(pack_boxes(report.fn, self.title))

    @classmethod
    def from_reports(cls, reports, title):
        if len(reports) != len(set([rep.title for rep in reports])):
            raise KeyError('Cannt merge reports with same titles')
        metareport = cls([], [], [], title)
        for report in reports:
            metareport.update(report)
        return metareport

    def split(self):
        tag2report = OrderedDict()
        try:
            for tagbox, _ in self.tp:
                tag2report.setdefault(tagbox.tag, Report()).tp.append(tagbox.content)
            for tagbox, _ in self.fp:
                tag2report.setdefault(tagbox.tag, Report()).fp.append(tagbox.content)
            for tagbox, _ in self.fn:
                tag2report.setdefault(tagbox.tag, Report()).fn.append(tagbox.content)
            for tag, report in tag2report.items():
                report.title = tag
        except AttributeError:
            raise AssertionError('The report cannot be split')
        return list(tag2report.values())

    @classmethod
    def from_scale(cls, gold_number, precision, recall, title):
        """
        deprecated, for backward compactbility
        try to use from_score
        """
        tp_count = get_numerator(recall, gold_number)
        positive_count = get_denominator(precision, tp_count)
        fp_count = positive_count - tp_count
        fn_count = gold_number - tp_count
        scale_report = cls(['tp'] * tp_count,
                           ['fp'] * fp_count,
                           ['fn'] * fn_count,
                           title)
        return scale_report

    @classmethod
    def from_score(cls, precision, recall, title, goldstandard_size=1000):
        tp_count = get_numerator(recall, goldstandard_size)
        positive_count = get_denominator(precision, tp_count)
        fp_count = positive_count - tp_count
        fn_count = goldstandard_size - tp_count
        score_report = cls(['tp'] * tp_count,
                           ['fp'] * fp_count,
                           ['fn'] * fn_count,
                           title)
        return score_report

    def plot(self, split_report=False, **argkw):

        with prplot(**argkw) as ax:
            size = argkw.get('size', 6)
            fontsize = argkw.get('fontsize', 2*size)
            ax.set_title(self.title)
            if split_report:
                reports = self.split()
                max_goldnum = max([len(report.tp)+len(report.fn) for report in reports])
                for report in self.split():
                    ax.scatter(report.precision(), report.recall(),
                               s=100.0*(len(report.tp)+len(report.fn))/max_goldnum*size, zorder=10)
                    ax.annotate(report.title, (report.precision(), report.recall()), fontsize=fontsize, zorder=11)
            else:
                ax.scatter(self.precision(), self.recall())

    def html_table(self, split_report=False):
        html_template = """<table>
<tr>
    <th>Title</th>
    <th>Ture Positive</th>
    <th>False Positive</th>
    <th>False Negative</th>
    <th>Precision</th>
    <th>Recall</th>
    <th>F-measure</th>
</tr>
{}
</table>"""
        line_template = """<tr>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{}</th>
    <th>{:.3f}</th>
    <th>{:.3f}</th>
    <th>{:.3f}</th>
</tr>"""
        lines = []
        if split_report:
            reports = self.split()
        else:
            reports = [self]
        for report in reports:
            line = line_template.format(report.title,
                                        len(report.tp),
                                        len(report.fp),
                                        len(report.fn),
                                        report.precision(),
                                        report.recall(),
                                        report.f1())
            lines.append(line)

        body = '\n'.join(lines)
        return html_template.format(body)
