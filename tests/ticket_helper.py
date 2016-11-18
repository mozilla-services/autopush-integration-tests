import json


LINE = '----------------------------'


def format_results(name_test, results, bugzilla=True):
    name_test = name_test.upper()
    name_test = name_test.replace('TEST_','')
    name_test = name_test.replace('_',' ')
    results = json.dumps(
        results, sort_keys=True, indent=2, separators=(',', ': '))
    if bugzilla:
        header = '{0}\n{1}\n{0}'.format(LINE, name_test)
        return '{0}\n{1}'.format(header, results)
    else:
        header = '{1}\n{0}'.format(LINE, name_test) 
        return '{0}\n```\n{1}\n```'.format(header, results)
