#!/usr/bin/env python

"""Test the bridge-damage function.

Sources of test data:

Ken's recent paper: 'Modelling Bridge Damage Due to Earthquake Ground Motions'
FEMA paper:         'HAZUS-MH MR4 Technical Manual'
Ken's spreadsheet:  'Bridge Fragility Toro - 1 in 5000.xls'
"""


import unittest
import bridge_damage as bd
import numpy as np

import eqrm_code.damage_model as dm
import eqrm_code.bridges as bridges



class DataObj(object):
    """
    A data object class.

    Used: obj = DataObj(lon=100.2, lat=-25.3, id=1)
          print obj.lon

    The idea is to create an object with attributes with the
    names of the keyword args on the creation call.
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            msg = 'DataObj() must be called with keyword args ONLY!'
            raise RuntimeError(msg)

        self.__dict__ = kwargs



class TestBridgeDamage(unittest.TestCase):

    """Class to test the 'linear' model damage functions."""

    ######
    # preload bridge damage data from external files
    ######

    def setUp(self):
        bd.load_bridge_data()

    ######
    # test case to ensure bad class string is handled OK
    ######

    def test_bad_CLASS(self):
        """Check that a bad CLASS string gives RuntimeError."""

        CLASS = 'bad'
        sa_1_0 = np.array([0.125, 0.444])
        sa_0_3 = np.array([0.25, 1.655])
        skew = 40
        num_spans = 4
        model = 'LINEAR'
        self.failUnlessRaises(RuntimeError, bd.bridge_states_ModelLinear,
                              model, CLASS, sa_0_3, sa_1_0, skew, num_spans)

    ######
    # test case to ensure bad model string is handled OK
    ######

    def test_bad_model(self):
        CLASS = 'HWB17'
        sa_1_0 = np.array([0.125, 0.444])
        sa_0_3 = np.array([0.25, 1.655])
        skew = 0
        num_spans = 2
        model = 'BAD_MODEL'
        self.failUnlessRaises(RuntimeError, bd.bridge_states,
                              model, CLASS, sa_0_3, sa_1_0, skew, num_spans)

    ######
    # test cases compared with published examples
    ######

    def test_Ken_paper(self):
        # case from Ken's recent paper
        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[1.655]])
        skew = 0
        num_spans = 2
        model = 'LINEAR'
        expected = np.array([[[0.32, 0.16, 0.22, 0.13]]])

        # first, call function using model string
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans,
                                  model=model)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=2.0e-2), msg)

        # second, call function using default model
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=2.0e-2), msg)

        # finally, call lower-level function direct
        result = bd.bridge_states_ModelLinear(model, CLASS, sa_0_3, sa_1_0,
                                              skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=2.0e-2), msg)

    def test_FEMA(self):
        # case from FEMA paper, chapter 7
        # NOTE: this example seems to calculate modified spectral acceleration
        # values (soil, etc) and THEN USES THE ORIGINAL SA VALUES!?
        # Anyway, if I do the above, their figures match our calculations?
        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.43]])
        sa_0_3 = np.array([[2.1]])
        skew = 32
        num_spans = 3
        expected = np.array([[[0.20, 0.16, 0.26, 0.20]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-2), msg)

    def test_Ken_0631A(self):
        # case 0631A from Ken's spreadsheet
        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.7610]])
        sa_0_3 = np.array([[1.0]])        # doesn't matter, Ishape==0
        skew = 20
        num_spans = 6
        expected = np.array([[[0.07115, 0.09580, 0.25756, 0.54371]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-4), msg)

    def test_Ken_1046(self):
        # case 1046 from Ken's spreadsheet
        CLASS = 'HWB22'
        sa_1_0 = np.array([[0.6963]])
        sa_0_3 = np.array([[1.5221]])     # back-calculated from Sa 1.0 & Kshape
        skew = 4
        num_spans = 2
        expected = np.array([[[0.261532, 0.093043, 0.092339, 0.062811]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-3), msg)

    def test_Ken_1469(self):
        # case 1469 from Ken's spreadsheet
        CLASS = 'HWB3'
        sa_1_0 = np.array([[0.7610]])
        sa_0_3 = np.array([[1.654693]])   # back-calculated from Sa 1.0 & Kshape
        skew = 0
        num_spans = 1
        expected = np.array([[[0.17196, 0.075055, 0.085537, 0.043495]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-3), msg)

    def test_Ken_1466(self):
        # case 1466 from Ken's spreadsheet
        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.7610]])
        sa_0_3 = np.array([[1.0]])        # doesn't matter, Ishape==0
        skew = 0
        num_spans = 1
        expected = np.array([[[0.14633, 0.12911, 0.28476, 0.40802]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-3), msg)

    def test_Ken_1153(self):
        # case 1153 from Ken's spreadsheet
        CLASS = 'HWB10'
        sa_1_0 = np.array([[0.4351]])
        sa_0_3 = np.array([[0.951]])      # back-calculated from Sa 1.0 & Kshape
        skew = 12
        num_spans = 3
        expected = np.array([[[0.137936, 0.041399, 0.031169, 0.013268698]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-3), msg)

    def test_Ken_0361(self):
        # case 0361 from Ken's spreadsheet, assume EQ1 and Ishape==0
        CLASS = 'HWB28'
        sa_1_0 = np.array([[0.7610]])
        sa_0_3 = np.array([[1.0]])        # doesn't matter, Ishape==0
        skew = 0
        num_spans = 3
        expected = np.array([[[0.209448, 0.087666, 0.107411, 0.062283]]])

        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-3), msg)

    ######
    # test cases generated in bridge_test_spreadsheet.xls
    ######

    def test_HWB1(self):
        CLASS = 'HWB1'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.0226067278361395, 0.00305901076489201,
                               0.000466402653954534, 0.000125420916749441]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-2), msg)

        CLASS = 'HWB1'
        sa_1_0 = np.array([[0.3]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.199779032280055, 0.0764151557561195,
                               0.0247604596230755, 0.0148658562671364]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB1'
        sa_1_0 = np.array([[0.4]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 4
        expected = np.array([[[0.150281401318974, 0.177672069453813,
                               0.0858753785967035, 0.086171150630509]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB1'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 6
        expected = np.array([[[0.062688221772304, 0.220505529642397,
                               0.141827149439272, 0.220009655476609]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB2(self):
        CLASS = 'HWB2'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.000554759070666988,
                               0.00000660062667900974, 0.00000171303801194123,
                               0.000000040674200008084]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB2'
        sa_1_0 = np.array([[0.25]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.065606542703304, 0.00415650478592905,
                               0.00225376037820901, 0.000201308582581938]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB2'
        sa_1_0 = np.array([[0.55]])
        sa_0_3 = np.array([[01.1]])
        skew = 0
        num_spans = 4
        expected = np.array([[[0.272201835045366, 0.071079158152995,
                               0.076799167644141, 0.0220131613807735]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB2'
        sa_1_0 = np.array([[0.8]])
        sa_0_3 = np.array([[01.6]])
        skew = 30
        num_spans = 5
        expected = np.array([[[0.25433759847428, 0.125497254506874,
                               0.196382173622389, 0.10796246947007]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB3(self):
        CLASS = 'HWB3'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 45
        num_spans = 1
        expected = np.array([[[0.0000700072089775405, 0.00013538873612351,
                               0.0000538680341489739, 0.00000463449519000347]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-2), msg)

        CLASS = 'HWB3'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 30
        num_spans = 2
        expected = np.array([[[0.000257395958851048, 0.0000049524840500248,
                               0.0000014720250819944,
                               0.0000000780064569605443]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB3'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 15
        num_spans = 3
        expected = np.array([[[0.000123888210153578, 0.000098786260276984,
                               0.0000380878808785012, 0.00000313612313096456]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB3'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 4
        expected = np.array([[[0.000252783390140066, 0.00000837200173098296,
                               0.0000025955124730026,
                               0.000000147570095976324]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB4(self):
        CLASS = 'HWB4'
        sa_1_0 = np.array([[0.25]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 4
        expected = np.array([[[0.000346527491546067, 0.00577536813580498,
                               0.00363303330841502, 0.000666333662943941]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=7.0e-2), msg)

        CLASS = 'HWB4'
        sa_1_0 = np.array([[0.25]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 3
        expected = np.array([[[0.00380968885199001, 0.00390830747617804,
                               0.00231578466350552, 0.000387481607036444]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB4'
        sa_1_0 = np.array([[0.25]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 2
        expected = np.array([[[0.00522600577715954, 0.0031207929285445,
                               0.00179044992294003, 0.000284013970065944]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB4'
        sa_1_0 = np.array([[0.25]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 1
        expected = np.array([[[0.00643303293246755, 0.00243559627336398,
                               0.00135132481029654, 0.000201308582581938]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB5(self):
        CLASS = 'HWB5'
        sa_1_0 = np.array([[0.165]])
        sa_0_3 = np.array([[0.5]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.192077279264365, 0.0315890148576205,
                               0.0177845070174765, 0.00271506826627649]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB5'
        sa_1_0 = np.array([[0.165]])
        sa_0_3 = np.array([[0.5]])
        skew = 0
        num_spans = 2
        expected = np.array([[[0.192077279264365, 0.0315890148576205,
                               0.0177845070174765, 0.00271506826627649]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB5'
        sa_1_0 = np.array([[0.165]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 1
        expected = np.array([[[0.177968245376908, 0.0390669687564825,
                               0.023225196677269, 0.00390545859507846]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB5'
        sa_1_0 = np.array([[0.165]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 2
        expected = np.array([[[0.177968245376908, 0.0390669687564825,
                               0.023225196677269, 0.00390545859507846]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB6(self):
        CLASS = 'HWB6'
        sa_1_0 = np.array([[0.35]])
        sa_0_3 = np.array([[01]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.431310476564271, 0.0659153325097525,
                               0.07773018238093, 0.026603939027761]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB6'
        sa_1_0 = np.array([[0.4]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 1
        expected = np.array([[[0.439569646434213, 0.0848891250130694,
                               0.112419154730197, 0.0473015698961335]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB6'
        sa_1_0 = np.array([[0.45]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 1
        expected = np.array([[[0.415821819797592, 0.102311725891719,
                               0.152651683613235, 0.0796925697387565]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB6'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01]])
        skew = 40
        num_spans = 1
        expected = np.array([[[0.36229520645097, 0.115491247830133,
                               0.195680641028677, 0.12924724856131]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB7(self):
        CLASS = 'HWB7'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 1
        expected = np.array([[[0.326183205744067, 0.18891640321782,
                               0.161393378068422, 0.0739848120109929]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB7'
        sa_1_0 = np.array([[0.7]])
        sa_0_3 = np.array([[01.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.330052835175742, 0.179470435730569,
                               0.143331401630736, 0.059897465212959]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB7'
        sa_1_0 = np.array([[0.6]])
        sa_0_3 = np.array([[01.5]])
        skew = 15
        num_spans = 4
        expected = np.array([[[0.339870813054322, 0.147032790984779,
                               0.0996616913135815, 0.0328920587888865]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB7'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 0
        num_spans = 7
        expected = np.array([[[0.302714343871091, 0.113751688584847,
                               0.0659828999656645, 0.017551067578398]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB8(self):
        CLASS = 'HWB8'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.336710325793568, 0.119670951477157,
                               0.160956042981945, 0.106396488960342]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB8'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.244276754670342, 0.119056000820545,
                               0.159309180345029, 0.104334121408691]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB8'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.153297085195215, 0.0773765278544625,
                               0.07999255314419, 0.0333095597571875]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB8'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.0227024419323315, 0.0117430206432225,
                               0.00735353643235098, 0.00133319821870198]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB9(self):
        CLASS = 'HWB9'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 0
        num_spans = 4
        expected = np.array([[[0.328706942812843, 0.178546020434008,
                               0.062396001389144, 0.0753815916945875]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB9'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 0
        num_spans = 3
        expected = np.array([[[0.231831318679924, 0.0555565731074785,
                               0.0120384306694525, 0.00839132462482295]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB9'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 2
        expected = np.array([[[0.00229205641090752, 0.0000532860369100163,
                               0.00000315502378800403,
                               0.000000724202709467825]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB9'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 30
        num_spans = 1
        expected = np.array([[[0.000554094714926512, 0.00000854355378449023,
                               0.000000397730552492703,
                               0.0000000774102944522959]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB10(self):
        CLASS = 'HWB10'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.425419008850471, 0.0367353150095365,
                               0.0269462443656945, 0.010899431774298]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB10'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.176522919666644, 0.036076249168107,
                               0.026344451960731, 0.010578580163215]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB10'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.0123828393697725, 0.0121114740002715,
                               0.00705087759281853, 0.00197475024252647]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB10'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.000723215073467509, 0.000481699681355974,
                               0.00017914683550696, 0.0000254210423650258]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB11(self):
        CLASS = 'HWB11'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 0
        num_spans = 4
        expected = np.array([[[-0.0668014125590425, 0.107858528198849,
                               0.116600594806922, 0.0918644905119685]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB11'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 0
        num_spans = 3
        expected = np.array([[[0.0122032221693135, 0.037317984059287,
                               0.0274812536275105, 0.0111870907149564]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB11'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 2
        expected = np.array([[[0.00602397313671799, 0.0000434094816600394,
                               0.0000125131268129963, 0.00000124265493445241]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB11'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 30
        num_spans = 1
        expected = np.array([[[0.000116402222118006, 0.0000071281308674509,
                               0.00000175264668950126,
                               0.000000137917074483074]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB12(self):
        CLASS = 'HWB12'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.197412515706753, 0.16057880143149,
                               0.273438056472016, 0.244609849639399]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB12'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.219916234889833, 0.165746943524793,
                               0.248079082819341, 0.177878179860242]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB12'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.201619078934544, 0.142133860243051,
                               0.153699836578046, 0.0654732336863845]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB12'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.062534105247658, 0.0365171370564325,
                               0.021425008239778, 0.00348452620647294]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB13(self):
        CLASS = 'HWB13'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.116759898312611, 0.0905227464381905,
                               0.254751838850059, 0.474628595593084]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB13'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.30337872737527, 0.115442207584209,
                               0.1954695856772, 0.12894951764617]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB13'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.0431430703956895, 0.00252570383523198,
                               0.00148409798270949, 0.000148697682502474]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB13'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.0168205843811605, 0.000641554658023513,
                               0.000312680893656492, 0.0000227928269189714]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB14(self):
        CLASS = 'HWB14'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.373415208357384, 0.0794225850525125,
                               0.0389311577305945, 0.00823104885950848]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB14'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.308366770170129, 0.056231760521429,
                               0.0241298111556609, 0.00426375583218003]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB14'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.127711898755744, 0.0231765664446985,
                               0.00756182774910952, 0.000926971872932447]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB14'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.00909424791896907, 0.0011235386710185,
                               0.000193301456511474, 0.0000101745522109731]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB15(self):
        CLASS = 'HWB15'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[-0.250950502409458, 0, 0.250423879887798,
                               0.355496066191077]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB15'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[-0.0697547158024719, 0,
                               0.139266922133295, 0.077822704953647]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB15'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.0131254216066475, 0,
                               0.000600626492281986, 0.0000591821728454511]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB15'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.000288205794277963, 0,
                               0.0000964161792224583, 0.00000684713544502058]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB16(self):
        CLASS = 'HWB16'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.174941209809168, 0.0367353150095365,
                               0.0269462443656945, 0.010899431774298]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB16'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.0411663779432355, 0.02471126194828,
                               0.0165399123728119, 0.00577199830674002]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB16'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[-0.011347753784602, 0.0101898036215705,
                               0.00571470383091999, 0.00152438473223698]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB16'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[-0.000469346847316032, 0.000420685793241504,
                               0.000152766141724991, 0.0000213158290989779]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB17(self):
        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.0434824802069249, 0.0799841750577186,
                               0.236549375430427, 0.60646402809954]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.205454135208941, 0.164797722130269,
                               0.258937487451865, 0.201633652662689]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.0739821826113545, 0.00796464711051303,
                               0.00325529578004452, 0.000303962625467447]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.032972284716354, 0.00234071502327599,
                               0.000766979926793532, 0.0000509004738994401]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB18(self):
        CLASS = 'HWB18'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.442995437308532, 0.106138854043849,
                               0.163337069296872, 0.090242983221838]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB18'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.441771659926242, 0.0918720405069585,
                               0.127271730751203, 0.0580691138933175]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB18'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.30054481008745, 0.057142307833487,
                               0.064322533401655, 0.0200836709006835]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB18'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.0590673208368785, 0.00737879730640545,
                               0.00508909080759806, 0.00068290749914196]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB19(self):
        CLASS = 'HWB19'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.231302742273763, 0.204359748272209,
                               0.201241353836096, 0.113573954659235]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB19'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.276460404723582, 0.088941203871352,
                               0.045781503551595, 0.0103433713220429]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB19'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.00568755491284501, 0.000116527807583477,
                               0.0000140838764144946,
                               0.000000464983279990783]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB19'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.00155420227960001, 0.0000181762237285166,
                               0.00000171303801194123,
                               0.000000040674200008084]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB20(self):
        CLASS = 'HWB20'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.336710325793568, 0.119670951477157,
                               0.160956042981945, 0.106396488960342]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB20'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.244276754670342, 0.119056000820545,
                               0.159309180345029, 0.104334121408691]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB20'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.153297085195215, 0.0773765278544625,
                               0.07999255314419, 0.0333095597571875]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB20'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.0227024419323315, 0.0117430206432225,
                               0.00735353643235098, 0.00133319821870198]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB21(self):
        CLASS = 'HWB21'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.220181888061553, 0.213531431709565,
                    0.085903411836385, 0.12541382472308]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB21'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.213123388813974, 0.067563602995356,
                    0.015564034829525, 0.0115666204428225]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB21'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.00231012950055554, 0.0000365617925455197,
                    0.00000207205314700643, 0.000000458328066943459]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB21'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.000557899428087483, 0.00000495623955798497,
                    0.000000217700175497715, 0.0000000400417369816886]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB22(self):
        CLASS = 'HWB22'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.425419008850471, 0.0367353150095365,
                               0.0269462443656945, 0.010899431774298]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB22'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.176522919666644, 0.036076249168107,
                               0.026344451960731, 0.010578580163215]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB22'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.0123828393697725, 0.0121114740002715,
                               0.00705087759281853, 0.00197475024252647]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB22'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.000723215073467509, 0.000481699681355974,
                               0.00017914683550696, 0.0000254210423650258]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB23(self):
        CLASS = 'HWB23'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[-0.175326467310333, 0.12445166029053,
                               0.151427018041691, 0.14896998993681]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB23'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[-0.00650470769663597, 0.044827260919497,
                               0.0346251018948745, 0.015241895453332]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-2), msg)

        CLASS = 'HWB23'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.006042046226366, 0.0000298996903435045,
                               0.00000840411192348789,
                               0.000000788371492477236]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB23'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.000120206935278977, 0.00000416251494900211,
                               0.000000979227089026313,
                               0.0000000722394324359499]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB24(self):
        CLASS = 'HWB24'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.257120688271313, 0.165078597634955,
                               0.256554281214481, 0.197285656128909]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB24'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.282871699650173, 0.164789798150821,
                               0.224618547063916, 0.139340396229299]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB24'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.233404437366949, 0.134583457709386,
                               0.139765918869943, 0.055172195495747]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB24'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.0692601069236095, 0.0330561896754215,
                               0.018721532527, 0.00292294762431045]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB25(self):
        CLASS = 'HWB25'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.132381813523088, 0.0944275209563564,
                               0.258814679003244, 0.451039065711256]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB25'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.337139661822335, 0.111581018938995,
                               0.182569491683299, 0.111949865838221]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB25'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.044736358246255, 0.0016066659161515,
                               0.00087974601350449, 0.0000787997202224555]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB25'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.0172344993502015, 0.000378383655817494,
                               0.000173402631678476, 0.0000113271220619771]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB26(self):
        CLASS = 'HWB26'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.149333681735332, 0,
                               0.133611932043633, 0.0720238298904525]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB26'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[-0.0172450575979909, 0,
                               0.111428074159181, 0.0531518947232795]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=1.0e-2), msg)

        CLASS = 'HWB26'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[-0.0402917013150355, 0,
                               0.041717596106548, 0.0123593354802625]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB26'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[-0.0021181249088465, 0,
                               0.00222259252316248, 0.000287001494629457]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB27(self):
        CLASS = 'HWB27'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[-0.242765025239021, 0,
                               0.24958558897048, 0.348148879937958]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB27'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 30
        num_spans = 3
        expected = np.array([[[-0.061942749184368, 0,
                               0.135292848457845, 0.0739848120109929]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB27'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 15
        num_spans = 2
        expected = np.array([[[0.013210790913014, 0,
                               0.000524420731571995, 0.0000500186271889524]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB27'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 0
        num_spans = 1
        expected = np.array([[[0.00031531146410646, 0,
                               0.0000713686694265303, 0.00000478897541245082]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_HWB28(self):
        CLASS = 'HWB28'
        sa_1_0 = np.array([[0.5]])
        sa_0_3 = np.array([[01.5]])
        skew = 10
        num_spans = 1
        expected = np.array([[[0.151740329021806, 0.0304537508144065,
                               0.0262491872181935, 0.00823104885950848]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB28'
        sa_1_0 = np.array([[0.425]])
        sa_0_3 = np.array([[01]])
        skew = 20
        num_spans = 2
        expected = np.array([[[0.105678152024632, 0.020204900746228,
                               0.0158887313490904, 0.00426375583218003]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB28'
        sa_1_0 = np.array([[0.275]])
        sa_0_3 = np.array([[0.5]])
        skew = 30
        num_spans = 3
        expected = np.array([[[0.024652537757816, 0.00728100594648901,
                               0.00475275377386353, 0.000926971872932447]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB28'
        sa_1_0 = np.array([[0.125]])
        sa_0_3 = np.array([[0.25]])
        skew = 40
        num_spans = 4
        expected = np.array([[[0.000620175724826533, 0.000250145791963474,
                               0.00010589581171, 0.0000101745522109731]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_array_sequential(self):
        """Initial part of 'array' test.

        Take a copy of test_HWB17() above, make all bridge parameters
        the same and pervert 'expected' to make this test pass.

        Then collapse the four sequential tests into one in test_array_array()
        below.
        """

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.75]])
        sa_0_3 = np.array([[01.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.0434824802069249, 0.0799841750577186,
                               0.236549375430427, 0.60646402809954]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.444]])
        sa_0_3 = np.array([[01]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.1212962, 0.1565718, 0.27978019, 0.273137]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.11]])
        sa_0_3 = np.array([[0.5]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.047551, 0.02388763, 0.01246965, 0.00170067]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.085]])
        sa_0_3 = np.array([[0.25]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.02230382, 0.00941589, 0.00397589, 0.00039163]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)

    def test_array_array(self):
        """Do test_array_sequential() above as one call to bridge_states().

        This test just ensures that the results in test_array_sequential() are 
        repeated if we do them all at once.
        """

        CLASS = 'HWB17'
        sa_1_0 = np.array([[0.75, 0.444, 0.11, 0.085]])
        sa_0_3 = np.array([[01.5, 01, 0.5, 0.25]])
        skew = 45
        num_spans = 4
        expected = np.array([[[0.0434824802069249, 0.0799841750577186,
                               0.236549375430427, 0.60646402809954],
                              [0.1212962, 0.1565718, 0.27978019, 0.273137],
                              [0.047551, 0.02388763, 0.01246965, 0.00170067],
                              [0.02230382, 0.00941589, 0.00397589, 0.00039163]]])
        result = bd.bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans)
        msg = ('\nexpected=\n%s\nresult=\n%s' % (str(expected), str(result)))
        self.failUnless(np.allclose(expected, result, rtol=5.0e-3), msg)


    def test_choose_random_state(self):
        """Test the choose_random_state() function."""

        # check that the state change values are as expected
        # that is, around the 0.2, 0.4, etc places
        states = np.array([[0.2, 0.2, 0.2, 0.2]])

        rand_value = 0.0
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 0)
        
        rand_value = 0.1999
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 0)
        
        rand_value = 0.2001
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 1)
        
        rand_value = 0.3999
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 1)
        
        rand_value = 0.4001
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 2)
        
        rand_value = 0.5999
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 2)
        
        rand_value = 0.6001
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 3)
        
        rand_value = 0.7999
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 3)
        
        rand_value = 0.8001
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 4)
        
        rand_value = 0.9999
        state = bd.choose_random_state(states, rand_value)
        self.failUnless(state[0] == 4)

        # now try tuples that are one state only, any random gets that state
        states = np.array([[0.0, 0.0, 0.0, 0.0],	# none
                           [1.0, 0.0, 0.0, 0.0],	# slight
                           [0.0, 1.0, 0.0, 0.0],	# moderate
                           [0.0, 0.0, 1.0, 0.0],	# extensive
                           [0.0, 0.0, 0.0, 1.0],	# complete
                          ])
        expected_states = np.array([0, 1, 2, 3, 4])
 
        result_states = bd.choose_random_state(states)
        msg = ('expected_states=%s\nresult_states=%s'
               % (str(expected_states), str(result_states)))
        self.failUnless(np.alltrue(result_states == expected_states), msg)
        
    def test_interpret_damage_state(self):
        """Test the interpret_damage_state() function."""

        states = (0, 1, 2, 3, 4)
        expected = {0: 'none',
                    1: 'slight',
                    2: 'moderate',
                    3: 'extensive',
                    4: 'complete'}

        for s in states:
            result_str = bd.interpret_damage_state(s)
            expected_str = expected[s]
            msg = 'result_str=%s, expected_str=%s' % (result_str, expected_str)
            self.failUnless(result_str == expected_str, msg)


    def test_calc_total_loss(self):
        """Test calling calc_total_loss() directly with bridge data.

        Use raw data from test_array_array().
        """

        # bridge-specific data from test_array_array()
        # SITE_CLASS can be anything
        lat = np.array([-35.352085])
        lon = np.array([149.236994])
        clsf = np.array(['HWB17'])
        cat = np.array(['BRIDGE'])
        skew = np.array([45])
        span = np.array([4])
        #cls = np.array(['E'])
        cls = np.array(['X'])

        attributes = {'STRUCTURE_CLASSIFICATION': clsf,
                      'STRUCTURE_CATEGORY': cat,
                      'SKEW': skew,
                      'SPAN': span,
                      'SITE_CLASS': cls}

        sites = bridges.Bridges(lat, lon, **attributes)

        # indices in atten_periods that are 0.3 and 1.0
        bridge_SA_indices = (2, 6)

        # any values, except columns 2 & 6 must be from test_array_array():
        #sa_1_0 = np.array([[0.75, 0.444, 0.11, 0.085]])
        #sa_0_3 = np.array([[01.5, 01, 0.5, 0.25]])
        SA = np.array([[[0.14210731, 0.29123634, 1.5, 0.13234554,
                         0.08648546, 0.06338455, 0.75, 0.04140068,
                         0.03497466, 0.02969136, 0.02525473, 0.02151188,
                         0.018371, 0.01571802, 0.01344816, 0.01148438,
                         0.00980236, 0.00836594, 0.00714065, 0.00609482],
                        [0.2093217, 0.30976405, 1.0, 0.06989206,
                         0.03216174, 0.01945677, 0.444, 0.00987403,
                         0.00799221, 0.00660128, 0.00547129, 0.0045463,
                         0.0042072, 0.00418348, 0.0041599, 0.00413222,
                         0.00410333, 0.00407463, 0.00404614, 0.00401785],
                        [0.01450217, 0.02750284, 0.5, 0.01127933,
                         0.00793098, 0.00621618, 0.11, 0.00430777,
                         0.00364714, 0.0031542, 0.00279411, 0.00247654,
                         0.0022153, 0.001994, 0.0017948, 0.00161223,
                         0.00144737, 0.00129929, 0.00117312, 0.00105988],
                        [0.01450217, 0.02750284, 0.25, 0.01127933,
                         0.00793098, 0.00621618, 0.085, 0.00430777,
                         0.00364714, 0.0031542, 0.00279411, 0.00247654,
                         0.0022153, 0.001994, 0.0017948, 0.00161223,
                         0.00144737, 0.00129929, 0.00117312, 0.00105988]]])

        # any data, indices (2, 6) must be 0.3 and 1.0 respectively (bridges)
        atten_periods =  np.array([0.,      0.17544, 0.3,    0.52632, 0.70175,
                                   0.87719, 1.0,     1.2281, 1.4035,  1.5789,
                                   1.7544,  1.9298,  2.1053, 2.2807,  2.4561,
                                   2.6316,  2.807,   2.9825, 3.1579,  3.3333 ])

        # fudge up a THE_PARAM_T object, anything with required attributes is OK
        # run test adding required attributes until no errors
        THE_PARAM_T = DataObj(atten_periods=atten_periods)
        pseudo_event_set_Mw = None		# not needed for bridges
       
        # now call calc_total_loss, check results 
        (total_loss, damage) = dm.calc_total_loss(sites, SA, THE_PARAM_T,
                                                  pseudo_event_set_Mw,
                                                  bridge_SA_indices)
        (structure_state, non_structural_state,
             acceleration_sensitive_state) = damage.get_states()

        # test the 'money' return, should be same as from test_array_array()
        expected = np.array([[[0.0434824802069249, 0.0799841750577186,
                               0.236549375430427, 0.60646402809954],
                              [0.1212962, 0.1565718, 0.27978019, 0.273137],
                              [0.047551, 0.02388763, 0.01246965, 0.00170067],
                              [0.02230382, 0.00941589, 0.00397589, 0.00039163]]])

        msg = ('\nexpected=\n%s\nstructure_state=\n%s'
                % (str(expected), str(structure_state)))
        self.failUnless(np.allclose(expected, structure_state, rtol=5.0e-3),
                        msg)

        # we expect the other return values (non_structural_state &
        # acceleration_sensitive_state) to be same shape as structure_state
        # and filled with zeroes
        other_expected = np.zeros(structure_state.shape)
        msg = ('\nother_expected=\n%s\nnon_structural_state=\n%s'
                % (str(other_expected), str(non_structural_state)))
        self.failUnless(np.allclose(other_expected,
                                    non_structural_state, rtol=1.0e-6),
                        msg)
        msg = ('\nother_expected=\n%s\nacceleration_sensitive_state=\n%s'
                % (str(other_expected), str(acceleration_sensitive_state)))
        self.failUnless(np.allclose(other_expected,
                                    acceleration_sensitive_state, rtol=1.0e-6),
                        msg)
        

################################################################################

if __name__ == '__main__':
    suite = unittest.makeSuite(TestBridgeDamage,'test')
    #suite = unittest.makeSuite(TestBridgeDamage,'test_calc_total_loss')
    runner = unittest.TextTestRunner()
    runner.run(suite)

