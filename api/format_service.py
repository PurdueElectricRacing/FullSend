from api.googleservice import get_email_template

event_invites = {
    'Aerodynamics': R'https://calendly.com/purdueelectricracing/aero',
    'Battery': R'https://calendly.com/purdueelectricracing/battery',
    'Business': R'https://calendly.com/purdueelectricracing/business',
    'Chassis': R'https://calendly.com/purdueelectricracing/chassis',
    'Drivetrain': R'https://calendly.com/purdueelectricracing/drivetrain',
    'Electronics': R'https://calendly.com/purdueelectricracing/electronics',
    'Vehicle Dynamics': R'https://calendly.com/purdueelectricracing/vehicledynamics'
}

def format_email(email_type, settings):
    content = get_email_template(email_type)

    # Set line endings
    content = content.replace('\r\n', '<br />').replace('\n', '<br />')

    content = content.replace('{{NAME}}', settings['name'])

    if 'subteam' in settings and settings['subteam'] != '':
        content = content.replace('{{INVITE_URL}}', event_invites[settings['subteam']])

    return content
