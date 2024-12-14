import requests
import time
import re
import json
import hidden
import datecompat
from elasticsearch import Elasticsearch, RequestsHttpConnection
import dateutil.parser as parser

secrets = hidden.elastic

def parsemaildate(md) :
    try:
        pdate = parser.parse(md)
        test_at = pdate.isoformat()
        return test_at
    except:
        return datecompat.parsemaildate(md)

class Elasticmail:

    def __init__(self) -> None:
        self.es = None
        self.baseurl = 'http://mbox.dr-chuck.net/sakai.devel/'
        self.indexname = None
        self.__set_up()
        self.__clean_up()
        self.start_mail_process()

    def __set_up(self):
        self.es = Elasticsearch(
            [secrets['host']],
            http_auth=(secrets['user'], secrets['pass']),
            url_prefix=secrets['prefix'],
            scheme=secrets['scheme'],
            port=secrets['port'],
            connection_class=RequestsHttpConnection,
        )
        self.indexname = secrets['user']

    def __clean_up(self):
        res = self.es.indices.delete(index=self.indexname, ignore=[400, 404])
        print("Dropped index")
        print(res)

        res = self.es.indices.create(index=self.indexname)
        print("Created the index...")
        print(res)

    def end_all(self):
        self.es.close()

    def start_mail_process(self):
        many = 0
        count = 0
        fail = 0
        start = 0
        while True:
            if (many < 1):
                sval = input('How many messages:')
                if (len(sval) < 1): break
                many = int(sval)

            start = start + 1

            many = many - 1
            url = self.baseurl + str(start) + '/' + str(start + 1)

            text = 'None'
            try:
                # Open with a timeout of 30 seconds
                response = requests.get(url)
                text = response.text
                status = response.status_code
                if status != 200:
                    print('Error code=', status, url)
                    break
            except KeyboardInterrupt:
                print('')
                print('Program interrupted by user...')
                break
            except Exception as e:
                print('Unable to retrieve or parse page', url)
                print('Error', e)
                fail = fail + 1
                if fail > 5: break
                continue

            print(url, len(text))
            count = count + 1

            if not text.startswith('From '):
                print(text)
                print('Did not find From ')
                fail = fail + 1
                if fail > 5: break
                continue

            pos = text.find('\n\n')
            if pos > 0:
                hdr = text[:pos]
                body = text[pos + 2:]
            else:
                print(text)
                print('Could not find break between headers and body')
                fail = fail + 1
                if fail > 5: break
                continue

            # Accept with or without < >
            email = None
            x = re.findall('\nFrom: .* <(\S+@\S+)>\n', hdr)
            if len(x) == 1:
                email = x[0]
                email = email.strip().lower()
                email = email.replace('<', '')
            else:
                x = re.findall('\nFrom: (\S+@\S+)\n', hdr)
                if len(x) == 1:
                    email = x[0]
                    email = email.strip().lower()
                    email = email.replace('<', '')

            # Hack the date
            sent_at = None
            y = re.findall('\nDate: .*, (.*)\n', hdr)
            if len(y) == 1:
                tdate = y[0]
                tdate = tdate[:26]
                try:
                    sent_at = parsemaildate(tdate)
                except:
                    print(text)
                    print('Parse fail', tdate)
                    fail = fail + 1
                    if fail > 5: break
                    continue

            # Make the headers into a dictionary
            hdrlines = hdr.split('\n')
            hdrdict = dict()
            for line in hdrlines:
                # [('From', '"Glenn R. Golden" <ggolden@umich.edu>')]
                y = re.findall('([^ :]*): (.*)$', line)
                if len(y) != 1: continue
                tup = y[0]
                if len(tup) != 2: continue
                # print(tup)
                key = tup[0].lower()
                value = tup[1].lower()
                hdrdict[key] = value

            # Override the date field
            hdrdict['date'] = sent_at

            # Reset the fail counter
            fail = 0
            doc = {'offset': start, 'sender': email, 'headers': hdrdict, 'body': body}
            res = self.es.index(index=self.indexname, id=str(start), body=doc)
            print('   ', start, email, sent_at)

            print('Added document...')
            print(res['result'])

            if count % 100 == 0: time.sleep(1)

    def check_elastic_server_connection(self):
        self.es.ping()
        return True

    def search(self, param):
        body = json.dumps({"query": {"query_string": {"query": param}}})
        return self.es.search(index=self.indexname, body=body)

if __name__ == '__main__':
    elasticmail = Elasticmail()