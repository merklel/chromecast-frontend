from tkinter import *
from tkinter.ttk import *
from chromecast_volumecontrol.control_chromecasts import Control_Chromecasts
import time
import os

# Settings
TIME_BETWEEN_UPDATES = 2 # Time between updates of the sliders: read from the chromecasts

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

        if cc.status.status_text != "":
            self.configure(style="mystyle.green.TFrame")


        ## Create children
        current_value = cc.status.volume_level
        self.scale = Scale(self, from_=100, to=0, orient = "vertical", length = 300)
        self.scale.set(current_value*100)
        ttk_label=Label(self, text=cc.device.friendly_name)
        self.ttk_percentage=Label(self, text=str(round(current_value*100,2)) + " %")

        # set frame name
        self.configure(text="    " + cc.device.friendly_name + "    ")

        self.scale.bind("<ButtonRelease-1>", self.scale_callback)
        self.scale.pack(side=BOTTOM)
        #ttk_label.pack(side=TOP)
        self.ttk_percentage.pack(side=TOP)



    def scale_callback(self, v):
        self.cc.set_volume(float(v.widget.get() / 100))
        print("set volume on ", self.cc.device.friendly_name)
        self.ttk_percentage.configure(text=str(round(v.widget.get(), 2)) + " %")

    def update_percent_label(self):
        current_value = round(self.cc.status.volume_level,2)
        self.ttk_percentage.configure(text=str(current_value) + " %")
        self.scale.set(current_value*100)


class Control_Chromecasts_Gui():
    def __init__(self, master):

        self.frame_top_line = Frame(master)
        self.frame_top_line.pack(side=TOP)

        self.frame = Frame(master, width=768, height=576)
        self.frame.pack(side=TOP)

        frame_buttons = Frame(master)
        frame_buttons.pack(side=BOTTOM)


        self.master = master
        self.chromecasts=[]
        self.slider_frames=[]

        # Create styles
        style = Style()
        style.configure("mystyle.TFrame", bordercolor="black", highlightthickness=5)
        style.configure("mystyle.green.TFrame", bordercolor="#00cc00", highlightthickness=20)

        # self.button = Button(frame, text="Exit", command=None)
        # self.button.pack(side=BOTTOM)
        self.research = Button(frame_buttons, text="Search for CCs", command=self.__get_chromecasts)
        self.research.pack(side=LEFT)
        self.research = Button(frame_buttons, text="Manual update control", command=self.manual_update)
        self.research.pack(side=LEFT)
        self.research = Button(frame_buttons, text="Exit", command=self.exit)
        self.research.pack(side=LEFT)

        self.load_label = Label(self.frame_top_line, text="Currently looking for chromecasts, be patient...")
        self.load_label.pack()

    def exit(self):
        self.master.destroy()

    def get_and_draw_chromecasts(self):
        # Setup the chomecasts sliders
        # self.chromecasts = [DummyChromecast("Arbeitszimmer", active=True), DummyChromecast("Küche"), DummyChromecast("Wohnung"), DummyChromecast("Wohnzimmer")]
        self.__get_chromecasts()

        self.slider_frames = [CC_Slider_Frame(self.frame, cc) for cc in self.chromecasts]
        [sf.pack(side=LEFT) for sf in self.slider_frames]

        self.Found_CCs=Label(self.frame_top_line, text="Found chromecasts:")
        self.Found_CCs.pack(side=TOP)
        self.load_label.destroy()

    def __get_chromecasts(self):
        CC = Control_Chromecasts()
        self.chromecasts = CC.chromecasts
        return CC.chromecasts

    def manual_update(self):
        # update ccs
        [cc.wait() for cc in self.chromecasts]

        # update percent label
        [cf.update_percent_label() for cf in self.slider_frames]



if __name__ == "__main__":

    root = Tk()
    # root.wm_iconbitmap(bitmap="@ico/cc.xbm")
    root.iconphoto(True, PhotoImage(file=os.path.abspath(os.path.join("chromecast_volumecontrol/ico/")) +"/cc.png"))
    root.protocol("WM_DELETE_WINDOW", root.iconify)
    root.style = Style()
    root.title("Control my Chromecasts")
    root.style.theme_use("clam")
    app = Control_Chromecasts_Gui(root)
    root.update_idletasks()
    root.update()

    app.get_and_draw_chromecasts()

    s0=time.monotonic()
    while True:
        root.update_idletasks()
        root.update()

        # print(s0)
        # print(time.monotonic())
        if time.monotonic()-s0 > TIME_BETWEEN_UPDATES:
            print("update")
            app.manual_update()
            s0=time.monotonic()

    root.destroy()  # optional; see description below






