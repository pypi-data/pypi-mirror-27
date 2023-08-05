from random import randint
import xml.etree.ElementTree as XML
from jenkins_jobs.errors import MissingAttributeError


defn = 'org.biouno.unochoice.CascadeChoiceParameter'
choices_type = ['PT_SINGLE_SELECT','PT_MULTI_SELECT','PT_RADIO','PT_CHECKBOX']

def reactive_choice(parser, xml_parent, data):

    """
      - reactive_choice:
          name: SNAPSHOT_NAMES
          description: "Return list of snapshot names."
          projectName: Test_Job
          referencedParameters: ENV_NAME
          script: |
            if (ENV_NAME == 'production') {
                return ['rds-backup-prod-2017-11-29',
                        'rds-backup-prod-2017-11-30']
            }
    """

    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    random_num = random_with_N_digits(16)

    r_p = XML.SubElement(xml_parent,
                         defn)
    r_p.set('plugin', 'uno-choice@2.0')

    try:
        name = data['name']
    except KeyError:
        raise MissingAttributeError('name')

    try:
        script = data['script']
    except KeyError:
        raise MissingAttributeError('script')

    try:
        projectName = data['projectName']
    except KeyError:
        raise MissingAttributeError('projectName')

    choiceType = data.get('choiceType')
    if choiceType is not None and choices_type not in choices_type:
        raise MissingAttributeError('Not valid choice')

    XML.SubElement(r_p, 'name').text = name
    XML.SubElement(r_p, 'description').text = data.get('description', '')
    XML.SubElement(r_p, 'randomName').text = 'choice-parameter-{0}'.format(
        random_num)
    XML.SubElement(r_p, 'visibleItemCount').text = '1'
    XML.SubElement(r_p, 'referencedParameters').text = data.get(
        'referencedParameters', '')
    XML.SubElement(r_p, 'choiceType').text = 'PT_SINGLE_SELECT'
    XML.SubElement(r_p, 'filterable').text = 'false'
    XML.SubElement(r_p, 'filterLength').text = data.get('filterLength', '1')
    XML.SubElement(r_p, 'projectName').text = projectName

    __script = XML.SubElement(r_p, 'script')
    __script.set('class', 'org.biouno.unochoice.model.GroovyScript')
    XML.SubElement(__script, 'script').text = data.get('script', '')

    XML.SubElement(__script, 'script').text = script
    XML.SubElement(__script, 'fallbackScript').text = data.get(
        'fallbackScript', '')


    __script = XML.SubElement(r_p, 'parameters')
    __script.set('class', 'linked-hash-map')
