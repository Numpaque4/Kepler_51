from geotrans_test import *

System=dict2obj(dict(\
#########################################
#SYSTEM PRIMARY PARAMETERS
#########################################
#//////////////////////////////
#DETECTOR
#//////////////////////////////
Ddet=0.5,#Aperture, m
qeff=1.0,#Quantum efficiency
#//////////////////////////////
#STAR
#//////////////////////////////
Mstar=1.0*MSUN,
Rstar=1.0*RSUN,
Lstar=1.0*LSUN,
Tstar=1.0*TSUN,
Dstar=1*KILO*PARSEC,
c1=0.70,#Limb Darkening
c2=-0.24,#Limb Darkening
#//////////////////////////////
#ORBIT
#//////////////////////////////
ap=1.0*AU,
ep=0.0,
iorb=90.0*DEG,
wp=0.0*DEG,
#//////////////////////////////
#PLANET
#//////////////////////////////
Mplanet=1.0*MSAT,
Rplanet=1.0*RSAT,
fp=0.0, #Oblateness
#//////////////////////////////
#RINGS
#//////////////////////////////
fe=5.0, #Exterior ring (Rp)
fi=1.2, #Interior ring (Rp)
ir=10.0*DEG, #Ring inclination
phir=0.0*DEG, #Ring roll angle
tau=2.0, #Opacity
))

#########################################
#SYSTEM DERIVATIVE PARAMETERS
#########################################
derivedSystemProperties(System)
updatePlanetRings(System)
updatePosition(System,System.tcen)
