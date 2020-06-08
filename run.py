import numpy as np
import openmdao.api as om
from openmdao.api import Problem, IndepVarComp, ScipyOptimizeDriver

from aircraft import Aircraft
from aircraft_group import AircraftGroup
from geometry.geometry import Geometry
from geometry.lifting_surface_geometry import LiftingSurfaceGeometry
from geometry.body_geometry import BodyGeometry
from geometry.part_geometry import PartGeometry
from analyses.analyses import Analyses
from aerodynamics.aerodynamics import Aerodynamics



from turbofan.group_thrust import TurbofanGroup
from weights.group_weight import weightGroup
from cost.group_cost import CostGroup
from group_weight_cost import weight_cost




n = 1
shape = (n,)

geometry = Geometry()

geometry.add(LiftingSurfaceGeometry(
    name='wing',
    lift_coeff_zero_alpha=0.23,
))
geometry.add(LiftingSurfaceGeometry(
    name='tail',
    dynamic_pressure_ratio=0.9,
))
geometry.add(BodyGeometry(
    name='fuselage',
    fuselage_aspect_ratio=10.,
))
geometry.add(PartGeometry(
    name='balance',
    parasite_drag_coeff=0.006,
))
# 
analyses = Analyses()
aerodynamics = Aerodynamics()
analyses.add(aerodynamics)
# 
aircraft = Aircraft(
    geometry=geometry,
    analyses=analyses,
    aircraft_type='transport',
)


prob = Problem()
comp = IndepVarComp()
#comp.add_output('altitude_km', val=7,units='km')
comp.add_output('speed', val=250., shape=shape,units='m/s')
comp.add_output('altitude', val=11., shape=shape)
comp.add_output('mean_chord',val=1, units='m')
comp.add_output('alpha', val=3. * np.pi / 180., shape=shape)
comp.add_output('wing_area',val=427.8,units='m**2')
comp.add_output('wing_span',val=44, units='m')
prob.model.add_subsystem('opt_input_comp', comp, promotes=['*'])


comp = IndepVarComp()
comp.add_output('ref_area', val=427.8, shape=shape)
comp.add_output('ref_mac', val=7., shape=shape)
comp.add_output('drag',val=44000, units='kN')

prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])


comp = IndepVarComp()
comp.add_output('large_production_quentity',val=1600)#constant production plan in 10 years (1600)
comp.add_output('learning_curve',val=0.8)        #constant learning curve effect 60%~95%
comp.add_output('mission_year',val=100)    #constant missions per year
        
comp.add_output('passenger',val=400)
comp.add_output('ticket_price',val=150)

comp.add_output('R',val=700,units='NM') #range
comp.add_output('payload_weight',val=4400, units='kg')
comp.add_output('crew_weight',val=4400, units='kg')
#comp.add_output('empty_weight_fraction',val=0.4)

comp.add_output('A', val=8.) ## still need to fix these values #Modeling Constants
comp.add_output('B', val=0.2)#Modeling Constants
comp.add_output('n', val=8.)#Modeling Constants
comp.add_output('k', val=0.2) #Modeling Constants

comp.add_output('MHFH', val=10) ## Maintaince Hour Per Flight Hour
comp.add_output('M_max', val=0.83) ## Engine max mach number
comp.add_output('T_max', val=7440, units='kN') ## Engine max Thrust
comp.add_output('EN', val=500 * 2) ## Engine Number
comp.add_output('FH', val=3500, units='h') ###flight hour
comp.add_output('FTA', val=3) ###FTA flight test
comp.add_output('Q', val=500) ### Less number production
comp.add_output('Tinlet', val = 3303, units='K') ## Turbine inlet temperature

prob.model.add_subsystem('constants', comp, promotes=['*'])

aircraft_group = AircraftGroup(shape=shape, aircraft=aircraft)
prob.model.add_subsystem('aircraft_group', aircraft_group, promotes=['*'])

group = TurbofanGroup(shape=shape)
prob.model.add_subsystem('propulsion_group', group, promotes=['*'])

group = weight_cost()

#prob.driver = ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'SLSQP'
#prob.driver.options['tol'] = 1e-15
#prob.driver.options['disp'] = True

prob.setup(check=True)
prob['wing_geometry_group.area'] = 427.8
prob['wing_geometry_group.wetted_area'] = 427.8 * 2.1
prob['wing_geometry_group.characteristic_length'] = 7.
prob['wing_geometry_group.sweep'] = 31.6 * np.pi / 180.
prob['wing_geometry_group.incidence_angle'] = 0.
prob['wing_geometry_group.aspect_ratio'] = 8.68
prob['wing_geometry_group.mac'] = 7.

prob['tail_geometry_group.area'] = 101.3
prob['tail_geometry_group.wetted_area'] = 101.3 * 2.1
prob['tail_geometry_group.characteristic_length'] = 5.
prob['tail_geometry_group.sweep'] = 35. * np.pi / 180.
prob['tail_geometry_group.incidence_angle'] = 0.
prob['tail_geometry_group.aspect_ratio'] = 4.5
prob['tail_geometry_group.mac'] = 5.

prob['fuselage_geometry_group.wetted_area'] = 73 * 2 * np.pi * 3.1
prob['fuselage_geometry_group.characteristic_length'] = 73.
prob.run_model()
prob.model.list_outputs(prom_name=True)
#prob.run_driver()

prob.check_partials(compact_print=True)



#### add solver for coupled groups for values Keeps feeding until converge
#### two groups coupled wherever they are called: 
#two groups being solved: d1 d2
# add the usb system groups and then add the solver block immediately after
# make non linear solver own group
# two groups that are coupled => create seperate group

#abs relative error numb is very smoll