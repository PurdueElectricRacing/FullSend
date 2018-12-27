import requests
import uuid
import json

from FullSend.settings import DEBUG

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

# Generic API Sending
def make_api_call(method, url, token, payload = None, parameters = None):
  # Send these headers with all API calls
  headers = { 'User-Agent' : 'FullSend/1.0',
              'Authorization' : 'Bearer {0}'.format(token),
              'Accept' : 'application/json' }

  # Use these headers to instrument calls. Makes it easier
  # to correlate requests and responses in case of problems
  # and is a recommended best practice.
  request_id = str(uuid.uuid4())
  instrumentation = { 'client-request-id' : request_id,
                      'return-client-request-id' : 'true' }

  headers.update(instrumentation)

  response = None

  if (method.upper() == 'GET'):
      response = requests.get(url, headers = headers, params = parameters)
  elif (method.upper() == 'DELETE'):
      response = requests.delete(url, headers = headers, params = parameters)
  elif (method.upper() == 'PATCH'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
  elif (method.upper() == 'POST'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

  return response

def get_me(access_token):
  get_me_url = graph_endpoint.format('/me')

  # Use OData query parameters to control the results
  #  - Only return the displayName and mail fields
  query_parameters = {'$select': 'displayName,mail'}

  r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_my_messages(access_token):
  get_messages_url = graph_endpoint.format('/me/mailfolders/inbox/messages')

  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the ReceivedDateTime, Subject, and From fields
  #  - Sort the results by the ReceivedDateTime field in descending order
  query_parameters = {'$top': '10',
                      '$select': 'receivedDateTime,subject,from',
                      '$orderby': 'receivedDateTime DESC'}

  r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def test_send_message(access_token):
    post_messages_url = graph_endpoint.format('/me/sendMail')

    email = {
        'message': {
            'subject': 'Test subject',
            'body': {
                'contentType': 'HTML',
                'content': 'Test with <b>bolded</b> text!'
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': 'schwar95@purdue.edu'
                    }
                }
            ]
        }
    }

    r = make_api_call('POST', post_messages_url, access_token, payload = email)

    if (r.status_code == requests.codes.accepted):
      # return r.json()
      return 'Message sent!'
    else:
      return "{0}: {1}".format(r.status_code, r.text)

def generate_email(form):
    email = []
    if form['send_type'] == 'individual':
        for recipient in form['send_list']:
            email.append({
                'message': {
                    'subject': form['subject'],
                    'body': {
                        'contentType': 'HTML',
                        'content': form['content']
                    },
                    'toRecipients': [
                        {
                            'emailAddress': {
                                'address': recipient
                            }
                        }
                    ]
                }
            })
    elif form['send_type'] == 'bcc':
        email.append({
            'message': {
                'subject': form['subject'],
                'body': {
                    'contentType': 'HTML',
                    'content': form['content']
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': 'eformula@purdue.edu'
                        }
                    }
                ],
                'bccRecipients': []
            }
        })
        for recipient in form['send_list']:
            email[0]['message']['bccRecipients'].append({
                'emailAddress': {
                    'address': recipient
                }
            })
    return email

def send_message(access_token, emails):
    post_messages_url = graph_endpoint.format('/me/sendMail')
    if DEBUG == True:
        # Don't actually send the emails in DEBUG mode
        print('Emails that would have been sent:')
        print(emails)
    else:
        for email in emails:
            res = make_api_call('POST', post_messages_url, access_token, payload = email)
            if res.status_code != requests.codes.accepted:
                return "{0}: {1}".format(r.status_code, r.text)

    return 'Message sent!'
