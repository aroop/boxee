import mc
import simplejson

API_KEY = 'e5529a761ee3394ffbd237269966e9f53a4c7bf3'

lf_category = 0
lf_erun = 0
lf_video = 0

def get_categories():
    response = mc.Http().Get('http://api.giantbomb.com/video_types/?api_key=' + API_KEY + '&format=json')
    category_data = simplejson.loads(response)['results']

    categories = mc.ListItems()

    # Latest category
    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Latest'.encode('utf-8'))
    item.SetProperty('id', 'latest'.encode('utf-8'))
    categories.append(item)

    for cat in category_data:
        item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
        item.SetLabel(cat['name'].encode('utf-8'))
        item.SetProperty('id', str(cat['id']).encode('utf-8'))
        categories.append(item)

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Search'.encode('utf-8'))
    item.SetProperty('id', 'search'.encode('utf-8'))
    categories.append(item)

    return categories

def get_eruns():
    eruns = mc.ListItems()

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Deadly Premonition'.encode('utf-8'))
    item.SetProperty('id', '5-DP'.encode('utf-8'))
    eruns.append(item)

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Persona 4'.encode('utf-8'))
    item.SetProperty('id', '5-P4'.encode('utf-8'))
    eruns.append(item)

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('The Matrix Online: Not Like This'.encode('utf-8'))
    item.SetProperty('id', '5-MO'.encode('utf-8'))
    eruns.append(item)

    return eruns

def get_videos(cat_id):
    if cat_id == 'latest':
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&sort=-publish_date&format=json')
    elif cat_id == 'search':
        query = mc.ShowDialogKeyboard("Search", "", False).replace(' ', '%20')
        response = mc.Http().Get('http://api.giantbomb.com/search/?api_key=' + API_KEY + '&resources=video&query=' + query + '&format=json')
    elif cat_id == '5-DP':
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=5&offset=161&format=json')
    elif cat_id == '5-P4':
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=5&format=json')
    elif cat_id == '5-MO':
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=5&offset=105&limit=21&format=json')
    else:
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=' + cat_id + '&sort=-publish_date&format=json')

    video_data = simplejson.loads(response)['results']

    if cat_id == '5-P4':
        response = mc.Http().Get('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=5&offset=100&limit=61&format=json')
        video_data += simplejson.loads(response)['results']
        video_data = [video for video in video_data if not video['name'].startswith('The Matrix Online')]
    elif cat_id == '5-MO':
        video_data = [video for video in video_data if video['name'].startswith('The Matrix Online')]

    videos = mc.ListItems()

    border = 'bg_imgFlare_640x360.png'.encode('utf-8')
    for vid in video_data:
        date = vid['publish_date'].encode('utf-8').split(' ')[0].split('-')
        item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        item.SetLabel(vid['name'].encode('utf-8'))
        item.SetDescription(vid['deck'].encode('utf-8'))
        item.SetThumbnail(vid['image']['super_url'].encode('utf-8'))
        item.SetImage(0, border)
        item.SetPath('http://media.giantbomb.com/video/' + vid['url'].replace('.mp4', '_1500.mp4').encode('utf-8'))
        item.SetDate(int(date[0]), int(date[1]), int(date[2]))
        videos.append(item)

        if border == 'bg_imgFlare_640x360.png'.encode('utf-8'):
            border = 'bg_imgFlare2_640x360.png'.encode('utf-8')
        else:
            border = 'bg_imgFlare_640x360.png'.encode('utf-8')

    return videos
