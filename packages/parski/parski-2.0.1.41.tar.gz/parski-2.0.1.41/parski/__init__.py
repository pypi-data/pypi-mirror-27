"""package for getting and filtering api/file data"""

def filter_data(data, search_input, max_results=5000, silent=False):
    """filter data class/function wrapper"""
    from FilterData import FilterData

    options = {}
    options['data'] = data
    options['search_input'] = search_input
    options['max_results'] = max_results
    options['silent'] = silent

    filter_object = FilterData(options)
    filter_object.filter_data()

    return filter_object

def get_data(url=None, file_name='output.json', source="file",
             key_var="PCT_API_READ_KEY", silent=False, api_retry=3):
    """get data class/function wrapper"""
    from GetData import GetData

    options = {}
    options['url'] = url
    options['file_name'] = file_name
    options['source'] = source.lower()
    options['key_var'] = key_var
    options['silent'] = silent
    options['api_retry'] = api_retry

    get_object = GetData(options)
    results = get_object.get_data()
    get_object.data = results['data']
    get_object.status_code = results['status_code']
    get_object.error_msg = results['error_msg']

    return get_object
