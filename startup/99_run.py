
from qtpy.QtWidgets import QApplication
import sys
from iss_xsample import xsample

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




#import matplotlib
#matplotlib.use('Qt5Agg')




app = QApplication.instance() or QApplication(sys.argv)  # IPython's Qt integration may already own one



xsample_gui = xsample.XsampleGui(gas_cart=gas_cart,
                                 mobile_gh_system = mobile_gh_system,
                                 total_flow_meter=total_flow_meter,
                                 rga=rga,
                                 rga_channels=rga_channels,
                                 rga_masses=rga_masses,
                                 ghs=ghs,
                                 switch_manifold=switch_manifold,
                                 RE=RE,
                                 archiver = arch_iss,
                                 sample_envs_dict=sample_envs_dict,
                                 reset_rga = reset_rga,
                                 flow_condition_valves=flow_condition_valves,
                                 pdu=pdu3)
#
def xsample_show():
    xsample_gui.show()

xsample_show()
