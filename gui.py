from tkinter import *
from tkinter.ttk import *
from control_chromecasts import Control_Chromecasts

class DummyDevice():
    def __init__(self,name):
        self.friendly_name=name
class DummyStatus():
    def __init__(self,vl):
        self.volume_level=vl
class DummyChromecast():
    def __init__(self, name):
        self.device = DummyDevice(name)
        self.status = DummyStatus(0.5)

    def wait(self):
        pass

    def set_volume(self, v):
        self.status.volume_level=v


class Control_Chromecasts_Gui():
    def __init__(self, master):
        frame = Frame(master, width=768, height=576)
        frame.pack()
        self.master = master
        self.mainframe = frame
        self.chromecasts=[]

        self.button = Button(
            frame, text="Exit", command=frame.quit
        )
        self.button.pack(side=BOTTOM)
        self.research = Button(
            frame, text="Search for CCs", command=self.__get_chromecasts
        )
        self.research.pack(side=BOTTOM)

        self.Found_CCs=Label(self.mainframe, text="Found chromecasts:")
        self.Found_CCs.pack(side=TOP)

        # Setup the chomecasts sliders
        # self.chromecasts = [DummyChromecast("Arbeitszimmer"), DummyChromecast("Küche"), DummyChromecast("Wohnung"), DummyChromecast("Wohnzimmer")]
        self.__get_chromecasts()


    def __get_chromecasts(self):
        CC = Control_Chromecasts()
        self.chromecasts = CC.chromecasts

        [c.wait() for c in self.chromecasts]
        self.frames = [self.__create_slider(c.device.friendly_name, c.status.volume_level) for c in self.chromecasts]
        [sc["frame"].pack(side=LEFT) for sc in self.frames]
        return CC.chromecasts

    def __create_slider(self, label, current_value):
        # scale = Scale(self.master, from_=100, to=0, length=300, width=20, resolution=1, label=label)
        frame = Frame(self.mainframe,relief="ridge", padding=2)
        scale = Scale(frame, from_=100, to=0, orient = "vertical", length = 300)
        scale.set(current_value*100)
        ttk_label=Label(frame, text=label)
        ttk_percentage=Label(frame, text=str(round(current_value*100,2)) + " %")

        scale.bind("<ButtonRelease-1>", self.scale_callback(label))
        scale.pack(side=BOTTOM)
        ttk_label.pack(side=TOP)
        ttk_percentage.pack(side=TOP)

        return {"label": label, "frame": frame, "ttk_label": ttk_label, "ttk_percentage": ttk_percentage}

    def scale_callback(self, i):
        return lambda v:self.scale_callback_level2(i,v)

    def scale_callback_level2(self, i, v):
        print(v.widget._name, v.widget.get())
        print(i)
        cc = next(c for c in self.chromecasts if c.device.friendly_name == i)
        if cc:
            cc.set_volume(float(v.widget.get()/100))
            print("set volume on ", cc.device.friendly_name)
            percentage_label = next(f for f in self.frames if f["label"] == i)["ttk_percentage"]
            percentage_label.configure(text=str(round(v.widget.get(),2)) + " %")
            print(0)

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == "__main__":

    root = Tk()
    root.style = Style()
    root.style.theme_use("clam")
    app = Control_Chromecasts_Gui(root)

    root.mainloop()
    root.destroy()  # optional; see description below






