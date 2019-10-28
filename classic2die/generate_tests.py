import os
import sys

def run(*input_files):
    verbs = {'GET': 'get', 'HEAD': 'head', 'POST': 'post', 'OPTIONS': 'options'}
    for f in input_files:
        if not os.path.exists(f):
            sys.stderr.write('%s does not exist\n' % f)
        fi = open(f, 'r')
        
        # ignore the first line
        fi.readline()
        
        i = -1
        for line in fi:
            i += 1
            freq,freqinternal,status,verb,pattern,example = line.strip().split('\t')
            
            print '''def url_%(i)03d(self, user=anonymous_user_classic):
    """
    (%(i)03d) %(pattern)s freq=%(freq)s (internal traffic: %(internal)3.2f, orig_status=%(status)s)
    """
    r = user.%(method)s('%(example)s')
    self.assertEquals(r.status_code, %(status)s)

''' % dict(i=i, pattern=pattern, freq=freq, internal=float(freqinternal)/float(freq), status=status, 
       method=verbs.get(verb, 'unknown'), example=example)
        
        

if __name__ == '__main__':
    run(*sys.argv[1:])