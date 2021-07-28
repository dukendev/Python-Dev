from tkinter import ttk,Tk,PhotoImage,Canvas, filedialog, colorchooser,RIDGE,GROOVE,ROUND,Scale,HORIZONTAL
import cv2
from PIL import ImageTk, Image
import numpy as np

class frontEnd:
    def __init__(self,master):
        self.master = master
        self.menuInitialisation()

    def menuInitialisation(self):
        self.master.geometry('750x630+250+10')
        self.master.title('Swift Meme Editor - Tkinter and OpenCV')
#master is root window which is passed to this class

#We have header frame
        self.frameHeader = ttk.Frame(self.master)
        self.frameHeader.pack()

        self.logo = PhotoImage(file="./giphy.gif").subsample(5,3)
        ttk.Label(self.frameHeader,image=self.logo).grid(row=0,column=0,rowspan=3)


#using grid geometry manager here istead of pack() because it is more flexible

#frames we will use pack and for labels we will use grid

        ttk.Label(self.frameHeader,text="Swift Image editor for Memes!").grid(row=1,column=2)

        ttk.Label(self.frameHeader,text="Tkinter and OpenCV project").grid(row=2,column=2)
        
        self.frameMenu = ttk.Frame(self.master)
        self.frameMenu.pack()
        self.frameMenu.config(relief=RIDGE,padding=(50,15))

        ttk.Button(self.frameMenu,text="Upload",command=self.uploadAction).grid(row=0,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Crop",command=self.cropAction).grid(row=1,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Add text",command=self.textAction).grid(row=2,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Draw",command=self.drawAction).grid(row=3,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Filters",command=self.filtersAction).grid(row=4,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Blur",command=self.blurAction).grid(row=5,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Levels",command=self.levelsAction).grid(row=6,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Rotate",command=self.rotateAction).grid(row=7,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Flip",command=self.flipAction).grid(row=8,column=0,padx=5,pady=5)
        ttk.Button(self.frameMenu,text="Save as",command=self.saveAction).grid(row=9,column=0,padx=5,pady=5)
    #Bottom frame ---------------------------------------------------------------------------------
        self.frameBottom = ttk.Frame(self.master)
        self.frameBottom.pack()

        ttk.Button(self.frameBottom,text="Apply",command=self.applyAction).grid(row=0,column=0,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameBottom,text="Cancel",command=self.cancelAction).grid(row=0,column=1,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameBottom,text="Undo",command=self.undoAction).grid(row=0,column=2,padx=5,pady=5,sticky='sw')

    #canvas it is part of main frame only-------------------------------------------------------

        self.canvas = Canvas(self.frameMenu ,bg = "gray",width = 300,height = 400)
        self.canvas.grid(row=0, column=1, rowspan=10)



   #function to handle refresh of Sub menus

    def refreshSubMenu(self):
        try :
            self.frameSubMenu.grid_forget()
        except:
            pass
        
        self.frameSubMenu = ttk.Frame(self.frameMenu)
        self.frameSubMenu.grid(row=0,column=2,rowspan=10)
        self.frameSubMenu.config(relief=GROOVE,padding=(50,15))

    #Menu functions========================================================================================= 
    
    def uploadAction(self):

        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()
        self.original_image = cv2.imread(self.filename)

        self.edited_image = cv2.imread(self.filename)
        self.filtered_image = cv2.imread(self.filename)
        self.display_image(self.edited_image)

    #----------------------------------------------------------------------------------------------------------
       
    def cropAction(self):
        self.rectangle_id = 0
        
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0

        self.canvas.bind("<ButtonPress>", self.startCrop)
        self.canvas.bind("<B1-Motion>", self.Crop)
        self.canvas.bind("<ButtonRelease>", self.endCrop)

    #---------------------------------------------------------------------------------------------------------    
    def textAction(self):
        self.text_extracted = "Enter text here"
        self.refreshSubMenu()
        
        ttk.Label(self.frameSubMenu, text="Enter text here").grid(row=0, column=2, padx=5, pady=5, sticky='sw')
        self.text_on_image = ttk.Entry(self.frameSubMenu)
        self.text_on_image.grid(row=1, column=2, padx=5, sticky='sw')

        ttk.Button(self.frameSubMenu, text="Pick A Font Color", command=self.chooseColor).grid(row=2, column=2, padx=5, pady=5, sticky='sw')
        self.textActionHelper()

    #--------------------------------------------------------------------------------------------------------
    def drawAction(self):
        self.color_code = ((255, 0, 0), '#ff0000')
        self.refreshSubMenu()
        self.canvas.bind("<ButtonPress>", self.startDraw)
        self.canvas.bind("<B1-Motion>", self.Draw)
        self.draw_color_button = ttk.Button(self.frameSubMenu, text="Choose A Color", command=self.chooseColor)
        self.draw_color_button.grid(row=0, column=2, padx=5, pady=5, sticky='sw')
    
    #---------------------------------------------------------------------------------------------------------
    def filtersAction(self):

        self.refreshSubMenu()
        ttk.Button(self.frameSubMenu,text="Negative",command=self.negativeAction).grid(row=0,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Black & White",command=self.bnwAction).grid(row=1,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Stylize",command=self.stylizeAction).grid(row=2,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Sketch",command=self.sketchAction).grid(row=3,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Emboss",command=self.embossAction).grid(row=4,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Sepia",command=self.sepiaAction).grid(row=5,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Binary Thresholding",command=self.binaryThresholdingAction).grid(row=6,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Erosion",command=self.erosionAction).grid(row=7,column=2,padx=5,pady=5,sticky='sw')
        ttk.Button(self.frameSubMenu,text="Dilation",command=self.dilationAction).grid(row=8,column=2,padx=5,pady=5,sticky='sw')

    #----------------------------------------------------------------------------------------------------------
    def blurAction(self):

        self.refreshSubMenu()

        ttk.Label(self.frameSubMenu, text="Averaging Blur").grid(row=0, column=2, padx=5, sticky='sw')

        self.averageSlider = Scale(self.frameSubMenu, from_=0, to=256, orient=HORIZONTAL, command=self.averagingAction)
        self.averageSlider.grid(row=1, column=2, padx=5,  sticky='sw')

        ttk.Label(self.frameSubMenu, text="Gaussian Blur").grid(row=2, column=2, padx=5, sticky='sw')

        self.gaussianSlider = Scale(self.frameSubMenu, from_=0, to=256, orient=HORIZONTAL, command=self.gaussianAction)
        self.gaussianSlider.grid(row=3, column=2, padx=5,  sticky='sw')

        ttk.Label(self.frameSubMenu, text="Median Blur").grid(row=4, column=2, padx=5, sticky='sw')

        self.medianSlider = Scale(self.frameSubMenu, from_=0, to=256, orient=HORIZONTAL, command=self.medianAction)
        self.medianSlider.grid(row=5, column=2, padx=5,  sticky='sw')
    
    #-----------------------------------------------------------------------------------------------------------------
    def levelsAction(self):
        self.refreshSubMenu()
        ttk.Label(self.frameSubMenu, text="Brightness").grid(row=0, column=2, padx=5, pady=5, sticky='sw')

        self.brightness_slider = Scale(self.frameSubMenu, from_=0, to_=2,  resolution=0.1, orient=HORIZONTAL, command=self.brightnessAction)
        self.brightness_slider.grid(row=1, column=2, padx=5,  sticky='sw')
        self.brightness_slider.set(1)

        ttk.Label(self.frameSubMenu, text="Saturation").grid(row=2, column=2, padx=5, pady=5, sticky='sw')
        self.saturation_slider = Scale(self.frameSubMenu, from_=-200, to=200, resolution=0.5, orient=HORIZONTAL, command=self.saturationAction)
        self.saturation_slider.grid(row=3, column=2, padx=5,  sticky='sw')
        self.saturation_slider.set(0)


    #--------------------------------------------------------------------------------------------------------------
    def rotateAction(self):
        self.refreshSubMenu()
        ttk.Button(self.frameSubMenu, text="Rotate Left", command=self.rotateLeftAction).grid(row=0, column=2, padx=5, pady=5, sticky='sw')
        ttk.Button(self.frameSubMenu, text="Rotate Right", command=self.rotateRightAction).grid(row=1, column=2, padx=5, pady=5, sticky='sw')
    #-------------------------------------------------------------------------------------------------------------
    def flipAction(self):
        self.refreshSubMenu()
        ttk.Button(self.frameSubMenu, text="Vertical Flip", command=self.verticalAction).grid(row=0, column=2, padx=5, pady=5, sticky='sw')
        ttk.Button(self.frameSubMenu, text="Horizontal Flip", command=self.horizontalAction).grid(row=1, column=2, padx=5, pady=5, sticky='sw')
    #-------------------------------------------------------------------------------------------------------------
    def saveAction(self):
        original_file_type = self.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        save_as_image = self.edited_image
        cv2.imwrite(filename, save_as_image)
        self.filename = filename

    #--------------------------------------------------------------------------------------------------------------
    def applyAction(self):
        self.edited_image = self.filtered_image
        self.display_image(self.edited_image)

    #---------------------------------------------------------------------------------------------------------------
    def cancelAction(self):
        self.display_image(self.edited_image)

    #---------------------------------------------------------------------------------------------------------------
    def undoAction(self):
        self.edited_image = self.original_image.copy()
        self.display_image(self.original_image)

    
    #======================================================functions of subMenu buttons and others===============================================================



    #functions of Filter submenu----------------------------------------------------------------


    def negativeAction(self):
        self.filtered_image = cv2.bitwise_not(self.edited_image)
        self.display_image(self.filtered_image)

    def bnwAction(self):
        self.filtered_image = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)
        self.display_image(self.filtered_image)

    def stylizeAction(self):
        self.filtered_image = cv2.stylization(self.edited_image, sigma_s=150, sigma_r=0.25)
        self.display_image(self.filtered_image)

    def sketchAction(self):
        ret, self.filtered_image = cv2.pencilSketch(self.edited_image, sigma_s=60, sigma_r=0.5, shade_factor=0.02)
        self.display_image(self.filtered_image)

    def embossAction(self):
            kernel = np.array([[0, -1, -1],[1, 0, -1],[1, 1, 0]])
            self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
            self.display_image(self.filtered_image)

    def sepiaAction(self):
        kernel = np.array([[0.272, 0.534, 0.131],[0.349, 0.686, 0.168],[0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
        self.display_image(self.filtered_image)

    def binaryThresholdingAction(self):
        ret, self.filtered_image = cv2.threshold(self.edited_image, 127, 255, cv2.THRESH_BINARY)
        self.display_image(self.filtered_image)
        
    def erosionAction(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_image = cv2.erode(self.edited_image, kernel, iterations=1)
        self.display_image(self.filtered_image)

    def dilationAction(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_image = cv2.dilate(self.edited_image, kernel, iterations=1)
        self.display_image(self.filtered_image)

# Blur Sub menu functions-----------------------------------------------------------------
    def averagingAction(self,value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_image = cv2.blur(self.edited_image, (value, value))
        self.display_image(self.filtered_image)

    def gaussianAction(self,value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_image = cv2.GaussianBlur(self.edited_image, (value, value), 0)
        self.display_image(self.filtered_image)

    def medianAction(self,value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.filtered_image = cv2.medianBlur(self.edited_image, value)
        self.display_image(self.filtered_image)
# Rotate sub menu functions--------------------------------------------------------------
    def rotateLeftAction(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.display_image(self.filtered_image)

    def rotateRightAction(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_CLOCKWISE)
        self.display_image(self.filtered_image)

# Flip Sub Menu functions----------------------------------------------------------------
    def verticalAction(self):
        self.filtered_image = cv2.flip(self.filtered_image, 0)
        self.display_image(self.filtered_image)
    def horizontalAction(self):
        self.filtered_image = cv2.flip(self.filtered_image, 2)
        self.display_image(self.filtered_image)

# Levels sub menu function---------------------------------------------------------------
    def saturationAction(self,event):
        self.filtered_image = cv2.convertScaleAbs(self.edited_image, alpha=1, beta=self.saturation_slider.get())
        self.display_image(self.filtered_image)

    def brightnessAction(self,value):
        self.filtered_image = cv2.convertScaleAbs(self.edited_image, alpha=self.brightness_slider.get())
        self.display_image(self.filtered_image)



#Draw helper and subMenu function---------------------------------------------------------
    def startDraw(self,event):
        self.x = event.x
        self.y = event.y
        self.draw_ids = []

    def Draw(self,event):
        
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,fill=self.color_code[-1], capstyle=ROUND, smooth=True))

        cv2.line(self.filtered_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
                 (int(event.x * self.ratio), int(event.y * self.ratio)), (0, 0, 255), thickness=int(self.ratio * 2),lineType=8)

        self.x = event.x
        self.y = event.y

    def chooseColor(self):
        self.color_code = colorchooser.askcolor(title="Choose color")

#Crop Submenu and helper functions-------------------------------------------------------
    def startCrop(self,event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y
    
    def Crop(self,event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,self.crop_end_x, self.crop_end_y, width=1)

    def endCrop(self,event):

        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        self.filtered_image = self.edited_image[y, x]
        self.display_image(self.filtered_image)


#Text Submenu helper function--------------------------------------------------------------
    def textActionHelper(self):
        self.rectangle_id = 0
        # self.ratio = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.canvas.bind("<ButtonPress>", self.startCrop)
        self.canvas.bind("<B1-Motion>", self.Crop)
        self.canvas.bind("<ButtonRelease>", self.endTextCrop)

    def endTextCrop(self,event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        if self.text_on_image.get():
            self.text_extracted = self.text_on_image.get()
        start_font = start_x, start_y
        #print(self.color_code)#((r,g,b),'#ff00000')
        r, g, b = tuple(map(int, self.color_code[0]))

        self.filtered_image = cv2.putText(self.edited_image, self.text_extracted, start_font, cv2.FONT_HERSHEY_SIMPLEX, 2, (b, g, r), 5)
        self.display_image(self.filtered_image)

#utility function for displaying image on canvas-------------------------------------------
    def display_image(self, image=None):

        self.canvas.delete("all")
        if image is None:
            image = self.edited_image.copy()
        else:
            image = image

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > 400 or width > 300:
            if ratio < 1:
                new_width = 300
                new_height = int(new_width * ratio)
            else:
                new_height = 400
                new_width = int(new_height * (width / height))
        
        #This ratio is calculated for crop function
        self.ratio = height / new_height
        self.new_image = cv2.resize(image, (new_width, new_height))

        self.new_image = ImageTk.PhotoImage(Image.fromarray(self.new_image))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2,  image=self.new_image)





root = Tk()
frontEnd(root)
root.mainloop()
