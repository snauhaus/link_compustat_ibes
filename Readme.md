Link_compustat_ibes
===================

Python script to create a mapping table between I/B/E/S and Compustat via CRSP. Requires WRDS login credentials.

Example call
------------

    python3 link_compustat_ibes.py -o ~/linktable.csv

This asks the script to create a link table in the user's home path.

Downloads I/B/E/S, CRSP, and a Compustat-CRSP linktable from WRDS SQL server to create a linktable for I/B/E/S and Compustat.

