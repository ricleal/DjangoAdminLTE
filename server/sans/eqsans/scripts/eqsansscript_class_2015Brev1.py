# EQSANS reduction script
# Edited by C. Do on 2014-10-22
import mantid
from mantid.simpleapi import *
from reduction_workflow.instruments.sans.sns_command_interface import *
config = ConfigService.Instance()
config['instrumentName']='EQSANS'
from datetime import datetime
#INCLUDE: Necessary for creating a mask of back tubes
from numpy import arange

class EQconf(object):
    #create a list of back tubes to mask (Z+ plane on 'Show Instrument' display)

    FluxMonRatioFile = "/SNS/EQSANS/IPTS-8057/shared/flux_mon_ratio_2.nxs"

    alltubes = arange(0,192*256,1)
    alltubes = alltubes.reshape(192/4,256*4)
    mask_backtubes = alltubes[1::2,:]
    mask_backtubes = mask_backtubes.ravel().tolist()

    mask30_ws = Load(Filename="/SNS/EQSANS/shared/NeXusFiles/EQSANS/2015B_mp/beamstop30_mask_1o3m.nxs")
    ws30, masked30_detectors = ExtractMask(InputWorkspace=mask30_ws, OutputWorkspace="__edited_mask30")
    detector_ids30 = [int(i) for i in masked30_detectors]

    mask60_ws = Load(Filename="/SNS/EQSANS/shared/NeXusFiles/EQSANS/2015B_mp/beamstop60_mask_4m.nxs")
    ws60, masked60_detectors = ExtractMask(InputWorkspace=mask60_ws, OutputWorkspace="__edited_mask60")
    detector_ids60 = [int(i) for i in masked60_detectors]
    
    mask90_ws = Load(Filename="/SNS/EQSANS/shared/NeXusFiles/EQSANS/2015B_mp/beamstop90_mask_4m.nxs")
    ws90, masked90_detectors = ExtractMask(InputWorkspace=mask90_ws, OutputWorkspace="__edited_mask90")
    detector_ids90 = [int(i) for i in masked90_detectors]
    
    mask60_8m_ws = Load(Filename="/SNS/EQSANS/shared/NeXusFiles/EQSANS/2015B_mp/beamstop60_mask_8m2.nxs")
    ws60_8m, masked60_8m_detectors = ExtractMask(InputWorkspace=mask60_8m_ws, OutputWorkspace="__edited_mask60_8m")
    detector_ids60_8m = [int(i) for i in masked60_8m_detectors]
    
    # Mask data is supplied by instrument scientist
    # Following four Masks are default ones
    Mask_BS30_1o3m_MB = detector_ids30 + mask_backtubes
    Mask_BS30_1o3m = detector_ids30
    Mask_BS60_4m = detector_ids60
    Mask_BS60_8m = detector_ids60_8m
    Mask_BS60_4m_MB = detector_ids60 + mask_backtubes
    Mask_BS90_4m = detector_ids90
    Mask_BS90_4m_MB = detector_ids90 + mask_backtubes
    
    #_Mask_BS60_4o5m updated on 2014-5-30
    Mask_BS60_4o5m = [24699, 24700, 24701, 24702, 24703, 24704, 24705, 24706, 24707, 24708, 24709, 24710, 24711, 24712, 24713, 23160, 23161, 23162, 23163, 23164, 23165, 23166, 23167, 23168, 23169, 23170, 23171, 23172, 23173, 23174, 23175, 23176, 23177, 23178, 23179, 23180, 23181, 20351, 20352, 21887, 21888, 20357, 20358, 21890, 20359, 21891, 20360, 21892, 20361, 21893, 21894, 21895, 21896, 21897, 20607, 22138, 20608, 22139, 22140, 22141, 20613, 22144, 20614, 22145, 20615, 22146, 20616, 22147, 20617, 22148, 22149, 22150, 22151, 22152, 22153, 22154, 22155, 23418, 23419, 23420, 23421, 23422, 23423, 23424, 23425, 23426, 23427, 23428, 23429, 23430, 23431, 23432, 23433, 23434, 20863, 20864, 20869, 20870, 20871, 20872, 20873, 23672, 22393, 23673, 22394, 23674, 23675, 22395, 23676, 22396, 23677, 22397, 23678, 22398, 23679, 22399, 22400, 23680, 22401, 23681, 22402, 23682, 22403, 23683, 22404, 23684, 22405, 23685, 22406, 23686, 22407, 23687, 22408, 23688, 22409, 23689, 22410, 23690, 23691, 23692, 23928, 23929, 23930, 23931, 23932, 23933, 23934, 23935, 23936, 23937, 23938, 22649, 23939, 22650, 23940, 23941, 22651, 22652, 23942, 22653, 22654, 22655, 22656, 22657, 22658, 22659, 22660, 22661, 22662, 22663, 22664, 22665, 22666, 22667, 22668, 22669, 22670, 22671, 22672, 23943, 23944, 23945, 23946, 21114, 21115, 21119, 21120, 21121, 21122, 21123, 21124, 21125, 21126, 21127, 21128, 21129, 22903, 22904, 22905, 22906, 22907, 22908, 22909, 22910, 22911, 22912, 22913, 22914, 22915, 22916, 22917, 22918, 22919, 22920, 22921, 22922, 22923, 22924, 22925, 22926, 21370, 21371, 21372, 21373, 21374, 21375, 21376, 21377, 21378, 21379, 21380, 21381, 21382, 21383, 21384, 21385, 21386, 21387, 24186, 24187, 24188, 24189, 24190, 24191, 24192, 24193, 24194, 24195, 24196, 24197, 24198, 24199, 24200, 24201, 24443, 24444, 24445, 24446, 24447, 24448, 24449, 24450, 24451, 24452, 24453, 24454, 24455, 24456]

    # mask_total = mask_backtubes + mask_beamstop
    Mask_4m10A = [24705, 24706, 24707, 24708, 23159, 24709, 23160, 24710, 23161, 24711, 23162, 24712, 23163, 23164, 23165, 23166, 23167, 23168, 23169, 23170, 23171, 23172, 23173, 23174, 23175, 23176, 23177, 23178, 23416, 23417, 23418, 23419, 23420, 23421, 23422, 23423, 23424, 23425, 23426, 23427, 23428, 23429, 23430, 23431, 23432, 23433, 23434, 23671, 23672, 23673, 23674, 23675, 23676, 23677, 23678, 23679, 23680, 23681, 23682, 23683, 23684, 23685, 23686, 23687, 23688, 23689, 23690, 23691, 22145, 22146, 22147, 22148, 22149, 22150, 22151, 22392, 22393, 22394, 22395, 22396, 22397, 22398, 22399, 22400, 22401, 22402, 22403, 22404, 22405, 22406, 22407, 22408, 22409, 22410, 23927, 23928, 23929, 23930, 23931, 23932, 23933, 23934, 23935, 23936, 23937, 23938, 23939, 23940, 23941, 23942, 23943, 23944, 23945, 23946, 24184, 24185, 24186, 24187, 24188, 24189, 24190, 24191, 24192, 24193, 24194, 24195, 24196, 24197, 24198, 24199, 22648, 22649, 22650, 24200, 24201, 24202, 22651, 22652, 22653, 22654, 22655, 22656, 22657, 22658, 22659, 22660, 22661, 22662, 22663, 22664, 22665, 22666, 22903, 22904, 22905, 22906, 22907, 22908, 22909, 22910, 22911, 22912, 22913, 22914, 22915, 22916, 22917, 22918, 22919, 22920, 22921, 24449, 24450, 22922, 24451, 22923, 24452, 24453, 24454, 24455, 24456, 21377, 21378, 21379, 21380, 21381, 21382, 21383]

    Mask_5m10A = Mask_BS60_4m + [22139, 22140, 22141, 22142, 22143, 22144, 22390, 22391, 22392, 22393, 22394, 22395, 22396, 22397, 22398, 22399, 22400, 22401, 22646, 22647, 22648, 22649, 22650, 22651, 22652, 22653, 22654, 22655, 22656, 22657, 22901, 22902, 22903, 22904, 22905, 22906, 22907, 22908, 22909, 22910, 22911, 22912, 22913, 23158, 23159, 23160, 23161, 23162, 23163, 23164, 23165, 23166, 23167, 23168, 23169, 23415, 23416, 23417, 23418, 23419, 23420, 23421, 23422, 23423, 23670, 23671, 23672, 23673, 23674, 23675, 23676, 23677, 23678, 23679, 23680, 23681, 23926, 23927, 23928, 23929, 23930, 23931, 23932, 23933, 23934, 23935, 23936, 23937, 24183, 24184, 24185, 24186, 24187, 24188, 24189, 24190, 21370, 21371, 21372, 21373, 21374, 21375, 21376]



class EQVar(object):
    #def __init__(self):

    NormalizationChoice = "TotalCharge"

    OutputPathName = "/SNS/EQSANS/IPTS-10068/shared/" 
    OutputFileName = 'default_output'
    
    Solid = True
    DetectorTubeFlag = True # True: Yes tube detector
    ThetaTrans = True # True: perform theta dependent correction
    UseDefaultTOF = True # True: use default TOF cut (500, 2000)
    Cut_i = 0 # Min TOF cut
    Cut_f = 0 # Max TOF cut 
    UseDefaultMask = True # Yes, use the default mask
    MaskChoice = 'Mask_BS60_4m'
    SensChoice = '/SNS/EQSANS/shared/NeXusFiles/EQSANS/2014B_mp/Sensitivity_patched_thinPMMA_4m_39732_event.nxs'
    DarkChoice = '/SNS/EQSANS/shared/NeXusFiles/EQSANS/2014B_mp/EQSANS_39388_event.nxs'

    SampleAP = 10 # Diameter of Sample Aperture for Resolution
    UseFlightPathCorrection = True # True: perform correction
    
    Flood_Min = 0.4 # Min value of sensitivity
    Flood_Max = 2.5 # Max value of sensitivity
    
    Trans_Radius = 5 # Use 5 pixel radius for transmission calculation
    UseFitTrans = True # True: fitted transmission for sample
    SampleTransVal = 1.0
    UseCombinedTransFit = False # False: Each wavelength band trans is fitted independently. Only for frame-skipping mode
    UseBckCorrection = True # True if you want to perform background subtraction
    UseFitBckTrans = True # True: fitted transmission for background
    BckTransVal = 1.0
    
    Nbins = 200 # Default is 128
    Nbins_XY = 200 # for QxQy 2D Plot
    UseLogBin = False # Use Linear Binning by default
    
    AbsScale = 1.0
    Thickness = 0.1
    WaveStep = 0.1
    EmptyBeam = '36378'
    EmptyBeamTrans = EmptyBeam
    BackScatt = "36392"
    BackTrans = "36379"
    SamScattList = ['36393']
    SamTransList = ['36380']
    ErrorLog = ''
    ReductionLog = ''
    
    
# EmptyBeam, EmptyBeamTrans, BackScatt, BackTrans, SamScattList, SamTransList, AbsScale, Thickness, SensitivityFile, MaskFile, Nbins, OutputPathName, DarkCurrentFile
def ReduceEQSANS_List(UserInput):
    eqc = EQconf()
    numList = 0
    for SamScattNum in UserInput.SamScattList:
        SamScatt = str(SamScattNum)
        SamTrans = str(UserInput.SamTransList[numList])
        print '\nReducing..... S='  +  SamScatt + ' .......with T=' + SamTrans + ' at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        UserInput.ReductionLog = 'Reducing..... S='  +  SamScatt + ' .......with T=' + SamTrans + ' at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        numList = numList +1
        EQSANS()
        if UserInput.Solid:
            print "...Using solid angle correction (default)"
            SolidAngle(detector_tubes = UserInput.DetectorTubeFlag)
        else:
            print "...Turn off solid angle correction"
        # SetWavelengthStep(UserInput.WaveStep)
        DarkCurrent(UserInput.DarkChoice)
        if UserInput.NormalizationChoice == "Monitor":
            BeamMonitorNormalization(eqc.FluxMonRatioFile)
            print '...Using monitor normalization'
        else:
            TotalChargeNormalization()
            print '...Using total charge normalization (default)'
        SetAbsoluteScale(UserInput.AbsScale)
        AzimuthalAverage(n_bins=UserInput.Nbins, n_subpix=1, log_binning=UserInput.UseLogBin)
        IQxQy(nbins=UserInput.Nbins_XY)
        print "...Using mask " ,  UserInput.MaskChoice
        MaskDetectors(eqc.__getattribute__(UserInput.MaskChoice))
        OutputPath(UserInput.OutputPathName)
        if UserInput.UseDefaultTOF:
            UseConfigTOFTailsCutoff(True)
            print "...Using default TOF Cuts (default)"
        else:
            print "...Using custom TOF Cuts  ", UserInput.Cut_i, " and ", UserInput.Cut_f
            UseConfigTOFTailsCutoff(False)
            SetTOFTailsCutoff(UserInput.Cut_i, UserInput.Cut_f)
        UseConfigMask(UserInput.UseDefaultMask)
        Resolution(sample_aperture_diameter= UserInput.SampleAP)
        PerformFlightPathCorrection(UserInput.UseFlightPathCorrection)
        DirectBeamCenter(UserInput.EmptyBeam)
        print "...Using sensitivity: " ,  UserInput.SensChoice
        SensitivityCorrection(UserInput.SensChoice, min_sensitivity= UserInput.Flood_Min, max_sensitivity= UserInput.Flood_Max, use_sample_dc=True)
        DivideByThickness(UserInput.Thickness)
        if UserInput.UseFitTrans:
            DirectBeamTransmission(SamTrans, UserInput.EmptyBeamTrans, beam_radius=UserInput.Trans_Radius)
            print "...Using measured transmission"
        else:
            SetTransmission(UserInput.SampleTransVal, 0)
            print "...Using manual transmission value, ", UserInput.SampleTransVal
        ThetaDependentTransmission(UserInput.ThetaTrans)
        #Note: Data path was not found at script generation, will try at run time.
        AppendDataFile([SamScatt])
        CombineTransmissionFits(UserInput.UseCombinedTransFit)
        if UserInput.UseBckCorrection:
            Background(UserInput.BackScatt)
            print "...Using background correction"
            if UserInput.UseFitBckTrans:
                BckDirectBeamTransmission(UserInput.BackTrans, UserInput.EmptyBeamTrans, beam_radius=UserInput.Trans_Radius)
                print "...Using measured transmission"
            else:
                SetBckTransmission(UserInput.BckTransVal, 0)
                print "...Using manual transmission value, ", UserInput.BckTransVal
            BckThetaDependentTransmission(UserInput.ThetaTrans)
            BckCombineTransmissionFits(UserInput.UseCombinedTransFit)
        SaveIq(process='None')
        Reduce()
        wks_transraw = '__transmission_raw_EQSANS_'+ SamTrans + '_event.nxs'
        wks_transfit = '__transmission_fit_EQSANS_'+ SamTrans + '_event.nxs'
        wks_bkgtransraw = '__transmission_raw_EQSANS_'+ UserInput.BackTrans + '_event.nxs'
        wks_bkgtransfit = '__transmission_fit_EQSANS_'+ UserInput.BackTrans + '_event.nxs'
        wksfs_transraw = '__transmission_raw_'+ SamScatt
        wksfs_transfit = '__transmission_fit_'+ SamScatt
        wksfs_bkgtransraw = '__transmission_raw___background_'+ SamScatt
        wksfs_bkgtransfit = '__transmission_fit___background_'+ SamScatt
        if wks_transraw in mtd:
            SaveAscii(InputWorkspace = wks_transraw, Filename = UserInput.OutputPathName + SamScatt + '_T' + SamTrans + '_raw.txt')
        elif wksfs_transraw in mtd:
            SaveAscii(InputWorkspace = wksfs_transraw, Filename = UserInput.OutputPathName + SamScatt + '_T' + SamTrans + '_raw.txt')
        else: 
            UserInput.ErrorLog += 'Transmission_raw does not exist. Skipping saveascii.\n'
            print '...Transmission_raw does not exist. Skipping saveascii.'
        if wks_transfit in mtd:
            SaveAscii(InputWorkspace = wks_transfit, Filename = UserInput.OutputPathName + SamScatt + '_T' + SamTrans + '_fit.txt')
        elif wksfs_transfit in mtd:
            SaveAscii(InputWorkspace = wksfs_transfit, Filename = UserInput.OutputPathName + SamScatt + '_T' + SamTrans + '_fit.txt')
        else:
            UserInput.ErrorLog += 'Transmission_fit does not exist. Skipping saveascii.\n'
            print '...Transmission_fit does not exist. Skipping saveascii.'
            
        if wks_bkgtransraw in mtd:
            SaveAscii(InputWorkspace = wks_bkgtransraw, Filename = UserInput.OutputPathName + SamScatt + '_bkgT' + UserInput.BackTrans + '_raw.txt')
        elif wksfs_bkgtransraw in mtd:
            SaveAscii(InputWorkspace = wksfs_bkgtransraw, Filename = UserInput.OutputPathName + SamScatt + '_bkgT' + UserInput.BackTrans + '_raw.txt')
        else: 
            UserInput.ErrorLog += 'Background Transmission_raw does not exist. Skipping saveascii.\n'
            print '...Background Transmission_raw does not exist. Skipping saveascii.'
            
        if wks_bkgtransfit in mtd:
            SaveAscii(InputWorkspace = wks_bkgtransfit, Filename = UserInput.OutputPathName + SamScatt + '_bkgT' + UserInput.BackTrans + '_fit.txt')
        elif wksfs_bkgtransfit in mtd:
            SaveAscii(InputWorkspace = wksfs_bkgtransfit, Filename = UserInput.OutputPathName + SamScatt + '_bkgT' + UserInput.BackTrans + '_fit.txt')
        else:
            UserInput.ErrorLog += 'Background Transmission_fit does not exist. Skipping saveascii.\n'
            print '...Background Transmission_fit does not exist. Skipping saveascii.'    
        f = open(UserInput.OutputPathName + SamScatt + '_log.txt', 'w')
        for i in dir(UserInput):
            if i[0] !="_":
                f.write(i + ' = ' + str(UserInput.__getattribute__(i)) + '\n')
        f.close()
        

def ReduceEQSANS_Single(UserInput):
    eqc = EQconf()
    #_SamScattList and _SamTransList should be list of strings. Run number within ''
    print '\nReducing..... S='  +  UserInput.SamScattList[0] + ' .......with T=' + UserInput.SamTransList[0] + ' at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    UserInput.ReductionLog = 'Reducing..... S='  +  UserInput.SamScattList[0] + ' .......with T=' + UserInput.SamTransList[0] + ' at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    EQSANS()
    if UserInput.Solid:
        print "...Using solid angle correction (default)"
        SolidAngle(detector_tubes = UserInput.DetectorTubeFlag)
    else:
        print "...Turn off solid angle correction"
    # SetWavelengthStep(UserInput.WaveStep)
    DarkCurrent(UserInput.DarkChoice)
    if UserInput.NormalizationChoice == "Monitor":
        BeamMonitorNormalization(eqc.FluxMonRatioFile)
        print '...Using monitor normalization'
    else:
        TotalChargeNormalization()
        print '...Using total charge normalization (default)'
    SetAbsoluteScale(UserInput.AbsScale)
    AzimuthalAverage(n_bins=UserInput.Nbins, n_subpix=1, log_binning=UserInput.UseLogBin)
    IQxQy(nbins=UserInput.Nbins_XY)
    print "...Using mask " ,  UserInput.MaskChoice
    MaskDetectors(eqc.__getattribute__(UserInput.MaskChoice))
    OutputPath(UserInput.OutputPathName)
    if UserInput.UseDefaultTOF:
        UseConfigTOFTailsCutoff(True)
        print "...Using default TOF Cuts (default)"
    else:
        print "...Using custom TOF Cuts  ", UserInput.Cut_i, " and ", UserInput.Cut_f
        UseConfigTOFTailsCutoff(False)
        SetTOFTailsCutoff(UserInput.Cut_i, UserInput.Cut_f)
    UseConfigMask(UserInput.UseDefaultMask)
    Resolution(sample_aperture_diameter= UserInput.SampleAP)
    PerformFlightPathCorrection(UserInput.UseFlightPathCorrection)
    DirectBeamCenter(UserInput.EmptyBeam)
    print "...Using sensitivity: " ,  UserInput.SensChoice
    SensitivityCorrection(UserInput.SensChoice, min_sensitivity= UserInput.Flood_Min, max_sensitivity= UserInput.Flood_Max, use_sample_dc=True)
    DivideByThickness(UserInput.Thickness)
    if UserInput.UseFitTrans:
        DirectBeamTransmission(UserInput.SamTransList[0], UserInput.EmptyBeamTrans, beam_radius=UserInput.Trans_Radius)
        print "...Using measured transmission"
    else:
        SetTransmission(UserInput.SampleTransVal, 0)
        print "...Using manual transmission value, ", UserInput.SampleTransVal
    ThetaDependentTransmission(UserInput.ThetaTrans)
    #Note: Data path was not found at script generation, will try at run time.
    AppendDataFile(UserInput.SamScattList)
    CombineTransmissionFits(UserInput.UseCombinedTransFit)
    if UserInput.UseBckCorrection:
        Background(UserInput.BackScatt)
        print "...Using background correction"
        if UserInput.UseFitBckTrans:
            BckDirectBeamTransmission(UserInput.BackTrans, UserInput.EmptyBeamTrans, beam_radius=UserInput.Trans_Radius)
            print "...Using measured transmission"
        else:
            SetBckTransmission(UserInput.BckTransVal, 0)
            print "...Using manual transmission value, ", UserInput.BckTransVal
        BckThetaDependentTransmission(UserInput.ThetaTrans)
        BckCombineTransmissionFits(UserInput.UseCombinedTransFit)
    SaveIq(process='None')
    Reduce()
    wks_transraw = '__transmission_raw_EQSANS_'+ UserInput.SamTransList[0] + '_event.nxs'
    wks_transfit = '__transmission_fit_EQSANS_'+ UserInput.SamTransList[0] + '_event.nxs'
    wks_bkgtransraw = '__transmission_raw_EQSANS_'+ UserInput.BackTrans + '_event.nxs'
    wks_bkgtransfit = '__transmission_fit_EQSANS_'+ UserInput.BackTrans + '_event.nxs'
    wksfs_transraw = '__transmission_raw_'+ UserInput.SamTransList[0]
    wksfs_transfit = '__transmission_fit_'+ UserInput.SamTransList[0]
    wksfs_bkgtransraw = '__transmission_raw___background_'+ UserInput.BackTrans
    wksfs_bkgtransfit = '__transmission_fit___background_'+ UserInput.BackTrans
    if wks_transraw in mtd:
        SaveAscii(InputWorkspace = wks_transraw, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_T' + UserInput.SamTransList[0] + '_raw.txt')
    elif wksfs_transraw in mtd:
        SaveAscii(InputWorkspace = wksfs_transraw, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_T' + UserInput.SamTransList[0] + '_raw.txt')
    else: 
        UserInput.ErrorLog += 'Transmission_raw does not exist. Skipping saveascii.\n'
        print '...Transmission_raw does not exist. Skipping saveascii.'
        
    if wks_transfit in mtd:
        SaveAscii(InputWorkspace = wks_transfit, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_T' + UserInput.SamTransList[0] + '_fit.txt')
    elif wksfs_transfit in mtd:
        SaveAscii(InputWorkspace = wksfs_transfit, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_T' + UserInput.SamTransList[0] + '_fit.txt')
    else:
        UserInput.ErrorLog += 'Transmission_fit does not exist. Skipping saveascii.\n'
        print '...Transmission_fit does not exist. Skipping saveascii.'
        
    if wks_bkgtransraw in mtd:
        SaveAscii(InputWorkspace = wks_bkgtransraw, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_bkgT' + UserInput.BackTrans + '_raw.txt')
    elif wksfs_bkgtransraw in mtd:
        SaveAscii(InputWorkspace = wksfs_bkgtransraw, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_bkgT' + UserInput.BackTrans + '_raw.txt')
    else: 
        UserInput.ErrorLog += 'Background Transmission_raw does not exist. Skipping saveascii.\n'
        print '...Background Transmission_raw does not exist. Skipping saveascii.'
        
    if wks_bkgtransfit in mtd:
        SaveAscii(InputWorkspace = wks_bkgtransfit, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_bkgT' + UserInput.BackTrans + '_fit.txt')
    elif wksfs_bkgtransfit in mtd:
        SaveAscii(InputWorkspace = wksfs_bkgtransfit, Filename = UserInput.OutputPathName + UserInput.SamScattList[0] + '_bkgT' + UserInput.BackTrans + '_fit.txt')
    else:
        UserInput.ErrorLog += 'Background Transmission_fit does not exist. Skipping saveascii.\n'
        print '...Background Transmission_fit does not exist. Skipping saveascii.'  
    f = open(UserInput.OutputPathName + UserInput.SamScattList[0] + '_log.txt', 'w')
    for i in dir(UserInput):
        if i[0] !="_":
            f.write(i + ' = ' + str(UserInput.__getattribute__(i)) + '\n')
    f.close()
    
    wks_iq = UserInput.SamScattList[0] + '_Iq'
    wksfs1_iq = UserInput.SamScattList[0] + 'frame1_Iq'
    wksfs2_iq = UserInput.SamScattList[0] + 'frame2_Iq'
    if wks_iq in mtd:
        SaveAscii(InputWorkspace = UserInput.SamScattList[0] + '_Iq', Filename = UserInput.OutputPathName + UserInput.OutputFileName + '.txt', WriteXError=True)
    elif wksfs1_iq in mtd:
        SaveAscii(InputWorkspace = wksfs1_iq, Filename = UserInput.OutputPathName + UserInput.OutputFileName + '_f1.txt', WriteXError=True)
        if wksfs2_iq in mtd:
            SaveAscii(InputWorkspace = wksfs2_iq, Filename = UserInput.OutputPathName + UserInput.OutputFileName + '_f2.txt', WriteXError=True)
