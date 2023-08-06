def new_server(args):
    attr_list = ['<ip>', '<username>', '<name>', '<location>']
    new_server = {}
    for attr in attr_list:
        if attr in args.keys():
            pretty_attr = attr.replace('<', '').replace('>', '')
            new_server[pretty_attr] = args[attr]
    return new_server
