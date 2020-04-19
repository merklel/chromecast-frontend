import pychromecast



class Control_Chromecasts():
    def __init__(self):
        self.chromecasts = pychromecast.get_chromecasts()
        print(self.chromecasts)

    def get_chromecast_names(self):
        names = [c.device.friendly_name for c in self.chromecasts]
        return names



if __name__ == "__main__":
    cc = Control_Chromecasts()

    print(cc.get_chromecast_names())







