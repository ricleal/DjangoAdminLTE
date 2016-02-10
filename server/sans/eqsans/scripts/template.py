#
# Test script just to make sure if works!
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


