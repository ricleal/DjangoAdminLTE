from django.template import Template, Context

from pprint import pformat
import os
import logging

logger = logging.getLogger('util.script')


def build_script(script_file_path, data):
    '''
    Build a script from a template file @script_file_path,
    @data is a dictionary
    '''
    logger.debug(pformat(data))
            
    script_filtered = ""
    if os.path.isfile(script_file_path):
        with open(script_file_path) as f:
            lines = f.readlines()
            text = '\n'.join(lines)
            template = Template(text)            
            context = Context(data)
            script = template.render(context)
            script_filtered = "\n".join([ll.rstrip() for ll in script.splitlines() if ll.strip()])
    else:
        logger.error("File %s does not exist!"%script_file_path)
    return script_filtered