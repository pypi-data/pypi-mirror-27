#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import division
import sys
import argparse
from hicexplorer import HiCMatrix as hm
from hicexplorer.utilities import enlarge_bins
from scipy import sparse
import numpy as np


def parse_arguments(args=None):
    """
    get command line arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Uses a measure called TAD score to identify the separation between '
                    'left and right regions for a given position. This is done for a '
                    'running window of different sizes. Then, TADs are called as those '
                    'positions having a local minimum.')

    # define the arguments
    parser.add_argument('--matrix', '-m',
                        help='matrix to use.',
                        metavar='.npz file format',
                        required=True)

    parser.add_argument('--minDepth',
                        help='window length to be considered left and right '
                             'of the cut point in bp. This number should be at least 2 times '
                             'as large as the bin size of the Hi-C matrix.',
                        metavar='INT bp',
                        type=int,
                        default=20000
                        )

    parser.add_argument('--maxDepth',
                        help='window length to be considered left and right '
                             'of the cut point in bp. This number should around 6 times '
                             'as large as the bin size of the Hi-C matrix.',
                        metavar='INT bp',
                        type=int,
                        default=60000
                        )

    parser.add_argument('--lookahead',
                        help='number of bins ahead to look for before deciding '
                             'if a local minimum is a boundary.'
                             'points.',
                        type=int,
                        default=2
                        )

    parser.add_argument('--delta',
                        help='minimum difference between a peak and following'
                             'points.',
                        type=float,
                        default=0.001
                        )

    parser.add_argument('--outPrefix',
                        help='File prefix to save the resulting files: boundary positions, '
                             'bedgraph matrix containing the multi-scale TAD scores, '
                             'the BED files for the TAD clusters and the linkage BED file that '
                             'can be used with hicPlotTADs.',
                        required=True)

    parser.add_argument('--useLogValues',
                        help='If set, the log of the matrix values are'
                             'used.',
                        action='store_true')

    return parser


def get_cut_weight(matrix, cut, depth):
    """
    Get inter cluster edges sum.
    Computes the sum of the counts
    between the left and right regions of a cut

    >>> matrix = np.array([
    ... [ 0,  0,  0,  0,  0],
    ... [10,  0,  0,  0,  0],
    ... [ 5, 15,  0,  0,  0],
    ... [ 3,  5,  7,  0,  0],
    ... [ 0,  1,  3,  1,  0]])

    Test a cut at position 2, depth 2.
    The values in the matrix correspond
    to:
          [[ 5, 15],
           [ 3,  5]]
    >>> get_cut_weight(matrix, 2, 2)
    28

    For the next test the expected
    submatrix is [[10],
                  [5]]
    >>> get_cut_weight(matrix, 1, 2)
    15
    >>> get_cut_weight(matrix, 4, 2)
    4
    >>> get_cut_weight(matrix, 5, 2)
    0
    """
    # the range [start:i] should have running window
    # length elements (i is excluded from the range)
    start = max(0, cut - depth)
    # same for range [i+1:end] (i is excluded from the range)
    end = min(matrix.shape[0], cut + depth)

    # the idea is to evaluate the interactions
    # between the upstream neighbors with the
    # down stream neighbors. In other words
    # the inter-domain interactions
    return matrix[cut:end, :][:, start:cut].sum()


def get_min_volume(matrix, cut, depth):
    """
    The volume is the weight of the edges
    from a region to all other.

    In this case what I compute is
    a submatrix that goes from
    cut - depth to cut + depth
    """
    start = max(0, cut - depth)
    # same for range [i+1:end] (i is excluded from the range)
    end = min(matrix.shape[0], cut + depth)

    left_region = matrix[start:end, :][:, start:cut].sum()
    right_region = matrix[cut:end, :][:, start:end].sum()

    return min(left_region, right_region)

def get_conductance(matrix, cut, depth):
    """
    Computes the conductance measure for
    a matrix at a given cut position and
    up to a given depth.

    If int = inter-domain counts

    then the conductance is defined as

    conductance = int / min(int + left counts, int + right counts)

    The matrix has to be lower or uppper to avoid
    double counting

    In the following example the conductance is to be
    computed for a cut at index position 2 (between column 2 and 3)
    >>> matrix = np.array([
    ... [ 0,  0,  0,  0,  0],
    ... [10,  0,  0,  0,  0],
    ... [ 5, 15,  0,  0,  0],
    ... [ 3,  5,  7,  0,  0],
    ... [ 0,  1,  3,  1,  0]])

    The lower left intra counts are [0,10,0]',
    The lower right intra counts are [0, 7 0],
    The inter counts are:
          [[ 5, 15],
           [ 3,  5]], sum = 28

    The min of left and right is min(28+7, 28+10) = 35
    >>> res = get_conductance(matrix, 2, 2)
    >>> res == 28.0 / 35
    True
    """
    start = max(0, cut - depth)
    # same for range [i+1:end] (i is excluded from the range)
    end = min(matrix.shape[0], cut + depth)

    inter_edges = get_cut_weight(matrix, cut, depth)
    edges_left = inter_edges + matrix[start:cut, :][:, start:cut].sum()
    edges_right = inter_edges + matrix[cut:end, :][:, cut:end].sum()

#    return float(inter_edges) / min(edges_left, edges_right)
    return float(inter_edges) / max(edges_left, edges_right)
#    return float(inter_edges) / 100000
#    return float(inter_edges) / (sum([edges_left, edges_right]) - inter_edges)


def get_coverage(matrix, cut, depth):
    """
    The coverage is defined as the
    intra-domain edges / all edges

    It is only computed for a small running window
    of length 2*depth

    The matrix has to be lower or upper to avoid
    double counting
    """
    start = max(0, cut - depth)
    # same for range [i+1:end] (i is excluded from the range)
    end = min(matrix.shape[0], cut + depth)

    cut_weight = get_cut_weight(matrix, cut, depth)
    total_edges = matrix[start:end, :][:, start:end].sum()
    return cut_weight / total_edges


def compute_matrix(hic_ma, min_win_size=8, max_win_size=50, outfile=None):
    """
    Iterates over the Hi-C matrix computing at each bin
    interface the conductance at different window lengths
    :param hic_ma: Hi-C matrix object from HiCMatrix
    :param outfile: String, path of a file to save the conductance
                matrix in *bedgraph matrix* format
    :return: (chrom, start, end, matrix)
    """

    positions_array = []
    cond_matrix = []
    chrom, start, end, __ = hic_ma.cut_intervals[0]
    prev_length = int((end - start) / 2)
    for cut in range(1, hic_ma.matrix.shape[0]-1):

        chrom, chr_start, chr_end, _ = hic_ma.cut_intervals[cut]

        # the evaluation of the conductance happens
        # at the position between bins, thus the
        # conductance is stored in bins that
        # span the neighboring bins. In other
        # words, the conductance is evaluated
        # at the position between let's say
        # bins number 14 and 15. Instead of
        # storing a score at the position in between
        # bin 14 and bin 15, a region of the size
        # of the bins, centered on the interface is used.
        this_length = int((chr_end - chr_start) / 2)

        if chr_start + this_length > 0:
            chr_end =  chr_start + this_length
        else:
            continue

        if chr_start - prev_length > 0:
            chr_start -= prev_length
        else:
            chr_start = 0

        prev_length = this_length

        # get conductance
        # for multiple window lengths at a time
        mult_matrix = [get_coverage(hic_ma.matrix, cut, x)
                       for x in range(min_win_size, max_win_size, 1)]
#        mult_matrix = [get_conductance(hic_ma.matrix, cut, x)
#                       for x in range(8, 50, 2)]
        cond_matrix.append(mult_matrix)

        positions_array.append((chrom, chr_start, chr_end))

    chrom, chr_start, chr_end = zip(*positions_array)
    # save matrix as chrom, start, end ,row, values separated by tab
    # I call this a bedgraph matrix (bm)
    cond_matrix = np.vstack(cond_matrix)
    if outfile:
        # save matrix as chrom start end row values (bed graph matrix)
        with open(outfile, 'w') as f:
            for idx in range(len(chrom)):
                matrix_values = "\t".join(
                        np.char.mod('%f', cond_matrix[idx,:]))
                f.write("{}\t{}\t{}\t{}\n".format(chrom[idx], chr_start[idx],
                                                  chr_end[idx], matrix_values))

    return chrom, chr_start, chr_end, cond_matrix


def peakdetect(y_axis, x_axis=None, lookahead=3, delta=0):
    """
    Based on the MATLAB script at:
    http://billauer.co.il/peakdet.html

    function for detecting local maximum and minimum in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximum and minimum respectively

    keyword arguments:
    :param: y_axis -- A list containig the signal over which to find peaks
    :param: x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the position of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    :param: lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak
    :param: delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.


    :return: -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tuple
        of: (position, peak_value)
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do:
        x, y = zip(*tab)
    """
    max_peaks = []
    min_peaks = []
    dump = []   #Used to pop the first hit which almost always is false

    # check input data
    if x_axis is None:
        x_axis = np.arange(len(y_axis))

    if len(y_axis) != len(x_axis):
        raise (ValueError,
                'Input vectors y_axis and x_axis must have same length')

    # store data length for later use
    length = len(y_axis)

    # perform some checks
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, "delta must be a positive number"

    # maximum and minimum candidates are temporarily stored in
    # mx and mn respectively
    min_y, max_y = np.Inf, -np.Inf
    max_pos, min_pos = None, None
    search_for = None
    # Only detect peak if there is 'lookahead' amount of points after it
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead],
                                       y_axis[:-lookahead])):
        if y > max_y:
            max_y = y
            max_pos = x
        if y < min_y:
            min_y = y
            min_pos = x

        # look for max
        if y < max_y - delta and max_y != np.Inf and search_for != 'min':
            # Maximum peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index + lookahead].max() < max_y:
                max_peaks.append([max_pos, max_y])
                dump.append(True)
                # set algorithm to only find minimum now
                max_y = y
                min_y = y
                search_for = 'min'
                if index + lookahead >= length:
                    # end is within lookahead no more peaks can be found
                    break
                continue

        # look for min
        if y > min_y + delta and min_y != -np.Inf and search_for != 'max':
            # Minimum peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index + lookahead].min() > min_y:
                min_peaks.append([min_pos, min_y])
                dump.append(False)
                # set algorithm to only find maximum now
                min_y = y
                max_y = y
                search_for = 'max'
                if index + lookahead >= length:
                    # end is within lookahead no more peaks can be found
                    break

    # Remove the false hit on the first value of the y_axis
    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except IndexError:
        # no peaks were found, should the function return empty lists?
        pass

    return [max_peaks, min_peaks]


def find_consensus_minima(matrix, lookahead=3, delta=0):
    """
    Finds the minimum over the average values per column
    :param matrix:
    :return:
    """


    # use the matrix transpose such that each row
    # represents the conductance at each genomic
    # position

    _max, _min= peakdetect(matrix.mean(axis=1), lookahead=lookahead, delta=delta)
    min_indices, __ = zip(*_min)
    return np.unique(min_indices)


def hierarchical_clustering(boundary_list, clusters_cutoff=[]):
    """
    :param boundary_list: is a list of tuples each containing
    the location of a boundary. The order should be sorted
    and contain the following values:
        (chrom, start, value)
    :param clust_cutoff: List of values to separate clusters. The
        clusters found at those value thresholds are returned.


    :return: Z, clusters

    For Z, the format used is similar as the scipy.cluster.hierarchy.linkage() function
    which is described as follows:

    A 4 by :math:`(n-1)` matrix ``Z`` is returned. At the
    :math:`i`-th iteration, clusters with indices ``Z[i, 0]`` and
    ``Z[i, 1]`` are combined to form cluster :math:`n + i`. A
    cluster with an index less than :math:`n` corresponds to one of
    the :math:`n` original observations. The distance between
    clusters ``Z[i, 0]`` and ``Z[i, 1]`` is given by ``Z[i, 2]``. The
    fourth value ``Z[i, 3]`` represents the number of original
    observations in the newly formed cluster.

    The difference is that instead of a 4 times n-1 array, a
    6 times n-1 array is returned. Where positions 4, and 5
    correspond to the genomic coordinates of ``Z[i, 0]`` and ``Z[i, 1]``

    """
    # run the hierarchical clustering per chromosome
    if clusters_cutoff:
        # sort in reverse order
        clusters_cutoff = np.sort(np.unique(clusters_cutoff))[::-1]

    chrom, start, value = zip(*boundary_list)

    unique_chr, indices = np.unique(chrom, return_index=True)
    indices = indices[1:]  # the first element is not needed
    start_per_chr = np.split(start, indices)
    value_per_chr = np.split(value, indices)
    Z = {}

    def get_domain_positions(boundary_position):
        """
        returns for each boundary a start,end position
        corresponding to each TAD
        :param boundary_position: list of boundary chromosomal positions
        :return: list of (start, end) tuples.
        """
        start_ = None
        domain_list = []
        for position in boundary_position:
            if start_ is None:
                start_ = position
                continue
            domain_list.append((start_, position))
            start_ = position

        return domain_list

    def find_in_clusters(clusters_, search_id):
        """
        Given a list of clusters (each cluster defined as as set,
        the function returns the position in which an id is found
        :param clusters_:
        :param search_id:
        :return:
        """
        for set_idx, set_of_ids in enumerate(clusters_):
            if search_id in set_of_ids:
                return set_idx

    def cluster_to_regions(clusters_, chrom_name):
        """
        Transforms a list of sets of ids from the hierarchical
        clustering to genomic positions
        :param clusters: cluster ids
        :return: list of tuples with (chrom_name, start, end)

        Example:

        clusters = [set(1,2,3), set(4,5,10)]

        """
        start_list = []
        end_list = []
        for set_ in clusters_:
            if len(set_) == 0:
                continue

            # the ids in the sets are created in such a
            # that the min id is the one with the smaller start position
            start_list.append(domains[min(set_)][0])
            end_list.append(domains[max(set_)][1])

        start_list = np.array(start_list)
        end_list = np.array(end_list)
        order = np.argsort(start_list)

        return zip([chrom_name] * len(order), start_list[order], end_list[order])

    return_clusters = {} # collects the genomic positions of the clusters per chromosome
                         # The values are a list, one for each cutoff.
    for chrom_idx, chrom_name in enumerate(unique_chr):
        Z[chrom_name] = []
        return_clusters[chrom_name] = []
        clust_cutoff = clusters_cutoff[:]
        domains = get_domain_positions(start_per_chr[chrom_idx])
        clusters = [{x} for x in range(len(domains))]

        # initialize the cluster_x with the genomic position of domain centers
        cluster_x = [int(d_start + float(d_end - d_start) / 2) for d_start, d_end in domains]
        # number of domains should be equal to the number of values minus 1
        assert len(domains) == len(value_per_chr[chrom_idx]) -1, "error"

        """
        domain:id
             0            1               2            3
         |---------|---------------|----------------|----|
        values:id
         0         1               3                3    4
        values id after removing flanks
                   0               1                2
         """
        values = value_per_chr[chrom_idx][1:-1] # remove flanking values that do not join TADs
        start_trimmed = start_per_chr[chrom_idx][1:-1]
        # from highest to lowest merge neighboring domains
        order = np.argsort(values)[::-1]
        for idx, order_idx in enumerate(order):
            if len(clust_cutoff) and idx + 1 < len(order) and \
                    values[order_idx] >= clust_cutoff[0] > values[order[idx + 1]]:
                clust_cutoff = clust_cutoff[1:] # remove first element
                return_clusters[chrom_name].append(cluster_to_regions(clusters, chrom_name))
            # merge domains order_idx - 1 and order_idx
            left = find_in_clusters(clusters, order_idx)
            right = find_in_clusters(clusters, order_idx + 1)
            Z[chrom_name].append((left, right, values[order_idx],
                                  len(clusters[left]) + len(clusters[right]),
                                  cluster_x[left], cluster_x[right]))

            # set as new cluster position the center between the two merged
            # clusters
            gen_dist = int(float(abs(cluster_x[left] - cluster_x[right]))/2)
            cluster_x.append(min(cluster_x[left], cluster_x[right]) + gen_dist)


            clusters.append(clusters[left].union(clusters[right]))
            clusters[left] = set()
            clusters[right] = set()


    # convert return_clusters from a per chromosome dictionary to
    # a per cut_off dictionary merging all chromosomes in to one list.
    ret_ = {}  # dictionary to hold the clusters per cutoff. The key of
               # each item is the str(cutoff)

    for idx, cutoff  in enumerate(clusters_cutoff):
        cutoff = str(cutoff)
        ret_[cutoff] = []
        for chr_name in return_clusters:
            try:
                ret_[cutoff].extend(return_clusters[chr_name][idx])
            except IndexError:
                pass

    return  Z, ret_


def save_linkage(Z, file_name):
    """

    :param Z: Z has a format similar to the scipy.cluster.linkage matrix (see function
                hierarchical_clustering).
    :param file_name: File name to save the results
    :return: None
    """

    try:
        file_h = open(file_name, 'w')
    except IOError:
        sys.stderr.write("Can't save linkage file:\n{}".format(file_name))
        return

    count = 0
    for chrom, values in Z.iteritems():
        for id_a, id_b, distance, num_clusters, pos_a, pos_b in values:
            count += 1
            file_h.write('{}\t{}\t{}\tclust_{}\t{}\t.\t{}\t{}\t{}\n'.format(chrom,
                                                                        int(pos_a),
                                                                        int(pos_b),
                                                                        count,
                                                                        distance,
                                                                        id_a, id_b,
                                                                        num_clusters))


def get_domains(boundary_list):
    """
    returns for each boundary a chrom, start,end position
    corresponding to each TAD
    :param boundary_position: list of boundary chromosomal positions
    :return: list of (chrom, start, end, value) tuples.
    """
    prev_start = None
    prev_chrom = boundary_list[0][0]
    domain_list = []
    for chrom, start, value in boundary_list:
        if start is None:
            prev_start = start
            prev_chrom = chrom
            continue
        if prev_chrom != chrom:
            prev_chrom = chrom
            prev_start = None
            continue
        domain_list.append((chrom, prev_start, start, value))
        prev_start = start
        prev_chrom = chrom

    return domain_list


def save_clusters(clusters, file_prefix):
    """

    :param clusters: is a dictionary whose key is the cut of used to create it.
                     the value is a list of tuples, each representing
                      a genomec interval as ('chr', start, end).
    :param file_prefix: file prefix to save the resulting bed files
    :return: list of file names created
    """
    for cutoff, intervals in clusters.iteritems():
        fileh = open("{}_{}.bed".format(file_prefix, cutoff) , 'w')
        for chrom, start, end in intervals:
            fileh.write("{}\t{}\t{}\t.\t0\t.\n".format(chrom, start, end))


def main(args=None):

    args = parse_arguments().parse_args(args)
    if args.maxDepth <= args.minDepth:
        exit("Please check that maxDepth is larger than minDepth.")

    hic_ma = hm.hiCMatrix(args.matrix)
    #hic_ma.keepOnlyTheseChr('chrX')
    #sys.stderr.write("\nWARNING: using only chromosome X\n\n")
    # remove self counts
    hic_ma.diagflat(value=0)
    sys.stderr.write('removing diagonal values\n')

    if args.useLogValues is True:
        # use log values for the computations
        hic_ma.matrix.data = np.log(hic_ma.matrix.data)
        sys.stderr.write('using log matrix values\n')

    # mask bins without any information
    hic_ma.maskBins(hic_ma.nan_bins)
    orig_intervals = hic_ma.cut_intervals

    # extend remaining bins to remove gaps in
    # the matrix
    new_intervals = enlarge_bins(hic_ma.cut_intervals)

    # rebuilt bin positions if necessary
    if new_intervals != orig_intervals:
        hic_ma.interval_trees, hic_ma.chrBinBoundaries = \
            hic_ma.intervalListToIntervalTree(new_intervals)

    if args.minDepth % hic_ma.getBinSize() != 0:
        sys.stderr.write('Warning. specified depth is not multiple of the '
                         'hi-c matrix bin size ({})\n'.format(hic_ma.getBinSize()))

    binsize = hic_ma.getBinSize()

    min_depth_in_bins = int(args.minDepth / binsize)
    max_depth_in_bins = int(args.maxDepth / binsize)
    print (min_depth_in_bins, max_depth_in_bins)
    sys.stderr.write("computing spectrum for window sizes between {} ({} bp)"
                     "and {} ({} bp)\n".format(min_depth_in_bins,
                                               binsize * min_depth_in_bins,
                                               max_depth_in_bins,
                                               binsize * max_depth_in_bins))
    if min_depth_in_bins <= 1:
        sys.stderr.write('ERROR\nminDepth length too small. Use a value that is at least'
                         'twice as large as the bin size which is: {}\n'.format(binsize))
        exit()

    if max_depth_in_bins <= 1:
        sys.stderr.write('ERROR\nmaxDepth length too small. Use a value that is larger '
                         'than the bin size which is: {}\n'.format(binsize))
        exit()

    # work only with the lower matrix
    hic_ma.matrix = sparse.tril(hic_ma.matrix, k=0, format='csr')

    # compute conductance matrix
    chrom, chr_start, chr_end, matrix = compute_matrix(hic_ma, min_depth_in_bins,
                                                       max_depth_in_bins,
                                                       outfile=args.outPrefix + "_spectrum.bm")

    mean_mat = matrix.mean(axis=1)
    min_idx = find_consensus_minima(matrix, lookahead=args.lookahead, delta=args.delta)

#    boundary_list = [(chrom[min], chr_start[min], mean_mat[min]) for min in min_idx]
    boundary_list = [(hic_ma.cut_intervals[min_][0], hic_ma.cut_intervals[min_][2], mean_mat[min_]) for min_ in min_idx]

    Z, clusters = hierarchical_clustering(boundary_list, clusters_cutoff=[0.4, 0.3, 0.2])

    save_linkage(Z, args.outPrefix + '_linkage.bed')
    save_clusters(clusters, args.outPrefix)

    # save results
    prev_start = 0
    prev_chrom = chrom[0]
    count = 0
    file_boundaries = open(args.outPrefix + '_boundaries.bed', 'w')
    file_domains = open(args.outPrefix + '_domains.bed', 'w')
    rgb = '31,120,180'
    for idx in min_idx:
        # 1. save boundaries position
        chrom_name = hic_ma.cut_intervals[idx][0]
        start = hic_ma.cut_intervals[idx][2]
        end = start + 1  # boundaries at 1 bp resolution
        file_boundaries.write("{}\t{}\t{}\tmin\t{}\t.\n".format(chrom_name, start, end, matrix[idx, -1]))

        if prev_chrom != chrom[idx]:
            chrom_first_bin_id, chrom_last_bin_id = hic_ma.getChrBinRange(prev_chrom)
            file_domains.write("{0}\t{1}\t{2}\tID_{3}\t{4}\t."
                        "\t{1}\t{2}\t{5}\n".format(chrom[idx],
                                                   prev_start,
                                                   hic_ma.cut_intervals[chrom_last_bin_id-1][2],
                                                   idx,
                                                   mean_mat[idx],
                                                   rgb))

        # 2. save domain intervals
        if count % 2 == 0:
            rgb = '51,160,44'
        else:
            rgb = '31,120,180'
        file_domains.write("{0}\t{1}\t{2}\tID_{3}\t{4}\t."
                    "\t{1}\t{2}\t{5}\n".format(chrom_name,
                                               prev_start,
                                               start,
                                               idx,
                                               mean_mat[idx],
                                               rgb))

        count += 1
        prev_start = start

    # save last domain
    chrom_first_bin_id, chrom_last_bin_id = hic_ma.getChrBinRange(chrom_name)
    file_domains.write("{0}\t{1}\t{2}\tID_{3}\t{4}\t."
                "\t{1}\t{2}\t{5}\n".format(chrom_name,
                                           prev_start,
                                           hic_ma.cut_intervals[chrom_last_bin_id-1][2],
                                           idx,
                                           mean_mat[idx],
                                           rgb))

    """
    ## legacy code just in case
    ## the following lines center the boundary in the bin that
    ## has the minimun and not between two bins.

    boundary_center = chr_end[idx] - int((chr_end[idx] - chr_start[idx])/2)
    # previous method to get boundaries. I don't remember why I replaced it
    # but they return different, yet similar, regions.

    # this happens at the borders of chromosomes
    if boundary_center < 0:
        continue
    fileh.write("{0}\t{1}\t{2}\tID_{3}\t{4}\t.\n".format(
            chrom[idx],
            boundary_center,
            boundary_center + 1,
            idx,
            mean_mat[idx]))
    # 2. save domain intervals

    if count % 2 == 0:
        rgb = '51,160,44'
    else:
        rgb = '31,120,180'
    filed.write("{0}\t{1}\t{2}\tID_{3}\t{4}\t."
                "\t{1}\t{2}\t{5}\n".format(chrom[idx],
                                           prev_start,
                                           boundary_center,
                                           idx,
                                           mean_mat[idx],
                                           rgb))
    """

