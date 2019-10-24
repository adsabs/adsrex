import os, sys
import gzip

ADS_CLASSIC_MIRROR_LIST = [
    'astrobib.u-strasbg.fr',
    'ads.nao.ac.jp',
    'ads.astro.puc.cl',
    'esoads.eso.org',
    'ukads.nottingham.ac.uk',
    'ads.iucaa.ernet.in',
    'ads.inasan.ru',
    'ads.bao.ac.cn',
    'ads.mao.kiev.ua',
    'ads.ari.uni-heidelberg.de',
    'ads.arsip.lipi.go.id',
    'ads.on.br',
    'saaoads.chpc.ac.za',
    'adsabs.harvard.edu'
]

def run(*log_files):

    sys.stderr.write('going to process %s log files\n' % (len(log_files)))
    collection = {}
    i = 0
    e = 0

    for f in log_files:
        if not os.path.exists(f):
            sys.stderr.write('%s not exists\n' % (f))
            continue
        if f.endswith('.gz'):
            fi = gzip.open(f)
        else:
            fi = open(f, 'r')

        for line in fi:
            i += 1
            try:
                row = apache2_logrow(line)
                harvest(row, collection)
            except Exception, exc:
                sys.stderr.write(str(exc) + '\n')
                e += 1
            if i % 1000000 == 0:
                sys.stderr.write('%s:%s\n' % (f, i))
        fi.close()

    sys.stderr.write('processed %s entries (%s errored)\n' % (i, e))
    printout(collection)

def printout(collection):
    print '#entries\t#internal\tstatus\tverb\tpattern\texample'
    
    for k,v in sorted(collection.items(), key=lambda x: x[1]['#count'], reverse=True):
        print '%5s\t%5s\t%s\t%s' % (v['#count'], v['#classic'], '\t'.join(k.split(' ')), v['#example'])

def harvest(row, collection):

    verb, target, version = row[4].split(' ')
    status = row[5]
    length = row[6]
    referrer = row[7]
    
    # ip = row[0], client = row[8], cookie = row[9]
    
    # can't hurt
    verb = verb.upper()
    target = target.lower()

    if '?' in target:
        target = target[0:target.index('?')] + '?<params>'
    for s in ['/abs/', '/doi/', '/full/', '/pdf', '/articles/abstracts/']:
        if target.startswith(s):
            r = target[len(s):]
            x = '/'.join(map(lambda x: str(len(x)), target[len(s):].split('/')))
            target = '%s<%s>' % (s, x)

    key = '%s %s %s' % (status, verb, target)
    if key not in collection:
        collection[key] = {'#count': 0, '#classic': 0, '#example': row[4].split(' ')[1]}

    collection[key]['#count'] += 1
    if referrer:
        for x in ADS_CLASSIC_MIRROR_LIST:
            if x in referrer:
                collection[key]['#classic'] += 1


def apache2_logrow(s):
    ''' Fast split on Apache2 log lines

    http://httpd.apache.org/docs/trunk/logs.html
    https://stackoverflow.com/questions/12544510/parsing-apache-log-files
    '''
    row = [ ]
    qe = qp = None # quote end character (qe) and quote parts (qp)
    for s in s.replace('\r','').replace('\n','').split(' '):
        if qp:
            qp.append(s)
        elif '' == s: # blanks
            row.append('')
        elif '"' == s[0]: # begin " quote "
            qp = [ s ]
            qe = '"'
        elif '[' == s[0]: # begin [ quote ]
            qp = [ s ]
            qe = ']'
        else:
            row.append(s)

        l = len(s)
        if l and qe == s[-1]: # end quote
            if l == 1 or s[-2] != '\\': # don't end on escaped quotes
                row.append(' '.join(qp)[1:-1].replace('\\'+qe, qe))
                qp = qe = None
    return row


if __name__ == '__main__':
    run(*sys.argv[1:])