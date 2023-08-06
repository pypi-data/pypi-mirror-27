from inscriptis import get_text

class RSSResult:
    def __init__(self, feed):
        self.feed = feed
        self._raw = self.get_raw(feed)

    def __str__(self):
        return self.raw()

    def text(self):
        result = get_text(self._raw.strip().replace("\t","").replace('<br />', '\n'))
        return result

    def raw(self):
        return self._raw

    def get_raw(self, feed):
        if len(feed) == 0:
            return None
        if len(feed[0]) == 0:
            return None
        return feed[0][0]
