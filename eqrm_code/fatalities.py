
from scipy.stats import norm
from scipy import zeros, nonzero, logical_and, log, array

def forecast_fatality(MMI, population, beta=0.17, theta=14.05):
    """
    Forecast fatalities from MMI values and population
    formula taken from USGS Open-File-Report 2009-1136
    default value for beta and theta is for Indonesia
    """
    MMI = array(MMI)
    fatality_rate = zeros(MMI.shape)
    ind = nonzero(MMI<5)
    fatality_rate[ind] = 0
    
    ind = nonzero(logical_and(MMI>=5,MMI<=10))
    fatality_rate[ind] = norm.cdf(1.0/beta*log(MMI[ind]/theta))
    
    ind = nonzero(MMI>10)
    fatality_rate[ind] = norm.cdf(1.0/beta*log(10/theta))
    
    fatality = fatality_rate*population
    
    return fatality
