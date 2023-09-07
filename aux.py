def make_xlabel(texified, tau0, p, q):
    if texified:
        return r'''$\displaystyle{\tau_0 = %s, \quad p = %s, \quad q = %s, \quad f \colon n \mapsto \frac{n(1-p)}{9}+p}$''' % (tau0, p, q)
    return 'tau0 = %s, p = %s, q = %s, f(n) = n(1-p)/9+p' % (tau0, p, q)

def make_ylabel(texified, rate, frameNum):
    if texified:
        return r'\noindent Rate: ${:.2f}$ \\ Step: ${}$'.format(rate, frameNum+1)
    return 'Rate: {:.2f}, Step: {}'.format(rate, frameNum+1)

def make_title(texified):
    if texified:
        return r'''Simulation with 1\textsuperscript{st} order neighbourhood'''
    return 'Simulation with 1st order neighbourhood'