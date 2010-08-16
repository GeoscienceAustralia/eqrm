"""
 Title: equivalent linear solver.py
  
  Author:  Peter Row, peter.row@ga.gov.au


  Description: Equivalent linear solver.  Used by capacity_spectrum_model
  

  Version: $Revision: 1144 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-09-18 17:10:15 +1000 (Fri, 18 Sep 2009) $
"""

from eqrm_code.util import dict2csv  
from scipy import nan_to_num, where, array, zeros, indices, ndarray

def solve(SA,SD,SAcap,update_function,rtol=0.05,maxits=100):
    """
    #FIXME DSG-EQRM what is the dimensions of these, and the return value?
    SA = demand curve (g)
    SAcap = capacity curve (g)
    SD = x axis (for both capcity and demand) (mm)

    update_function(intersection_point.x) makes a new SA,SD,SAcap.
    it also returns an exit flag
    it is usaully (always?)
    eqrm_code.capacity_spectrum_model.Capacity_spectrum_model.updated_responce

    rtol of 0.05 process will halt if intersection_x moved by
    less than 5% in the last iteration. All points are deemed to
    have converged. 

    maxits is the maximum iterations. If maxits is exceeded, then
    any points that are not yet deemed to have converged are set
    to (intersection_x + old_intersection_x)/2
    """
    # old terminology, SDcr was intersection_x
    iters=0
    intersection_x=find_intersection(SD,SA,SAcap)
    exit_flag=False
    while ((iters<=maxits)&(not exit_flag)):
        #if 1:
        #if iters>0:
        #    #print 'iter'
        #    print iters
        iters+=1 # update number of iterations
        old_intersection_x=intersection_x.copy() # copy old intersection
        #print "SAcap", SAcap[0][0][0:6]
        #print "SA",SA[0][0][0:6]
        #print "SD", SD[0][0][0:6]
        #print "intersection_x", intersection_x
        if False: # Note, this is a hack.  For one event, one site examples
            attribute_dic = {'SA(g)':SA.tolist()[0][0],
                             'SD(mm)':SD.tolist()[0][0],
                             'SAcap(g)':SAcap.tolist()[0][0]}
            title_index_dic = {'SA(g)':0,
                             'SD(mm)':1,
                             'SAcap(g)':2} 
            dict2csv('csm_internal'+str(iters)+'.csv', title_index_dic, attribute_dic)
        SA,SD,SAcap,exit_flag=update_function(intersection_x) # update curves
       
        intersection_x=find_intersection(SD,SA,SAcap) # get new intersection
        diff=abs(intersection_x-old_intersection_x)/old_intersection_x # diff
        # This is needed in windows to stop nan's setting the diff to -1.#IND
        diff=nan_to_num(diff)
        max_diff=diff.max() # find the relative change in intersection_x
        if max_diff<rtol:
            exit_flag=True # check for convergence

    if (iters >= maxits): 
        # if iteration doesn't converge, take the average value
        # use average values 
        non_convergent=where(diff>=rtol) # find non_convergent cases
        # x = (x+x_old)/2
        intersection_x[non_convergent]+=old_intersection_x[non_convergent]
        intersection_x[non_convergent]*=0.5
    else: non_convergent=array([])
    return intersection_x,non_convergent

############################################################################
# The rest of the code just finds the (interpolated) intersection point
# of Y1,Y2,X. It looks like a good candidate for porting to c - it may
# actually be simpler in c than in its current vectorized form.
############################################################################
# def new_find_intersection(SD,SA,SAcap):
#     # Note, this doesn't yet work.
#     num_sites,num_events,num_periods=SA.shape
#     assert SA.shape==SD.shape
#     assert SA.shape==SAcap.shape
#     SDcr=zeros((num_sites,num_events),dtype=float)

    
#     try:
#         from scipy import weave
#         from scipy.weave import converters
#         code="""
#         double SDout,y1,y0,x1,x0,dx,dy;
#         int i,j,k,k0,k1;
#         for (i=0;i<num_sites;++i){
#             for (j=0;i<num_events;++j){
#                 for (k=0;k<num_periods;++k){                
#                     if (SAcap(i,j,k) > SA(i,j,k)){
#                         break;
#                     }
#                 }
#                 if (k==0){
#                     SDout=SD(i,j,0);
#                 }
#                 else if (k==num_periods){
#                     SDout=SD(i,j,0);
#                     for (k=1;k<num_periods;++k){
#                         if (SD(i,j,k) > SDout){
#                             SDout=SD(i,j,k);
#                         }
#                     }
#                 }
#                 else{
#                     k1=k;
#                     k0=k1-1;
#                     x0=SD(i,j,k0);
#                     x1=SD(i,j,k1);
#                     if (x1==x0){
#                         SDout=x0;
#                     }
#                     else{
#                         y0=SA(i,j,k0)-SAcap(i,j,k0);
#                         y1=SA(i,j,k1)-SAcap(i,j,k1);
#                         dx=x1-x0;
#                         dy=y1-y0;
#                         SDout=x1-(y1*(dx/dy));
#                     }
#                 }
#                 SDcr(i,j)=SDout;
#             }
#         }   
#         """
#         weave.inline(code,
#                      ['SD','SA','SAcap','SDcr',
#                       'num_sites','num_events','num_periods'],
#                      type_converters=converters.blitz,
#                      compiler='gcc')
#     except:
#         print 'Slow, running equevalent linear solver in python'
#         for i in range(num_sites):
#             for j in range(num_events):
#                 for k in range(num_periods):
#                     if SAcap[i,j,k]>SA[i,j,k]:
#                         break
#                     k=k+1
#                 if k==0:
#                     SDout=SD[i,j,0]
#                 elif k==num_periods:
#                     SDout=SD[i,j,0]
#                     for k in range(1,num_periods):
#                         if SD[i,j,k]>SDout:
#                             SDout=SD[i,j,k]
#                 else:
#                     k1=k
#                     k0=k1-1
#                     x0=SD[i,j,k0]
#                     x1=SD[i,j,k1]
#                     if x1==x0:
#                         SDout=x0
#                     else:
#                         y0=SA[i,j,k0]-SAcap[i,j,k0]
#                         y1=SA[i,j,k1]-SAcap[i,j,k1]
#                         dx=x1-x0
#                         dy=y1-y0
#                         # interpolate SD
#                         SDout=x1-y1*(dx/dy)
#                 SDcr[i,j]=SDout
#     return SDcr


def findfirst(condition,axis=-1,no_intersection=-1):
    """
    Condition is an array of true/false values
    
    Get the indexes where condition is true, the first time on the axis

    If the condition is all false, return no_intersection (default -1)
    If the condition is all true, return 0 (obviously - it has already met)

    returns an array of 1 less dimension (the axis dimension collapses)
    (or maybe a int32scalar if it collapses completely
    """
    # Try to find the first index where condition is true:
    # (note argmax will return as 0 if the condition is
    #  false for the whole axis)
    first_index=(condition.argmax(axis=axis))

    if isinstance(first_index,int): # if it collapsed
        if condition.max()==0:
            first_index=no_intersection
        first_index=array((first_index,)) # return an array
    else:
        first_index[where(~condition.max(axis=axis))]=no_intersection
        # Where it is all false, return no_intersection
        # (this happens if the building is flattened by the quake)
    return first_index

def get_intersection_indices(condition,axis=-1):
    """
    In case you want to modify the indicies that get returned
    (which is not too likely), see caveat (in the code).
    """
    n=condition.shape[axis]
    id1=findfirst(condition,axis=axis,no_intersection=n)
    # get the first point where SA > SAcap
    if id1.shape==(1,): # if it has collapsed
        if id1==0:id1[:]=1
        id0=id1-1
        #if id1==0:id0[:]=0 # no nves
        if id1==n: id1[:]=n-1
        return id0,id1
    else:
        id1[where(id1==0)]=1
        
        id0=id1-1 # make id0 the point below, id1 is the point above  
        id1[where(id1==n)]=n-1
        #id0[where(id1==0)]=0 # no -ves
        
        # Make the indices for the other axis:
        indices_0=indices(id0.shape) # make indices for the boring axes
        indices_0=list(indices_0)
        indices_1=indices_0[:] # copy the list
        # CAVEAT:
        # In case you want to modify the indicies that get returned
        # (which is not too likely), note that other than on axis,
        # the indices are the same objects.

        # insert the interesting axis into the correct axis:
        if axis<0: axis=len(condition.shape)+axis
        indices_0.insert(axis,id0)
        indices_1.insert(axis,id1)

        indices_0=tuple(indices_0)
        indices_1=tuple(indices_1)
        return indices_0,indices_1

def get_interpolated_SD(SD,SAdiff,id0,id1):
    # Select points for interpolation:
    x0=SD[id0]
    y0=SAdiff[id0]
    x1=SD[id1]
    y1=SAdiff[id1]
    dx=x1-x0
    dy=y1-y0
    
    # interpolate SD
    SDcr=x1-y1*(dx/dy)
    return SDcr

def find_intersection(SD,SA,SAcap,axis=-1):
    """
    SDcr - critical Spectral displacement - where they intersect - is returned
    """
    #SDmax=SD.max(axis=axis)

    id0,id1=get_intersection_indices(condition=(SA<SAcap),axis=axis)
    # Note, I use id1,id0. Matlab uses newidx,newidx1 respectivly.
    
    SDcr=get_interpolated_SD(SD,SA-SAcap,id0,id1)
    # curve may be flat if index is zero (demand is saturated), or
    # if index is n (capacity is saturated). In other cases, it
    # won't be flat - or findfirst wouldn't have returned it.
    if isinstance(id0,ndarray): # if it is a single ndarray, not a tuple
        n=SD.shape[axis]
        if id0==id1:
            if id0==0: SDcr[:]=SD[0]
            if id0==n-1: SDcr[:]=SD.max()
    else:
        # where id0 == id1, SDcr should be set equal to SD[id0].
        curve_flat=where(id1[axis]==id0[axis])

        #SDcr[[curve_flat]]=SD[tuple([i[curve_flat] for i in id0])]
        SDcr[curve_flat]=SD.max(axis)[curve_flat]
        # curve_flat prob' index to event
        # Note:
        # [SDcr] = site,event
        # [SD] = site,event,period
        # [id0[axis]] = [findfirst(condition,axis=axis)] = site,event
        # [id0] = 3,site,event
        
    if len(SD.shape)==1:
        SDcr=SDcr[0] # collapse
        
    if not ((len(SDcr.shape)==len(SD.shape)-1)
            and (SDcr.shape==SD.shape[:-1])):    
            print 'Wrong shape!'
            print SDcr.shape,SD.shape
            raise Exception        
    return SDcr
