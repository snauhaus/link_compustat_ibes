#!/usr/bin/env python3

"""
script: link_compustat_ibis.py
author: Steffen Nauhaus
date:   Spring 2018

This script creates a mapping table between IBES and Compustat. 

It supports the following methods:

 - Link via CRSP
 - Link via S_SECURITY

Notes:
    - Output can be specified manually or via argparse
    - 

References:
[1] https://wrds-web.wharton.upenn.edu/wrds/support/Data/_010Linking%20Databases/_000Linking%20IBES%20and%20CRSP%20Data.cfm (WRDS tutorial on mapping IBES to CRSP)
[2] https://wrds-web.wharton.upenn.edu/wrds/support/code_show.cfm?path=I-B-E-S/cibeslink.sas (WRDS SAS script mapping IBES to Compustat)
[3] http://www.wrds.us/index.php/forum_wrds/viewthread/6/ (Additional clarifications from a forum post)


"""

import wrds
import argparse
import pandas as pd
import os, sys

def main(output_file, method):
    
    # Change working directory to path of script
    # This ensures that oufile is written to script directory if its not an absolute path
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    
    # Connect to wrds
    db = wrds.Connection()
    
    # Execute method
    if method is None: # Nothind specifed
        crsp_method(db, output_file)
    elif method.upper() == 'GSEC':
        gsec_method(db, output_file)
    elif method.upper() == 'CRSP':
        crsp_method(db, output_file)
    else:
        print("Unknown method specified:", method)

def gsec_method(db, output_file):
    """
    This method uses the IBTIC variable from Compustat's G_SECURITY table to add the Compustat GVKEY to IBES
    
    See: https://wrds-web.wharton.upenn.edu/wrds/tools/variable.cfm?library_id=7&file_id=64675
    
    """
    
    # Get IBES data
    ibes = db.get_table(library='ibes', table='idsum', columns=['ticker', 'cusip', 'cname'])
    ibes.drop_duplicates(inplace=True)

    # Get G_SECURITY data
    gsec = db.get_table(library='comp', table='security', columns=['gvkey', 'ibtic'])
    gsec.drop_duplicates(inplace=True)

    # Link G_Security and foreign CRSP
    out = ibes.merge(gsec, left_on='ticker', right_on='ibtic')

    # Export complete table
    out.to_csv(output_file, index=False)


def crsp_method(db, output_file):
    """
    This function maps cusip in IBES to ncusip in CRSP (ignoring date because it's "of little benefit" [1]). It then maps CRSP Compustat via the permno found in ccmxpf_lnkhist ([2]). The resulting linktable contains the IBES Ticker, CUSIP, company name (CNAME) and Compustat GVKEY.
    
    """
    
    # Get IBES data
    ibes = db.get_table(library='ibes', table='idsum', columns=['ticker', 'cusip', 'cname'])
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
    out.drop_duplicates(inplace=True)

    # Export complete table
    out.to_csv(output_file, index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create link table between Compustat and IBES. WRDS login credentials are required. ')
    parser.add_argument('-o', '--output', help='Output file (csv)', required=True, type=str) # Output file arg
    parser.add_argument('-m', '--method', help='Method to use to create the link table. Options are "gsec" for the "G_SECURITY" table method, and "crsp" for the CRSP table method. Defaults to CRSP method', required=False, type=str) # Output file arg
    args = vars(parser.parse_args())
    outfile = args['output']
    method = args['method']
    main(outfile, method)
    
    
    
    
    
    