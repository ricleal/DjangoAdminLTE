#
# Test script
#

# Edited by C. Do on 2014-2-13
import eqsansscript_class_2015Brev1
reload(eqsansscript_class_2015Brev1)
from eqsansscript_class_2015Brev1 import *


{{title}}

{{ipts}}

{{ configuration.absolute_scale_factor }}

{% for entry in entries %}
    {{ entry.background_scattering}} {{ entry.background_transmission}} {{ entry.empty_beam}}
{% endfor %}

###########################
##### USER EDIT BEGIN #####
###########################
user = EQVar()
user.OutputPathName = "/SNS/EQSANS/IPTS-14455/shared/" 

InstrumentFolder = "/SNS/EQSANS/shared/NeXusFiles/EQSANS/2015B_mp/"
Dark_39388 = InstrumentFolder + "EQSANS_39388_event.nxs"
Dark_39723 = InstrumentFolder + "EQSANS_39723_event.nxs"
Dark_42845 = InstrumentFolder + "EQSANS_42845_event.nxs"
Dark_43373 = InstrumentFolder + "EQSANS_43373_event.nxs"
Dark_45222 = InstrumentFolder + "EQSANS_45222_event.nxs"
Dark_54585 = InstrumentFolder + "EQSANS_54585_event.nxs"
Dark_56973 = InstrumentFolder + "EQSANS_56973_event.nxs"
Dark = Dark_56973

Sens_1o3m = InstrumentFolder + "Sensitivity_patched_thinPMMA_1o3m_30BS_54593_event.nxs"
Sens_1o3mS = InstrumentFolder + "Sensitivity_patched_thinPMMA_1o3m_30BS_56987_event.nxs"
Sens_2o5m = InstrumentFolder + "Sensitivity_patched_thinPMMA_2o5m_56985_event.nxs" 
Sens_4m = InstrumentFolder + "Sensitivity_patched_thinPMMA_4m_58109_event.nxs"
Sens_4m_nopat   = "/SNS/EQSANS/IPTS-14784/data/EQSANS_54587_event.nxs"





#--------------------------------------------------
# 8 m 12A 
#--------------------------------------------------
##### USER EDIT BEGIN #####
user.EmptyBeam = "60239"
user.EmptyBeamTrans = user.EmptyBeam
user.BackScatt = "60258"
user.BackTrans = "60240"
user.SamScattList = ['60259'] # If no data, leave as blank.
user.SamTransList = ['60241']
user.AbsScale = 1
user.Thickness = 0.1
user.Nbins = 200
user.MaskChoice = 'Mask_BS60_8m'
user.SensChoice = Sens_4m
user.DarkChoice = Dark
user.UseDefaultTOF = True
# user.Cut_i = 500 # Min TOF cut
# user.Cut_f = 12500 # Max TOF cut 
user.OutputFileName = 'Porsil_8m12A_raw'
##### USER EDIT END #####
ReduceEQSANS_Single(user)



#--------------------------------------------------
# 4 m 
#--------------------------------------------------
##### USER EDIT BEGIN #####
user.EmptyBeam = "60187"
user.EmptyBeamTrans = user.EmptyBeam
user.BackScatt = "60200"
user.BackTrans = "60188"
user.SamScattList = ['60201'] # If no data, leave as blank.
user.SamTransList = ['60189']
user.AbsScale = 1
user.Thickness = 0.2
user.Nbins = 200
user.MaskChoice = 'Mask_BS60_4m'
user.SensChoice = Sens_4m
user.DarkChoice = Dark
user.UseDefaultTOF = True
# user.Cut_i = 4500 # Min TOF cut
# user.Cut_f = 8500 # Max TOF cut 
user.OutputFileName = 'Porsil_4m2o5A_raw'
##### USER EDIT END #####
ReduceEQSANS_Single(user)


#--------------------------------------------------
# 4 m 
#--------------------------------------------------
##### USER EDIT BEGIN #####
user.OutputPathName = "/SNS/EQSANS/IPTS-14455/shared/tof/" 
user.EmptyBeam = "60187"
user.EmptyBeamTrans = user.EmptyBeam
user.BackScatt = "60200"
user.BackTrans = "60188"
user.SamScattList = ['60207', '60208'] # If no data, leave as blank.
user.SamTransList = ['60195', '60196']
user.AbsScale = 1
user.Thickness = 0.2
user.Nbins = 200
user.MaskChoice = 'Mask_BS60_4m'
user.SensChoice = Sens_4m
user.DarkChoice = Dark
user.UseDefaultTOF = False
user.Cut_i = 500 # Min TOF cut
user.Cut_f = 14000 # Max TOF cut 
user.OutputFileName = 'Si_4m6A_abs_3'
##### USER EDIT END #####
#DeleteWorkspace('60207')
#DeleteWorkspace('60208')
#ReduceEQSANS_List(user)
