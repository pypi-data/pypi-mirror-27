===========
Hyperion V0.0.1
===========

Hyperion provides an intuitive and efficient way to store logs from python into AWS CloudWatch.
Typical usage looks like this::

    #Create an alias for the package
    import hyperion

    #returns a logger with the cloud watch handler established.  The steam name should be unique to the application.
    log = hyperion.get_logger(stream_name="holy_grail_app",log_group='monty_python')

    additional parameters for get_logger(stream_name,log_group,default_level):
    stream_name = the unique stream that the logs will be inserted into. defaults to: test_stream
    log_group = the group of streams that are associated with your team. defaults to: test_group
    default_level = the default logging level ie: debug,info,warning,error,critical. defaults to: info


    #Any log functions or configurations can be done to the log object returned.
    log.setLevel(logging.DEBUG)




