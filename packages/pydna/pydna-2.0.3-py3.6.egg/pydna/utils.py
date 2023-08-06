#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''This module provides miscellaneous functions.

'''
import shelve    as _shelve
import os        as _os
import logging   as _logging
import base64    as _base64
import pickle    as _pickle
import hashlib   as _hashlib
_module_logger = _logging.getLogger("pydna."+__name__)

from Bio.SeqUtils.CheckSum  import seguid   as _base64_seguid
from itertools import tee                   as _tee
from Bio.SeqFeature import SeqFeature       as _SeqFeature
from Bio.SeqFeature import FeatureLocation  as _FeatureLocation
from Bio.SeqFeature import CompoundLocation as _CompoundLocation
from pydna._pretty  import pretty_str       as _pretty_str
from Bio.Seq             import _maketrans
from Bio.Data.IUPACData  import ambiguous_dna_complement as _amb_compl

_amb_compl.update({"U":"A"})
_complement_table = _maketrans(_amb_compl)

def rc(sequence):
    '''returns the reverse complement of sequence (string)
    accepts mixed DNA/RNA
    '''
    return sequence.translate(_complement_table)[::-1]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = _tee(iterable)
    next(b, None)
    return zip(a, b)

def eq(*args,**kwargs):
    '''Compares two or more DNA sequences for equality i.e. they
    represent the same DNA molecule. Comparisons are case insensitive.

    Parameters
    ----------
    args : iterable
        iterable containing sequences
        args can be strings, Biopython Seq or SeqRecord, Dseqrecord
        or dsDNA objects.
    circular : bool, optional
        Consider all molecules circular or linear
    linear : bool, optional
        Consider all molecules circular or linear

    Returns
    -------
    eq : bool
        Returns True or False

    Notes
    -----

    Compares two or more DNA sequences for equality i.e. if they
    represent the same DNA molecule.

    Two linear sequences are considiered equal if either:

    * They have the same sequence (case insensitive)
    * One sequence is the reverse complement of the other (case insensitive)

    Two circular sequences are considered equal if they are circular permutations:

    1. They have the same lengt, AND
    2. One sequence or can be found in the concatenation of the other sequence with itself, OR
    3. The reverse complement can be found in the concatenation of the other sequence with itself.

    The topology for the comparison can be set using one of the keywords
    linear or circular to True or False.

    If circular or linear is not set, it will be deduced from the topology of
    each sequence for sequences that have a linear or circular attribute
    (like Dseq and Dseqrecord).

    Examples
    --------

    >>> from pydna.dseqrecord import Dseqrecord
    >>> from pydna.utils import eq
    >>> eq("aaa","AAA")
    True
    >>> eq("aaa","AAA","TTT")
    True
    >>> eq("aaa","AAA","TTT","tTt")
    True
    >>> eq("aaa","AAA","TTT","tTt", linear=True)
    True
    >>> eq("Taaa","aTaa", linear = True)
    False
    >>> eq("Taaa","aTaa", circular = True)
    True
    >>> a=Dseqrecord("Taaa")
    >>> b=Dseqrecord("aTaa")
    >>> eq(a,b)
    False
    >>> eq(a,b,circular=True)
    True
    >>> a=a.looped()
    >>> b=b.looped()
    >>> eq(a,b)
    True
    >>> eq(a,b,circular=False)
    False
    >>> eq(a,b,linear=True)
    False
    >>> eq(a,b,linear=False)
    True
    >>> eq("ggatcc","GGATCC")
    True
    >>> eq("ggatcca","GGATCCa")
    True
    >>> eq("ggatcca","tGGATCC")
    True


    '''

    from Bio.Seq import reverse_complement
    from Bio.SeqRecord import SeqRecord
    import itertools
    args=list(args)
    for i, arg in enumerate(args):
        if not hasattr(arg, "__iter__") or isinstance(arg, SeqRecord) or isinstance(arg, (bytes,str)):
            args[i] = (arg,)
    args = list(itertools.chain.from_iterable(args))

    topology = None

    if "linear" in kwargs:
        if kwargs["linear"]==True:
            topology = "linear"
        if kwargs["linear"]==False:
            topology = "circular"
    elif "circular" in kwargs:
        if kwargs["circular"]==True:
            topology = "circular"
        if kwargs["circular"]==False:
            topology = "linear"
    else:
        # topology keyword not set, look for topology associated to each sequence
        # otherwise raise exception
        topology = set([arg.circular if hasattr(arg, "circular") else None for arg in args])

        if len(topology)!=1:
            raise Exception("sequences have different topologies")
        topology = topology.pop()
        if topology in (False, None):
            topology = "linear"
        elif topology==True:
            topology = "circular"

    #args_string_list    = [str(arg.seq).lower() if hasattr(arg,"seq") else str(arg).lower() for arg in args]

    args = [arg.seq if hasattr(arg, "seq") else arg for arg in args]
    args_string_list    = [arg.watson.lower() if hasattr(arg, "watson") else str(arg).lower() for arg in args]

    length = set((len(s) for s in args_string_list))

    if len(length)!=1:
        return False
    same = True

    if topology == "circular":
        # force circular comparison of all given sequences
        for s1, s2 in itertools.combinations(args_string_list, 2):
            if not ( s1 in s2+s2 or reverse_complement(s1) in s2+s2):
                same = False
    elif topology == "linear":
        # force linear comparison of all given sequences
        for s1,s2 in itertools.combinations(args_string_list, 2):
            if not ( s1==s2 or s1==reverse_complement(s2) ):
                same = False
    return same

def shift_origin(seq, shift):
    '''Shift the origin of seq which is assumed to be a circular
    sequence.

    Parameters
    ----------
    seq : string, Biopython Seq, Biopython SeqRecord, Dseq or Dseqrecord
        sequence to be shifted.

    Returns
    -------
    new_seq : string, Biopython Seq, Biopython SeqRecord, Dseq or Dseqrecord
        sequence with a new origin.

    Examples
    --------

    >>> from pydna.utils import shift_origin
    >>> shift_origin("taaa",1)
    'aaat'
    >>> shift_origin("taaa",0)
    'taaa'
    >>> shift_origin("taaa",2)
    'aata'
    >>> shift_origin("gatc",2)
    'tcga'

    See also
    --------
    pydna.dseqrecord.Dseqrecord.shifted
    '''

    length=len(seq)

    if not 0<=shift<length:
        raise ValueError("shift ({}) has to be 0<=shift<length({})",format((shift,length,)))

    if hasattr(seq, "linear"):
        new = seq.tolinear()
    else:
        new = seq

    new = (new+new)[shift:shift+length]

    def wraparound(feature):
        new_start = length -(shift-feature.location.start)
        new_end   = feature.location.end-shift

        c = _SeqFeature(_CompoundLocation( [_FeatureLocation(0, new_end),
                                          _FeatureLocation(new_start, length)]),
                       type=feature.type,
                       location_operator="join",
                       strand=feature.strand,
                       id=feature.id,
                       qualifiers=feature.qualifiers)
        sub_features=[]
        for sf in feature.sub_features:
            if feature.location.end<shift:
                sub_features.append(_SeqFeature(_FeatureLocation(length-feature.location.start,
                                                               length-feature.location.end),
                                    type=feature.type,
                                    location_operator=feature.location_operator,
                                    strand=feature.strand,
                                    id=feature.id,
                                    qualifiers=feature.qualifiers,
                                    sub_features=None))
            elif feature.location.start>shift:
                sub_features.append(_SeqFeature(_FeatureLocation(feature.location.start-shift,
                                                               feature.location.end-shift),
                                    type=feature.type,
                                    location_operator=feature.location_operator,
                                    strand=feature.strand,
                                    id=feature.id,
                                    qualifiers=feature.qualifiers,
                                     sub_features=None))
            else:
                sub_features.extend(wraparound(sf))
        c.sub_features.extend(sub_features)
        return c

    if hasattr(seq, "features"):
        for feature in seq.features:
            if shift in feature:
                new.features.append(wraparound(feature))

    if hasattr(seq, "linear"):
        new = new.looped()

    return new

def copy_features(source_sr, target_sr, limit = 10):
    '''This function tries to copy all features in source_seq and copy
    them to target_seq. Source_sr and target_sr are objects with
    a features property, such as Dseqrecord or Biopython SeqRecord.

    Parameters
    ----------

    source_seq : SeqRecord or Dseqrecord
        The sequence to copy features from

    target_seq : SeqRecord or Dseqrecord
        The sequence to copy features to

    Returns
    -------
    bool : True
        This function acts on target_seq in place.
        No data is returned.


    '''
    import re
    from Bio.Seq import reverse_complement as rc
    target_length    = len(target_sr)
    target_string    = str(target_sr.seq).upper()

    try:
        circular = bool(target_sr.circular)
    except AttributeError:
        circular=False

    newfeatures=[]

    trgt_string = target_string
    trgt_string_rc = rc(trgt_string)

    for feature in [f for f in source_sr.features if len(f)>limit]:
        fsr            = feature.extract(source_sr).upper()
        featurelength  = 0# len(fsr)

        if circular:
            trgt_string = target_string+target_string[:featurelength]
            trgt_string_rc = rc(trgt_string)

        positions = (
        [(m.start(), m.end(), 1,) for m in re.finditer(str(fsr.seq),trgt_string)]
        +
        [(len(trgt_string_rc)-m.end(),len(trgt_string_rc)-m.start(),-1,)
                      for m in re.finditer(str(fsr.seq),trgt_string_rc)])

        for begin, end, strand in positions:
            if circular and begin<target_length<end:
                end = end-len(
                              target_sr)
                sf1 = _SeqFeature(_FeatureLocation(begin, trgt_length),
                                 type=feature.type,
                                 location_operator=feature.location_operator,
                                 strand=strand,
                                 id=feature.id,
                                 qualifiers=feature.qualifiers,
                                 sub_features=None,)
                sf2 = _SeqFeature(_FeatureLocation(0, end),
                                 type=feature.type,
                                 location_operator=feature.location_operator,
                                 strand=strand,
                                 id=feature.id,
                                 qualifiers=feature.qualifiers,
                                 sub_features=None,)
                nf =  _SeqFeature(_FeatureLocation(begin, end),
                                 type=feature.type,
                                 location_operator="join",
                                 strand=strand,
                                 id=feature.id,
                                 qualifiers=feature.qualifiers,
                                 sub_features=[sf1,sf2],)
            else:
                nf = _SeqFeature(_FeatureLocation(begin,end),
                     type=feature.type,
                     location_operator=feature.location_operator,
                     strand=strand,
                     id=feature.id,
                     qualifiers=feature.qualifiers,
                     sub_features=None)
            newfeatures.append(nf)
    target_sr.features.extend(newfeatures)
    return True



def ChenFoxLyndonBreakpoints(s):
    """Find starting positions of Chen-Fox-Lyndon decomposition of s.
    The decomposition is a set of Lyndon words that start at 0 and
    continue until the next position. 0 itself is not output, but
    the final breakpoint at the end of s is. The argument s must be
    of a type that can be indexed (e.g. a list, tuple, or string).
    The algorithm follows Duval, J. Algorithms 1983, but uses 0-based
    indexing rather than Duval's choice of 1-based indexing.

    Algorithms on strings and sequences based on Lyndon words.
    David Eppstein, October 2011.

    """
    k = 0
    while k < len(s):
        i,j = k,k+1
        while j < len(s) and s[i] <= s[j]:
            i = (s[i] == s[j]) and i+1 or k     # Python cond?yes:no syntax
            j += 1
        while k < i+1:
            k += j-i
            yield k

def ChenFoxLyndon(s):
    """Decompose s into Lyndon words according to the Chen-Fox-Lyndon theorem.
    The arguments are the same as for ChenFoxLyndonBreakpoints but the
    return values are subsequences of s rather than indices of breakpoints.

    Algorithms on strings and sequences based on Lyndon words.
    David Eppstein, October 2011.

    """
    old = 0
    for k in ChenFoxLyndonBreakpoints(s):
        yield s[old:k]
        old = k

def SmallestRotation(s):
    """Find the rotation of s that is smallest in lexicographic order.
    Duval 1983 describes how to modify his algorithm to do so but I think
    it's cleaner and more general to work from the ChenFoxLyndon output.

    Algorithms on strings and sequences based on Lyndon words.
    David Eppstein, October 2011.

    """
    prev,rep = None,0
    for w in ChenFoxLyndon(s+s):
        if w == prev:
            rep += 1
        else:
            prev,rep = w,1
        if len(w)*rep == len(s):
            return w*rep
    raise Exception("Reached end of factorization with no shortest rotation")

def seguid(seq):
    '''Returns the url safe SEGUID checksum for the sequence. This is the SEGUID
    checksum with the '+' and '/' characters of standard Base64 encoding are respectively
    replaced by '-' and '_'.
    '''
    return _pretty_str( _base64_seguid( str(seq).upper() ).replace("+","-").replace("/","_") )

def cseguid(seq):
    '''Returns the cSEGUID for the sequence. The cSEGUID is the url safe SEGUID checksum
    calculated for the lexicographically minimal string rotation of a DNA sequence.
    Only defined for circular sequences.
    '''
    from Bio.Seq import reverse_complement as rc
    return _pretty_str( seguid( min( SmallestRotation(str(seq).upper()), SmallestRotation(str(rc(seq)).upper()))))

def memorize(filename):
    def decorator(f):
        def wrappee( *args, **kwargs):
            _module_logger.info( "#### memorizer ####" )
            _module_logger.info( "pydna_cache = %s", _os.getenv("pydna_cache") )
            _module_logger.info( "cache filename = %s", filename )
            fresh = cached = None
            if _os.environ["pydna_cache"] not in ("cached", "nocache", "refresh", "compare"):
                raise Exception("pydna_cache is {}, should be compare,cached,nocache or refresh".format(_os.environ["pydna_cache"]))
            if _os.environ["pydna_cache"] == "nocache" or filename not in _os.environ["pydna_cached_funcs"].split(","):
                _module_logger.info("made it new!")
                return f(*args, **kwargs)                 
            cached = refresh = False

            key = _base64.urlsafe_b64encode(_hashlib.sha1(_pickle.dumps((args, kwargs))).digest()).decode("ascii")
            _module_logger.info( "key = %s", key )

            if _os.environ["pydna_cache"] in ("cached","compare"):
                cache = _shelve.open(_os.path.join(_os.environ["pydna_data_dir"], filename), writeback=False)
                try:
                    cached = cache[key]
                    _module_logger.info( "found %s in cache", key)
                except KeyError:
                    if _os.environ["pydna_cache"] == "compare":
                         _module_logger.warning("no result for key %s in shelve %s", key, filename)
                    else:
                        refresh = True
                cache.close()
            _module_logger.info("refresh = %s", refresh)
            if refresh or _os.environ["pydna_cache"] in ("compare","refresh"):
                fresh = f(*args, **kwargs)
                _module_logger.info("made it new!")
            
            if _os.environ["pydna_cache"] == "compare":
                if fresh == cached:
                    _module_logger.info('cache ok for key %s in %s', key, filename)
                else:
                    _module_logger.warning('cache different from fresh for key %s in %s', key, filename)
                                
            if refresh or _os.environ["pydna_cache"] == "refresh":
                cache = _shelve.open(_os.path.join(_os.environ["pydna_data_dir"], filename), writeback=False)
                cache[key] = fresh
                _module_logger.info("saved result under key %s", key)
                cache.close()
            return cached or fresh
        return wrappee
    return decorator      

if __name__=="__main__":
    cache = _os.getenv("pydna_cache")
    _os.environ["pydna_cache"]="nocache"
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    _os.environ["pydna_cache"]=cache

