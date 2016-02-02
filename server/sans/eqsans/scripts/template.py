#
# Test script
#

{{title}}

{{ipts}}

{{ configuration.absolute_scale_factor }}

{% for entry in entries %}
    {{ entry.background_scattering}} {{ entry.background_transmission}} {{ entry.empty_beam}}
{% endfor %}