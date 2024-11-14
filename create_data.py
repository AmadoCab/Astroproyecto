#!/usr/bin/env python3

import pandas as pd

## Parse Blazar data and others ##
dtypes = {
    'name': 'string',
    'flux_1_100_gev': 'float64',
    'assoc_name': 'string',
    'frac_variability': 'float64',
    'frac_variability_error': 'float64',
    'source_type': 'string'
}
data = pd.read_excel('browse_results.xls', sheet_name='Muestra',
                     usecols=list(dtypes.keys()), dtype=dtypes)
data['name'] = data['name'].str.replace(' ', '_')
data['source_type'] = data['source_type'].str.lower()

data.to_csv('browse_results.csv', index=False)
