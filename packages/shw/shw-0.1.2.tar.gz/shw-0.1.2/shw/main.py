import os
import json
import argparse
import traceback

home_dir = os.path.expandvars('$HOME')
def init():
    config_file = home_dir+'/.shw.json'
    if not os.path.exists(config_file):
        print 'config file not found, generating...'
        comments = """{
  "_comments": [
    "cmd is the ssh command",
    "name is about the name you gonna type."
  ],  
  "hosts": [
          {   
                  "cmd": "ssh command...",
                  "todo": "......"
          },  
          {"example": {
                  "cmd": "ssh username@host -p port"
          }
    }
  ]
}"""
        with open(config_file, 'a') as f:
            f.writelines(comments)

    # todo: error caption for wrong json format
    try:
        with open(config_file, 'rb') as f:
            json_data = json.load(f)
    except:
        print 'please check your ~/.shw.json file format'
    # else:
        # pass
    return json_data

def parse_json(json_data, key):
    try:
        return json_data.get('hosts')[1].get(key).get('cmd')
    except AttributeError, e:
        print traceback.format_exc()
        # print repr(e)
        print 'please make sure you type the right name~\n'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", action='store', type=str, help='ssh name')
    args = parser.parse_args()
    return args


def main():
    json_data = init()
    args = parse_args()
    command = parse_json(json_data, args.n)
    os.system(command)
    # print args.n, type(args.n)


if __name__ == '__main__':
    main()

