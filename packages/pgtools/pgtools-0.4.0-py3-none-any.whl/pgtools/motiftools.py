import os
import bs4
import numpy
import scipy
import pandas
import math
import re
import datetime
import collections
import statsmodels.sandbox.stats.multicomp
from Bio.motifs._pwm import calculate as biopython_motif_calculate

from pgtools import toolbox
#from model import genomic_tools

BACKGROUND_FREQUENCY_FILENAME = toolbox.home_path('model_data/background_nucleotide_frequencies.csv')

WHITESPACE = re.compile(r'\s+')

def parse_known_motifs(motif_dir):

    table_data = {}
    known_motif_file_name = os.path.join(motif_dir, 'knownResults.html')
    
    with open(known_motif_file_name, 'rt') as html_file:
        known_motifs = bs4.BeautifulSoup(html_file.read(), 'html.parser')

        table_body = known_motifs.table
        table_rows = table_body.find_all('tr')
        header_row = table_rows[0]
        col_headers = [ele.contents[0].encode() for ele in header_row.find_all('td')]
#         print col_headers
        for rank, row in enumerate(table_rows[1:]):
            new_row_data = {}
            for field_name, field_value in zip(col_headers, row.find_all('td')):

                if not field_value.findChildren():
                    new_value = field_value.contents[0].strip().encode()
#                     print new_value
                    if field_name == 'Name':
                        new_value = new_value.split('/')[0]

                    new_row_data[field_name.encode()] = new_value

                else:
                    if field_name == 'Motif':
                        new_row_data['Motif'] = field_value.findChildren()[0].attrs['src'].encode()

            table_data[rank] = new_row_data
        return table_data


def known_motifs_to_df(motif_data_dict):
    COL_ORDER = ['Name',
                 'P-value',
                 'q-value (Benjamini)',
                 '% of Targets Sequences with Motif',
                 '% of Background Sequences with Motif',
                 '# Target Sequences with Motif',
                 '# Background Sequences with Motif'
                 ]
    motif_df = pandas.DataFrame(motif_data_dict).T
    motif_df = motif_df.loc[:, COL_ORDER]
    return motif_df


def parse_de_novo_motifs(motif_dir):

    table_data = {}
    
    de_novo_motif_file_name = os.path.join(motif_dir, 'homerResults.html')
    
    with open(de_novo_motif_file_name, 'rt') as html_file:
        known_motifs = bs4.BeautifulSoup(html_file.read(), 'html.parser')

        table_body = known_motifs.table
        table_rows = table_body.find_all('tr')
        header_row = table_rows[0]
        col_headers = [ele.contents[0].encode() for ele in header_row.find_all('td')]
#         print col_headers
        for rank, row in enumerate(table_rows[1:]):
            new_row_data = {}
            for field_name, field_value in zip(col_headers, row.find_all('td')):

                if not field_value.findChildren():
                    new_value = field_value.contents[0].strip().encode()
#                     print new_value
#                     print field_name
                    
                    new_row_data[field_name.encode()] = new_value

                else:
                    if field_name == 'Motif':
                        new_row_data['Motif'] = field_value.findChildren()[0].attrs['src'].encode()
                    elif field_name == 'Best Match/Details':
                        new_value = field_value.get_text()
                        new_value = new_value.split('/')[0]
                        new_row_data['Name'] = new_value.encode()
#                     elif field_name == 'Rank':
#                         print new_value

            table_data[rank] = new_row_data
#             else:
#                 print row.find_all('td')
        
        return table_data
    
    
def de_novo_motifs_to_df(motif_data_dict):
    COL_ORDER = ['Name',
                 'P-value',
                 '% of Targets',
                 '% of Background'
                 ]
    motif_df = pandas.DataFrame(motif_data_dict).T
    motif_df = motif_df.loc[:, COL_ORDER]
    return motif_df
    

def process_motifs(motif_dir):
    known_output_path = os.path.join(motif_dir, 'compact_known_results.csv')
    known_motifs_to_df(parse_known_motifs(motif_dir)).to_csv(known_output_path, index=False)
    print('Processed known motif analysis and wrote {}'.format(known_output_path))
    de_novo_output_path = os.path.join(motif_dir, 'compact_homer_results.csv')
    de_novo_motifs_to_df(parse_de_novo_motifs(motif_dir)).to_csv(de_novo_output_path, index=False)
    print('Processed de novo motif analysis and wrote {}'.format(de_novo_output_path))
    

def get_background_frequencies(genome_build, background_frequency_fname=BACKGROUND_FREQUENCY_FILENAME):
    updated = False

    print('Loading background nucleotide frequencies from {}'.format(background_frequency_fname))
    try:
        background_models = pandas.read_csv(background_frequency_fname, index_col=0).to_dict('list')
    except (IOError, OSError):
        background_models = {}
        print('File not found.'.format(background_frequency_fname))
    else:
        print('Background frequencies loaded.')

    if genome_build in background_models:
        print('Found background model for genome {}: {}'.format(genome_build, background_models[genome_build]))
    else:
        print('\tBackground frequencies for genome build {} not found. Computing now...'.format(
            genome_build))
        genome = genomic_tools.Genome(genome_build)
        #chroms= pileups.get_chrom_length_dict(os.path.join(os.environ['HOME'], 'model_data', 'reference_genomes', '{}'.format(genome_build), '{}.chrom.sizes'.format(genome_build)))
        #genome = pileups.Pileups(name='{} sequence'.format(genome_build), build=genome_build, chrom_lengths=chroms)
        background_models[genome_build] = genome.compute_nucleotide_frequencies()
        updated = True
        
    if updated:
        print('Saving updated background nucleotide frequencies to {}'.format(background_frequency_fname))
        pandas.DataFrame(background_models).to_csv(background_frequency_fname)
        
    return background_models[genome_build]

    
def generate_random_sequence(size, background_frequencies=[0.25]*4, random_seed=None):
    numpy.random.seed(random_seed)
    return ''.join(numpy.random.choice(['A', 'C', 'G', 'T'], size=size, p=background_frequencies))

    
def load_PFM_auto(pfm_filename):
    with open(pfm_filename, 'rU') as pfm_file:
        max_len = 0
        for line in pfm_file:
            if line[0] != '>':
                split_line = re.split(WHITESPACE, line.strip())
                max_len = max(max_len, len(split_line))
        if max_len == 4 or (split_line[0].find('|') == 1 and max_len == 5):
            return load_PFM_vertical(pfm_filename)
        else:
            return load_PFM_horizontal(pfm_filename)
            

# def load_PFM_horizontal(pfm_filename):
# """
#     Loads a PFM from a horizontal format with a FASTA-style header line at top and nucleotide labels for each row
#     :param pfm_filename:
#     :return:
#     """
#     with open(pfm_filename, 'rU') as pfm_file:
#         frequencies = []
#         for line in pfm_file:
#             line = line.strip()
#             if not line.startswith('>'):
#                 new_row = [int(item) for item in line.split('\t')[1:]]
#                 if len(new_row) > 1:
#                     frequencies.append(new_row)
#     pfm = numpy.zeros((4, len(frequencies[0])), dtype=int)
#     for row_num, row in enumerate(frequencies):
#         assert len(row) == len(frequencies[0])
#         pfm[row_num] = numpy.array(row)
#     return pfm


def load_PFM_horizontal(pfm_filename, data_type='counts'):
    """
    Loads PFMs from a text file containing horitzontal PFMs (positions in columns, nucleotides in rows) with FASTA-style
    headers before each sequence. Returns them as a dictionary of horizontal PFM matrices keyed by header.

    :param pfm_filename:
    :return:
    """
    toolbox.check_params('data_type', data_type, ('frequencies', 'counts'))
    def convert_to_matrix(pfm_string_list):
        assert len(pfm_string_list) == 4
        split_line = re.split(WHITESPACE, pfm_string_list[0].strip())
        if split_line[0].find('|') > 0:
            num_columns = len(split_line) - 1
        else:
            num_columns = len(split_line)
        matrix = numpy.zeros((4, num_columns), dtype=int)
        for pfm_row, line in enumerate(pfm_string_list):
            split_line = re.split(WHITESPACE, line.strip())
            # assert len(split_line) == 4
            if split_line[0].find(r'|') == 1:
                split_line = split_line[1:]
            if data_type=='counts':
                matrix[pfm_row, :] = numpy.array([int(element) for element in split_line])
            elif data_type=='frequencies':
                matrix[pfm_row, :] = numpy.array([float(element) for element in split_line])
            
        return matrix

    with open(pfm_filename, 'rU') as pfm_file:
        pfm_dict = {}
        this_pfm = []
        for line in pfm_file:
            if line.startswith('>'):  # header line
                if this_pfm:
                    pfm_dict[header] = convert_to_matrix(this_pfm)
                    this_pfm = []
                header = line[1:].strip()
            else:
                this_pfm.append(line.strip())
        pfm_dict[header] = convert_to_matrix(this_pfm)
    return pfm_dict
    

def load_PFM_JASPAR_horizontal(pfm_filename):
    """
    Loads PFMs from a text file containing horizontal PFMs (positions in columns, labeled nucleotides in rows, brackets around row content) with FASTA-style
    headers before each sequence. Returns them as a dictionary of horizontal PFM matrices keyed by header.

    :param pfm_filename:
    :return:
    """

    def convert_to_matrix_JASPAR(pfm_string_list):
        assert len(pfm_string_list) == 4
        row_arrays = {}
        for line in pfm_string_list:
            line_elements = re.split('[\s\[\]]+', line)[:-1]
            row_arrays[line_elements[0]] = numpy.array([int(e) for e in line_elements[1:]])
        matrix = numpy.vstack([row_arrays[nucleotide] for nucleotide in ('A', 'C', 'G', 'T')])
        return matrix

    with open(pfm_filename, 'rU') as pfm_file:
        pfm_dict = {}
        this_pfm = []
        for line in pfm_file:
            if line.startswith('>'):  # header line
                if this_pfm:
                    pfm_dict[header] = convert_to_matrix_JASPAR(this_pfm)
                    this_pfm = []
                header = line[1:].strip()
            elif line != '\n':
                this_pfm.append(line.strip())
        pfm_dict[header] = convert_to_matrix_JASPAR(this_pfm)
    return pfm_dict
    

def load_PFM_vertical(pfm_filename, data_type='counts'):
    """
    Loads PFMs from a text file containing vertical PFMs (nucleotides in columns, positions in rows) with FASTA-style
    headers before each sequence. Returns them as a dictionary of horizontal PFM matrices keyed by header.

    See UmassPGFE_PWMfreq_PublicDatasetB_20150206.txt from http://pgfe.umassmed.edu/ for example file.
    :param pfm_filename:
    :return:
    """
    toolbox.check_params('data_type', data_type, ('frequencies', 'counts'))
   
    def convert_to_matrix(pfm_string_list):
        matrix = numpy.zeros((4, len(pfm_string_list)), dtype={'frequencies':float, 'counts':int}[data_type])
        for pfm_row, line in enumerate(pfm_string_list):
            split_line = re.split(WHITESPACE, line.strip())
            assert len(split_line) == 4
            if data_type == 'counts':
                matrix[:, pfm_row] = numpy.array([int(element) for element in split_line])
            elif data_type == 'frequencies':
                matrix[:, pfm_row] = numpy.array([float(element) for element in split_line])
            
        return matrix

    with open(pfm_filename, 'rU') as pfm_file:
        pfm_dict = {}
        this_pfm = []
        for line in pfm_file:
            if line.startswith('>'):  # header line
                if this_pfm:
                    pfm_dict[header] = convert_to_matrix(this_pfm)
                    this_pfm = []                    
                header = line[1:].strip()
                
            else:
                this_pfm.append(line.strip())
        pfm_dict[header] = convert_to_matrix(this_pfm)
    return pfm_dict


def entropy_by_pos(pwm):
    entropy_weights = numpy.zeros(pwm.shape[1])
    for pos in range(pwm.shape[1]):
        for nuc in range(pwm.shape[0]):
            entropy_weights[pos] -= pwm[nuc, pos] * math.log(pwm[nuc, pos], 2)
    return entropy_weights


def pcm_to_pfm(pcm, pseudo_count=0):
     """
     Converts a position count matrix (PCM) to position frequency matrix (PFM) by converting counts to frequencies
     (assume nucleotides in rows in alpha order A,C,G,T,
     transpose the input if nucleotides in columns).
     Adds <psuedo_count> to each entry before calculating.
     """
     return ((pcm + pseudo_count) / pcm.sum(axis=0)).astype(float)


def pcm_to_pwm(pcm, background_model=[0.25] * 4, pseudo_count=0):
    """
    Converts a PCM to PWM by converting counts to frequencies (assume nucleotides in rows in alpha order A,C,G,T,
    transpose the input if nucleotides in columns), then calculating the log2 ratio between the matrix frequency and
    the background frequency (<background_model> should be given as a sequence of four frequencies in A,C,G,T order.)

    Adds <psuedo_count to each entry>.
    """
    return numpy.log2(numpy.apply_along_axis(numpy.divide, 0, pcm_to_pfm(pcm, pseudo_count), background_model))
    
def pfm_to_pwm(pfm, background_model=[0.25] * 4, pseudo_frequency=0.001):
    """
    Converts a PFM to PWM by converting frequencies to weights (assume nucleotides in rows in alpha order A,C,G,T,
    transpose the input if nucleotides in columns), then calculating the log2 ratio between the matrix frequency and
    the background frequency (<background_model> should be given as a sequence of four weights in A,C,G,T order.)

    Adds <pseudo_frequency to each entry>.
    """
    return numpy.log2(numpy.apply_along_axis(numpy.divide, 0, pfm, background_model))


def motif_rev_complement(motif_matrix):
    """
    Creates the reverse complement of a motif (either PWM or PFM) by reversing the order and transposing A/T and C/G.
    :param motif_matrix: A 2D matrix with nucleotides in rows in alpha order A,C,G,T and positions in columns
    :return:  A 2D matrix with nucleotides in rows in alpha order A,C,G,T and positions in columns
    """
    return motif_matrix[(3, 2, 1, 0), ::-1]


def export_homer_motif(pfm, motif_name, motif_filename, llr_threshold=0):
    with open(motif_filename, 'wt') as motif_file:
        motif_file.write('>{}\t{}\t{}\n'.format(''.join(consensus_sequence(pfm)), motif_name, llr_threshold))
        for col in range(pfm.shape[1]):
            motif_file.write('{}\n'.format('\t'.join([str(x) for x in pfm[:, col]])))
 
    
def compute_background_distribution(seq, normalize=True):
    """
    Computes the background nucleotide distribution of a sequence (essentially a 1-position PWM)
    Returns a PFM (<normalize> if you want a PWM)
    """
    background_freq = toolbox.freq(seq)
    background_pwm = numpy.array(
        [background_freq[k] for k in sorted(background_freq.keys()) if k in ('A', 'C', 'G', 'T')])
    if normalize:
        return pcm_to_pfm(background_pwm)
    else:
        return pcm_to_pfm


def exclusive_joint(prob_a, prob_b):
    """
    Returns the joint probability of (A and not B) or (B and not A)
    """
    return prob_a + prob_b - prob_a * prob_b


def binding_probabilities(energies, mu=0):
    """
    Returns a vector of binding probabilities given a single strand vector of binding energy values (such as generated by a PWM)
    and a scalar <mu> that adjusts for the free concentration of ligand (theoretically equal to ln[TF]).
    :param energies:
    :param mu:
    :return:
    """
    return 1 / (1 + numpy.exp(-energies - mu))

    
def energy_to_prob(energy_neg, energy_pos, mu):
    return exclusive_joint(binding_probabilities(energy_pos, mu), binding_probabilities(energy_neg, mu))

    
def motif_entropy(pfm):
    """
    Calculates the entropy for each position in a PFM (Position Frequency Matrix)
    (assume nucleotides in rows in alpha order A,C,G,T,
    transpose the input if nucleotides in columns).

    Adds <psuedo_count to each entry>.
    """
    entropy_weights = numpy.zeros(pfm.shape[1])
    for pos in range(pfm.shape[1]):
        entropy_weights[pos] = -numpy.sum(pfm[:, pos] * numpy.log2(pfm[:, pos]))
    return entropy_weights


def consensus_sequence(horizontal_motif_matrix):
    """
    Given either a PWM or PFM in horizontal format, returns a string containing the consensus
    sequence of that motif (best-matching nucleotide at each position)
    """
    nucs = numpy.array(['A', 'C', 'G', 'T'])
    return nucs[numpy.argmax(horizontal_motif_matrix, axis=0)]


def scan_pwm(seq, pwm, score_offset=0, at_motif_midpoint=True, method='Bio'):
    """
    Given a sequence <seq> and a PWM in log-odds format (each row is a nucleotide, each column is a position),
    compute the single-stranded binding energy of the subsequence starting at each
    position. Scores are placed at the starting point of the motif subsequence unless <score_offset> is specified, in
    which case they are shifted by the given amount toward the end of the motif.
    """
    if at_motif_midpoint:
        motif_length = pwm.shape[1]
        motif_midpoint = motif_length / 2 - 1
        score_offset += motif_midpoint
    if method == 'Bio':
        scan = scan_pwm_biopython(seq, pwm, score_offset=score_offset)
    else:
        scan = scan_pwm_native_python(seq, pwm, score_offset=score_offset)
    assert len(scan) == len(seq)  # check that we didn't screw this up
    return scan


def scan_pwm_biopython(seq, pwm, score_offset=0):
    """
    Biopython expects nucleotides in columns, but since I like to have them in rows, this function assumes rows
    and transposes the PWM that's passed to Biopython.

    Scores are placed at the starting point of the motif subsequence unless <score_offset> is specified, in
    which case they are shifted by the given amount toward the end of the motif.
    :param seq:
    :param pwm:
    :return:
    """
    motif_length = pwm.shape[1]
    score_offset = int(score_offset)
    if type(seq) == numpy.ndarray:
        scan = biopython_motif_calculate(''.join(seq), pwm.T)
    else:
        scan = biopython_motif_calculate(seq, pwm.T)
    return numpy.concatenate((numpy.zeros(score_offset), scan, numpy.zeros(motif_length - score_offset - 1)))


def scan_pwm_native_python(seq, pwm, score_offset=0, N_score=-4.64):
    """
    Given a sequence <seq> and a PWM in log-odds format, compute the single-stranded binding energy of the subsequence starting at each
    position. Scores are placed at the starting point of the motif subsequence unless <score_offset> is specified, in
    which case they are shifted by the given amount toward the end of the motif.

    Any 'N's in the sequence will be assigned the value of <N_score>. Default is roughly equivalent to a 1/100
    probability versus a background of 1/4
    """
    nuc_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    score = numpy.zeros(len(seq))
    for start_pos in range(len(seq) - pwm.shape[1]):
        for offset in range(pwm.shape[1]):
            if seq[start_pos + offset] == 'N':
                score[start_pos + score_offset] += N_score
            else:
                score[start_pos + score_offset] += pwm[nuc_dict[seq[start_pos + offset]]][offset]
    return score


def export_pwm_to_meme(motif_name, pwm, fname, background_model, meme_version=4, strands='+'):
    with open(fname, 'wt') as out_file:
        out_file.write('MEME version {}\n'.format(meme_version))
        out_file.write('ALPHABET = ACGT\n')
        out_file.write('STRANDS: +\n')
        out_file.write('Background letter frequencies\n')
        out_file.write('A {} C {} G {} T {}\n'.format(*background_model))
        out_file.write('MOTIF {}\n'.format(motif_name))


def find_motifs_empirical(genome, pwm, lr_threshold=0, fdr=0.05, p_val_threshold=None):
    """
    An early attempt at motif site thresholding by empirical p-value. Not recommended.
    """
    start_time = datetime.datetime.now()
    # number the contigs
    contig_names = {contig_number:contig_name for contig_number, contig_name in enumerate(sorted(genome.contig_names))}
    contig_numbers = {contig_name:contig_number for contig_number, contig_name in enumerate(sorted(genome.contig_names))}

    rev_pwm = motif_rev_complement(pwm) # compute the reverse complement of the motif

    # build genome wide arrays: contig identity, motif score, and start location
    contig_ids_by_contig = []
    motif_scores_by_contig = []
    start_locations_by_contig = []
    strands_by_contig = []
    print('Scoring genome sequence ...')
    for contig_name in toolbox.numerical_string_sort(genome.contig_lengths.keys()):
        contig_length = genome.contig_lengths[contig_name]
        print('\tScoring contig {} ...'.format(contig_name))
        for strand in (True, False):        
            contig_ids_by_contig.append(numpy.full(shape=contig_length, fill_value=contig_numbers[contig_name], dtype=numpy.int))
            motif_scores_by_contig.append(scan_pwm(genome.get_dna_sequence(contig_name), (rev_pwm, pwm)[strand], at_motif_midpoint=False))
            start_locations_by_contig.append(numpy.arange(contig_length))
            strands_by_contig.append(numpy.full(shape=contig_length, fill_value=strand, dtype=numpy.bool))
            
    print('Concatenating results ...')
    contig_ids = numpy.concatenate(contig_ids_by_contig)
    del(contig_ids_by_contig)
    motif_scores = numpy.concatenate(motif_scores_by_contig)
    del(motif_scores_by_contig)
    start_locations = numpy.concatenate(start_locations_by_contig)
    del(start_locations_by_contig)
    strands = numpy.concatenate(strands_by_contig)
    del(strands_by_contig)

    # remove any loci with NaN scores
    print('Filtering out invalid loci ...')
    nonnan_loci = numpy.nonzero(~numpy.isnan(motif_scores))[0]
    contig_ids = contig_ids[nonnan_loci]
    motif_scores = motif_scores[nonnan_loci]
    start_locations = start_locations[nonnan_loci]
    strands = strands[nonnan_loci]
    print('\tRemoved {} out of {} loci'.format((genome.size*2) - len(nonnan_loci), (genome.size*2)))
    del(nonnan_loci)

    # Fit a normal distribution to the whole dataset prior to filtering
    print('Fitting normal distribution ...')
    data_size = len(motif_scores)
    data_mean, data_std = motif_scores.mean(), motif_scores.std()
    motif_score_distribution = scipy.stats.norm(loc=data_mean, scale=data_std)
    print('\tMotif scores have mean {:>0.2}, SD {:>0.2}'.format(data_mean, data_std))

    # threshold by likelihood ratio
    if lr_threshold is not None:
        print('Filtering by likelihood ratio > {}'.format(lr_threshold))
        candidate_mask = motif_scores > lr_threshold
        motif_scores = motif_scores[candidate_mask]
        contig_ids = contig_ids[candidate_mask]
        start_locations = start_locations[candidate_mask]
        strands = strands[candidate_mask]
        print('\tFound {} loci out of {}.'.format(len(motif_scores), data_size))

    print('Computing p-values ...')
    # Compute p-values
    p_vals = 1 - motif_score_distribution.cdf(motif_scores)
    print('\tDone.')

    # threshold by p-value
    if p_val_threshold is not None:
        initial_hit_size = len(motif_scores)
        print('Discarding hits with p-values greater than {} ...'.format(p_val_threshold))
        p_val_mask = p_vals < p_val_threshold
        p_vals = p_vals[p_val_mask]
        motif_scores = motif_scores[p_val_mask]
        contig_ids = contig_ids[p_val_mask]
        start_locations = start_locations[p_val_mask]
        strands = strands[p_val_mask]
        print('\t{} out of {} hits passed p-value cutoff'.format(len(p_vals), initial_hit_size))   
        
    print('Applying multiple testing correction ...')
    pass_fail, q_vals, dummy, dummy = statsmodels.sandbox.stats.multicomp.multipletests(p_vals, alpha=fdr, method='fdr_bh')

    print('\tFound {} hits at an FDR of {}'.format(pass_fail.sum(), fdr))
    
    print('Constructing output ...')
    q_vals = q_vals[pass_fail]
    length_cutoff = len(q_vals)
    
    # Do final sorting and thresholding.
    sort_index = numpy.argsort(motif_scores)[::-1]
    motif_scores = motif_scores[sort_index][:length_cutoff]
    contig_ids = contig_ids[sort_index][:length_cutoff]
    start_locations = start_locations[sort_index][:length_cutoff]
    strands = strands[sort_index][:length_cutoff]
    p_vals = p_vals[sort_index][:length_cutoff]
    
    strand_translate = {True:'+', False:'-'}

    output_regions = pandas.DataFrame({'contig':[contig_names[contig_num] for contig_num in contig_ids],
                                      'start': start_locations,
                                      'end': start_locations + pwm.shape[1],
                                      'strand': [strand_translate[strand] for strand in strands],
                                      'motif_lr_score': motif_scores,
                                      'p_value': p_vals,
                                      'q_value': q_vals,
                                      })[['contig', 'start','end', 'strand', 'motif_lr_score', 'p_value', 'q_value']]
                                      
    print('All done in {}'.format(datetime.datetime.now() - start_time))
    return output_regions
    

def find_motifs(sequence_dictionary, pwm, llr_threshold=0, fdr=0.05, p_val_threshold=None, polish_partition=True, initial_search_fraction=1e-7, mem_map=False):
    """
    Models the motif score distribution as a mixture of signal component defined by a PWM
    and a gaussian noise component.
    """
    # ToDo: Add KS test sanity check for agreement of background scores to background distribution.
    
    start_time = datetime.datetime.now()
    motif_width = pwm.shape[1]
    
    # number the contigs
    contig_names = {contig_number:contig_name for contig_number, contig_name in enumerate(sorted(sequence_dictionary))}
    contig_numbers = {contig_name:contig_number for contig_number, contig_name in enumerate(sorted(sequence_dictionary))}
    contig_lengths = {contig_name:len(sequence_dictionary[contig_name]) for contig_name in sequence_dictionary}
    genome_size = sum([len(sequence_dictionary[contig_name]) for contig_name in sequence_dictionary])

    rev_pwm = motif_rev_complement(pwm) # compute the reverse complement of the motif

    # build genome wide arrays: contig identity, motif score, and start location
    contig_ids_by_contig = []
    motif_scores_by_contig = []
    start_locations_by_contig = []
    strands_by_contig = []
    print('Scoring genome sequence ...')
    for contig_name in toolbox.numerical_string_sort(sequence_dictionary):
        contig_length = len(sequence_dictionary[contig_name])
        print('\tScoring contig {} ...'.format(contig_name))
        for strand in (True, False):        
            contig_ids_by_contig.append(numpy.full(shape=contig_length, fill_value=contig_numbers[contig_name], dtype=numpy.int16)[:-(motif_width -1)])
            motif_scores_by_contig.append(scan_pwm(sequence_dictionary[contig_name], (rev_pwm, pwm)[strand], at_motif_midpoint=False)[:-(motif_width -1)])
            start_locations_by_contig.append(numpy.arange(contig_length).astype(numpy.int32)[:-(motif_width -1)])
            strands_by_contig.append(numpy.full(shape=contig_length, fill_value=strand, dtype=numpy.bool)[:-(motif_width -1)])

    del(sequence_dictionary)
            
    print('Concatenating chromosomes ...')
    contig_ids = numpy.concatenate(contig_ids_by_contig)
    del(contig_ids_by_contig)
    motif_scores = numpy.concatenate(motif_scores_by_contig)
    del(motif_scores_by_contig)
    start_locations = numpy.concatenate(start_locations_by_contig)
    del(start_locations_by_contig)
    strands = numpy.concatenate(strands_by_contig)
    del(strands_by_contig)

    # remove any loci with NaN scores
    print('Filtering out invalid loci ...')
    nonnan_loci = numpy.nonzero(~numpy.isnan(motif_scores))[0]
    contig_ids = contig_ids[nonnan_loci]
    motif_scores = motif_scores[nonnan_loci]
    start_locations = start_locations[nonnan_loci]
    strands = strands[nonnan_loci]
    print('\tRemoved {} out of {} loci'.format((genome_size*2) - len(nonnan_loci), (genome_size*2)))
    del(nonnan_loci)

    print('Prioritizing ...')
    sort_index = numpy.argsort(motif_scores)[::-1]
    motif_scores = motif_scores[sort_index]
    contig_ids = contig_ids[sort_index]
    start_locations = start_locations[sort_index]
    strands = strands[sort_index]
    del(sort_index)
    
    if mem_map:
        print('Mem mapping ...')
        motif_scores = toolbox.replace_with_mem_map(motif_scores, tmp_dir=TMP_DIR)
        contig_ids = toolbox.replace_with_mem_map(contig_ids, tmp_dir=TMP_DIR)
        start_locations = toolbox.replace_with_mem_map(start_locations, tmp_dir=TMP_DIR)
        strands = toolbox.replace_with_mem_map(strands, tmp_dir=TMP_DIR)
    

    print('Computing initial partition ...')
    background_mean = motif_scores.mean()
    background_std = motif_scores.std()
    print('\tInitial background N({}, {})'.format(background_mean, background_std))
    length_cutoff = numpy.argmin(numpy.abs(motif_scores - numpy.log2(toolbox.my_normal_pdf(motif_scores,
                                                                                   mean=background_mean,
                                                                                   sigma=background_std))))

    print('\tEstimated {} true motifs.'.format(length_cutoff))
    
    if polish_partition:
        def obj_func(params):
            cutoff = int(params)

            background_scores = motif_scores[cutoff:]
            background_mean = background_scores.mean()
            background_std = background_scores.std()
            ll_background = numpy.log2(toolbox.my_normal_pdf(background_scores, mean=background_mean, sigma=background_std)).sum()
            
            true_scores = motif_scores[:cutoff]
            ll_true = true_scores.sum()
            
            ll_total = ll_background + ll_true

            print('\tcutoff {}; background N({}, {})'.format(cutoff, background_mean, background_std))
            print('\tll bkg=bkg {:>0.2}, true=true {:>0.2}, total {:>0.2}'.format(ll_background, ll_true, ll_total))

            return -ll_total
    
        initial_right_bound = length_cutoff + int(len(motif_scores) * initial_search_fraction)
        
        print('Searching for  maximum likelihood partition from {} to {} ...'.format(length_cutoff, initial_right_bound))
        length_cutoff = toolbox.binary_int_min(obj_func, bounds=(length_cutoff, initial_right_bound))
        if length_cutoff == initial_right_bound: # the true minimum may be past our cutoff
            print('Initial search failed! Extending search to whole genome ...')
            length_cutoff = toolbox.binary_int_min(obj_func, bounds=(length_cutoff, len(motif_scores)))

    print('Found {} likely true motifs'.format(length_cutoff))
    true_scores = motif_scores[:length_cutoff]
    background_scores = motif_scores[length_cutoff:]
              
    print('Fitting normal distribution to background scores ...')
    data_size = len(motif_scores)
    background_mean, background_std = background_scores.mean(), background_scores.std()                                
    background_score_distribution = scipy.stats.norm(loc=background_mean, scale=background_std)
    del(background_scores)
    print('\tBackground scores have mean {:>0.2}, SD {:>0.2}'.format(background_mean, background_std))

    print('Computing final log-likelihood ratios ...')
    llr = motif_scores - numpy.log2(toolbox.my_normal_pdf(motif_scores, mean=background_mean, sigma=background_std))
    
    if llr_threshold is not None:
        print('Finding motif hits with log-likelihood ratios greater than {} ...'.format(llr_threshold))
        llr_mask = llr > llr_threshold
        motif_scores = motif_scores[llr_mask]
        contig_ids = contig_ids[llr_mask]
        start_locations = start_locations[llr_mask]
        strands = strands[llr_mask]
        del(llr_mask)
        print('\tKept {} motif hits.'.format(len(motif_scores)))
                                                  
    print('Computing p-values ...')
    # Compute p-values
    p_vals = 1 - background_score_distribution.cdf(motif_scores)
    print('\tDone.')

    # threshold by p-value
    if p_val_threshold is not None:
        initial_hit_size = len(motif_scores)
        print('Discarding hits with p-values greater than {} ...'.format(p_val_threshold))
        p_val_mask = p_vals < p_val_threshold
        p_vals = p_vals[p_val_mask]
        motif_scores = motif_scores[p_val_mask]
        contig_ids = contig_ids[p_val_mask]
        start_locations = start_locations[p_val_mask]
        llr = llr[p_val_mask]
        strands = strands[p_val_mask]
        del(p_val_mask)
        print('\t{} out of {} hits passed p-value cutoff'.format(len(p_vals), initial_hit_size))   
        
    print('Applying multiple testing correction ...')
    pass_fail, q_vals, dummy, dummy = statsmodels.sandbox.stats.multicomp.multipletests(p_vals, alpha=fdr, method='fdr_bh')

    print('\tFound {} hits at an FDR of {}'.format(pass_fail.sum(), fdr))
    
    print('Constructing output ...')
    q_vals = q_vals[pass_fail]
    length_cutoff = len(q_vals)
    
    # Do final thresholding.
    motif_scores = motif_scores[:length_cutoff]
    contig_ids = contig_ids[:length_cutoff]
    start_locations = start_locations[:length_cutoff]
    strands = strands[:length_cutoff]
    p_vals = p_vals[:length_cutoff]
    llr = llr[:length_cutoff]
    
    strand_translate = {True:'+', False:'-'}

    output_regions = pandas.DataFrame({'contig':[contig_names[contig_num] for contig_num in contig_ids],
                                      'start': start_locations,
                                      'end': start_locations + pwm.shape[1],
                                      'strand': [strand_translate[strand] for strand in strands],
                                      'motif_score': motif_scores,
                                      'empirical_llr': llr,
                                      'p_value': p_vals,
                                      'q_value': q_vals,
                                      })[['contig', 'start','end', 'strand', 'motif_score', 'empirical_llr','p_value', 'q_value']]
                                      
    print('All done in {}'.format(datetime.datetime.now() - start_time))
    return output_regions

    
def emit_sequences(linear_probabilities, size=1, random_seed=None):
    """
    Given a matrix of probabilities for each nucleotide by position, returns
    a list of sequences randomly drawn from this distribution using :param:`random_seed`
    """
    numpy.random.seed(random_seed)
    return [''.join([numpy.random.choice(('A', 'C', 'G','T'), p=linear_probabilities[:,col_number]) for col_number in range(linear_probabilities.shape[1])]) for i in range(size)]


def count_aligned_motifs(motif_sequence_list):
    """
    Given a list of aligned sequences (as strings), return a DataFrame of counts for each observed
    character by position.
    """
    motif_counts = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    for motif_sequence in motif_sequence_list:
        for char_pos, char in enumerate(motif_sequence):
            motif_counts[char_pos][char] += 1
    return (pandas.DataFrame(motif_counts).sort_index(axis=0)).fillna(value=0)
    

class HomerMotifEnrichment():
    def __init__(self, homer_output_directory):
        """
        Wrapper for extracting the output of HOMER's motif enrichment analyses
        """
        self.homer_output_directory = homer_output_directory
        print('Initializing data wrapper for HOMER motif enrichment analyses in {}'.format(homer_output_directory))
        
        known_motif_fname = os.path.join(self.homer_output_directory, 'knownResults.html')
        denovo_motif_fname = os.path.join(self.homer_output_directory, 'homerResults.html')
        
        self.has_known = os.path.isfile(known_motif_fname)
        self.has_denovo = os.path.isfile(denovo_motif_fname)
        
        if self.has_known:
            print('Found known motif enrichments. Loading ...')
            self.known_motif_dict = self._parse_known_motifs(known_motif_fname)
            self.known_motif_table = self._known_motifs_to_df(self.known_motif_dict)
        if self.has_denovo:
            print('Found de novo motif enrichments. Loading ...')
            self.denovo_motif_dict = self._parse_denovo_motifs(denovo_motif_fname)
            self.denovo_motif_table = self._denovo_motifs_to_df(self.denovo_motif_dict)
            #self.denovo_motifs = load_PFM_vertical(os.path.join(self.homer_output_directory, 'homerMotifs.all.motifs'), data_type='frequencies')
            self.denovo_pfms = self._load_denovo_pfms(os.path.join(self.homer_output_directory, 'homerResults'), range(len(self.denovo_motif_dict)))

    def _parse_known_motifs(self, known_motif_file_name):
        table_data = {}
    #     known_motif_file_name = os.path.join(motif_dir, 'knownResults.html')

        with open(known_motif_file_name, 'rt') as html_file:
            known_motifs = bs4.BeautifulSoup(html_file.read(), 'html.parser')

            table_body = known_motifs.table
            table_rows = table_body.find_all('tr')
            header_row = table_rows[0]
            col_headers = [ele.contents[0].encode() for ele in header_row.find_all('td')]
            for rank, row in enumerate(table_rows[1:]):
                new_row_data = {}
                for field_name, field_value in zip(col_headers, row.find_all('td')):
                    field_name = field_name.decode()
                    if field_value.findChildren():
                        if field_name == 'Motif':
                            new_row_data['Motif'] = field_value.findChildren()[0].attrs['src']
                    else:
                        new_value = field_value.contents[0].strip()
                        if field_name == 'Name':
                            new_value = new_value.split('/')[0]
                        new_row_data[field_name] = toolbox.smart_convert(new_value)

                table_data[rank] = new_row_data
            return table_data

    def _known_motifs_to_df(self, motif_data_dict):
        COL_ORDER = ['Name',
                     'P-value',
                     'q-value (Benjamini)',
                     '% of Targets Sequences with Motif',
                     '% of Background Sequences with Motif',
                     '# Target Sequences with Motif',
                     '# Background Sequences with Motif'
                     ]
        motif_df = pandas.DataFrame(motif_data_dict).T
        motif_df = motif_df.loc[:, COL_ORDER]
        return motif_df

    def _parse_denovo_motifs(self, de_novo_motif_file_name):

        table_data = {}

        with open(de_novo_motif_file_name, 'rt') as html_file:
            known_motifs = bs4.BeautifulSoup(html_file.read(), 'html.parser')

            table_body = known_motifs.table
            table_rows = table_body.find_all('tr')
            header_row = table_rows[0]
            col_headers = [ele.contents[0].encode() for ele in header_row.find_all('td')]
    #         print col_headers
            for rank, row in enumerate(table_rows[1:]):
                new_row_data = {}
                for field_name, field_value in zip(col_headers, row.find_all('td')):
                    field_name = field_name.decode()
                    if field_value.findChildren():
                        if field_name == 'Motif':
                            new_row_data['Motif'] = field_value.findChildren()[0].attrs['src']
                        elif field_name == 'Best Match/Details':
                            best_match_text = field_value.get_text()
                            matching_motif_name = best_match_text.split('/')[0]
                            similarity = float(best_match_text.split('/')[-1].split('(')[-1].split(')')[0])
                            new_row_data['Best Match'] = matching_motif_name
                            new_row_data['Similarity'] = similarity
                    else:  
                        new_value = field_value.contents[0].strip()                
                        new_row_data[field_name] = toolbox.smart_convert(new_value)

                table_data[rank] = new_row_data

            return table_data

    def _denovo_motifs_to_df(self, motif_data_dict):
        COL_ORDER = ['Best Match',
                     'Similarity',
                     'P-value',
                     '% of Targets',
                     '% of Background',
                     'STD(Bg STD)'
    #                  'Best Match/Details'
                     ]
        motif_df = pandas.DataFrame(motif_data_dict).T
        motif_df = motif_df.loc[:, COL_ORDER]
        return motif_df
    
    def _load_denovo_pfms(self, motif_directory, motif_numbers):
        print('Loading PFMs for de novo motifs ...')
        pfm_dict = {}
        for motif_num in motif_numbers:
            motif_fname = os.path.join(motif_directory, 'motif{}.motif'.format(motif_num+1))
            
            pfm_dict[motif_num] = list(load_PFM_vertical(motif_fname, data_type='frequencies').values())[0]
        return pfm_dict
     
     
def parse_motif_name(motif_name):
    """
    Given a motif data header from HOMER, return a tuple consisting of the trimmed motif name, the motif class, and the LLR threshold
    """
    partial_name = motif_name.split('\t')[1].split('/')[0]
    motif_class = partial_name.split('(')[1].split(')')[0]
    trimmed_name = partial_name.split('(')[0]
    threshold = float(motif_name.split('\t')[2])
    return trimmed_name, motif_class, threshold            