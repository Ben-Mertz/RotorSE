# --- Import Modules
import numpy as np
import os
from openmdao.api import IndepVarComp, Component, Group, Problem, Brent, ScipyGMRES
from rotorse.rotor_aeropower import RotorAeroPower
from rotorse.rotor_geometry import RotorGeometry, NREL5MW, DTU10MW, NINPUT
from rotorse import RPM2RS, RS2RPM, TURBULENCE_CLASS, DRIVETRAIN_TYPE
# ---

# --- Init Problem
rotor = Problem()
myref = DTU10MW()

npts_coarse_power_curve = 20 # (Int): number of points to evaluate aero analysis at
npts_spline_power_curve = 200  # (Int): number of points to use in fitting spline to power curve

rotor.root = RotorAeroPower(myref, npts_coarse_power_curve, npts_spline_power_curve)
rotor.setup()
# ---

# === blade grid ===
rotor['hubFraction'] = myref.hubFraction #0.025  # (Float): hub location as fraction of radius
rotor['bladeLength'] = myref.bladeLength #61.5  # (Float, m): blade length (if not precurved or swept) otherwise length of blade before curvature
rotor['precone'] = myref.precone #2.5  # (Float, deg): precone angle
rotor['tilt'] = myref.tilt #5.0  # (Float, deg): shaft tilt
rotor['yaw'] = 0.0  # (Float, deg): yaw error
rotor['nBlades'] = myref.nBlades #3  # (Int): number of blades

# === blade geometry ===
rotor['r_max_chord'] = myref.r_max_chord #0.23577  # (Float): location of max chord on unit radius
rotor['chord_in'] = myref.chord #np.array([3.2612, 4.5709, 3.3178, 1.4621])  # (Array, m): chord at control points. defined at hub, then at linearly spaced locations from r_max_chord to tip
rotor['theta_in'] = myref.theta #np.array([13.2783, 7.46036, 2.89317, -0.0878099])  # (Array, deg): twist at control points.  defined at linearly spaced locations from r[idx_cylinder] to tip
rotor['precurve_in'] = myref.precurve #np.array([0.0, 0.0, 0.0])  # (Array, m): precurve at control points.  defined at same locations at chord, starting at 2nd control point (root must be zero precurve)
rotor['presweep_in'] = myref.presweep #np.array([0.0, 0.0, 0.0])  # (Array, m): precurve at control points.  defined at same locations at chord, starting at 2nd control point (root must be zero precurve)
rotor['sparT_in'] = myref.spar_thickness #np.array([0.05, 0.047754, 0.045376, 0.031085, 0.0061398])  # (Array, m): spar cap thickness parameters
rotor['teT_in'] = myref.te_thickness #np.array([0.1, 0.09569, 0.06569, 0.02569, 0.00569])  # (Array, m): trailing-edge thickness parameters

# === atmosphere ===
rotor['analysis.rho'] = 1.225  # (Float, kg/m**3): density of air
rotor['analysis.mu'] = 1.81206e-5  # (Float, kg/m/s): dynamic viscosity of air
rotor['hub_height'] = myref.hub_height #90.0
rotor['analysis.shearExp'] = 0.25  # (Float): shear exponent
rotor['turbine_class'] = myref.turbine_class #TURBINE_CLASS['I']  # (Enum): IEC turbine class
rotor['cdf_reference_height_wind_speed'] = myref.hub_height #90.0  # (Float): reference hub height for IEC wind speed (used in CDF calculation)

# === control ===
rotor['control_Vin'] = myref.control_Vin #3.0  # (Float, m/s): cut-in wind speed
rotor['control_Vout'] = myref.control_Vout #25.0  # (Float, m/s): cut-out wind speed
rotor['control_ratedPower'] = myref.rating #5e6  # (Float, W): rated power
rotor['control_minOmega'] = myref.control_minOmega #0.0  # (Float, rpm): minimum allowed rotor rotation speed
rotor['control_maxOmega'] = myref.control_maxOmega #12.0  # (Float, rpm): maximum allowed rotor rotation speed
rotor['control_tsr'] = myref.control_tsr #7.55  # (Float): tip-speed ratio in Region 2 (should be optimized externally)
rotor['control_pitch'] = myref.control_pitch #0.0  # (Float, deg): pitch angle in region 2 (and region 3 for fixed pitch machines)

# === aero and structural analysis options ===
rotor['nSector'] = 4  # (Int): number of sectors to divide rotor face into in computing thrust and power
rotor['AEP_loss_factor'] = 1.0  # (Float): availability and other losses (soiling, array, etc.)
rotor['drivetrainType'] = myref.drivetrain #DRIVETRAIN_TYPE['GEARED']  # (Enum)
# ---


# === run and outputs ===
rotor.run()

print 'AEP =', rotor['AEP']
print 'diameter =', rotor['diameter']
print 'ratedConditions.V =', rotor['rated_V']
print 'ratedConditions.Omega =', rotor['rated_Omega']
print 'ratedConditions.pitch =', rotor['rated_pitch']
print 'ratedConditions.T =', rotor['rated_T']
print 'ratedConditions.Q =', rotor['rated_Q']

import matplotlib.pyplot as plt
plt.plot(rotor['V'], rotor['P']/1e6)
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power (MW)')
plt.show()
# ---


# outpath = '..\images'
# # Power Curve
# f, ax = plt.subplots(1,1,figsize=(5.3, 4))
# ax.plot(rotor['V'], rotor['P']/1e6)
# ax.set(xlabel='Wind Speed (m/s)' , ylabel='Power (MW)')
# ax.set_ylim([0, 10.3])
# ax.set_xlim([0, 25])
# f.tight_layout()
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# f.savefig(os.path.abspath(os.path.join(outpath,'power_curve_dtu10mw.png')))
# f.savefig(os.path.abspath(os.path.join(outpath,'power_curve_dtu10mw.pdf')))

# # Chord
# fc, axc = plt.subplots(1,1,figsize=(5.3, 4))
# rc_c = np.r_[0.0, myref.r_cylinder, np.linspace(rotor['r_max_chord'], 1.0, NINPUT-2)]
# r = (rotor['spline.r_pts'] - rotor['spline.Rhub'])/rotor['bladeLength']
# axc.plot(r, rotor['spline.chord'], c='k')
# axc.plot(rc_c, rotor['chord_in'], '.', c='k')
# for i, (x, y) in enumerate(zip(rc_c, rotor['chord_in'])):
#     txt = '$c_%d$' % i
#     if i<=1:
#         axc.annotate(txt, (x,y), xytext=(x+0.01,y-0.4), textcoords='data')
#     else:
#         axc.annotate(txt, (x,y), xytext=(x+0.01,y+0.2), textcoords='data')
# axc.set(xlabel='Blade Fraction, $r/R$' , ylabel='Chord (m)')
# axc.set_ylim([0, 7])
# axc.set_xlim([0, 1.1])
# fc.tight_layout()
# axc.spines['right'].set_visible(False)
# axc.spines['top'].set_visible(False)
# fc.savefig(os.path.abspath(os.path.join(outpath,'chord_dtu10mw.png')))
# fc.savefig(os.path.abspath(os.path.join(outpath,'chord_dtu10mw.pdf')))

# # Twist
# ft, axt = plt.subplots(1,1,figsize=(5.3, 4))
# rc_t = rc_c#np.linspace(myref.r_cylinder, 1.0, NINPUT)
# r = (rotor['spline.r_pts'] - rotor['spline.Rhub'])/rotor['bladeLength']
# axt.plot(r, rotor['spline.theta'], c='k')
# axt.plot(rc_t, rotor['theta_in'], '.', c='k')
# for i, (x, y) in enumerate(zip(rc_t, rotor['theta_in'])):
#     txt = '$\Theta_%d$' % i
#     axt.annotate(txt, (x,y), xytext=(x+0.01,y+0.1), textcoords='data')
# axt.set(xlabel='Blade Fraction, $r/R$' , ylabel='Twist ($\deg$)')
# axt.set_ylim([-1, 15])
# axt.set_xlim([0, 1.1])
# ft.tight_layout()
# axt.spines['right'].set_visible(False)
# axt.spines['top'].set_visible(False)
# ft.savefig(os.path.abspath(os.path.join(outpath,'theta_dtu10mw.png')))
# ft.savefig(os.path.abspath(os.path.join(outpath,'theta_dtu10mw.pdf')))


# plt.show()
