from scipy import array

class A(object):
    def dis(self, depth, Vs30):
        self.depth = depth
        self.Vs30 = Vs30
        print "A done"

        
class B(object):
    def dis(self, depth, mg):
        self.depth = depth
        self.mg = mg
        print "B done"


class A1(object):
    def dis(self, **kwargs):
        self.depth = kwargs['depth']
        self.Vs30 = kwargs['Vs30']
        print "A done"
        
class B1(object):
    def dis(self, **kwargs):
        self.depth = kwargs['depth']
        self.mg = kwargs['mg']
        print "B done"
        
class Dummy:
    def __init__(self):
        pass

def sunny(a, b, c=3):
    assert a == 1
    assert b == 2
    assert c == 3
    print "a", str(a)
    print "b", str(b)
    print "c", str(c)

def dark(a, b, c):
    assert a == 1
    assert b == 2
    assert c == 3
    print "a", str(a)
    print "b", str(b)
    print "c", str(c)
    
def three(a, b=1, **kwargs):
    c = kwargs["c"]
    assert a == 1
    assert b == 2
    assert c == 3
    print "3 a", str(a)
    print "3 b", str(b)
    print "3 c", str(c)
    
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
       
    if False: 
        retcode = 0 
        current_dir = getcwd()
        chdir(join(util.determine_eqrm_path(), 'demo'))
        
        retcode += util.run_call(join('demo','demo_batchrun.py'))
        if retcode == 0:
            print "Pass"
        else:
            print "Fail"
        
    if False: #True:
        sunny(1,2,3)

        q = {'a':1,'b':2,'c':3}
        sunny(**q)

        q = {'b':2,'c':3}
        sunny(1,**q)
        dark(1,**q)
        
        q = {'b':2}
        sunny(a=1, c=3 ,**q)
        
        q = {'b':2}
        three(a=1, c=3 ,**q)
        
        # Below is invalid
        # TypeError: sunny() got an unexpected keyword argument 'y'
        #q = {'z':2,'y':3}
        #sunny(1,**q)
        #dark(1,**q)
        # Below is invalid
        #q = {'b':2}
        #sunny(1,**q, c=3)

    if True:
        a = array([[[0],[1]],
                   [[2],[3]],
                   [[4],[5]]])
        print "a.shape", a.shape
        b = a.reshape((-1,))
        print "b", b
        c = b.reshape(3,2,1)
        print "c", c
        
