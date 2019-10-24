Link_compustat_ibes
===================

Python script to create a mapping table between I/B/E/S and Compustat. Requires WRDS login credentials.

Supported methods are via [CRSP](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_010Linking%20Databases/_000Linking%20IBES%20and%20CRSP%20Data.cfm) and via [G_Security](https://wrds-support.wharton.upenn.edu/hc/en-us/articles/115003441852-Merging-International-I-B-E-S-with-Compustat-Global).

Example call
------------

    python3 link_compustat_ibes.py -o ~/linktable.csv

This asks the script to create a link table in the user's home path. It will download I/B/E/S, CRSP, and a Compustat-CRSP linktable from WRDS SQL server and merge the three tables in order to create a linktable for I/B/E/S and Compustat. This requires valid login credentials to WRDS. 

The option `-m` (or `--method`) can be used to specify the method with which the two tables should be merged (see above). The script can either perform the merge via the *CRSP* key or via *G_security*. CRSP is the default. To merge via G_security, run

    python3 link_compustat_ibes.py -o ~/linktable2.csv -m 'gsec'


