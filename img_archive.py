'''
    img_archive.py - pandora_client plugin

    custom parse_path for pandora_client to parse image archive paths in the form

    YYYY/MM_YYYY/DD_MM_YYYY/Location 1/Location 2/Subject 1/Cinematographer/Subject 2(optional)/party.PNG

'''
import re
import ox
import os

def example_path(client):
    #return '\t' + 'YYYY/MM_YYYY/DD_MM_YYYY/Location 1/Location 2/Subject 1/Shooter/Subject 2(optional)/party.PNG'
    return '\t' + 'Subject 1/Subject 2/Subject 3(optional)/party.PNG'  

def parse_path(client, path):
    '''
        args:
            client - Client instance
            path   - path without volume prefix 
        return:
            return None if file is ignored, dict with parsed item information otherwise
    '''
    #m = re.compile('^(\d{4})/(\d{2})_(\d{4})/(?P<day>\d+)_(?P<month>\d+)_(?P<year>\d{4})/(?P<location1>.+?)/(?P<location2>.+?)/(?P<subject1>.+?)/(?P<shooter>.+?)/((?P<subject2>.+?)/|).*').match(path)
    m = re.compile('^(?P<subject1>.+?)/(?P<subject2>.+?)/((?P<subject3>.+?)/|).*').match(path)    
    if not m:
        return None
    info = m.groupdict()
    #date = '%s-%s-%s' % (info['year'], info['month'], info['day'])
    for key in info:
        if info[key]:
            info[key] = info[key].replace('_', ' ')

    #topic = [info['subject']]
    topic = [info['subject1']]
    '''
    if info['subject2']:
        topic.append(info['subject2'])
        title = "%s, %s (%s)" % (info['subject1'], info['subject2'], date)
    else:
        title = "%s (%s)" % (info['subject1'], date)
    title = "%s %s at %s, %s" % (title,
        info['shooter'],info['location2'],info['location1'])        
    '''
    title = path

    r = {
        #'cinematographer': [info['shooter']],
        'title': title,
        #'date': date,
        #'location': '%s, %s' % (info['location2'], info['location1']),        
        #'collection': os.path.dirname(path),
        'topic': topic
    }
    _info = ox.movie.parse_path(path)
    for key in ('extension', 'type'):
        r[key] = _info[key]
    return r


