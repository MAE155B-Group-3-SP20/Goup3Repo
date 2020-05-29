from openmdao.api import ExplicitComponent


class MainComp(ExplicitComponent):

    def setup(self):
        self.add_input('We')
        
        self.add_output('Main')

        self.declare_partials('Main', 'We')

    def compute(self, inputs, outputs):
        We = inputs['We']

        outputs['Main'] = 

    def compute_partials(self, inputs, partials):
        We = inputs['We']
        

        partials['We', 'Main'] = 

