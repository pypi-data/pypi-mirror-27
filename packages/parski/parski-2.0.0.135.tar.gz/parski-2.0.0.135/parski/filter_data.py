"""module for filtering data"""
from __future__ import print_function

import time
import re
from copy import deepcopy

from filter_datetime import filter_datetime
from path_dict_conv import dict_to_paths

class FilterData(dict):
    """filter data using search_input"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, data, search_input, max_results=5000, silent=False):
        dict.__init__(self)
        self.search_input = deepcopy(search_input)
        self.data = data
        self.max_results = max_results
        self.silent = silent
        self.metrics = {
            'missing_keys': {
                'total_missing': 0
            },
            'regex_errors': 0,
            'searches': 0,
            'search_time': 0
        }
        self.results = self.filter_data()
        if self.metrics['searches'] == 0:
            self.metrics['search_avg'] = None
        else:
            self.metrics['search_avg'] = self.metrics['search_time'] / self.metrics['searches']
        del self.data

    def __whisper(self, text):
        """print wrapper to check silent parameter"""
        if not self.silent:
            print(text)

    @staticmethod
    def __is_search_path(item):
        """check if item is a search_path"""
        if not isinstance(item, dict):
            return False
        if sorted(item.keys()) != ['path', 'value']:
            return False
        if not isinstance(item['path'], list):
            return False
        if isinstance(item['value'], (dict, list)):
            return False
        return True

    def __standardize_input(self):
        """standardize input to always have path group"""

        #check if search path or search dict and converts to search path groups
        if isinstance(self.search_input, dict):
            if self.__is_search_path(self.search_input):
                self.search_input = [[self.search_input]]
            else:
                self.search_input = [dict_to_paths(self.search_input)]

        #check if list of paths or list of dicts and converts if needed
        elif isinstance(self.search_input, list):
            for index, item in enumerate(self.search_input):

                #list of dicts
                if isinstance(item, dict):
                    if not self.__is_search_path(item):
                        self.search_input[index] = dict_to_paths(self.search_input[index])
                    else:
                        self.search_input[index] = [item]

                #list of lists
                elif isinstance(item, list):
                    for inner_item in item:
                        #list of lists must be search paths
                        if not self.__is_search_path(inner_item):
                            raise TypeError("Search input list must be path groups or search dicts")

                #list of garbage
                else:
                    raise TypeError("Search input list must be path groups or search dicts")

        #not list or dict
        else:
            raise TypeError("Search input must be a list or dict")

    def filter_data(self):
        """filter data based on path list or search dict arrays"""

        self.__standardize_input()

        if not self.data:
            self.__whisper("Input data is empty.  No results found.")
            return []
        self.__whisper("Data length: %i" % len(self.data))
        self.__whisper("Search Input:")
        for item in self.search_input:
            self.__whisper(str(item))
        self.__whisper("Running Search...")


        #each path_list is OR'd with each other, so results are added
        start_time = time.time()
        valid_indices = []
        for index, path_list in enumerate(self.search_input):
            for path in path_list:
                #make sure first path is an integer."
                try:
                    int(path['path'][0])
                except (ValueError, TypeError):
                    path['path'] = [index] + path['path']

            #Remove paths where value is None
            path_list = [x for x in path_list if x['value'] is not None]

            #check each entry in data
            for i, entry in enumerate(self.data):
                #check if max results have been found
                if len(valid_indices) >= self.max_results:
                    self.metrics['search_time'] = time.time() - start_time
                    return [self.data[index] for index in valid_indices]
                #actually do the filtering
                if i in valid_indices:
                    continue
                elif self.__entry_filter(entry, path_list, True):
                    valid_indices.append(i)
                self.metrics['searches'] += 1

        self.__whisper("Results found: %i" % len(valid_indices))
        self.metrics['search_time'] = time.time() - start_time
        return [self.data[index] for index in valid_indices]

    def __entry_filter(self, entry, path_list, first):
        """filter single entry with path_list"""

        path_groups = []
        remaining = path_list
        while remaining:
            current_path = remaining[0]
            #check if path has ended and doesn't equal value.
            if len(current_path['path']) <= 1:
                #One fail is total fail.  One pass is NOT total pass.
                if self.__value_check(entry, current_path) is False:
                    return False
                remaining = remaining[1:]
            #remaining paths sorted into groups based on first value
            else:
                new_group = [x for x in remaining if x['path'][0] == current_path['path'][0]]
                remaining = [x for x in remaining if x not in new_group]
                path_groups.append(new_group)

        return self.__filter_path_groups(entry, path_groups, first)

    def __filter_path_groups(self, entry, path_groups, first):
        """Groups checks by list to ensure passes are at same index"""
        if entry is None:
            return False

        if first:
            for group in path_groups:
                #go one further down the path
                group = [{'value': x['value'], 'path': x['path'][1:]} for x in group]
                return self.__entry_filter(entry, group, False)
        else:
            for group in path_groups:
                current_index = group[0]['path'][0]

                #go one further down the path
                group = [{'value': x['value'], 'path': x['path'][1:]} for x in group]

                #check if list, if so check for at least one match
                if isinstance(entry, list):
                    passes = [x for x in entry if self.__entry_filter(x, group, False)]
                    if not passes:
                        return False
                else:
                    if current_index in list(entry):
                        if not self.__entry_filter(entry[current_index], group, False):
                            return False
                    else:
                        return False
            return True


    def __value_check(self, entry, path):
        """check if end value is equal to the the one defined in the path"""

        value = str(path['value'])
        if value == 'null':
            value = 'None'
        entry_index = path['path'][0]

        ##check for key errors
        try:
            entry[entry_index]
        except KeyError:
            if entry_index not in self.metrics['missing_keys']:
                self.metrics['missing_keys'][entry_index] = 1
            else:
                self.metrics['missing_keys'][entry_index] += 1
            self.metrics['missing_keys']['total_missing'] += 1
            return False

        ##check regex and for compile errors
        try:
            regex_value = re.compile(value, re.IGNORECASE)
            return bool(re.search(regex_value, str(entry[entry_index])) or
                        filter_datetime(value, entry[entry_index]))
        except Exception:
            self.metrics['regex_errors'] += 1
            return False
