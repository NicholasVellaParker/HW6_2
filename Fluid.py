#region class definitions
class Fluid():
    #region constructor
    def __init__(self, mu=0.0000205, rho=1.93):
        '''
        default properties are for water
        :param mu: dynamic viscosity in psi*s -> (lbf*s)/ft^2
        :param rho: density in slug/ft^3
        '''
        #region attributes
        self.mu= mu# $JES MISSING CODE$  # simply make a copy of the value in the argument as a class property
        self.rho= rho # $JES MISSING CODE$  # simply make a copy of the value in the argument as a class property
        self.nu= mu/rho #JES MISSING CODE$ # calculate the kinematic viscosity in units of ft^2/s
        #endregion
    #endregion
#endregion
