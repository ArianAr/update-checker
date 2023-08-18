import json

def read_settings_file():
    with open('settings.json') as f:
      settings = json.load(f)
    return settings

def write_settings_file(settings):
    with open('settings.json', 'w') as f:
      json.dump(settings, f, indent=2)

settings = read_settings_file()

PROGRAMS = settings['programs']
BOT_TOKEN = settings['telegram']['token']
CHAT_ID = settings['telegram']['chat_id']