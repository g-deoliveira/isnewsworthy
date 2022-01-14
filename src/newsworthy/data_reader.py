import os
from pathlib import Path
import json
from collections import Counter

DATA_BASE_PATH = '../../data/parsed'


class DataReader:
    '''
    Reads the parsed data files in `base_path`
    and returns the labeled features for machine learning
    applications.
    '''

    def __init__(self, verbose=False):

        #self.base_path = base_path
        self.verbose = verbose

        # generate the absolute path to the data directory
        script_path = Path(__file__)
        package_root = Path(script_path, '../../..')
        assert package_root.resolve().name == 'isnewsworthy'
        data_path = Path(package_root, 'data/parsed')
        self.data_path = data_path.resolve()

        self._prefixes = self._get_file_prefixes()
    
    
    def _get_file_prefixes(self):
    
        prefixes = [f for f in os.listdir(self.data_path)]
        prefixes = set([p[:p.index('.')] for p in prefixes])

        print(f'Collected {len(prefixes)} prefixes.')
        
        return sorted(list(prefixes))
    

    def _get_record(self, prefix):

        # metadata is a dictionary 
        metadata = self._read_metadata(prefix)
        
        if metadata.get('error'):
            # these URLs were not properly parsed so we skip these
            raise ValueError('parsing error')

        else:

            label = metadata.get('label')
    
            raw_features = self._read_raw_features(prefix)

            return raw_features, label


    def get_Xy_data(self):
        '''
        Returns the labeled feature dataset (features, labels) where:
        data: list of dictionaries, where each dictionary corresponds to one feature record
        target: the corresponding labels 
        '''

        labels = []
        features = []

        for prefix in self._prefixes:
            if self.verbose: print(prefix)
            
            try:
                raw_features, label = self._get_record(prefix)
            except ValueError as ve:
                if self.verbose: print(f'ValueError for prefix {prefix}')
                continue

            features.append(raw_features)
            labels.append(label)
        
        assert len(labels) == len(features)

        # compute the target distribution for display purposes
        target_distribution = Counter(labels)

        print(len(features), target_distribution)

        return features, labels


    def _read_metadata(self, prefix):
        '''
        The metadata is stored in files '1234.json'
        where 1234 is the prefix.
        '''
        
        file_name = f'{prefix}.json'
        if self.verbose: print(file_name)

        f = Path(self.data_path, file_name)    
        data = json.loads(f.read_text())
        
        return data


    def _read_raw_features(self, prefix):
        '''
        The features parsed from the website is stored in json format
        in files with naming convention '1234.raw_features'
        where 1234 is the prefix.
        '''
        
        file_name = f'{prefix}.raw_features'
        if self.verbose: print(file_name)

        f = Path(self.data_path, file_name)
        data = json.loads(f.read_text())
        
        return data
    
    def get_record(self, prefix):
        '''
        prefix: int
        '''

        # convert prefix to the expected format
        prefix = str(prefix).zfill(4)
        if self.verbose: print(f'prefix={prefix}')

        # get the record if the prefix is found
        if prefix in self._prefixes:
            return self._get_record(prefix)
        else:
            print('prefix not found')



if __name__ == '__main__':
    
    dr = DataReader()
    features, labels = dr.get_Xy_data()

    record, label = dr.get_record(prefix=10)

    print(
        json.dumps(
            {k:v[:80]+'...' if isinstance(v,str) else v for k,v in record.items()}
            ,indent=2)
    )

    

