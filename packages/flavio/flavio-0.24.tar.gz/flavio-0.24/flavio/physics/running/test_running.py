import unittest
from .running import *
import numpy as np
import flavio

par = {}
par['alpha_s'] = 0.1185
par['alpha_e'] = 1/127.
par['m_Z'] = 91.1876
par['m_b'] = 4.18
par['m_d'] = 4.8e-3
par['m_s'] = 0.095
par['m_t'] = 173.21
par['m_c'] = 1.275
par['m_u'] = 2.3e-3

par_pdg = par.copy()
par_pdg['alpha_s'] = 0.1193
par_pdg['alpha_e'] = 1/127.94
par_pdg['m_Z'] = 91.1876
par_pdg['m_b'] = 4.18

# to compare to RunDec
par_noqed = par.copy()
par_noqed['alpha_e'] = 0.

# to compare to 1107.3100
par_ks = par.copy()
par_ks['m_c'] = 1.329
par_ks['m_b'] = 4.183

class TestRunning(unittest.TestCase):

    def test_runningcouplings(self):
        alpha_b = get_alpha(par_noqed, 4.2)
        # compare to 3-loop alpha_s at 4.2 GeV according to RunDec
        self.assertAlmostEqual(alpha_b['alpha_s']/0.225911,1.,places=4)
        # compare to alpha_em at m_tau as given on p. 4 of
        # http://pdg.lbl.gov/2015/reviews/rpp2014-rev-standard-model.pdf
        alpha_tau = get_alpha(par_pdg, 1.777)
        self.assertAlmostEqual(1/alpha_tau['alpha_e']/133.465,1.,places=2)

    def test_runningmasses(self):
        # compare to RunDec
        np.testing.assert_almost_equal(get_mb(par, 120.)/2.79211, 1,decimal=2)
        np.testing.assert_almost_equal(get_mt(par, 120.)/167.225, 1,decimal=2)
        np.testing.assert_almost_equal(get_mb_pole(par, nl=2)/4.78248, 1,decimal=2)
        np.testing.assert_almost_equal(get_mc_pole(par, nl=2)/1.68375, 1,decimal=2)
        np.testing.assert_almost_equal(get_mb_pole(par, nl=3)/4.92987, 1,decimal=2)
        # compare to 1107.3100
        # KS -> MSbar conversion
        self.assertAlmostEqual(
            flavio.physics.running.masses.mKS2mMS(4.55, 4, get_alpha(par_ks, 4.55)['alpha_s'], Mu=1, nl=2),
            4.20, delta=0.01)
        self.assertAlmostEqual(
            flavio.physics.running.masses.mKS2mMS(1.15, 3, get_alpha(par_ks, 1.15)['alpha_s'], Mu=1, nl=2),
            1.329, delta=0.01)
        # MSbar -> KS conversion
        self.assertAlmostEqual(get_mb_KS(par_ks, 1.), 4.553, delta=0.01)
        self.assertAlmostEqual(get_mc_KS(par_ks, 1.), 1.091, delta=0.07) # this is satisfied poorly!
