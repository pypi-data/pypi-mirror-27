#!/usr/bin/env python
from __future__ import division

def main():

    import numpy as np
    import pandas as pd
    import ast
    import inspect
    import re
    
    # Need this to enable logo rendering without a graphical backend
    import matplotlib as mpl
    mpl.use('Agg')
    
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties, FontManager
    from matplotlib.transforms import Bbox
    from matplotlib.colors import to_rgba
    import pdb
    
    import validate
    from validate import validate_parameter, validate_mat
    
    from data import load_alignment
    from Logo import Logo
    from make_logo import make_logo
    from character import get_fontnames_dict, get_fontnames
    from make_styled_logo import make_styled_logo
    
    import argparse
    from validate import params_with_values_in_dict
    from documentation_parser import parse_documentation_file
    
    parser = argparse.ArgumentParser(description='Create logo from FASTA file.')
    
    doc_file = 'make_logo_arguments.txt'
    doc_dict = parse_documentation_file(doc_file)
    
    # Register all variable names and default values with argparse
    names, x, xx, default_values = inspect.getargspec(make_logo)
    for name, default in zip(names, default_values):
    
        # Create dict to hold keyword arguments
        tmp_dict = {}
        tmp_dict['default'] = default
        tmp_dict['type'] = str
        if name == 'enrichment_logbase':
            tmp_dict['choices'] = {'2', '10', 'e'}
        elif name in params_with_values_in_dict:
            tmp_dict['choices'] = params_with_values_in_dict[name]
    
        # Get documentation for that function
        if name in doc_dict:
    
            # Get entry
            entry = doc_dict[name]
            entry.set_default(default)
    
            # Set documentation string
            tmp_dict['help'] = entry.get_argparse_doc()
        else:
            tmp_dict['help'] = 'NOT DOCUMENTED.'
    
        parser.add_argument('--%s' % name, **tmp_dict)
    
    # Create parsers for *all*
    args = parser.parse_args()
    kwargs = vars(args)
    logo = make_logo(**kwargs)
    print 'Logo created!'
    
main()
    
