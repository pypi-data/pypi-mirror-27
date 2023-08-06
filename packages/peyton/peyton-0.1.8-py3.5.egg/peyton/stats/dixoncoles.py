from scipy.stats import poisson


class dixoncoles(object):
    """
    Implements a Dixon-Coles distribution

    See http://www.math.ku.dk/~rolf/teaching/thesis/DixonColes.pdf - p270
    """

    @staticmethod
    def tau(k1, k2, mu1, mu2, rho=0.0):
        """
        The perturbing function used in Dixon-Coles joint distribution. Shifts weight between scores in the
        0-0, 1-0, 0-1, 1.1 grid to account for bias in the independent Poisson model.

        Parameters
        -----------
        k1 - int
            Value of home goals (non-negative integer)

        k2 - int
            Value of away goals (non-negative integer)

        mu1 - float
            Lambda rate parameter for home goals

        mu2 - float
            Lambda rate parameter for away goals

        rho - float
            Shifting parameter. For 0.0, collapses to independent Poisson model

        Returns
        --------
        tau - float
            Tau parameter 
        """
        if k1 == k2 == 0:
            return 1.0 - mu1*mu2*rho
        elif k1 == 0 and k2 == 1:
            return 1.0 + mu1*rho
        elif k1 == 1 and k2 == 0:
            return 1.0 + mu2*rho
        elif k1 == k2 == 1:
            return 1.0 - rho
        else:
            return 1.0

    @staticmethod
    def pmf(k1, k2, mu1, mu2, loc1=0, loc2=0, rho=0.0):
        """
        The probability mass function of the Dixon-Coles distribution

        Parameters
        -----------
        k1 - int
            Value of home goals (non-negative integer)

        k2 - int
            Value of away goals (non-negative integer)

        mu1 - float
            Lambda rate parameter for home goals

        mu2 - float
            Lambda rate parameter for away goals

        loc1 - float
            Shifting parameter for the home goals distribution (default 0)

        loc2 - float
            Shifting parameter for the away goals distribution (default 0)

        rho - float
            Shifting parameter. For 0.0, collapses to independent Poisson model

        Returns
        --------
        tau - float
            Tau parameter 
        """

        return dixoncoles.tau(k1, k2, mu1, mu2, rho) * poisson.pmf(k=k1, mu=mu1, loc=loc1) * poisson.pmf(k=k2, mu=mu2, loc=loc2)

    @staticmethod
    def logpmf(k1, k2, mu1, mu2, loc1=0, loc2=0, rho=0.0):
        """
        The log probability mass function of the Dixon-Coles distribution

        Parameters
        -----------
        k1 - int
            Value of home goals (non-negative integer)

        k2 - int
            Value of away goals (non-negative integer)

        mu1 - float
            Lambda rate parameter for home goals

        mu2 - float
            Lambda rate parameter for away goals

        loc1 - float
            Shifting parameter for the home goals distribution (default 0)

        loc2 - float
            Shifting parameter for the away goals distribution (default 0)

        rho - float
            Shifting parameter. For 0.0, collapses to independent Poisson model

        Returns
        --------
        tau - float
            Tau parameter 
        """

        return np.log(dixoncoles.tau(k1, k2, mu1, mu2, rho)) + poisson.logpmf(k=k1, mu=mu1, loc=loc1) + poisson.logpmf(k=k2, mu=mu2, loc=loc2)
