from datetime import datetime
from deep_translator import exceptions
from objects import translator , fix_sub , fix_big_data , fix_another_problem
import tkinter as tk
from tkinter import filedialog
from arabic_reshaper import reshape #fix persian font 1
from bidi.algorithm import get_display #fix persian font 2
from os import mkdir , remove , path


def chek_file_len (path):
        with open (path , 'r' , encoding='utf-8') as file :
            len_file = file.read()
        return len (len_file)

def open_pathFile (path):
    with open (path , 'r' , encoding='utf-8') as file:
        content = file.read()
        output = reshape(content)
        biditext = get_display (output)
        return biditext

def write_pathFile (path , text):
    ob4 = fix_big_data(path)
    ob4.remove_file(path)
    #
    with open (path , 'w+' , encoding='utf-8') as file :
        file.write(text)

def open_file ():
    content = ''
    file_path = filedialog.askopenfilename()
    with open (file_path , 'r' , encoding='utf-8') as file :
        content = file.read()
    
    file_path = file_path.split('/')
    new_file = file_path [len(file_path)-1].split('.')
    new_file[0] += '(fix)'
    file_path [len(file_path)-1] = '.'.join(new_file)
    file_path = '/'.join(file_path)
    with open (file_path , 'w+' , encoding='utf-8') as file :
        file.write (content)

    #
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)
    #
    #enter subtitle in sub_entry textbox
    sub_entry.delete(1.0, tk.END)
    sub_entry.insert(1.0, open_pathFile(entry_path.get()))
    translate_entry.delete (1.0 , tk.END)

def save ():
    #
    
    #
    path_save = filedialog.asksaveasfilename()
    path_save = path_save.split('/')
    path_save.insert(len(path_save)-1 , f'data')
    
    if '.' in path_save[len(path_save)-1] :
        fix = path_save[len(path_save)-1]
        #print ('fix first is : ' , fix)
        fix = fix.split('.')
        #print ('fix list is : ' , fix)
        for i in range (0 , len(fix)-1 , 1) :
            fix.pop()
        #print ('fix after pop is : ' , fix)
        fix.append('srt')
        #print ('fix after append is : ' , fix)
        path_save[len(path_save)-1] = '.'.join(fix)
    #
    if '.srt' not in path_save[len(path_save)-1] :
        path_save[len(path_save)-1] += '.srt'
    
    else : pass
    path_save = '/'.join(path_save)
    #
    make_data_folder = path_save
    make_data_folder = make_data_folder.split('/')
    make_data_folder.pop()
    #
    make_data_folder = '/'.join(make_data_folder)
    print(f'make_data_folder is : {make_data_folder}')
    if not path.exists (make_data_folder) :
        mkdir (make_data_folder)
    else :
        # remove (make_data_folder)
        # mkdir (make_data_folder)
        pass
    #
    entry_nameFile.delete(0 , tk.END)
    entry_nameFile.insert(0 , path_save)

def translate():
    time = str(datetime.now())
    time = time.split('.')
    time.pop()
    time = ''.join(time)
    time = time.replace(':', '')
    time = time.replace(' ', '_')
    path_save = entry_nameFile.get()
    #
    path_file_to_translate = entry_path.get()
    List_path = path_file_to_translate.split('/')

    # path_file_to_make_sub = List_path
    # path_file_to_make_sub.pop()

    path_file_to_make_sub = path_save #'/'.join(path_file_to_make_sub) +'/' + entry_nameFile.get() + '.srt' ###
    print ('\npath_file_to_make_sub (text)= ' , path_file_to_make_sub)

    path_file_to_make_fix_sub = path_file_to_make_sub.replace('.srt', '.ass')
    print ('\npath_file_to_make_fix_sub = ' , path_file_to_make_fix_sub)
    List_path = path_file_to_make_fix_sub.split('/')
    sliced_path_file = List_path
    sliced_path_file.pop()

    sliced_path_file = '/'.join(sliced_path_file)
    print ('\nsliced path file = ' , sliced_path_file)
    List_path = sliced_path_file.split('/')
    file_len_checker = '/'.join(List_path) + "/file_len_checker.txt"
    print ('\nFile len checker = ' , file_len_checker)


    name_slicing_file = 1
    list_slicing_file = []
    darsad = 1
    slice_meter = 50

    ##############################################################################################################
    # 
    try:
        ob = translator()
        ob.translate(path_file_to_translate) #translate subtitle
        ob.make_sub(path_file_to_make_sub) #make subtitle but its have some problem writing
        #
        #enter translated test in to the translate_entry
        translate_entry.delete(1.0, tk.END)
        translate_entry.insert(1.0, open_pathFile(path_file_to_make_sub))
        #
        ob2 = fix_sub()
        ob2.get_file(path_file_to_make_sub) #it get the persian subtitle who we make that
        ob2.get_times() 
        ob2.get_subs()
        ob2.make_fix_sub (path_file_to_make_fix_sub) #it make a persian subtitle without eny problem
        

    except exceptions.NotValidLength: #if english subtitle will be biger than 5000 character , this will run
        while True :
            ob = fix_big_data(path_file_to_translate)
            ob.slic_meter = slice_meter
            ob.getFile()
            print ("File loaded")
            terminal_entry.insert (tk.END , "\nFile loaded")
            #
            
            name_slice_file = file_len_checker #it is a file to name 'file_len_checker.txt' for check sliced files len
            ob.slicFile(name_slice_file , 0) # it slic our file ('name_slice_file') , if method == 0 ==> at first will write subtitle settings
            #
            print ("Check len file ...")
            terminal_entry.insert (tk.END , "\nCheck len file ...")

            if chek_file_len (name_slice_file) > 5000 :
                slice_meter -= 10
                ob.remove_file(name_slice_file)
                print ("oops , I should delet this :)")
                terminal_entry.insert (tk.END , "\noops , I should delet this :)")

                continue
            else :
                name_slice_file = fr"{sliced_path_file}\y({time})({name_slicing_file}).txt"
                ob.getFile()
                ob.slicFile (name_slice_file , 1)
                print (f"file y({time})({name_slicing_file}).txt created")
                terminal_entry.insert (tk.END , f"\nfile y({time})({name_slicing_file}).txt created")

                ob.remove_file (file_len_checker)
                list_slicing_file.append (name_slice_file)
            
            if chek_file_len(path_file_to_translate) > 5000 :
                slice_meter += 50
                print (f"slice meter = {ob.slic_meter}")
                terminal_entry.insert (tk.END , f"\nslice meter = {ob.slic_meter}")

                name_slicing_file += 1
                print ("continue\n-----------------------------")
                terminal_entry.insert (tk.END , "\ncontinue\n-----------------------------")

            else :
                list_slicing_file.append(path_file_to_translate)
                print ("Done")
                terminal_entry.insert (tk.END , "\nDone")

                break
        print ("Finish slicing file")
        terminal_entry.insert (tk.END , "\nFinish slicing file")


        ob = translator()
        ob2 = fix_sub()
        for i in list_slicing_file :
            path_file_to_translate = i
            
            ob.translate(path_file_to_translate)
            ob.make_sub(path_file_to_make_sub)
            #enter translated test in to the translate_entry
            translate_entry.delete(1.0, tk.END)
            translate_entry.insert(1.0, open_pathFile(path_file_to_make_sub))
            ######################################
            
            ob2.get_file(path_file_to_make_sub)
            ob2.get_times()
            ob2.get_subs()
            ob2.make_fix_sub (path_file_to_make_fix_sub)
            print (f"File '{path_file_to_translate}' translated\n######################## ")
            terminal_entry.insert (tk.END , f"\nFile '{path_file_to_translate}' translated\n######################## ")

        print ("FINISH translating\n\nTry to delet repeatation elements")
        terminal_entry.insert (tk.END , "\nFINISH translating\n\nTry to delet repeatation elements")


        ob3 = fix_another_problem (path_file_to_make_fix_sub)
        ob3.remove_repeated_elements()
        print ("Delet repeataion elements sucsesfull don :)")
        terminal_entry.insert (tk.END , "\nDelet repeataion elements sucsesfull don :)")

        write_pathFile (path_file_to_translate , sub_entry.get(1.0 , tk.END))
        ##############################################################################################
    #
    except exceptions.ConnectionError :
        print ('Conect problem :( , pleas try again')


def set_window_size(root, width_ratio, height_ratio):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)

    root.geometry(f"{window_width}x{window_height}")

# Create the main window
root = tk.Tk()
root.title("Convert auto language subtitle to Persian subtitle")

# Set the window size relative to the screen size (e.g., 80% width and 60% height)
set_window_size(root, width_ratio=0.8, height_ratio=0.7)
root.resizable(False , False) #it don't let to change size of window

# Create a button
button_open = tk.Button(root, text="Open File", command=open_file)
button_open.place (x = 10 , y = 6)

# Create a text entry widget
entry_path = tk.Entry(root, width=100)
entry_path.place (x = 80 , y = 10)

#creat save as button
button_saveAs = tk.Button(root, text=" Save as ", command=save)
button_saveAs.place (x = 10 , y = 46)

#creat name button
button_translate = tk.Button(root, text="Translate", command=translate)
button_translate.place (x = 700 , y = 46)

#creat text box for enter a name
entry_nameFile = tk.Entry(root, width=100)
entry_nameFile.place (x = 80 , y = 50)

#creat text box for subtitle
sub_entry = tk.Text(root, width=70 , height=20)
sub_entry.place (x = 10  , y = 100)

#creat text box for translated subtitle
translate_entry = tk.Text(root, width=70 , height=20)
translate_entry.place (x = 585  , y = 100)

#creat terminal entery
terminal_entry = tk.Text(root, width=142 , height=10)
terminal_entry.place (x = 10  , y = 430)
terminal_entry.insert (tk.END , datetime.now())


root.mainloop()