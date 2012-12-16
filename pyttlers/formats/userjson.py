from json import dumps

mediatype = 'application/vnd.tps12.pyttlers-user+v1.json'

def tojson(url, emailaddress):
    return dumps({ 'id': url, 'email_address': emailaddress })
