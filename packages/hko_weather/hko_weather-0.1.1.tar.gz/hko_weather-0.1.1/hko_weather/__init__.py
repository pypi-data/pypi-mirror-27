import requests
from xml.etree import ElementTree
from hko_weather.models import RSSResult

RSS_FEED_LIST = {
    'current_weather': "http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml",
    'current_warning_summary': "http://rss.weather.gov.hk/rss/WeatherWarningSummaryv2_uc.xml",
    'current_warning_bullet': "http://rss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml",
    'local_forecast': "http://rss.weather.gov.hk/rss/LocalWeatherForecast_uc.xml",
    'nine_days_forecast': "http://rss.weather.gov.hk/rss/SeveralDaysWeatherForecast_uc.xml",
    'world_earth_quake': "http://rss.weather.gov.hk/rss/QuickEarthquakeMessage_uc.xml",
    'local_earth_quake': "http://rss.weather.gov.hk/rss/FeltEarthquake_uc.xml",
}

def base_rss(url_name, lang="zh"):
    rss_url = RSS_FEED_LIST[url_name]
    if(lang != "zh"):
        rss_url = rss_url.replace("_uc","")
    r = requests.get(rss_url)
    tree = ElementTree.fromstring(r.content)
    item = tree.findall('channel/item')
    feed=[]
    for entry in item:
        #get description, url, and thumbnail
        desc = entry.findtext('description')
        feed.append([desc])
    return RSSResult(feed)

def current_weather(lang="zh"):
    return base_rss("current_weather", lang=lang)

def current_warning_summary(lang="zh"):
    return base_rss("current_warning_summary", lang=lang)

def current_warning_bullet(lang="zh"):
    return base_rss("current_warning_bullet", lang=lang)

def local_forecast(lang="zh"):
    return base_rss("local_forecast", lang=lang)

def nine_days_forecast(lang="zh"):
    return base_rss("nine_days_forecast", lang=lang)

def world_earth_quake(lang="zh"):
    return base_rss("world_earth_quake", lang=lang)

def local_earth_quake(lang="zh"):
    return base_rss("local_earth_quake", lang=lang)
