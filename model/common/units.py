from pint import UnitRegistry

ureg = UnitRegistry()
ureg.load_definitions('input/units.txt')

class Quantity:
    
    def __init__(self, params):
        self.params = params
    
    def __call__(self, *args, only_magnitude=True):
        """Usage:
        - Quant(string, to_unit):        Quant('20 GtCO2/yr', 'emissionsrate_unit')
        - Quant(value, unit, to_unit):   Quant(20, 'GtCO2/yr', 'emissionsrate_unit')
        """

        if len(args) not in [2, 3]: # If number of arguments is not 2 or 3
            raise RuntimeError("Incorrect number of arguments to Q")

        if (args[0] is False): # Sometimes a quantity (like carbon budget) can be skipped by setting to False
            return False

        # First parse target units with default units
        target_unit = self._parse_default_units(self._custom_replace(args[-1]))

        if len(args) == 2:
            string = self._custom_replace(str(args[0]))
            quantity = ureg.Quantity(string)
        elif len(args) == 3:
            value = args[0]
            unit = self._custom_replace(str(args[1]))
            quantity = ureg.Quantity(value, unit)
        else:
            raise Exception("Wrong usage of Quant function")

        if only_magnitude:
            return quantity.to(target_unit).magnitude
        else:
            return quantity.to(target_unit)

    def __repr__(self):
        units = ', '.join([f'{key}: {value}' for key, value in self.params['default units'].items()])
        return f'Quantity with units: {units}'
    
    
    
    ####### Private functions #######
    
    def _parse_default_units(self, units):
        for key, value in self.params['default units'].items():
            # Add brackets () to avoid order of operation problems with compound units
            units = units.replace(key, f'({value})')
        return units
    
    def _custom_replace(self, units):
        return units.replace('US$', 'USD')