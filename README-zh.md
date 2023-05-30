# extinction_coefficient

[English](README.md) | [中文](README-zh.md)

`extinction_coefficient`是一个天文的Python包，提供远紫外到中红外波段的*温度和消光依赖的***经验消光及红化系数**。更多信息见我们的文章[(Zhang & Yuan, 2022)](https://ui.adsabs.harvard.edu/abs/2023ApJS..264...14Z/abstract)。

对一个给定的对于一个给定的波段 *a* ，消光系数被定义为 E(a)/E(B-V)，即 *a* 波段的消光与 *B-V* 色余之比；  
类似地，对于一个给定的颜色 *a-b* ，红化系数被定义为 E(a-b)/E(B-V)。
本软件包中的 E(B-V )是直接取自SFD全天二维尘埃红化图 [Schlegel et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...500..525S/abstract)。

Our coefficients are mostly valid in the extinction range of 0-0.5 mag and the temperature range 
of 4000-10000 K. But note that the temperature range varies depending on the band. No extrapolation
for out-of-range input values, but rather assignment of boundary values. The valid range for each 
color is listed in Table 4 of [Zhang & Yuan (2022)](https://ui.adsabs.harvard.edu/abs/2023ApJS..264...14Z/abstract).

### Available photometric surveys and passband names
- GALEX passbands: "FUV", "NUV"; 
- Pan-STARRS 1 passbands: "g", "r", "i", "z", "y"; 
- SDSS passbands: "u'", "g'", "r'", "i'", "z'";
- Gaia DR3 passbands: "BP", "G", "RP";
- 2MASS passbands: "J", "H", "Ks";
- WISE passbands: "W1", "W2", "W3", "W4".

# How to Install
### Using pip
~~~python
# from PyPI (recommmand)
pip install extinction_coefficient

# from the master trunk on the repository, considered developmental code
pip install git+https://github.com/vnohhf/extinction_coeffcient.git
~~~

### From source
extinction_coefficient can be installed from the source code after downloading it from the git repo (https://github.com/vnohhf/extinction_coeffcient/):
~~~
python setup.py install
~~~

# Quick Start 
To get a single value extinction or reddening coefficients obtained when temperature and extinction are not considered, just put mode = 'simple':
~~~python
from extinction_coefficient import extinction_coefficient
extinction_coefficient('g', mode='simple')
extinction_coefficient('BP-RP', mode='simple')
extinction_coefficient(["BP-RP","FUV-g"], mode='simple')
~~~

To obtain extinction or reddening coefficients for (a group of) specific Teff and E(B-V):
~~~python
Band = 'BP'
EBV  = 0.3
Teff = [5000, 6000]
extinction_coefficient(Band,EBV=EBV,Teff=Teff)
~~~
~~~python
Band = np.array(["BP-RP","FUV-g","y-H","u'-W2"])
EBV  = [0.1, 0.1, 0.3, 0.5]
Teff = 5500
extinction_coefficient(Band,EBV=EBV,Teff=Teff)
~~~

If Teff is unknown in advance, the observed (BP-RP) color can be entered as a substitute. This program first makes a rough reddening correction to the observed (BP-RP) and then converts them to Teff using an empirical polynomial relationship between intrinsic color (BP-RP)0 and Teff. This allows the exact reddening factor to be obtained using Teff, and then the procedure iterates once.
~~~python
Band = ["BP-RP","FUV-g","i'-z'"]
EBV  = [0.1, 0.3, 0.5]
BP_RP = np.array([0.3, 0.6, 1.2])
extinction_coefficient(Band,EBV=EBV,BP_RP=BP_RP)
~~~

# API
~~~
extinction_coefficient(Band,EBV=None,BP_RP=None,Teff=None,mode='func')

Args:
    Band: str or array-like, shape (n, )
            The passband or color index. If color index are entered, '-' need to be used to connect 
            the two passband name strings (e.g. "BP-RP"). There support GALEX passbands: "FUV", "NUV"; 
            Pan-STARRS 1 passbands: "g", "r", "i", "z", "y"; 
            SDSS passbands: "u'", "g'", "r'", "i'", "z'";
            Gaia DR3 passbands: "BP", "G", "RP";
            2MASS passbands: "J", "H", "Ks";
            WISE passbands: "W1", "W2", "W3", "W4";
            
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
~~~
