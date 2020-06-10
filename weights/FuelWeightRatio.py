import numpy as np  
from openmdao.api import ExplicitComponent


class FuelWeightRatio(ExplicitComponent):




    def setup(self):
        self.add_input('R')
        self.add_input('specific_fuel_consum')
        self.add_input('LD')
        self.add_input('speed')


        self.add_output('Wfr')

        self.declare_partials('Wfr', 'speed')
        self.declare_partials('Wfr', 'LD')
        self.declare_partials('Wfr', 'specific_fuel_consum')

    def compute(self, inputs, outputs):
  
        R=inputs['R']
        SFC = inputs['specific_fuel_consum']
        LD = inputs['LD']
        V = inputs['speed']
     

        outputs['Wfr'] = 1-np.exp(-(9.807*R*SFC/(V*LD)))
        
    def compute_partials(self, inputs, partials):
   
        R=inputs['R']
        SFC = inputs['specific_fuel_consum']
        LD = inputs['LD']
        V = inputs['speed']
        

        partials['Wfr', 'speed'] = ((-1/LD)*R*(SFC/V**2))*np.exp(-1/LD*R*SFC/V)
        partials['Wfr', 'LD'] = ((-R*SFC/LD**2)/V)*np.exp(-1/LD*R*SFC/V)
        partials['Wfr', 'specific_fuel_consum'] =-((-1/LD)*R/V)*np.exp(-1/LD*R*SFC/V)
