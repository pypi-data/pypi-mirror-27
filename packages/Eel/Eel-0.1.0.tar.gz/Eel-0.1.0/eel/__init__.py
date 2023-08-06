import json as jsn, bottle as btl, bottle.ext.websocket as wbs, gevent as gvt
import re as rgx, os, webbrowser as wbr, subprocess as sps

_eel_js_file = os.path.join(os.path.dirname(__file__), 'eel.js')
_eel_js = open(_eel_js_file, encoding='utf8').read()
_mock_queue = []
_exposed_functions = {}
_js_functions = []
_chrome_path = None
_websockets = []

# Public functions

def expose(name_or_function = None):
    if name_or_function == None:
        return expose
    
    if type(name_or_function) == str:
        name =  name_or_function
        def decorator(function):
            _expose(name, function)
            return function
        return decorator
    else:
        function = name_or_function
        _expose(function.__name__, function)
        return function
        
def init(path):
    global root_path, _js_functions
    root_path = path

    js_functions = set()
    for root, _, files in os.walk(root_path):
        for name in files:
            try:
                with open(os.path.join(root, name), encoding='utf8') as file:                
                    contents = file.read()
                    js_functions.update(set(rgx.findall(r'eel\.expose\((.*)\)', contents)))
            except UnicodeDecodeError:
                pass    # Probably an image

    _js_functions = list(js_functions)
    for js_function in _js_functions:
        _mock_js_function(js_function)
           
    _find_chrome_installation()

def run(start_urls = [], host='localhost', port=8000, app_mode=True):
    if type(start_urls) is str:
        start_urls = [start_urls]
    
    for i, start_url in enumerate(start_urls):
        _open_browser('http://%s:%d/%s' % (host, port, start_url), app_mode, i == 0)

    btl.run(host=host, port=port, server=wbs.GeventWebSocketServer, quiet=True)

# Bottle Routes

@btl.route('/eel.js')
def _eel():
    function_names = list(_exposed_functions.keys())
    return _eel_js.replace('/** _py_functions **/', '_py_functions: %s,' % function_names)
    
@btl.route('/<path:path>')
def _static(path):
    if root_path is None:
        return 'Initialising...'
    
    return btl.static_file(path, root=root_path)    

@btl.get('/eel', apply=[wbs.websocket])
def _websocket(ws):
    global _websockets
    _websockets += [ws]
    
    for js_function in _js_functions:
        _import_js_function(js_function)
    
    while _mock_queue != []:
        name, args = _mock_queue.pop(0);
        globals()[name](*args)

    while True:
        msg = ws.receive()
        if msg != None:
            call = jsn.loads(msg)
            _exposed_functions[call['name']](*call['args'])
        else:
            _websockets.remove(ws)
            break
            
# Private functions

def _mock_js_function(f):
    exec('%s = lambda *args: _mock_call("%s", args)' % (f, f), globals())
    
def _import_js_function(f):
    exec('%s = lambda *args: _js_call("%s", args)' % (f, f), globals())
    
def _mock_call(f, args):
    global _mock_queue
    _mock_queue += [[f, args]]
    
def _js_call(name, args):
    js_call = {'name': name, 'args': args}
    for ws in _websockets:
        ws.send(jsn.dumps(js_call))

def _expose(name, function):
    if name in _exposed_functions:
        raise RuntimeError('Already exposed function with name "%s"' % name)
    _exposed_functions[name] = function

def _find_chrome_installation():
    global _chrome_path
    
    if os.name == 'nt':
        import winreg as reg
        
        reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
        
        for install_type in reg.HKEY_LOCAL_MACHINE, reg.HKEY_CURRENT_USER:
            try:
                reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
                _chrome_path = reg.QueryValue(reg_key, None)
            except WindowsError:
                pass
                
            reg_key.Close()
     
def _open_browser(start_url, app_mode, new_window):
    if _chrome_path != None:
        args = ' --aggressive-cache-discard --no-default-browser-check '
        if new_window:
            args += '--new-window --window-size="800,600" '
        if app_mode:
            args += ' --app='

        sps.Popen(_chrome_path + args + start_url)
    else:
        if new_window:
            wbr.open_new(start_url)
        else:
            wbr.open(start_url)
