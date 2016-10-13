import sys
from optparse import OptionParser
import json
import tornado.ioloop
import tornado.web

class APIData():
    def __init__(self, datafile):
        self.datafile = datafile    
        self.json_data = {}

    def _read_data(self): 
        with open(self.datafile) as json_file:
            self.json_data = json.load(json_file)
            print(json.dumps(self.json_data))
        return self.json_data
        
    def _write_data(self):
        with open(self.datafile, 'w') as json_file:
            json.dump(self.json_data, json_file)
    
    def __init__(self):
        self.json_data = self._read_data()
        
    def data(self):
        return self.json_data
     
    def dump(self):
        self._write_data()
    
    def load(self):
        self._read_data()
    
class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	if self.request.path == '/config/submit':
            self.write("not supported, please call POST method!")
        else:
            self.set_header("Content-Type", "application/json")
            self.write(self._response())
        self.finish()    
        
    def post(self):
        if self.request.path == '/config/submit':
            self._add_data()
            self.write("submitted!")
        else:
            self.set_header("Content-Type", "application/json")
            self.write(self._response())
        self.finish()
        
    def _add_data(self):
        data = json.loads(self.request.body)
        self.application.apidata.data()[data['path']] = data['data']
        self.application.apidata.dump()
        self.application.apidata.load()
    
    def _response(self):
        response = self._get_response()
        if response:
            return json.dumps(response)
        else:
            self.set_status(404)
            return "NOT FOUND"    
        
    def _get_response(self):
        if self.application.apidata.data().has_key(self.request.path): 
            return self.application.apidata.data()[self.request.path]
        else:
            return None;

class Application(tornado.web.Application):
    def __init__(self, datafile):
        self.apidata = APIData(datafile)
        handlers = [
            #(r"/config/submit", SubmitHandler),
            (r"/.*", MainHandler),
        ]
        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    usage = "usage: python http-server.py [options]"  
    parser = OptionParser(usage=usage)
    parser.add_option('-p', '--port', help="server port")
    parser.add_option('-d', '--data', help="data file")
    options, args = parser.parse_args(sys.argv)
    port = 8888
    if options.port is not None:  
        port = int(options.port)
    data = 'data.json'
    if options.port is not None:
        data = options.data  
    
    app = Application(data)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
    

