
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import scipy.misc

class Workspace:
    def destruct(self):
        self.master.destroy()


    def __init__(self, master, x, y, img, title):


        self.master = master
        master.overrideredirect(True)
        wx, wy = x, y 
        height, width = img.height, img.width
        master.geometry(str(width) + 'x' + str(height) + '+' + str(wx) +  '+' + str(wy))
        
        self.frame = tk.Frame(self.master)


        self.canvas = tk.Canvas(self.frame, width=width,height=height)
        data=np.array(np.random.random((width, height))*100,dtype=int) 
        #im=Image.frombytes('L', (data.shape[1],data.shape[0]), data.astype('b').tostring())
        im = img
        self.photo = ImageTk.PhotoImage(image=im)
        #self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)
        #self.canvas.place(x=-2,y=-2, width=width, height=height)
        #self.canvas.pack()


        w = tk.Label(master, 
                    compound = tk.TOP,
                    justify  = tk.LEFT,
                    text=title, 
                    font="Verdana 12 bold",
                    image=self.photo)
        w.pack()


        self.frame.pack()
class View:

    def loadMat(path):
        """
        Load matrix from path and return it.
        """
        m = (np.load(path) *255).astype("uint8")
        m = Image.fromarray(np.uint8(m), "RGB")
        return m

    def load(self, mat):
        print("load")
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry('0x0+0+0')
        height, width = self.imgAct.height, self.imgAct.width
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        rx, ry = int((sw- width*mat.shape[1] ) / 2), int((sh - height * mat.shape[0]) / 2)

        self.windows = [] 
        gap = 5
        for r in range(mat.shape[0]):
            cws = [None] * mat.shape[1]
            for c in range(mat.shape[1]):
                cm = mat[r, c]
                if int(cm[0]):
                    wnd = self.openWindow(rx + c * (width + gap), ry + r * (height+gap), self.imgNew, cm[1])
                    cws[c] = wnd
            self.windows = self.windows + cws 

        self.root.after(1000, self.destruct)
        self.root.mainloop()

    def __init__(self):


        prefix = ""
        pathNew = prefix + "mat/new.npy"
        pathAct = prefix + "mat/act.npy"
        pathCur = prefix + "mat/cur.npy"
        
        self.imgNew = View.loadMat(pathNew)
        self.imgAct = View.loadMat(pathAct)
        self.imgCur = View.loadMat(pathCur)





    def destruct(self):    
        for w in self.windows:
            if w :
                w.destruct()
        self.closeWindow(self.root)

    def closeWindow(self, wnd):
        wnd.destroy()

    def openWindow(self, x, y, img, title):
        newWindow = tk.Toplevel(self.root)
        app = Workspace(newWindow, x, y, img, title)
        return app


if __name__ == '__main__':
    mat = np.ones([4, 4,2])
    v = View()
    v.load(mat)
