# EQSANS reduction script
# Edited by C. Do on 2014-2-13
import eqsansscript_class_2015Brev1
reload(eqsansscript_class_2015Brev1)
from eqsansscript_class_2015Brev1 import *
# When new configurations (flood, dark, sens) are updated, plan is to have different files with 'rev' 
# For example, eqsansscript_class_2014A_rev1 
#############################################


############
#Examples###
############
# ReduceEQSANS_Single(user)   ## for single data reduction with specified name
# ReduceEQSANS_List(user) ## for multiple data reduction with run numbers as file names

##################
# user variables #
#################################
# Variable name = Default values#
#################################
# FluxMonRatioFile = "/SNS/EQSANS/IPTS-8057/shared/flux_mon_ratio_2.nxs"
# NormalizationChoice = "TotalCharge"

# OutputPathName = "/SNS/EQSANS/IPTS-10068/shared/" 
# OutputFileName = 'default_output.txt'

# DetectorTubeFlag = True # True: Yes tube detector
# ThetaTrans = True # True: perform theta dependent correction
# UseDefaultTOF = True # True: use default TOF cut (500, 2000)
# Cut_i = 0 # Min TOF cut
# Cut_f = 0 # Max TOF cut 
# UseDefaultMask = True # Yes, use the default mask
# MaskChoice = 'Mask_BS60_4m'

# SampleAP = 10 # Diameter of Sample Aperture for Resolution
# UseFlightPathCorrection = True # True: perform correction

# Flood_Min = 0.4 # Min value of sensitivity
# Flood_Max = 2 # Max value of sensitivity

# Trans_Radius = 5 # Use 5 pixel radius for transmission calculation
# UseFitTrans = True # True: fitted transmission for sample
# SampleTransVal = 1.0
# UseCombinedTransFit = False # False: Each wavelength band trans is fitted independently. Only for frame-skipping mode
# UseBckCorrection = True # True if you want to perform background subtraction
# UseFitBckTrans = True # True: fitted transmission for background
# BckTransVal = 1.0

# Nbins = 200 # Default is 128
# Nbins_XY = 100 # for QxQy 2D Plot
# UseLogBin = False # Use Linear Binning by default

# AbsScale = 1.0
# Thickness = 0.1
# WaveStep = 0.1
# EmptyBeam = '36378'
# EmptyBeamTrans = EmptyBeam
# BackScatt = "36392"
# BackTrans = "36379"
# SamScattList = ['36393']
# SamTransList = ['36380']

#######################################
# Available Masks for user.MaskChoice #
#######################################
# Mask_BS30_1o3m_MB
# Mask_BS30_1o3m
# Mask_BS60_4m
# Mask_BS60_4m_MB
# Mask_BS60_4o5m
# Mask_4m10A
# Mask_5m10A
#######################################


###############################################
# Available Sensitivities for user.SensChoice #
###############################################
# Sens_1o3m  
# Sens_2o5m 
# Sens_4m
# Sens_4mmono 
###############################################


#####################################################################
# TIP: Use following command to reset all the parameters to default #
# user = EQVar()                                                    #
#####################################################################




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

