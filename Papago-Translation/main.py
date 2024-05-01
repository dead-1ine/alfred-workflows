import sys

import ssl
import json

from urllib import request, parse


def req_papago_translation_api(text, source='en', target='ko'):
    data = f'source={source}&target={target}&text={parse.quote(text)}'

    req = request.Request(
        url='https://naveropenapi.apigw.ntruss.com/nmt/v1/translation',
        headers={
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_secret
        })
    
    response = request.urlopen(
        req, 
        data=data.encode('utf-8'), 
        context=ssl._create_unverified_context()
    )

    res_code = response.getcode()

    # TODO: handle error code with try-catch
    if(res_code == 200):
        response_body = json.loads(response.read().decode('utf-8'))
    else:
        print("Error Code:" + res_code)

    return response_body['message']['result']['translatedText']


def make_alfred_output(title, subtitle, arg=None):
    return {
        'title': title,
        'subtitle': subtitle,
        'icon': {'path': 'icon.png'},
        'arg': arg,
    }


if __name__ == '__main__':
    # call cli from Alfred Workflow - Script filter
    input_text = sys.argv[1]

    # Determine the source and target languages based on the input text
    if input_text.encode(encoding='utf-8').isalpha():
        source, target = 'en', 'ko' 
    else:
        source, target = 'ko', 'en'

    # Translate the input text using the Papago Translation API
    translate_text = req_papago_translation_api(
        input_text,
        source=source, 
        target=target
    )

    alfred_output = make_alfred_output(
        title=translate_text,
        subtitle='Copy result to clipboard :)', 
        arg=translate_text
    )

    alfred_json = json.dumps({
        'items': [alfred_output]
    })

    sys.stdout.write(alfred_json)
    sys.stdout.flush() # flush the stdout buffer