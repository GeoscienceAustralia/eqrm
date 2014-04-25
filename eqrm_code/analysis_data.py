"""
analysis_data.py
A class to hold data objects used in analysis.py
"""

from eqrm_code import file_store


class Analysis_Data(file_store.File_Store):

    def __init__(self):
        super(Analysis_Data, self).__init__('analysis_data')

    def __del__(self):
        super(Analysis_Data, self).__del__()

    # PROPERTIES #
    # Define getters and setters for each attribute to exercise the
    # file-based data structure
    bedrock_hazard = property(
        lambda self: self._get_file_array('bedrock_hazard'),
        lambda self, value: self._set_file_array('bedrock_hazard', value))

    soil_hazard = property(lambda self: self._get_file_array('soil_hazard'),
                           lambda self, value: self._set_file_array('soil_hazard', value))

    bedrock_SA_all = property(
        lambda self: self._get_file_array('bedrock_SA_all'),
        lambda self, value: self._set_file_array('bedrock_SA_all', value))

    soil_SA_all = property(lambda self: self._get_file_array('soil_SA_all'),
                           lambda self, value: self._set_file_array('soil_SA_all', value))
