import collections
from flask import request
import importlib

def serializeItem(obj, printLevel=False): 
    methodList = ['append', 'query_class', 'serialize', 'clear', 'copy', 'count', 'query', 'index', 'insert', 'metadata', 'extend', 'remove', 'sort', 'reverse', 'pop']
    list = []
    for a in dir(obj):            
          if not a.startswith('_') and not a.isupper() and a not in methodList:   
            avalue = getattr(obj, a)
            if not is_collection(avalue):       
              list.append('"%s" : "%s" ' % (a, avalue))
            else:  
              subContent = ''
              subContent += ' "%s" : [' % (a)       
              sublist = []
              for lv in avalue:             
                sublist.append(serializeItem(lv))

              subContent += ", ".join(sublist) 
              subContent += ']'              
              list.append(subContent)
   
    fstr = ", ".join(list)
    return '{' + fstr + '}';

def serializeList(obj, objTagName): 
    if isinstance(obj, list):
     itemList = []      
     
     for x in obj:
       itemList.append(serializeItem(x))
    
     fstr = ", ".join(itemList)
    
    return '{"' + objTagName + '": [' + fstr + ']}';



def is_collection(obj):
    return isinstance(obj, collections.Sequence) and not isinstance(obj, str)

def handleJsonRequest(class_):
    def wrap(f):        
        def decorator(*args):           
            obj = class_(**request.get_json())
            return f(obj)
        return decorator
    return wrap

def createInstance(module_name, class_name):
    class_ = None    
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)
            instance = class_()            
        except AttributeError:
            print('Class does not exist')
    except ImportError:
        print('Module does not exist')        
    return instance

def parseJsonRequest(module_name, class_name, requestJson):
      status = False
      instance = createInstance(module_name, class_name) 
      for k in requestJson: 
          setattr(instance, k, requestJson[k])    
          status = True
      return status, instance
  
class HttpStatusCode():      
  HttpOk = 200
  Http400 = 400
  Http401 = 401
  Http500 = 500 
  HttpCreated = 201