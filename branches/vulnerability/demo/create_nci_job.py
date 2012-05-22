from eqrm_code.nci_utils import create_nci_job
from optparse import OptionParser

if __name__ == '__main__':
    # Command line options
    parser = OptionParser()
    parser.add_option('-n', '--nodes', 
                      dest='nodes', help='Number of nodes to use at NCI')
    parser.add_option('-p', '--parameter_file',
                      dest='parameter_file', help='Parameter file to use')
    (options, args) = parser.parse_args()
    
    create_nci_job(int(options.nodes), str(options.parameter_file))
