#Made by multimokia
#Version 1.0.0
init -980 python in submod_utils:
    import inspect
    import store

    #Store the current label for use elsewhere
    current_label = None
    #Last label
    last_label = None

    function_plugins = dict()

    #START: Decorator Function
    def functionplugin(_label, _args=[]):
        """
        Decorator function to register a plugin
        """
        def wrap(_function):
            registerFunction(
                _label,
                _function,
                _args
            )
            return _function
        return wrap

    #START: Internal functions
    def getAndRunFunctions(key=None):
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins

        #If the key isn't provided, we assume it from the caller
        if not key:
            key = inspect.stack()[1][3]

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        for _action, args in func_dict.iteritems():
            try:
                store.run(_action, args)
            except Exception as ex:
                store.mas_utils.writelog("[ERROR]: function {0} failed because {1}\n".format(_action.__name__, ex))

    def registerFunction(key, _function, args=[]):
        """
        Registers a function to the function_plugins dict
        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable

        IN:
            key - key to add the function to
            _function - function to add
            args - list of args (must be in order) to pass to the function (Default: [])

        OUT:
            boolean:
                - True if the function was registered successfully
                - False otherwise
        """
        global function_plugins

        #Verify that the function is callable
        if not callable(_function):
            store.mas_utils.writelog("[ERROR]: {0} is not callable\n".format(_function.__name__))
            return False

        #Too many args
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.writelog("[ERROR]: Too many args provided for function {0}\n".format(_function.__name__))
            return False

        #Create the key if we need to
        if key not in function_plugins:
            function_plugins[key] = dict()

        #If we just created a key, then there won't be any existing values so we elif
        elif _function in function_plugins[key]:
            return False

        function_plugins[key][_function] = args
        return True

    def getArgs(key, _function):
        """
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        if not func_dict:
            return

        return func_dict.get(_function)

    def setArgs(key, _function, args=[]):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args
            args - list of args (must be in order) to pass to the function (Default: [])

        OUT:
            boolean:
                - True if args were set successfully
                - False if not
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in dict
        elif _function not in func_dict:
            return False

        #Too many args provided
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.writelog("[ERROR]: Too many args provided for function {0}\n".format(_function.__name__))
            return False

        #Otherwise we can set
        func_dict[_function] = args
        return True

    def unregisterFunction(key, _function):
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            _function - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins

        func_dict = function_plugins.get(key)

        #Key doesn't exist
        if not func_dict:
            return False

        #Function not in plugins dict
        elif _function not in func_dict:
            return False

        #Otherwise we can pop
        function_plugins[key].pop(_function)
        return True

#Global run area
init -990 python:
    def run(_function, args):
        """
        Runs a function in the global store
        """
        return _function(*args)

#Label callback to get last label and run function plugins from the label
init 999 python:
    def label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        #First, update the last label to what was current
        store.submod_utils.last_label = store.submod_utils.current_label
        #Now we can update the current
        store.submod_utils.current_label = name
        #Run functions
        store.submod_utils.getAndRunFunctions(name)

    config.label_callback = label_callback