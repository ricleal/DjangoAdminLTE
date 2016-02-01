from django.contrib.auth.models import Group

import logging

'''
My groups: rhf

"sns_bss_team"
"hfir_sans2_team"
"sns-spare"
"sns_nom_team"
"sns-topaz"
"sns_vis_team"
"sns-subversion"
"sns_cncs_team"
"sns_builds_users"
"sns_venus_team"
"sns-corelli"
"sns_aclr_team"
"sns_hys_team"
"sns_eqsans_team"
"adara"
"sns_pg3_team"
"sns_ref_l_team"
"mantidwheel"
"SNS_Neutron"
"sns_ref_m_team"
"sns_topaz_team"
"ucams"
"sns-heater"
"sns_arcs_team"
"sns_fd1_team"
"snswheel"
"sns_corelli_team"
"sns_seq_team"
"fermi-users"
"sns_builds_admins"
"hfir_sans1_team"
"sns_mandi_team"
"sns-dev"
"sns_snap_team"
"SNS_Neutron_dev"
"sns_vulcan_team"
"sns_usans_team"
'''

logger = logging.getLogger('catalog.permissions')

def user_has_permission_to_see_this_ipts(user,instrument,ipts):
    """
    @param user: user object
    @param instrument : string
    @param ipts : string

    User must belong to:
    - SNS_Neutron_dev (NDAV!)
    - Scientist from the instrument: sns_<instrument>_team
    - Or be in this IPTS group!

    """

    if user.groups.filter(name = 'SNS_Neutron_dev'):
        return True
    if  user.groups.filter(name = 'sns_%s_team'%instrument.lower()):
        return True
    if user.groups.filter(name = ipts.upper()):
        return True
    return False

def filter_user_permission(user, instrument, ipts_list):
    '''
    Iterates the ipts_list and returns a new ipts_list width
    ipts whose user is allowed to see
    '''
    return [ ipts for  ipts in ipts_list if user_has_permission_to_see_this_ipts(user,instrument,ipts) ]
