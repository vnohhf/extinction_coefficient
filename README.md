# extinction_coeffcient

extinction_coeffcient is a python package to provide empirical extinction or reddening coefficients 
from far-ultraviolet (UV) to the mid-infrared (IR).

# How to Install
## From source
extinction_coeffcient can be installed from the source code after downloading it from the git repo (https://github.com/vnohhf/extinction_coeffcient/):

python setup.py install

## Using pip
dust_extinction can be installed using pip:

~~~python
# from PyPI
pip install extinction_coeffcient

# from the master trunk on the repository, considered developmental code
pip install git+https://github.com/vnohhf/extinction_coeffcient.git
~~~

# Quick Start 



# API
## extinction_coeffcient(Band,EBV=None,BP_RP=None,Teff=None,mode='func')
Retruns empirical extinction or reddening coefficients, which are single value coefficients obtained
when temperature and extinction are not considered or interpolation results on functions of Teff and 
E(B-V). There also support a (BP-RP) input as a alternative to Teff. This function will interpolate 
R(Teff,E(B-V)) by deriving Teff from an empirical polynomial relationship between (BP-RP)0 and Teff.

Our coefficients are mostly valid in the extinction range of 0-0.5 mag and the temperature range 
of 4000-10000 K. But note that the temperature range varies depending on the band. No extrapolation
for out-of-range input values, but rather assignment of boundary values.

Args:
    Band: str or array-like, shape (n, )
            The passband or color index. If color index are entered, '-' need to be used to connect 
            the two passband name strings (e.g. "BP-RP"). There support GALEX passbands: "FUV", "NUV"; 
            Pan-STARRS 1 passbands: "g", "r", "i", "z", "y"; 
            SDSS passbands: "u'", "g'", "r'", "i'", "z'";
            2MASS passbands: "J", "H", "Ks";
            WISE passbands: "W1", "W2", "W3", "W4";
            Gaia DR3 passbands: "BP", "G", "RP";
            
    EBV: float or array-like, shape (n, ), optional
            The E(B-V), in magnitude.
    
    BP_RP: float or array-like, shape (n, ), optional
            The observed (BP-RP) color index.
    
    Teff: float or array-like, shape (n, ), optional
            The effective temperature, in Kelvins.
            
    mode: {'func', 'simple'} (default: 'func')
        The calculate mode of extinction or reddening coefficients. Possible values:
        'func': interpolation results on functions of Teff and E(B-V).
        'simple': single value coefficients obtained when temperature and extinction are not considered.

Returns: float or array-like, shape (n, )
    Empirical extinction or reddening coefficients. Has the largest shape as the input obj:`Band`, obj:`EBV`, 
    obj:`BP_RP`, or obj:`Teff`.
