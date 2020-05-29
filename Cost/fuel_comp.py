import numpy as np

from openmdao.api import ExplicitComponent


class FuelComp(ExplicitComponent):

    def initialize(self):
        

    def setup(self):
        self.add_input('We')
        self.add_input('SFC')
        self.add_output('Fuel')

        self.declare_partials('Fuel', 'We')
        self.declare_partials('Fuel', 'SFC')

    def compute(self, inputs, outputs):
        
        We = inputs['We']
        SFC = inputs['SFC']

        outputs['Fuel'] = 

    def compute_partials(self, inputs, partials):

        We = inputs['We']
        SFC = inputs['SFC']
        
        partials['Fuel', 'We'] = 
        partials['Fuel', 'SFC'] = 
