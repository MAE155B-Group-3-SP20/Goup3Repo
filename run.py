import numpy as np
import openmdao.api as om
from openmdao.api import Problem, IndepVarComp, ScipyOptimizeDriver
from powertrain.powertrain import Powertrain
from powertrain.powertrain_group import PowertrainGroup


from aircraft import Aircraft
from aircraft_group import AircraftGroup
from geometry.geometry import Geometry
from geometry.lifting_surface_geometry import LiftingSurfaceGeometry
from geometry.body_geometry import BodyGeometry
from geometry.part_geometry import PartGeometry
from analyses.analyses import Analyses
from aerodynamics.aerodynamics import Aerodynamics


from group_aero import AeroGroup
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
comp.add_output('speed', val=250., lower=200., upper = 300.) # units='m/s' , val=250.
comp.add_output('altitude',  val=7., lower=4., upper = 14.)# units = 'km' , val=7
comp.add_output('ref_mac', val=7., lower=4., upper = 14.) # , val=7.
comp.add_output('alpha', val=3. * np.pi / 180., lower=0.* np.pi / 180., upper = 5.* np.pi / 180.)# , val=3. * np.pi / 180.
comp.add_output('ref_area', val=427.8,lower=200., upper = 800.) # , val=427.8
comp.add_output('empty_weight_fraction',val=0.5,lower=0.45, upper =0.55)
prob.model.add_subsystem('opt_input_comp', comp, promotes=['*'])

comp = IndepVarComp()
comp.add_output('large_production_quentity',val=1600)#constant production plan in 10 years (1600)
comp.add_output('learning_curve',val=0.8)        #constant learning curve effect 60%~95%
comp.add_output('mission_year',val=100)    #constant missions per year   
comp.add_output('passenger',val=400)
comp.add_output('ticket_price',val=100)
#fix these?
comp.add_output('R',val=1300,units='km') #range
comp.add_output('payload_weight',val=44000, units='kg')
comp.add_output('crew_weight',val=1100, units='kg')
## fix these 
comp.add_output('A', val=0.222) ## still need to fix these values #Modeling Constants
comp.add_output('n', val=-0.6)#Modeling Constants
## Below prob okay
comp.add_output('specific_fuel_consum', val=0.0087, units= 'kg/(kN*s)') #dependent on engine General_Electric_CF6
comp.add_output('MHFH', val=10) ## Maintaince Hour Per Flight Hour
comp.add_output('M_max', val=0.83) ## Engine max mach number
comp.add_output('T_max', val=310, units='kN') ## Engine max Thrust
comp.add_output('EN', val= 2) ## Engine Number
comp.add_output('FH', val=3500, units='h') ###flight hour
comp.add_output('FTA', val=3) ###FTA flight test
comp.add_output('Q', val=500) ### Less number production
comp.add_output('Tinlet', val = 3303, units='K') ## Turbine inlet temperature
prob.model.add_subsystem('constants', comp, promotes=['*'])


########## Leave below commented ###########
aircraft_group = AircraftGroup(shape=shape, aircraft=aircraft)
prob.model.add_subsystem('aircraft_group', aircraft_group, promotes=['*'])
########## Leave above commented ###########


group = AeroGroup(shape=shape)
prob.model.add_subsystem('drag_lift_group', group, promotes=['*'])

group = TurbofanGroup(shape=shape)
prob.model.add_subsystem('propulsion_group', group, promotes=['*'])

group = weightGroup()
prob.model.add_subsystem('weight_group', group, promotes=['*'])

group = CostGroup()
prob.model.add_subsystem('cost_group', group, promotes=['*'])

prob.model.add_design_var('speed', lower=200., upper = 300.) # units='m/s' , val=250.
prob.model.add_design_var('altitude',lower=4000., upper = 14000.)# units = 'km' , val=7
prob.model.add_design_var('ref_mac', lower=4., upper = 14.) # , val=7.
prob.model.add_design_var('alpha', lower=0., upper = 5.* np.pi / 180.)# , val=3. * np.pi / 180.
prob.model.add_design_var('ref_area',lower=200., upper = 800.) # , val=427.8
prob.model.add_design_var('empty_weight_fraction',lower=0.45, upper =0.55)

prob.model.connect('aerodynamics_analysis_group.drag_coeff','drag_coeff')
prob.model.connect('aerodynamics_analysis_group.lift_to_drag_ratio','lift_to_drag_ratio')
#prob.driver = ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'SLSQP'
#prob.driver.options['tol'] = 1e-15
#prob.driver.options['disp'] = True

prob.setup(check=True)


########## Leave below commented ###########
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

prob['balance_geometry_group.wetted_area'] =  427.8 * 2.1
prob['balance_geometry_group.characteristic_length'] = 7. ## potentially wing and likely wign
########## Leave above commented ###########

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
