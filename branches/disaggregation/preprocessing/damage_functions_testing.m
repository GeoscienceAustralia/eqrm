
cd R:\earthquake\sandpits\prow\eqrm\eqrm_app\m_code\vuln;
t_all=[0.1,0.3,2.0,10.0,30.0];
aus_mag=[6.0;7];
nevents=length(aus_mag);
Tm=repmat(t_all, nevents, 1);
nper=length(t_all);
SA=[0.01 ,0.1 ,.05 ,100 ,1;0.01 ,0.1 ,.2 ,10 ,1];
THE_PARAM_T=struct('damp_flags',[0,1,0],'resp_crv_flag',0);
SELECT_RC_T = select_resp_curve(t_all,SA,aus_mag,Tm,nper,THE_PARAM_T)
% Break and get the variables out

SA=SELECT_RC_T.SA;
SD=SELECT_RC_T.SD;
Beff=[0.05;0.05]
TAV=SELECT_RC_T.TAV;
TVD=SELECT_RC_T.TVD;
damp_flags=[0,1,1]
[SDnew, SAnew, Rfact,TAV]=update_demand(t_all, SD, SA, Beff, TAV, TVD, damp_flags)


nevents=1
nper=5
numsites=2
design_strength=([0.077;0.063])*ones(nevents,1); % C
natural_elastic_period=([0.275;0.32])*ones(nevents,1); % T
fraction_in_first_mode=([0.9;0.9])*ones(nevents,1); % alpha1
height_to_displacement=([0.7;0.7])*ones(nevents,1); % alpha2
yield_to_design=([1.75;1.75])*ones(nevents,1); % gamma
ultimate_to_yield=([2;2])*ones(nevents,1); % plank
ductility=([7;7])*ones(nevents,1); % u

Ay=design_strength.*yield_to_design./fraction_in_first_mode
Dy=1000/(4*pi^2)*9.8.*Ay.*(natural_elastic_period.^2)        
Au=ultimate_to_yield.*Ay        
Du=ultimate_to_yield.*ductility.*Dy
cc=Ay
bb=(Ay./Dy)./(Au-Ay)
aa=(Ay-Au).*exp(bb.*Dy)

Ay=repmat(Ay, 1, nper)
Dy=repmat(Dy, 1, nper);
Au=repmat(Au, 1, nper);
Du=repmat(Du, 1, nper);
cc=repmat(cc, 1, nper);
bb=repmat(bb, 1, nper);
aa=repmat(aa, 1, nper);

SaCap = buildcap_rand(SDnew, Dy, Ay, Du, Au, aa, bb, cc)


