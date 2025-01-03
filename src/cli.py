from core.api import api
from resources.globals import utils
from db.collection import Collection
from resources.prefetch import prefetch__db

prefetch__db()

args = utils.parse_args()
match args.get('act'):
    case None:
        print('"--act" not passed.')
    case "config.get":
        if 'param' in args:
            print(api.getOption(args['param']))
        else:
            print('\'--param\' not passed.')
    case "config.set":
        if 'param' in args and 'value' in args:
            api.setOption(args.get('param'), args['value'])
        else:
            print('\'--param\' and \'--value\' are not passed.')
    case "config.reset":
        api.resetOptions()
    case "config.all":
        options = api.getAllOptions()
        for option in options:
            print("|" + option + "|" + options[option] + "|")
    case "collections.create":
        final_params = dict()

        if 'name' not in args:
            print('Error: "--name" not passed')
            exit(-1)

        final_params["name"] = args.get("name")
        final_params["description"] = args.get("description")

        if args.get('innertype') != None:
            final_params.innertype = args.get('innertype')
        
        if args.get('icon_hash') != None:
            final_params.icon_hash = args.get('icon_hash')

        final_params.order = Collection.getAllCount()
        if args.get('add_after') != None:
            final_params.hidden = 1
            to_add = Collection.get(args.get('add_after'))
            if to_add == None:
                print('Invalid collection')
                exit(-1)
            
            final_params.to_add = to_add
        
        api.createCollection(final_params)
