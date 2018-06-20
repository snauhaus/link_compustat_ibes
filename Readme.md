Link_compustat_ibes
===================

Python script to create a mapping table between I/B/E/S and Compustat. Requires WRDS login credentials.

Supported methods are via [CRSP](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_010Linking%20Databases/_000Linking%20IBES%20and%20CRSP%20Data.cfm) and via [G_Security](https://wrds-support.wharton.upenn.edu/hc/en-us/articles/115003441852-Merging-International-I-B-E-S-with-Compustat-Global).

Example call
------------

    python3 link_compustat_ibes.py -o ~/linktable.csv

This asks the script to create a link table in the user's home path.

Downloads I/B/E/S, CRSP, and a Compustat-CRSP linktable from WRDS SQL server to create a linktable for I/B/E/S and Compustat.


    python3 link_compustat_ibes.py -o ~/linktable2.csv -m 'gsec'

This asks the script to create a link table in the user's home path.

Downloads I/B/E/S and G_Security table from WRDS SQL server to create linktable2.csv for I/B/E/S ticker/cusip and Compustat's gvkey.

