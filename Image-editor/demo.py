from tkinter import ttk, Tk,PhotoImage,Canvas,filedialog

root = Tk()
my_label_object = ttk.Label(root,text="This is an example")
my_label_object.pack()

def dummy_func():
    print("press me harder")

my_button_object = ttk.Button(root,text="a button", command= dummy_func)
my_button_object.pack()

logo = PhotoImage(file = "./giphy.gif")

# ttk.Label(root,image=logo).pack()

canvas = Canvas(root, bg="gray",width=300,height=400)
canvas.pack()

canvas.create_image(300/2,400/2,image=logo)

#filename = filedialog.askopenfilename()
#print(filename)



root.mainloop()