import numpy as np

from openmdao.api import ExplicitComponent


class RDTEComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('Q', types=float)
        self.options.declare('FTA', types=float)

    def setup(self):
        self.add_input('We')
        self.add_input('V')
        self.add_output('RDTE')

        self.declare_partials('RDTE', 'We')
        self.declare_partials('RDTE', 'V')

    def compute(self, inputs, outputs)

        We = inputs['We']
        V = inputs['V']

        outputs['RDTE'] = 

    def compute_partials(self, inputs, partials):
        Q = self.options['Q']
        FTA = self.options['FTA']

        We = inputs['We']
        V = inputs['V']

        partials['RDTE', 'We'] = 
        partials['RDTE', 'V'] =  
