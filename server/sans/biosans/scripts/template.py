# HFIR Bio-SANS reduction script - qians@ornl.gov Shuo Qian 2016 May

import mantid
from mantid.simpleapi import *
from reduction_workflow.instruments.sans.hfir_command_interface import *

#
# {{title}}
# {{ipts}}




{% for entry in entries %}
    {{ entry.background_scattering}} {{ entry.background_transmission}} {{ entry.empty_beam}}
{% endfor %}




{{ configuration.absolute_scale_factor }}


SampleScattering="test_0031.xml"
BgScattering       ="test_bg_0031.xml"

dark60m_curr_file="psBioSANS_exp291_6mDark.xml" #detector at 6m & 1.13 m; 15m &1.13m for dark
flood_field_file     ="psBioSANS_exp291_Flood.xml" #a 6m&1.13 flat field
EmptyTrans         = "test_0031_trans_0001.xml"#6m MT beam file
beam60m_center_file = EmptyTrans
BgTrans             ="test_bg_0031_trans_0001.xml"

#Main detector reduction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BIOSANS()
#SetSampleDetectorOffset(3)
#SetWavelength(lmbda6, 0.15)
SolidAngle(detector_tubes=True)
DataPath(xml_data_folder)
DarkCurrent(dark60m_curr_file)
MonitorNormalization()
SetAbsoluteScale(1)
IQxQy(nbins=80)
#NoIQxQy()
#for main detector
MaskComponent("wing_detector")
Mask(nx_low=2, nx_high=2, ny_low=20, ny_high=20)
AzimuthalAverage(n_bins=80, n_subpix=1, log_binning=True)
# Mask main detector
#MaskComponent("detector1")
#Mask(nx_low=1, nx_high=1, ny_low=20, ny_high=20, component_name="wing_detector")
#AzimuthalAverage(binning="0.11,0.005,0.5", n_subpix=1,log_binning=False)
DirectBeamCenter(beam60m_center_file)
ThetaDependentTransmission(True)
DirectBeamTransmission(EmptyTrans, EmptyTrans, beam_radius=3)
TransmissionDarkCurrent(dark60m_curr_file)
AppendDataFile(SampleScattering, workspace=main_out_name)
Background(BgScattering)
BckDirectBeamTransmission(BgTrans, EmptyTrans, beam_radius=3)
BckThetaDependentTransmission(True)
BckTransm
