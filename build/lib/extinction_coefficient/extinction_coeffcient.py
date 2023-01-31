'''
Author       : Zhang,Ruoyi
Date         : 2023-01-31
Version      : 1.3
E-mail       : zry@mail.bnu.edu.cn
Description  : Copyright© 2023 Zhang,Ruoyi. ALL RIGHTS RESERVED.

'''

def extinction_coefficient(Band,EBV=[],BP_RP=[],Teff=[],mode='func'):
    """
    Retruns empirical extinction or reddening coefficients, which are single value coefficients obtained
    when temperature and extinction are not considered or coefficients for (a group of) specific Teff and
    E(B-V). 
    
    If Teff is unknown in advance, the observed (BP-RP) color can be entered as a substitute. This program
    first makes a rough reddening correction to the observed (BP-RP) and then converts them to Teff using
    an empirical polynomial relationship between intrinsic color (BP-RP)0 and Teff. This allows the exact
    reddening factor to be obtained using Teff, and then the procedure iterates once.
    
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

    """
    
    # import necessary package
    import numpy as np
    import pandas as pd
    
    #* Necessary data of extinction coefficient 
    R_function_coefficients = pd.DataFrame({"FUV": [6.973, 4.68e-10, -1.26e-05, 0.112, 6.520, -10.401, -319.943],
                                            "NUV": [7.293, 2.57e-12, -5.19e-07, 0.0076, -1.022, -3.608, -19.704],
                                            "g"  : [3.248, -8.98e-11, 1.72e-06, -0.0108, -0.556, -0.712, 25.885],
                                            "r"  : [2.363, -5.76e-11, 1.11e-06, -0.00704, -0.273, -0.542, 17.255],
                                            "i"  : [1.791, -3.56e-11, 6.91e-07, -0.00443, -0.417, -0.250, 11.249],
                                            "z"  : [1.398, -3.12e-11, 6e-07, -0.00381, -0.876, 0.253, 9.372],
                                            "y"  : [1.146, -2.67e-11, 5.05e-07, -0.00317, -0.957, 0.407, 7.699],
                                            "J"  : [0.748, -3.99e-12, 7.3e-08, -0.000448, 0.055, -0.176, 1.720],
                                            "H"  : [0.453, 3.85e-13, -9.67e-09, 7.91e-05, -0.366, 0.225, 0.213],
                                            "Ks" : [0.306, 0, 0, 0, 0, 0, 0.306],
                                            "W1" : [0.194, -7.18e-13, 1.11e-08, -5.18e-05, 0.128, -0.038, 0.261],
                                            "W2" : [0.138, 5.4e-12, -9.97e-08, 0.000615, 0.030, 0.062, -1.149],
                                            "W3" : [0.183, 0, 0, 0, 0, 0, 0.183],
                                            "W4" : [0.084, 0, 0, 0, 0, 0, 0.084],
                                            "BP" : [2.998, -1.27e-11, 2.76e-07, -0.00188, -0.673, -0.531, 7.185],
                                            "G"  : [2.364, -1.05e-11, 2.24e-07, -0.00145, -0.681, -0.381, 5.376],
                                            "RP" : [1.737, -7.88e-12, 1.76e-07, -0.00126, -0.630, -0.057, 4.670],
                                            "u'" : [4.500, -1.29e-10, 2.52e-06, -0.0162, 1.741, -2.760, 39.080],
                                            "g'" : [3.452, -9.46e-11, 1.82e-06, -0.0115, 0.221, -1.210, 27.571],
                                            "r'" : [2.400, -5.47e-11, 1.07e-06, -0.00691, -0.080, -0.568, 17.129],
                                            "i'" : [1.799, -3.98e-11, 7.8e-07, -0.00502, -0.675, 0.020, 12.450],
                                            "z'" : [1.299, -3.49e-11, 6.79e-07, -0.00433, -2.027, 1.144, 10.198],
                                            "BP-RP": [1.261, -4.864e-12, 1.006e-07, -6.201e-04, -4.329e-02, -4.741e-01, 2.515],})

    teff_range = pd.DataFrame({"FUV": [7000,10000], "NUV": [4000,9000], "g" : [4000,8000],  "r" : [4000,8000], 
                               "i"  : [4000,8000],  "z"  : [4000,9000], "y" : [4000,8000],  "J" : [4000,8000],
                               "H"  : [4000,8000],  "Ks" : [4000,8000], "W1": [4000,8000],  "W2": [4000,8000],
                               "W3" : [4000,4500],  "W4" : [4000,4500], "BP": [4000,10000], "G" : [4000,10000],
                               "RP" : [4000,9000],  "u'" : [4000,9000], "g'": [4000,8000],  "r'": [4000,8000],
                               "i'" : [4000,8000],  "z'" : [4000,8000], "BP-RP" : [4000,9000]})


    #* Check whether the entered value is valid
    def isnumeric(obj): # check if a variable is a number
        try:
            float(obj)
            return True
        except ValueError or TypeError:
            return False

    def Check_input(inputA,inputB,inputC): 
        # Create a list to store whether the input variables is sequence type
        TypeList = np.array([np.nan, np.nan, np.nan])
        SequenceType = (list, tuple, np.ndarray, pd.Series)
        inputLi = np.array([inputA,inputB,inputC],dtype=object)
        for i,input in enumerate(inputLi):
            if isinstance(input, SequenceType): TypeList[i] = 1
            elif isnumeric(input): TypeList[i] = 2
            elif isinstance(input, str): TypeList[i] = 3
        
        if np.nan in TypeList:
            raise ValueError('Invalid Input')
        
        # if input are sequence, their length needs to be equal.
        sequence_inputs = inputLi[TypeList==1]
        if len(sequence_inputs) > 1:
            for i in range(len(sequence_inputs)-1):
                if not len(sequence_inputs[i]) == len(sequence_inputs[i+1]) :
                    raise ValueError('Input sequences must be the same size')
        
        # Expanding single values into arrays of equal length.
        if len(sequence_inputs) >= 1:
            inputa, inputb, inputc = inputA, inputB, inputC
            if TypeList[0]==3:
                inputa = np.array([inputA for _ in range(len(sequence_inputs[0]))])
            if TypeList[1]==2:
                inputb = np.array([inputB for _ in range(len(sequence_inputs[0]))])
            if TypeList[2]==2:
                inputc = np.array([inputC for _ in range(len(sequence_inputs[0]))])
        else:
            s=True # mark if all inputs are not array
            return np.array([inputA]), np.array([inputB]), np.array([inputC]), s

        return np.array(inputa), np.array(inputb), np.array(inputc), False


    # Determining whether band names is valid
    # if input new color, update this band combination in the dataframe
    def Check_band(band, R_function_coefficients, teff_range): 
        if isinstance(band, str): band = np.array([band])
        for B in band:
            if B not in R_function_coefficients.keys():
                if len(B.split('-')) == 2:
                    B1,B2 = B.split('-')
                    if not {B1,B2}.issubset(set(R_function_coefficients.keys())):
                        raise ValueError('Wrong band name was entered')
                    temp = np.array([teff_range[B1],teff_range[B2]])
                    teff_range[B] = [np.max(temp[:,0]),np.min(temp[:,1])]
                    R_function_coefficients[B] = R_function_coefficients[B1] - R_function_coefficients[B2]
                    if teff_range[B].iloc[0] > teff_range[B].iloc[1]:
                        raise ValueError('The temperature ranges available in the two bands do not overlap')
                else:
                    raise ValueError('Wrong band name was entered')

        return band, R_function_coefficients, teff_range

    #* core function to calculate extinction coefficient
    def extinction_coefficient_core(band,ebv,teff,teff_range,R_function_coefficients):
        # Assignment of boundary values
        lowerLimit,upperLimit = teff_range[band].to_numpy()
        teff[teff < lowerLimit] = lowerLimit[teff < lowerLimit]
        teff[teff > upperLimit] = upperLimit[teff > upperLimit]
        ebv[ebv > 0.5] = 0.5
        
        a,b,c,d,e,f = np.array(R_function_coefficients[band].iloc[1:])
        
        return a * teff**3 + b * teff**2 + c * teff + d * ebv**2 + e * ebv + f 

    #* The main computational steps
    band, R_function_coefficients, teff_range = Check_band(Band, R_function_coefficients, teff_range)
    
    if mode=='simple': # If only ask for single-value R
        
        return [band].iloc[0].to_numpy()
    
    elif mode=='func': # If ask for R(EBV,Teff)
    
        if Teff != []: # calculate R(EBV,Teff)
            
            band,ebv,teff,s = Check_input(Band,EBV,Teff)
                    
        #* If Teff is not input, the input (BP-RP) will be deredden and roughly converted to Teff using a empirical relationship
        elif BP_RP != []: # calculate R(EBV,BPRP0)
            # A fourth-order polynomial is used in advance to fit the (BP-RP)0-Teff relationship, and the resulting coefficients
            Teff_BPRP0_coeff = [1187.26193963, -4925.6478914, 8268.06749031, -9038.59055765,9693.00903561]
            band,ebv,bp_rp,s = Check_input(Band,EBV,BP_RP)
            
            # initial BPRP0
            BPRP0 = bp_rp - R_function_coefficients["BP-RP"].iloc[0] * ebv
            fitTeff = np.polyval(Teff_BPRP0_coeff, BPRP0) 
            
            # iterated BPRP0
            bandnameLi = np.array(["BP-RP" for _ in range(len(ebv))])
            BPRP0 = bp_rp - extinction_coefficient_core(bandnameLi,ebv,fitTeff,teff_range,R_function_coefficients) * ebv
            
            # convert to Teff
            teff = np.polyval(Teff_BPRP0_coeff, BPRP0) 
            
        else: raise ValueError('Missing input value')
        
        # calculate extinction coefficient
        return_value = extinction_coefficient_core(band,ebv,teff,teff_range,R_function_coefficients)
        
        if s: return return_value[0]
        else: return return_value
    
            