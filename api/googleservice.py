def get_email_subject(title_name):
    return title_name

def get_email_template(template_name):
    if template_name == 'initial':
        return '''
What's up, ths is the initial <b>script</b>
        '''
    return template_name

def has_valid_template_type(template_name):
    return True