def reset_config(config_object):
    config_object["Config"] = {"backup configured": 'False', 
                            "task?": 'False',
                            "first run": 'False',
                            "is main running": 'True'}
    
    config_object.remove_section('USB PID VID')
    config_object.remove_section('Storage Location')
    config_object.remove_section('duration')

    config_object['USB PID VID']={}
    config_object['Storage Location']={}
    config_object['duration']={}