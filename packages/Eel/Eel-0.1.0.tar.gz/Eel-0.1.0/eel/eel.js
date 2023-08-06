eel = {
    expose: function(f, name) {
        if(name === undefined){
            name = f.toString();
            let i = 'function '.length, j = name.indexOf('(');
            name = name.substring(i, j).trim();
        }
        
        eel._exposed_functions[name] = f;
    },
    
    _exposed_functions: {},
    
    /** _py_functions **/
    
    _mock_queue: [],
    
    _mock_py_functions: function() {
        for(let i = 0; i < eel._py_functions.length; i++) {
            let name = eel._py_functions[i];
            eel[name] = function() {
                let py_call = eel._py_call(name, arguments);
                eel._mock_queue.push(py_call);
            }
        }
    },
    
    _import_py_function: function(name) {
        let func_name = name;
        eel[name] = function() {
            let py_call = eel._py_call(func_name, arguments);
            eel._websocket.send(JSON.stringify(py_call))
        }
    },
    
    _py_call: function(name, args) {
        let arg_array = [];
        for(let i = 0; i < args.length; i++){
            arg_array.push(args[i]);
        }
        return {'name': name, 'args': arg_array};
    },
    
    _init: function() {
        eel._mock_py_functions();
        
        let websocket_addr = (window.location.origin + '/eel').replace('http', 'ws');
        eel._websocket = new WebSocket(websocket_addr);
        
        eel._websocket.onopen = function() {
            for(let i = 0; i < eel._py_functions.length; i++){
                let py_function = eel._py_functions[i];
                eel._import_py_function(py_function);
            }
            
            while(eel._mock_queue.length > 0){
                let py_call = eel._mock_queue.shift();
                eel[py_call.name](...py_call.args);
            }
        };
        
        eel._websocket.onmessage = function (e) {
            let call = JSON.parse(e.data);
            if(call.name in eel._exposed_functions){
                eel._exposed_functions[call.name](...call.args);
            }
        };
    }
}

eel._init();