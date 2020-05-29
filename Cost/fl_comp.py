from openmdao.api import ExplicitComponent


class FlyawayComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('Q', types=float)
        
    def setup(self):
        self.add_input('We')
        self.add_input('V')
        self.add_input('Tmax')
        self.add_input('Mmax')

        self.add_output('Flyaway')

        self.declare_partials('Flyaway', 'We')
        self.declare_partials('Flyaway', 'V')
        self.declare_partials('Flyaway', 'Tmax')
        self.declare_partials('Flyaway', 'Mmax')

    def compute(self, inputs, outputs):
        We = inputs['We']
        V = inputs['V']
        Tmax = inputs['Tmax']
        Mmax = inputs['Mmax']

        outputs['Flyaway'] = 

    def compute_partials(self, inputs, partials):
        Q = self.options['Q']
        We = inputs['We']
        V = inputs['V']
        Tmax = inputs['Tmax']
        Mmax = inputs['Mmax']

        partials['Flyaway', 'We'] = 
        partials['Flyaway', 'V'] = 
        partials['Flyaway', 'Tmax'] = 
        partials['Flyaway', 'Mmax'] = 
