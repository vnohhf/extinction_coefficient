# extinction_coefficient

[English](README.md) | [中文](README-zh.md)

`extinction_coefficient`是一个天文的Python包，提供远紫外到中红外波段的 *温度和消光依赖的* **经验消光及红化系数**。更多信息见我们的文章[(Zhang & Yuan, 2022)](https://ui.adsabs.harvard.edu/abs/2023ApJS..264...14Z/abstract)。

对一个给定的对于一个给定的波段 *a* ，消光系数被定义为 E(a)/E(B-V)，即 *a* 波段的消光与 *B-V* 色余之比；  
类似地，对于一个给定的颜色 *a-b* ，红化系数被定义为 E(a-b)/E(B-V)。
本软件包中的 E(B-V) 是直接取自SFD全天二维尘埃红化图 [Schlegel et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...500..525S/abstract)。

我们的系数在 0 - 0.5 mag 的消光范围和 4000 - 10000 K 的温度范围内大多有效，但具体温度范围因波段而异（见文章中表4）。
对于超出范围的输入值，我们没有对函数进行外推，而是分配边界值。

### 可用的测光巡天项目和波段名称
*Note*: 代码中使用的波段名称需要与表格一致。SDSS的波段名称中含有`'`。
|  测光巡天        | 波段                |
|  :--:           | :--:               |
|  GALEX          | FUV, NUV           |
|  Pan-STARRS 1   | g, r, i, z, y      |
|  SDSS           | u', g', r', i', z' |
|  Gaia           | BP, G, RP          |
|  2MASS          | J, H, Ks           |
|  WISE           | W1, W2, W3, W4     |

# 如何安装
### 使用 pip
~~~
# 从 PyPI (推荐)
pip install extinction_coefficient

# 从本 github 库
pip install git+https://github.com/vnohhf/extinction_coeffcient.git
~~~

### 从源代码
从 git repo 中下载 extinction_coefficient 后，可以从源代码中安装
(https://github.com/vnohhf/extinction_coeffcient/):
~~~
python setup.py install
~~~

# 轻松使用 
要获得不考虑温度和消光依赖的情况下的**单值**消光或红化系数，只需令 mode = 'simple':
~~~python
from extinction_coefficient import extinction_coefficient
extinction_coefficient('g', mode='simple')
extinction_coefficient('BP-RP', mode='simple')
extinction_coefficient(["BP-RP","FUV-g"], mode='simple')
~~~

获得某个/一组 Teff 和 E(B-V) 时的消光或红化系数:  
（如果Teff 和 E(B-V) 的输入均使用数组，那么他们的长度应该保持一致）
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

若事先不知道Teff，可以输入 *BP-RP* 颜色的观测值作为替代。本程序会首先对观测颜色 *BP-RP* 进行粗略的红化修正，然后使用内禀颜色 *(BP-RP)0* 和 Teff 之间的经验多项式关系将它们转换为 Teff 。迭代一次后再用于求解准确的红化系数。
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
