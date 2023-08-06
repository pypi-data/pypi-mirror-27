# by lich666dead
#email lich666black@gmail.com
import os
import json


class PhantomJS:


    @classmethod
    def get( cls, url, load_image = False, userAgent = 'BasiliskJS', js_evalute = '', get_url = False,
             js = [], screenshot = False, image_name = 'BasiliskJS', content = False,  exit = True, command = 'phantomjs' ):
        size = {
            'width':1920,
            'height':1080
        }
        cls.creation(locals(), cls.node() )
        return cls.run( command + ' run.js' )

    @staticmethod
    def node():
        return """
var webPage = require('webpage');
var page = webPage.create();
var data = {};
var param = {
  'load_image':LOAD_IMAGE_SET,
  'size':{ width: SET_IMAGE_WIDTH, height: SET_IMAGE_HEIGHT },
  'userAgent':'SET_USERAGENT',
  'url':'SET_URL',
  'js':SET_JS_EVALUATE,
  'screenshot':'SCREENSHOT_SET_LOAD',
  'image_name':'SET_NAME_IMAGE',
  'content':'CONTENT_GET',
  'exit':'SET_EXIT_AND_NOEXIT',
  'get_url':'SET_GETURL'
};

page.settings.loadImages = param['load_image'];
page.viewportSize = param['size'];
page.settings.userAgent = param['userAgent'];
page.open( param['url'] , function(status) {
  data['status'] = status;
  });

page.onLoadFinished = function() {


  if ( param['js'].length > 0 ) {
    var temp = {};
    for (var i = 0; i != param['js'].length; i++) {
      try {
        temp[i] = page.evaluateJavaScript("function(){ return " + param['js'][i] + "; }");
      } catch (e) {
        temp[i] = 'error';
      }
    }
  } else {
    var temp = page.evaluate(function() {
      SET_INIT_JS_EVALUATE
    });
  };

  if (param['screenshot'] == 'True') {
        page.render( param['image_name'] + '.png');
  };

  if (param['content'] == 'True') {
    data['content'] = page.content;
  };

  if (param['get_url'] == 'True') {
    data['page_url'] = page.url;        
  };

  if (param['exit'] == 'True') {
    data['js'] = temp;
    console.log( JSON.stringify(data) );
    phantom.exit();
  } else {
    console.log( JSON.stringify(data) );
  };
};"""

    @staticmethod
    def creation( param, node ):
        with open('run.js', 'w') as f:
            f.write( str( node )
                     .replace('LOAD_IMAGE_SET', 'true' if param['load_image'] else 'false' )
                     .replace('SET_IMAGE_WIDTH', param['size']['width'].__str__() )
                     .replace('SET_IMAGE_HEIGHT', param['size']['height'].__str__() )
                     .replace('SET_USERAGENT', param['userAgent'])
                     .replace('SET_URL', param['url'])
                     .replace('SET_JS_EVALUATE', param['js'].__str__() )
                     .replace('SCREENSHOT_SET_LOAD', param['screenshot'].__str__() )
                     .replace('SET_NAME_IMAGE', param['image_name'] )
                     .replace('CONTENT_GET', param['content'].__str__() )
                     .replace('SET_EXIT_AND_NOEXIT', param['exit'].__str__() )
                     .replace('SET_INIT_JS_EVALUATE', param['js_evalute'])
                     .replace('SET_GETURL', param['get_url'].__str__() ))

    @staticmethod
    def run( command ):
        with os.popen( command ) as j:
            for i in j.read().split('\n'):
                try:
                    return json.loads(i)
                except:
                    continue

