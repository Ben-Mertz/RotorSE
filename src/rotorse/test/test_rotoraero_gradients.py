#!/usr/bin/env python
# encoding: utf-8
"""
test_rotoraero_gradients.py

Created by Andrew Ning on 2013-12-30.
Copyright (c) NREL. All rights reserved.
"""

import unittest
import numpy as np
from utilities import check_gradient_unit_test, check_for_missing_unit_tests
from rotoraero import Coefficients, SetupRunVarSpeed, RegulatedPowerCurve, AEP, RegulatedPowerCurveGroup
from rotoraerodefaults import GeometrySpline, CCBladeGeometry, CSMDrivetrain, \
    WeibullCDF, WeibullWithMeanCDF, RayleighCDF
from ccblade2 import CCBlade_to_RotorSE_connection as CCBlade
from enum import Enum
from openmdao.api import IndepVarComp, Component, Problem, Group, SqliteRecorder, BaseRecorder
from openmdao.drivers.pyoptsparse_driver import pyOptSparseDriver
import os

# class TestMaxTipSpeed(unittest.TestCase):

#     def test1(self):

#         ts = MaxTipSpeed()
#         ts.R = 63.0
#         ts.Vtip_max = 80.0

#         check_gradient_unit_test(self, ts)



class TestCoefficients(unittest.TestCase):

    def test1(self):

        V = np.array([12.5, 11.5574318317, 10.7470459579, 10.0428591371, 9.42527942463, 8.87925487168, 8.39303048389, 7.95729238704, 7.56456542753, 7.2087807692, 6.88496003209, 6.58898090313, 6.31740071221, 6.06732191135, 5.83628828803, 5.62220402072, 5.42326991915, 5.2379327383])
        T = np.array([297537.442366, 287373.577926, 276842.263638, 266577.02588, 257357.173035, 249612.50174, 243430.855264, 238328.580357, 232897.327461, 226569.543695, 218948.774702, 210325.108191, 201373.59928, 192450.494842, 183749.591171, 175393.691013, 167431.667222, 159881.687873])
        Q = np.array([2771187.76066, 2708873.98497, 2608206.05664, 2489419.14819, 2369374.79424, 2256062.60666, 2150350.91314, 2043415.20025, 1921526.97181, 1784742.05328, 1635134.27376, 1484081.73688, 1340896.38225, 1209094.24861, 1089686.69666, 982501.972978, 886537.720876, 800672.778302])
        P = np.array([1741188.62212, 1702035.72214, 1638784.19732, 1564148.18153, 1488722.08943, 1417525.94222, 1351105.32627, 1283915.63627, 1207331.00366, 1121386.50463, 1027385.16442, 932476.05638, 842510.044742, 759696.321788, 684670.344188, 617324.196089, 557028.078207, 503077.543649])
        R = 62.9400379597
        rho = 1.225

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', Coefficients(len(V)), promotes=['*'])
        prob.root.add('V', IndepVarComp('V', np.zeros(len(V))), promotes=['*'])
        prob.root.add('T', IndepVarComp('T', np.zeros(len(T))), promotes=['*'])
        prob.root.add('Q', IndepVarComp('Q', np.zeros(len(Q))), promotes=['*'])
        prob.root.add('P', IndepVarComp('P', np.zeros(len(P))), promotes=['*'])
        prob.root.add('R', IndepVarComp('R', 0.0), promotes=['*'])
        prob.root.add('rho', IndepVarComp('rho', 0.0), promotes=['*'])
        prob.setup(check=False)

        prob['V'] = V
        prob['T'] = T
        prob['Q'] = Q
        prob['P'] = P
        prob['R'] = R
        prob['rho'] = rho

        check_gradient_unit_test(self, prob)




class TestSetupRunVarSpeed(unittest.TestCase):

    def test1(self):

        control_Vin = 3.0
        control_Vout = 25.0
        control_tsr = 7.55
        control_maxOmega = 12.0
        R = 62.9400379597

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', SetupRunVarSpeed(), promotes=['*'])
        prob.root.add('control_Vin', IndepVarComp('control:Vin', control_Vin), promotes=['*'])
        prob.root.add('control_Vout', IndepVarComp('control:Vout', control_Vout), promotes=['*'])
        prob.root.add('control_tsr', IndepVarComp('control:tsr', control_tsr), promotes=['*'])
        prob.root.add('control_maxOmega', IndepVarComp('control:maxOmega', control_maxOmega), promotes=['*'])
        prob.root.add('R', IndepVarComp('R', 0.0), promotes=['*'])
        prob.root.add('rho', IndepVarComp('rho', 0.0), promotes=['*'])
        prob.setup(check=False)

        prob['control:Vin'] = control_Vin
        prob['control:Vout'] = control_Vout
        prob['control:tsr'] = control_tsr
        prob['control:maxOmega'] = control_maxOmega
        prob['R'] = R

        check_gradient_unit_test(self, prob)



class TestRegulatedPowerCurve(unittest.TestCase):

    def test1(self):
        control_Vin = 3.0
        control_Vout = 25.0
        control_ratedPower = 5e6
        control_tsr = 7.5
        control_pitch = 0.0
        control_maxOmega = 12.0
        Vcoarse = np.array([3.0, 4.15789473684, 5.31578947368, 6.47368421053, 7.63157894737, 8.78947368421, 9.94736842105, 11.1052631579, 12.2631578947, 13.4210526316, 14.5789473684, 15.7368421053, 16.8947368421, 18.0526315789, 19.2105263158, 20.3684210526, 21.5263157895, 22.6842105263, 23.8421052632, 25.0])
        Pcoarse = np.array([22025.3984542, 165773.30206, 416646.421046, 804477.093872, 1359097.659, 2110340.45488, 3088037.81999, 4297554.655, 5634839.03406, 7014620.69097, 8243314.7876, 9151515.42199, 9805082.34125, 10369558.6255, 10906183.6245, 11403861.5527, 11836495.4076, 12179487.9734, 12422864.4516, 12564556.3923])
        Tcoarse = np.array([52447.090344, 100745.549657, 164669.981102, 244220.384676, 339396.760382, 450199.108219, 576627.428186, 690511.171188, 779190.745114, 856112.80582, 912563.587402, 948902.381907, 976338.470922, 1006515.00082, 1040084.63496, 1074759.69165, 1108268.14897, 1138947.1794, 1166201.26418, 1190149.76946])
        Vrated = 12.0
        R = 62.9400379597

        prob = Problem()
        prob.root = Group()
        prob.root.add('powercurve', RegulatedPowerCurveGroup())
        prob.root.add('control_Vin', IndepVarComp('control:Vin', control_Vin), promotes=['*'])
        prob.root.add('control_Vout', IndepVarComp('control:Vout', control_Vout), promotes=['*'])
        prob.root.add('control_ratedPower', IndepVarComp('control:ratedPower', control_ratedPower), promotes=['*'])
        prob.root.add('control_tsr', IndepVarComp('control:tsr', control_tsr), promotes=['*'])
        prob.root.add('control_pitch', IndepVarComp('control:pitch', control_pitch), promotes=['*'])
        prob.root.add('control_maxOmega', IndepVarComp('control:maxOmega', control_maxOmega), promotes=['*'])
        prob.root.add('Vcoarse', IndepVarComp('Vcoarse', np.zeros(len(Vcoarse))), promotes=['*'])
        prob.root.add('Pcoarse', IndepVarComp('Pcoarse', np.zeros(len(Pcoarse))), promotes=['*'])
        prob.root.add('Tcoarse', IndepVarComp('Tcoarse', np.zeros(len(Tcoarse))), promotes=['*'])
        prob.root.add('Vrated', IndepVarComp('Vrated', Vrated))
        prob.root.add('R', IndepVarComp('R', 0.0), promotes=['*'])

        prob.root.connect('control:Vin', 'powercurve.control:Vin')
        prob.root.connect('control:Vout', 'powercurve.control:Vout')
        prob.root.connect('control:maxOmega', 'powercurve.control:maxOmega')
        prob.root.connect('control:pitch', 'powercurve.control:pitch')
        prob.root.connect('control:ratedPower', 'powercurve.control:ratedPower')
        prob.root.connect('control:tsr', 'powercurve.control:tsr')
        prob.root.connect('Vcoarse', 'powercurve.Vcoarse')
        prob.root.connect('Pcoarse', 'powercurve.Pcoarse')
        prob.root.connect('Tcoarse', 'powercurve.Tcoarse')
        prob.root.connect('R', 'powercurve.R')

        prob.setup(check=False)

        prob['control:Vin'] = control_Vin
        prob['control:Vout'] = control_Vout
        prob['control:ratedPower'] = control_ratedPower
        prob['control:tsr'] = control_tsr
        prob['control:pitch'] = control_pitch
        prob['control:maxOmega'] = control_maxOmega
        prob['Vcoarse'] = Vcoarse
        prob['Pcoarse'] = Pcoarse
        prob['Tcoarse'] = Tcoarse
        prob['R'] = R

        check_gradient_unit_test(self, prob, tol=3e-5, display=False, comp=prob.root.powercurve)




class TestAEP(unittest.TestCase):

    def test1(self):

        CDF_V = np.array([0.178275041966, 0.190296788962, 0.202568028297, 0.215071993446, 0.227791807017, 0.240710518196, 0.253811139789, 0.267076684744, 0.280490202059, 0.294034811963, 0.307693740274, 0.32145035184, 0.335288182978, 0.349190972822, 0.363142693506, 0.377127579106, 0.391130153286, 0.405135255571, 0.419128066214, 0.43309412959, 0.447019376098, 0.460890142513, 0.474693190784, 0.488415725243, 0.502045408211, 0.515570374001, 0.528979241305, 0.54226112398, 0.555405640233, 0.568402920224, 0.581243612108, 0.593918886545, 0.606420439704, 0.618740494789, 0.630871802149, 0.642807637993, 0.654541801767, 0.666068612246, 0.67738290239, 0.68848001302, 0.699355785386, 0.710006552662, 0.720429130464, 0.730620806428, 0.740579328925, 0.750302894983, 0.759790137479, 0.76904011166, 0.778052281079, 0.786826502994, 0.795363013307, 0.803662411103, 0.811725642861, 0.819553986387, 0.827149034543, 0.834512678823, 0.841647092838, 0.848554715765, 0.855238235811, 0.861700573747, 0.867944866556, 0.873974451244, 0.879792848857, 0.885403748745, 0.890810993109, 0.896018561866, 0.90103055787, 0.90585119251, 0.91048477172, 0.914935682413, 0.919208379383, 0.923307372661, 0.927237215373, 0.931002492094, 0.934607807711, 0.93805777681, 0.941357013592, 0.944510122313, 0.947521688261, 0.950396269264, 0.95313838773, 0.955752523204, 0.95824310546, 0.960614508091, 0.962871042612, 0.965016953057, 0.967056411054, 0.968993511377, 0.970832267946, 0.972576610282, 0.974230380379, 0.975797329995, 0.977281118336, 0.978685310119, 0.980013374, 0.981268681344, 0.982454505324, 0.98357402033, 0.984630301666, 0.985626325531, 0.986564969246, 0.987449011729, 0.988281134189, 0.98906392103, 0.989799860938, 0.990491348148, 0.991140683869, 0.991750077849, 0.992321650072, 0.992857432566, 0.993359371317, 0.99382932827, 0.994269083401, 0.994680336859, 0.995064711163, 0.995423753433, 0.995758937661, 0.996071667003, 0.996363276084, 0.996635033314, 0.996888143197, 0.997123748634, 0.997342933215, 0.997546723483, 0.997736091178, 0.997911955448, 0.998075185027, 0.998226600365, 0.998366975728, 0.998497041241, 0.998617484891, 0.99872895447, 0.998832059475, 0.998927372946, 0.999015433252, 0.999096745819, 0.999171784802, 0.999240994698, 0.999304791902, 0.999363566204, 0.999417682229, 0.999467480822, 0.999513280372, 0.999555378083, 0.999594051191, 0.999629558123, 0.999662139611, 0.999692019741, 0.999719406969, 0.999744495073, 0.999767464065, 0.999788481055, 0.99980770107, 0.999825267834, 0.999841314496, 0.999855964334, 0.999869331401, 0.999881521151, 0.999892631024, 0.999902750988, 0.999911964064, 0.999920346811, 0.999927969778, 0.99993489794, 0.999941191092, 0.999946904234, 0.999952087915, 0.999956788569, 0.99996104882, 0.999964907768, 0.99996840126, 0.999971562138, 0.999974420473, 0.999977003779, 0.999979337216, 0.999981443776, 0.999983344458, 0.999985058426, 0.999986603162, 0.999987994599, 0.999989247253, 0.999990374339, 0.999991387879, 0.999992298805, 0.999993117053, 0.999993851641, 0.999994510758, 0.999995101829, 0.999995631585, 0.999996106123, 0.999996530963, 0.999996911098, 0.999997251045, 0.999997554883, 0.999997826298, 0.999998068616, 0.999998284835, 0.999998477661, 0.999998649529, 0.999998802632])
        P = np.array([22025.3984542, 31942.1185436, 42589.4002304, 53993.2085473, 66179.5085267, 79174.2652013, 93003.4436034, 107693.008766, 123268.925721, 139757.159501, 157183.67514, 175574.437668, 194955.41212, 215352.563527, 236791.856922, 259299.257337, 282900.729806, 307622.23936, 333489.751032, 360529.229855, 388766.640862, 418227.949084, 448939.119554, 480926.117306, 514214.907371, 548831.454781, 584801.724571, 622151.681771, 660907.291415, 701094.518535, 742739.328164, 785867.685334, 830505.555078, 876678.902429, 924413.692418, 973735.890078, 1024671.46044, 1077246.36854, 1131486.57941, 1187418.05809, 1245066.76959, 1304458.67896, 1365619.75124, 1428575.95144, 1493353.24461, 1559977.59577, 1628474.96996, 1698871.33222, 1771192.64757, 1845464.88105, 1921713.99769, 1999965.96251, 2080246.74057, 2162582.29688, 2246998.59648, 2333521.6044, 2422177.28568, 2512991.60535, 2605990.52843, 2701200.01997, 2798646.04499, 2898354.56853, 3000351.55562, 3104662.97129, 3211314.78058, 3320332.94852, 3431743.44013, 3545572.22046, 3661284.29229, 3777883.06101, 3895967.17288, 4015492.83297, 4136416.74759, 4258697.48598, 4382294.05017, 4507165.36302, 4631531.67845, 4757024.71876, 4883638.63072, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0, 5000000.0])
        lossFactor = 0.95

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', AEP(), promotes=['*'])
        prob.root.add('CDF_V', IndepVarComp('CDF_V', np.zeros(len(CDF_V))), promotes=['*'])
        prob.root.add('P', IndepVarComp('P', np.zeros(len(P))), promotes=['*'])
        prob.root.add('lossFactor', IndepVarComp('lossFactor', 0.0), promotes=['*'])
        prob.setup(check=False)

        prob['CDF_V'] = CDF_V
        prob['P'] = P
        prob['lossFactor'] = lossFactor

        check_gradient_unit_test(self, prob, step_size=1)  # larger step size b.c. AEP is big value



class TestGeometrySpline(unittest.TestCase):

    def test1(self):


        r_af = np.array([0.02222276, 0.06666667, 0.11111057, 0.16666667, 0.23333333, 0.3, 0.36666667, 0.43333333, 0.5, 0.56666667, 0.63333333, 0.7, 0.76666667, 0.83333333, 0.88888943, 0.93333333, 0.97777724])
        idx_cylinder = 3
        r_max_chord = 0.22
        Rhub = 1.5
        Rtip = 63.0
        chord_sub = np.array([3.2612, 4.5709, 3.3178, 1.4621])
        theta_sub = np.array([13.2783, 7.46036, 2.89317, -0.0878099])

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', GeometrySpline(), promotes=['*'])
        prob.root.add('r_af', IndepVarComp('r_af', np.zeros(len(r_af))), promotes=['*'])
        prob.root.add('idx_cylinder', IndepVarComp('idx_cylinder', 0), promotes=['*'])
        prob.root.add('r_max_chord', IndepVarComp('r_max_chord', 0.0), promotes=['*'])
        prob.root.add('Rhub', IndepVarComp('Rhub', 0.0), promotes=['*'])
        prob.root.add('Rtip', IndepVarComp('Rtip', 0.0), promotes=['*'])
        prob.root.add('chord_sub', IndepVarComp('chord_sub', np.zeros(len(chord_sub))), promotes=['*'])
        prob.root.add('theta_sub', IndepVarComp('theta_sub', np.zeros(len(theta_sub))), promotes=['*'])
        prob.setup(check=False)

        prob['r_af'] = r_af
        prob['idx_cylinder'] = idx_cylinder
        prob['r_max_chord'] = r_max_chord
        prob['Rhub'] = Rhub
        prob['Rtip'] = Rtip
        prob['chord_sub'] = chord_sub
        prob['theta_sub'] = theta_sub

        check_gradient_unit_test(self, prob, tol=5e-5)



class TestCCBladeGeometry(unittest.TestCase):

    def test1(self):

        Rtip = 63.0
        precone = 5.0
        precurveTip = 0.0

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CCBladeGeometry(), promotes=['*'])
        prob.root.add('Rtip', IndepVarComp('Rtip', 0.0), promotes=['*'])
        prob.root.add('precone', IndepVarComp('precone', 0.0), promotes=['*'])
        prob.root.add('precurveTip', IndepVarComp('precurveTip', 0.0), promotes=['*'])
        prob.setup(check=False)

        prob['Rtip'] = Rtip
        prob['precone'] = precone
        prob['precurveTip'] = precurveTip

        check_gradient_unit_test(self, prob)


@unittest.skip("CCBlade test takes a long time")
class TestCCBlade(unittest.TestCase):

    def test1(self):

        r = np.array([2.8667, 5.6000, 8.3333, 11.7500, 15.8500, 19.9500, 24.0500,
                  28.1500, 32.2500, 36.3500, 40.4500, 44.5500, 48.6500, 52.7500,
                  56.1667, 58.9000, 61.6333])
        chord = np.array([3.542, 3.854, 4.167, 4.557, 4.652, 4.458, 4.249, 4.007, 3.748,
                      3.502, 3.256, 3.010, 2.764, 2.518, 2.313, 2.086, 1.419])
        theta = np.array([13.308, 13.308, 13.308, 13.308, 11.480, 10.162, 9.011, 7.795,
                      6.544, 5.361, 4.188, 3.125, 2.319, 1.526, 0.863, 0.370, 0.106])
        Rhub = 1.5
        Rtip = 63.0
        hubHt = 80.0
        precone = 2.5
        tilt = -5.0
        yaw = 0.0
        B = 3
        rho = 1.225
        mu = 1.81206e-5
        shearExp = 0.2
        nSector = 4
        precurve = np.zeros(len(r))
        precurveTip = 0.0

        # airfoils
        basepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '5MW_AFFiles/')

        # load all airfoils
        airfoil_types = [0]*8
        airfoil_types[0] = basepath + 'Cylinder1.dat'
        airfoil_types[1] = basepath + 'Cylinder2.dat'
        airfoil_types[2] = basepath + 'DU40_A17.dat'
        airfoil_types[3] = basepath + 'DU35_A17.dat'
        airfoil_types[4] = basepath + 'DU30_A17.dat'
        airfoil_types[5] = basepath + 'DU25_A17.dat'
        airfoil_types[6] = basepath + 'DU21_A17.dat'
        airfoil_types[7] = basepath + 'NACA64_A17.dat'

        # place at appropriate radial stations
        af_idx = [0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7, 7, 7, 7, 7]

        n = len(r)
        af = [0]*n
        for i in range(n):
            af[i] = airfoil_types[af_idx[i]]

        airfoil_files = np.array(af)

        run_case = 'power'
        Uhub = np.array([3.0, 4.15789473684, 5.31578947368, 6.47368421053, 7.63157894737, 8.78947368421, 9.94736842105, 11.1052631579, 12.2631578947, 13.4210526316, 14.5789473684, 15.7368421053, 16.8947368421, 18.0526315789, 19.2105263158, 20.3684210526, 21.5263157895, 22.6842105263, 23.8421052632, 25.0])
        Omega = np.array([3.43647024491, 4.76282718154, 6.08918411817, 7.41554105481, 8.74189799144, 10.0682549281, 11.3946118647, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0])
        pitch = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        n2 = len(Uhub)

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CCBlade(run_case, n, n2), promotes=['*'])
        prob.root.add('r', IndepVarComp('r', np.zeros(len(r))), promotes=['*'])
        prob.root.add('chord', IndepVarComp('chord', np.zeros(len(chord))), promotes=['*'])
        prob.root.add('theta', IndepVarComp('theta', np.zeros(len(theta))), promotes=['*'])
        prob.root.add('Rhub', IndepVarComp('Rhub', 0.0), promotes=['*'])
        prob.root.add('Rtip', IndepVarComp('Rtip', 0.0), promotes=['*'])
        prob.root.add('hubHt', IndepVarComp('hubHt', 0.0), promotes=['*'])
        prob.root.add('precone', IndepVarComp('precone', 0.0), promotes=['*'])
        prob.root.add('precurve', IndepVarComp('precurve', precurve), promotes=['*'])
        prob.root.add('precurveTip', IndepVarComp('precurveTip', 0.0), promotes=['*'])
        prob.root.add('tilt', IndepVarComp('tilt', 0.0), promotes=['*'])
        prob.root.add('yaw', IndepVarComp('yaw', 0.0), promotes=['*'])
        prob.root.add('B', IndepVarComp('B', 0), promotes=['*'])
        prob.root.add('rho', IndepVarComp('rho', 0.0), promotes=['*'])
        prob.root.add('mu', IndepVarComp('mu', 0.0), promotes=['*'])
        prob.root.add('shearExp', IndepVarComp('shearExp', 0.0, pass_by_obj=True), promotes=['*'])
        prob.root.add('nSector', IndepVarComp('nSector', nSector), promotes=['*'])
        prob.root.add('airfoil_files', IndepVarComp('airfoil_files', airfoil_files), promotes=['*'])
        prob.root.add('Uhub', IndepVarComp('Uhub', np.zeros(len(Uhub))), promotes=['*'])
        prob.root.add('Omega', IndepVarComp('Omega', np.zeros(len(Omega))), promotes=['*'])
        prob.root.add('pitch', IndepVarComp('pitch', np.zeros(len(pitch))), promotes=['*'])
        prob.setup(check=False)

        prob['r'] = r
        prob['chord'] = chord
        prob['theta'] = theta
        prob['Rhub'] = Rhub
        prob['Rtip'] = Rtip
        prob['hubHt'] = hubHt
        prob['precone'] = precone
        prob['tilt'] = tilt
        prob['yaw'] = yaw
        prob['B'] = B
        prob['rho'] = rho
        prob['mu'] = mu
        prob['shearExp'] = shearExp
        prob['nSector'] = nSector
        prob['airfoil_files'] = airfoil_files
        prob['Uhub'] = Uhub
        prob['Omega'] = Omega
        prob['pitch'] = pitch
        prob['precurve'] = precurve
        prob['precurveTip'] = precurveTip

        check_gradient_unit_test(self, prob, tol=1e-3, display=True)

    def test2(self):

        r = np.array([2.8667, 5.6000, 8.3333, 11.7500, 15.8500, 19.9500, 24.0500,
                  28.1500, 32.2500, 36.3500, 40.4500, 44.5500, 48.6500, 52.7500,
                  56.1667, 58.9000, 61.6333])
        chord = np.array([3.542, 3.854, 4.167, 4.557, 4.652, 4.458, 4.249, 4.007, 3.748,
                      3.502, 3.256, 3.010, 2.764, 2.518, 2.313, 2.086, 1.419])
        theta = np.array([13.308, 13.308, 13.308, 13.308, 11.480, 10.162, 9.011, 7.795,
                      6.544, 5.361, 4.188, 3.125, 2.319, 1.526, 0.863, 0.370, 0.106])
        Rhub = 1.5
        Rtip = 63.0
        hubHt = 80.0
        precone = 2.5
        tilt = -5.0
        yaw = 0.0
        B = 3
        rho = 1.225
        mu = 1.81206e-5
        shearExp = 0.2
        nSector = 4
        precurve = np.zeros(len(r))

        # airfoils
        basepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '5MW_AFFiles/')

        # load all airfoils
        airfoil_types = [0]*8
        airfoil_types[0] = basepath + 'Cylinder1.dat'
        airfoil_types[1] = basepath + 'Cylinder2.dat'
        airfoil_types[2] = basepath + 'DU40_A17.dat'
        airfoil_types[3] = basepath + 'DU35_A17.dat'
        airfoil_types[4] = basepath + 'DU30_A17.dat'
        airfoil_types[5] = basepath + 'DU25_A17.dat'
        airfoil_types[6] = basepath + 'DU21_A17.dat'
        airfoil_types[7] = basepath + 'NACA64_A17.dat'

        # place at appropriate radial stations
        af_idx = [0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7, 7, 7, 7, 7]

        n = len(r)
        af = [0]*n
        for i in range(n):
            af[i] = airfoil_types[af_idx[i]]

        airfoil_files = np.array(af)

        run_case = 'loads'
        V_load = 12.0
        Omega_load = 10.0
        pitch_load = 0.0
        azimuth_load = 180.0
        n2 = 1

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CCBlade(run_case, n, n2), promotes=['*'])
        prob.root.add('r', IndepVarComp('r', np.zeros(len(r))), promotes=['*'])
        prob.root.add('chord', IndepVarComp('chord', np.zeros(len(chord))), promotes=['*'])
        prob.root.add('theta', IndepVarComp('theta', np.zeros(len(theta))), promotes=['*'])
        prob.root.add('Rhub', IndepVarComp('Rhub', 0.0), promotes=['*'])
        prob.root.add('Rtip', IndepVarComp('Rtip', 0.0), promotes=['*'])
        prob.root.add('hubHt', IndepVarComp('hubHt', 0.0), promotes=['*'])
        prob.root.add('precone', IndepVarComp('precone', 0.0), promotes=['*'])
        prob.root.add('tilt', IndepVarComp('tilt', 0.0), promotes=['*'])
        prob.root.add('yaw', IndepVarComp('yaw', 0.0), promotes=['*'])
        prob.root.add('B', IndepVarComp('B', 0), promotes=['*'])
        prob.root.add('rho', IndepVarComp('rho', 0.0), promotes=['*'])
        prob.root.add('mu', IndepVarComp('mu', 0.0), promotes=['*'])
        prob.root.add('shearExp', IndepVarComp('shearExp', 0.0, pass_by_obj=True), promotes=['*'])
        prob.root.add('precurve', IndepVarComp('precurve', precurve), promotes=['*'])
        prob.root.add('nSector', IndepVarComp('nSector', nSector), promotes=['*'])
        prob.root.add('airfoil_files', IndepVarComp('airfoil_files', airfoil_files), promotes=['*'])
        prob.root.add('V_load', IndepVarComp('V_load', 0.0), promotes=['*'])
        prob.root.add('Omega_load', IndepVarComp('Omega_load', 0.0), promotes=['*'])
        prob.root.add('pitch_load', IndepVarComp('pitch_load', 0.0), promotes=['*'])
        prob.root.add('azimuth_load', IndepVarComp('azimuth_load', 0.0), promotes=['*'])
        prob.setup(check=False)

        prob['r'] = r
        prob['chord'] = chord
        prob['theta'] = theta
        prob['Rhub'] = Rhub
        prob['Rtip'] = Rtip
        prob['hubHt'] = hubHt
        prob['precone'] = precone
        prob['tilt'] = tilt
        prob['yaw'] = yaw
        prob['B'] = B
        prob['rho'] = rho
        prob['mu'] = mu
        prob['shearExp'] = shearExp
        prob['nSector'] = nSector
        prob['airfoil_files'] = airfoil_files
        prob['V_load'] = V_load
        prob['Omega_load'] = Omega_load
        prob['pitch_load'] = pitch_load
        prob['azimuth_load'] = azimuth_load
        prob['precurve'] = precurve

        check_gradient_unit_test(self, prob, tol=1e-3, display=True)



class TestCSMDrivetrain(unittest.TestCase):

    def test1(self):

        aeroPower = np.array([94518.9621316, 251637.667571, 525845.9078, 949750.895039, 1555959.84151, 2377079.95943, 3445718.46102, 4767739.26659, 6246980.6699, 7776655.12685, 9138828.60234, 10145691.7573, 10870259.0229, 11496057.2782, 12090978.6194, 12642721.8686, 13122354.9713, 13502608.5891, 13772424.3097, 13929508.977])
        ratedPower = 5000000.0

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CSMDrivetrain(len(aeroPower)), promotes=['*'])
        prob.root.add('aeroPower', IndepVarComp('aeroPower', np.zeros(len(aeroPower))), promotes=['*'])
        prob.root.add('ratedPower', IndepVarComp('ratedPower', 0.0), promotes=['*'])
        prob.root.add('drivetrainType', IndepVarComp('drivetrainType', Enum('geared', 'single_stage', 'multi_drive', 'pm_direct_drive'), pass_by_obj=True), promotes=['*'])
        prob.setup(check=False)

        prob['aeroPower'] = aeroPower
        prob['ratedPower'] = ratedPower
        prob['drivetrainType'] = 'geared'

        check_gradient_unit_test(self, prob, tol=6e-4)


    def test2(self):

        aeroPower = np.linspace(0.0, 10.0, 50)
        ratedPower = 5.0

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CSMDrivetrain(len(aeroPower)), promotes=['*'])
        prob.root.add('aeroPower', IndepVarComp('aeroPower', np.zeros(len(aeroPower))), promotes=['*'])
        prob.root.add('ratedPower', IndepVarComp('ratedPower', 0.0), promotes=['*'])
        prob.root.add('drivetrainType', IndepVarComp('drivetrainType', Enum('geared', 'single_stage', 'multi_drive', 'pm_direct_drive'), pass_by_obj=True), promotes=['*'])
        prob.setup(check=False)

        prob['aeroPower'] = aeroPower
        prob['ratedPower'] = ratedPower
        prob['drivetrainType'] = 'geared'

        check_gradient_unit_test(self, prob)


    def test3(self):

        aeroPower = np.linspace(-10.0, 10.0, 50)
        ratedPower = 5.0

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CSMDrivetrain(len(aeroPower)), promotes=['*'])
        prob.root.add('aeroPower', IndepVarComp('aeroPower', np.zeros(len(aeroPower))), promotes=['*'])
        prob.root.add('ratedPower', IndepVarComp('ratedPower', 0.0), promotes=['*'])
        prob.root.add('drivetrainType', IndepVarComp('drivetrainType', Enum('geared', 'single_stage', 'multi_drive', 'pm_direct_drive'), pass_by_obj=True), promotes=['*'])
        prob.setup(check=False)

        prob['aeroPower'] = aeroPower
        prob['ratedPower'] = ratedPower
        prob['drivetrainType'] = 'geared'

        check_gradient_unit_test(self, prob)


    def test4(self):

        aeroPower = np.linspace(-10.0, 30.0, 50)
        ratedPower = 5.0

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', CSMDrivetrain(len(aeroPower)), promotes=['*'])
        prob.root.add('aeroPower', IndepVarComp('aeroPower', np.zeros(len(aeroPower))), promotes=['*'])
        prob.root.add('ratedPower', IndepVarComp('ratedPower', 0.0), promotes=['*'])
        prob.root.add('drivetrainType', IndepVarComp('drivetrainType', Enum('geared', 'single_stage', 'multi_drive', 'pm_direct_drive'), pass_by_obj=True), promotes=['*'])
        prob.setup(check=False)

        prob['aeroPower'] = aeroPower
        prob['ratedPower'] = ratedPower
        prob['drivetrainType'] = 'geared'

        check_gradient_unit_test(self, prob)




class TestWeibullCDF(unittest.TestCase):

    def test1(self):

        A = 5.0
        k = 2.2
        x = np.linspace(1.0, 15.0, 50)
        n = len(x)

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', WeibullCDF(n), promotes=['*'])
        prob.root.add('A', IndepVarComp('A', A), promotes=['*'])
        prob.root.add('k', IndepVarComp('k', k), promotes=['*'])
        prob.root.add('x', IndepVarComp('x', x), promotes=['*'])
        prob.setup(check=False)

        prob['A'] = A
        prob['k'] = k
        prob['x'] = x

        check_gradient_unit_test(self, prob)

class TestWeibullWithMeanCDF(unittest.TestCase):

    def test1(self):

        xbar = 8.0
        k = 2.2
        x = np.linspace(1.0, 15.0, 50)
        n = len(x)

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', WeibullWithMeanCDF(n), promotes=['*'])
        prob.root.add('xbar', IndepVarComp('xbar', xbar), promotes=['*'])
        prob.root.add('k', IndepVarComp('k', k), promotes=['*'])
        prob.root.add('x', IndepVarComp('x', x), promotes=['*'])
        prob.setup(check=False)

        prob['xbar'] = xbar
        prob['k'] = k
        prob['x'] = x

        check_gradient_unit_test(self, prob)



class TestRayleighCDF(unittest.TestCase):

    def test1(self):

        xbar = 6.0
        x = np.array([3.0, 3.08805770406, 3.17611540812, 3.26417311218, 3.35223081624, 3.4402885203, 3.52834622436, 3.61640392842, 3.70446163248, 3.79251933654, 3.8805770406, 3.96863474466, 4.05669244872, 4.14475015278, 4.23280785684, 4.3208655609, 4.40892326496, 4.49698096902, 4.58503867308, 4.67309637714, 4.7611540812, 4.84921178526, 4.93726948932, 5.02532719338, 5.11338489744, 5.2014426015, 5.28950030556, 5.37755800962, 5.46561571369, 5.55367341775, 5.64173112181, 5.72978882587, 5.81784652993, 5.90590423399, 5.99396193805, 6.08201964211, 6.17007734617, 6.25813505023, 6.34619275429, 6.43425045835, 6.52230816241, 6.61036586647, 6.69842357053, 6.78648127459, 6.87453897865, 6.96259668271, 7.05065438677, 7.13871209083, 7.22676979489, 7.31482749895, 7.40288520301, 7.49094290707, 7.57900061113, 7.66705831519, 7.75511601925, 7.84317372331, 7.93123142737, 8.01928913143, 8.10734683549, 8.19540453955, 8.28346224361, 8.37151994767, 8.45957765173, 8.54763535579, 8.63569305985, 8.72375076391, 8.81180846797, 8.89986617203, 8.98792387609, 9.07598158015, 9.16403928421, 9.25209698827, 9.34015469233, 9.42821239639, 9.51627010045, 9.60432780451, 9.69238550857, 9.78044321263, 9.86850091669, 9.95655862075, 10.0446163248, 10.1326740289, 10.2207317329, 10.308789437, 10.3968471411, 10.4849048451, 10.5729625492, 10.6610202532, 10.7490779573, 10.8371356614, 10.9251933654, 11.0132510695, 11.1013087735, 11.1893664776, 11.2774241817, 11.3654818857, 11.4535395898, 11.5415972938, 11.6296549979, 11.717712702, 11.8505355749, 11.9833584479, 12.1161813209, 12.2490041939, 12.3818270669, 12.5146499398, 12.6474728128, 12.7802956858, 12.9131185588, 13.0459414318, 13.1787643047, 13.3115871777, 13.4444100507, 13.5772329237, 13.7100557967, 13.8428786696, 13.9757015426, 14.1085244156, 14.2413472886, 14.3741701616, 14.5069930345, 14.6398159075, 14.7726387805, 14.9054616535, 15.0382845265, 15.1711073994, 15.3039302724, 15.4367531454, 15.5695760184, 15.7023988914, 15.8352217644, 15.9680446373, 16.1008675103, 16.2336903833, 16.3665132563, 16.4993361293, 16.6321590022, 16.7649818752, 16.8978047482, 17.0306276212, 17.1634504942, 17.2962733671, 17.4290962401, 17.5619191131, 17.6947419861, 17.8275648591, 17.960387732, 18.093210605, 18.226033478, 18.358856351, 18.491679224, 18.6245020969, 18.7573249699, 18.8901478429, 19.0229707159, 19.1557935889, 19.2886164618, 19.4214393348, 19.5542622078, 19.6870850808, 19.8199079538, 19.9527308267, 20.0855536997, 20.2183765727, 20.3511994457, 20.4840223187, 20.6168451916, 20.7496680646, 20.8824909376, 21.0153138106, 21.1481366836, 21.2809595565, 21.4137824295, 21.5466053025, 21.6794281755, 21.8122510485, 21.9450739215, 22.0778967944, 22.2107196674, 22.3435425404, 22.4763654134, 22.6091882864, 22.7420111593, 22.8748340323, 23.0076569053, 23.1404797783, 23.2733026513, 23.4061255242, 23.5389483972, 23.6717712702, 23.8045941432, 23.9374170162, 24.0702398891, 24.2030627621, 24.3358856351, 24.4687085081, 24.6015313811, 24.734354254, 24.867177127, 25.0])

        prob = Problem()
        prob.root = Group()
        prob.root.add('comp', RayleighCDF(), promotes=['*'])
        prob.root.add('xbar', IndepVarComp('xbar', 0.0), promotes=['*'])
        prob.root.add('x', IndepVarComp('x', np.zeros(len(x))), promotes=['*'])
        prob.setup(check=False)

        prob['xbar'] = xbar
        prob['x'] = x

        check_gradient_unit_test(self, prob, tol=2e-6)




if __name__ == '__main__':
    import rotorse.rotoraero
    import rotorse.rotoraerodefaults

    check_for_missing_unit_tests([rotorse.rotoraero, rotorse.rotoraerodefaults])

    unittest.main()

    # from unittest import TestSuite
    # blah = TestSuite()
    # blah.addTest(TestRegulatedPowerCurve('test1'))
    # unittest.TextTestRunner().run(blah)
