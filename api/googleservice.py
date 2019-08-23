import requests

subject_map = {
    'welcome': 'Thanks for filling out our interest form!',
    'acceptance': 'Welcome to Purdue Electric Racing!',
}

content_map = {
    'welcome': 'welcome.html',
    'acceptance': 'acceptance.html',
}

def get_email_subject(template_name):
    if template_name not in subject_map:
        raise Exception(
            f'template name {template_name} not found in subject_map')

    return subject_map[template_name]

def get_email_template(template_name):
    if template_name not in content_map:
        raise Exception(
            f'template name {template_name} not found in content_map')

    r = requests.get(
        f'https://gist.githubusercontent.com/RyanSchw/4c3713d676f4d60511d98044b5083763/raw/{content_map[template_name]}')

    return r.text

def has_valid_template_type(template_name):
    return template_name in subject_map and template_name in content_map
