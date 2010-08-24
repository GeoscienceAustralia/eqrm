
class A(object):
    def dis(self, depth, vs30):
        self.depth = depth
        self.vs30 = vs30
        print "A done"

        
class B(object):
    def dis(self, depth, mg):
        self.depth = depth
        self.mg = mg
        print "B done"


class A1(object):
    def dis(self, **kwargs):
        self.depth = kwargs['depth']
        self.vs30 = kwargs['vs30']
        print "A done"
        
class B1(object):
    def dis(self, **kwargs):
        self.depth = kwargs['depth']
        self.mg = kwargs['mg']
        print "B done"
        
class Dummy:
    def __init__(self):
        pass
    
if __name__ == '__main__':
    from eqrm_code.exceedance_curves import do_collapse_logic_tree
    from scipy import allclose, array, sum, resize, zeros
    import util
    from os import getcwd, chdir
    from os.path import join
    
    if False:
        retcode = 0 
        retcode = util.run_call(join('eqrm_code','test_all.py'))
        print "retcode", retcode
       
    if True: 
        retcode = 0 
        current_dir = getcwd()
        chdir(join(util.determine_eqrm_path(), 'demo'))
        
        retcode += util.run_call(join('demo','demo_batchrun.py'))
        if retcode == 0:
            print "Pass"
        else:
            print "Fail"
        
