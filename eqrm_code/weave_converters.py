from scipy.weave import converters, blitz_spec
import numpy


class memmap_converter(blitz_spec.array_converter):

    """
    A numpy.memmap type converter for weave.

    As memmap is an ndarray-type object this subclasses the array_converter
    from blitz_spec and assigns memmap as the matching type.
    """

    def init_info(self):
        blitz_spec.array_converter.init_info(self)
        self.matching_types = [numpy.memmap]

# Use the blitz converters already used for weave inlines
# and add to start of list so we don't get the catchall
eqrm = [memmap_converter()] + converters.blitz
