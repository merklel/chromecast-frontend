from tkinter import *
from tkinter.ttk import *
from control_chromecasts import Control_Chromecasts

class DummyDevice():
    def __init__(self,name):
        self.friendly_name=name
class DummyStatus():
    def __init__(self,vl, active):
        self.volume_level=vl
        self.is_active_input=active
class DummyChromecast():
    def __init__(self, name, active=False):
        self.device = DummyDevice(name)
        self.status = DummyStatus(0.5, active)

    def wait(self):
        pass

    def set_volume(self, v):
        self.status.volume_level=v


class CC_Slider_Frame(LabelFrame):
    def __init__(self, root, cc, relief="solid", padding=0):

        super().__init__(root, relief=relief, padding=padding, style="mystyle.TFrame", text="WD")
        self.cc = cc
        self.cc.wait()

        if cc.status.is_active_input:
            self.configure(style="mystyle.green.TFrame")


        ## Create children
        current_value = cc.status.volume_level
        scale = Scale(self, from_=100, to=0, orient = "vertical", length = 300)
        scale.set(current_value*100)
        ttk_label=Label(self, text=cc.device.friendly_name)
        self.ttk_percentage=Label(self, text=str(round(current_value*100,2)) + " %")

        # set frame name
        self.configure(text="    " + cc.device.friendly_name + "    ")

        scale.bind("<ButtonRelease-1>", self.scale_callback)
        scale.pack(side=BOTTOM)
        #ttk_label.pack(side=TOP)
        self.ttk_percentage.pack(side=TOP)

    def scale_callback(self, v):
        self.cc.set_volume(float(v.widget.get() / 100))
        print("set volume on ", self.cc.device.friendly_name)
        self.ttk_percentage.configure(text=str(round(v.widget.get(), 2)) + " %")


class Control_Chromecasts_Gui():
    def __init__(self, master):
        frame = Frame(master, width=768, height=576)
        frame.pack()
        self.master = master
        self.chromecasts=[]

        # Create styles
        style = Style()
        style.configure("mystyle.TFrame", bordercolor="black", highlightthickness=5)
        style.configure("mystyle.green.TFrame", bordercolor="#00cc00", highlightthickness=20)

        self.Found_CCs=Label(frame, text="Found chromecasts:")
        self.Found_CCs.pack(side=TOP)

        # Setup the chomecasts sliders
        self.chromecasts = [DummyChromecast("Arbeitszimmer", active=True), DummyChromecast("Küche"), DummyChromecast("Wohnung"), DummyChromecast("Wohnzimmer")]
        # self.__get_chromecasts()

        self.slider_frames = [CC_Slider_Frame(self.master, cc) for cc in self.chromecasts]
        [sf.pack(side=LEFT) for sf in self.slider_frames]


        self.button = Button(frame, text="Exit", command=frame.quit)
        self.button.pack(side=BOTTOM)
        self.research = Button(frame, text="Search for CCs", command=self.__get_chromecasts)
        self.research.pack(side=BOTTOM)


    def __get_chromecasts(self):
        CC = Control_Chromecasts()
        self.chromecasts = CC.chromecasts
        return CC.chromecasts


if __name__ == "__main__":

    root = Tk()
    root.style = Style()
    root.style.theme_use("clam")
    app = Control_Chromecasts_Gui(root)

    root.mainloop()
    root.destroy()  # optional; see description below






