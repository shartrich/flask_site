import os
from utils.configs.settings import PROJECT_FOLDER

bokeh_folder = 'templates/news'


def get_latest_bokeh_file():
    print('%s/%s' % (PROJECT_FOLDER, bokeh_folder))
    all_files = os.listdir('%s/%s' % (PROJECT_FOLDER, bokeh_folder))
    most_recent_file = max(all_files)
    print(most_recent_file)
    return 'news/%s' % most_recent_file
