#!/usr/bin/env python3

"""
script: link_compustat_ibis.py
author: Steffen Nauhaus
date:   Spring 2018

This script creates a mapping table between IBES and Compustat via CRSP.

Notes:
    - Output can be specified manually or via argparse
    - Mapping IBES to CRSP using CUSIP-NCUSIP (ignoring date because it's "of little benefit" [1])
    - Mapping CRSP to Compustat via ccmxpf_lnkhist [2]

References:
[1] https://wrds-web.wharton.upenn.edu/wrds/support/Data/_010Linking%20Databases/_000Linking%20IBES%20and%20CRSP%20Data.cfm (WRDS tutorial on mapping IBES to CRSP)
[2] https://wrds-web.wharton.upenn.edu/wrds/support/code_show.cfm?path=I-B-E-S/cibeslink.sas (WRDS SAS script mapping IBES to Compustat)
[3] http://www.wrds.us/index.php/forum_wrds/viewthread/6/ (Additional clarifications from a forum post)


"""

import wrds
import argparse
import pandas as pd
import os, sys

def main(output_file):
    
    # Change working directory to path of script
    # This ensures that oufile is written to script directory if its not an absolute path
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    
    # Connect to wrds
    db = wrds.Connection()

    # Get IBES data
    ibes = db.get_table(library='ibes', table='idsum', columns=['ticker', 'cusip'])
    ibes.drop_duplicates(inplace=True)

    # Get CRSP data
    crsp = db.get_table(library='crsp', table='stocknames', columns=['permno', 'ncusip'])
    crsp.drop_duplicates(inplace=True)

    # Merge IBES and CRSP
    link1 = ibes.merge(crsp, left_on='cusip', right_on='ncusip')

    # Get Compustat-CRSP linktable
    link2 = db.get_table(library='crsp', table='ccmxpf_lnkhist', columns=['gvkey', 'lpermno', 'lpermco', 'linktype', 'linkprim']) # 'linkdt', 'linkenddt'
    link2 = link2[link2['linktype'].isin(['LC', 'LU'])]
    link2 = link2[link2['linkprim'].isin(['C', 'P'])]
    link2.drop(['linktype', 'linkprim'], axis=1, inplace=True)

    # Merge the two link tables
    out = link2.merge(link1, left_on='lpermno', right_on='permno')

    # Export complete table
    out.to_csv(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create link table between Compustat and IBES via CRSP. WRDS login credentials are required.')
    parser.add_argument('-o', '--output', help='Output file (csv)', required=True, type=str) # Output file arg
    args = vars(parser.parse_args())
    outfile = args['output']
    main(outfile)
    
    
    
    
    
    
    