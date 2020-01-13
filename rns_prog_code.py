try:
    import tkinter
except ImportError:  # python 2
    # noinspection PyPep8Naming
    import Tkinter as tkinter
import platform
import os
import sys

import matplotlib.pyplot as plt
# graf_frame -> run 'for loop (rns_exe_output_with_time_trigger)  -> rns_exe_output_with_time_trigger ->
# -> output_data_clean_up -> plot_one_data_set


cwd = os.getcwd()
os.chdir('{}'.format(cwd))

working_system = platform.system()
wanted_task = 'model'
option_points_txt = 'Max points computed '
def_eos = 'eosC'
points = '10'
cmd_list = []
cmd_time_list = []
time = 360 + 20 * int(points)
total_time = 0
output = []
lag_trigger = False
extract = False

besides_optmenu = ('gr/cm^3    ',
                   'axes ratio ',
                   'Mo         ',
                   'Mo         ',
                   '10^4 S^(-1)',
                   '(GMo^2)/c  ')

variables = {'e': 'central energy density',
             'r': 'axis ratiot ',
             'm': 'mass in Sun mass',
             'z': 'rest mass in Sun mass',
             'o': 'angular velocity',
             'j': 'angular momentum'}

tasks_explanation = {'model': 'Computes a model with {0} and {1}.'.format(variables['e'], variables['r']),
                     'gmass': 'Computes a model with {0} and {1}.'.format(variables['e'], variables['m']),
                     'rmass': 'Computes a model with {0} and {1}.'.format(variables['e'], variables['z']),
                     'omega': 'Computes a model with {0} and {1}.'.format(variables['e'], variables['o']),
                     'jmoment': 'Computes a model with {0} and {1}.'.format(variables['e'], variables['j']),
                     'static': 'Computes a non rotating model for a given {}.'.format(variables['e']),
                     'kepler': 'For a given {} computetes the model with Keplerian angular velocity'.format(variables['e']),
                     'test': 'Computes a test model'}

entry_var = {'model': 'er',
             'gmass': 'em',
             'rmass': 'ez',
             'omega': 'eo',
             'jmoment': 'ej',
             'static': 'e ',
             'kepler': 'e ',
             'test': '  '}

variables2 = {'e': 'gr/cm^3    ',
              'r': 'axes ratio ',
              'm': 'Mo         ',
              'z': 'Mo         ',
              'o': '10^4 S^(-1)',
              'j': '(GMo^2)/c  ',
              ' ': '           '}

test_out = '--eosC--task: -model-\ncentral energy density: 2.66e15-axes ratio: 0.75'

data_to_be_ploted = {'central energy density': '1',
                     'gravitational mass  ': '2',
                     'rest mass        ': '3',
                     'radius at the equator ': '4',
                     'angular velocity   ': '5',
                     'angular velocity of a \n particle in circular orbit': '6',
                     'rotational/gravitational\n energy': '7',
                     '(cJ/GMo^2 ) angular momentum': '8',
                     'moment of inertia': '9',
                     'h+': '10',
                     'h-': '11',
                     'Zp - polar redshift': '12',
                     'Zb - backward equatorial redshift': '13',
                     'Zf - forward equatorial redshift': '14',
                     'ratio of central value of \n potential ω to Ω': '15',
                     'coordinate equatorial radius': '16',
                     'axis ratio (polar to equatorial)': '17'}

# defs for data output


def extract_data():
    global extract
    print('extract data')
    extract = True
    run()


def at_exit():
    sys.exit()


def run():
    global count
    global c_cmd
    global final_model
    global x_axis
    global y_axis

    print('The following models will be computed')
    print(cmd_list)
    if extract is False:
        x_axis = int(x_data_to_menu.get())
        y_axis = int(y_data_to_menu.get())
        x_axis -= 1
        y_axis -= 1
    final_model = False
    count = 0
    for c_cmd in cmd_list:
        if c_cmd is cmd_list[-1]:
            final_model = True
        rns_exe_output_with_time_trigger()
        count += 1


def rns_exe_output_with_time_trigger():
    import subprocess
    import sys
    import threading
    global output
    global lag_trigger
    global c_cmd
    global count
    print('executing the following model:')
    print(c_cmd)
    print('Maximum computed time for this model:')
    print(cmd_time_list[count])
    lag_trigger = False

    def rns_time_trigger():
        global lag_trigger
        global output
        lag_trigger = True
        proc.terminate()
    output = []
    # time trigger it triggers after time = 6*points(calculated points)
    clock = threading.Timer(cmd_time_list[count], rns_time_trigger)
    clock.start()
    with subprocess.Popen(str(c_cmd), stdout=subprocess.PIPE, bufsize=1, stderr=subprocess.PIPE) as proc:
        for line in proc.stdout:
            if lag_trigger is True:
                proc.terminate()
                break
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
            dec = line.decode('utf-8')
            output.append(dec)
        proc.wait()
    proc.kill()
    clock.cancel()
    print(output)
    if extract is True:
        with open('output.txt', 'a+') as append:
            for line in output:
                append.writelines(line)

    else:
        output_data_clean_up()


def output_data_clean_up():
    global output
    global final_list

    final_list = []

    for elem in output:
        check = elem.split()
        try:
            float(check[0])
        except ValueError:
            continue
        except IndexError:
            print('-------------')

        if 'imaginary' in elem:
            continue

        if ('-1.#IND0e+000' or '1.#INF0e+000' or '1.#QNANe+000' or 'eos') in elem:
            continue

        if '-------------------------------------------------------------------------------' in elem:
            continue

        for line in elem.split():
            final_list.append(line)

    plot_one_data_set()


def plot_one_data_set():

    global final_list
    # edo tha zitao input mass   radious klp
    x_data = []
    y_data = []
    i = x_axis
    k = y_axis
    data_in_row = final_list
    length = len(data_in_row)
    print(run_list_text[count])
    for num in range(0, length, 20):
        x_data.append(float(data_in_row[num + i]))
        y_data.append(float(data_in_row[num + k]))
    print('-------------------------------------------------------------------------------------')
    print(x_data)
    print(y_data)

    plt.plot(x_data, y_data, label='{}'.format(run_list_text[count]))
    plt.legend()
    plt.ylim(bottom=0)
    plt.xlim(xmin=0)
    if final_model is True:
        print('final plot')
        plt.title('R.N.S.')
        plt.show()
        plt.clf()

    x_data = []
    y_data = []


def check_pop_up_window():
    global window
    global cmd_list
    global time


    def check_save():
        global total_time
        radio_buton = radiobut.get()
        if wanted_task in 'teststatickepler':
            time = 60
            if radio_buton is 1:
                time = 360 + 20 * int(points)
        elif radio_buton is 3:
            time = 60
        else:
            time = 360 + 20 * int(points)
        total_time = total_time + time
        print(time)
        print(total_time)
        cmd_list.append(w_cmd)
        cmd_time_list.append(time)
        checkwindow.destroy()

    checkwindow = tkinter.Toplevel()
    checkwindow.title('R.N.S.')
    checkwindow.geometry('500x120')
    checkwindow.minsize(500, 100)
    checkwindow.configure(background='white')
    checkwindow.rowconfigure(0, weight=1)
    checkwindow.columnconfigure(0, weight=1)

    check_descr_frame = tkinter.LabelFrame(checkwindow, text='Verification', relief='sunken')
    check_descr_frame.grid(row=0, column=0, sticky='news')
    check_descr_text = tkinter.Text(check_descr_frame)
    check_descr_text.insert('insert', 'command in cmd form:\n {}\n\n'.format(w_cmd))
    check_descr_text.grid(row=0, column=0, sticky='new')
    check_descr_text.insert('insert', 'System:\n {}'.format(working_system))
    check_button = tkinter.Button(checkwindow, text=' Ok ', command=check_save)
    check_button.grid(row=0, column=0, sticky='es')
    checkwindow.mainloop()


def cmd_constructor():
    global w_cmd

    eos = def_eos
    task = wanted_task
    num1 = var1.get()
    num2 = var2.get()
    num3 = var3.get()
    num4 = var4.get()
    var = list(entry_var[task])
    cmd = r''
    w_cmd = r''
    radio_buton = radiobut.get()
    if task in 'teststatickepler':
        if task in 'kepler':
            cmd = r' -f {} -t {} -e {} -p 2 -d 0'.format(eos, task, num1)
            if radio_buton is 1:
                cmd = r' -f {} -t {} -e {} -l {} -n {} -p 2 -d 0'.format(eos, task, num1, num3, points)
        if task in 'static':
            cmd = r' -f {} -t {} -e {} -p 2 -d 0'.format(eos, task, num1)
            if radio_buton is 1:
                cmd = r' -f {} -t {} -e {} -l {} -n {} -p 2 -d 0'.format(eos, task, num1, num3, points)
        if task in 'test':
            cmd = r' -f eosC -t test'
    else:
        if radio_buton is 2:
            cmd = r' -f {} -t {} -e {} -{} {} -l {} -n {} -p 2 -d 0'.format(eos, task, num1, var[1], num2, num4, points)
        if radio_buton is 1:
            cmd = r' -f {} -t {} -e {} -l {} -n {} -{} {} -p 2 -d 0'.format(eos, task, num1, num3, points, var[1], num2)
        if radio_buton is 3:
            cmd = r' -f {} -t {} -e {} -{} {} -p 2 -d 0'.format(eos, task, num1, var[1], num2)
    if working_system is 'Linux':
        ws = r'./rns'
        w_cmd = ws + cmd
    if working_system is 'Windows':
        ws = r'rns.exe'
        w_cmd = ws + cmd
    else:
        ws = r'system must be Windows or Linux'
        w_cmd = ws
    print(w_cmd)
    check_pop_up_window()


def graf_frame():

    global x_data_to_menu
    global y_data_to_menu
    global extract
    extract = False

    grafframe = tkinter.Tk()
    grafframe.title('Graph options')
    grafframe.geometry('320x240')
    grafframe.minsize(320, 240)
    grafframe.maxsize(321, 241)
    grafframe.config(background='white')
    for s in range(0, 5):
        grafframe.rowconfigure(s, weight=1)
    for s in range(0, 4):
        grafframe.columnconfigure(s, weight=1)

    # menu buttons
    x_menu_button = tkinter.Menubutton(grafframe, text='X axis', relief='raised')
    x_menu_button.grid(row=1, column=0, sticky='e')
    x_menu_button.menu = tkinter.Menu(x_menu_button, tearoff=0)
    x_menu_button['menu'] = x_menu_button.menu

    y_menu_button = tkinter.Menubutton(grafframe, text='Y axis', relief='raised')
    y_menu_button.grid(row=1, column=1, sticky='w')
    y_menu_button.menu = tkinter.Menu(y_menu_button, tearoff=0)
    y_menu_button['menu'] = y_menu_button.menu

    # menu buttons -- menu import

    x_data_to_menu = tkinter.StringVar()
    y_data_to_menu = tkinter.StringVar()

    for data_to_menu in data_to_be_ploted.keys():
        data_text = data_to_menu
        val = str(data_to_be_ploted[data_to_menu])
        labl = '{}'.format(data_text)
        x_menu_button.menu.add_radiobutton(label=labl, variable=x_data_to_menu, value=val)
        y_menu_button.menu.add_radiobutton(label=labl, variable=y_data_to_menu, value=val)
    x_data_to_menu.set(str(4))
    y_data_to_menu.set(str(2))

    menu_run_button = tkinter.Button(grafframe, text='Plot graph', command=run)
    menu_run_button.grid(row=4, column=1, sticky='e')
    runwindow.destroy()
    grafframe.protocol("WM_DELETE_WINDOW", at_exit)
    grafframe.mainloop()


def run_button_frame():
    global runwindow
    global cmd_list
    global run_list_text
    runwindow = tkinter.Tk()
    runwindow.title('R.N.S.')
    runwindow.geometry('800x300')
    runwindow.minsize(600, 300)
    runwindow.maxsize(600, 300)
    runwindow.configure(background='white')
    # configure
    for s in range(0, 5):
        runwindow.rowconfigure(s, weight=1)
    for s in range(0, 4):
        runwindow.columnconfigure(s, weight=1)

    # listbox frame
    run_list_frame = tkinter.LabelFrame(runwindow, text='Modules to be computed: ', relief='sunken')
    run_list_frame.grid(row=1, column=0, columnspan=3, sticky='n')

    # description labeled frame
    run_descr_frame = tkinter.LabelFrame(runwindow, text='Description', relief='sunken', width=300, height=200)
    run_descr_frame.grid(row=1, column=3, sticky='en')
    run_descr_frame.grid_propagate(False)

    # description frame text
    run_descr_text = tkinter.Text(run_descr_frame)
    run_descr_text.insert('insert', 'The symbols in the list represent\n the following variables:\n\n')
    for v in variables.keys():
        run_descr_text.insert('insert', '{}:{}\n'.format(v, variables[v]))
    run_descr_text.grid(row=0, column=0, sticky='ne')

    # listbox
    run_list = tkinter.Listbox(run_list_frame, bg='white', relief='sunken')
    run_list.grid(row=1, column=0, sticky='ne', rowspan=2)
    run_list_scrollbar = tkinter.Scrollbar(run_list_frame, orient=tkinter.VERTICAL, command=run_list.yview)
    run_list_scrollbar.grid(row=1, column=1, rowspan=2, sticky='enws')
    # list box insert data
    chars = ['-f', '-t', '-p 2', '-d 0', 'rns.exe', './rns']
    run_list_text = []
    for line in cmd_list:
        text = ''
        for char in chars:
            text = line.replace(char, '')
            line = text
        run_list_text.append(text)
    for item in run_list_text:
        print(item)
        run_list.insert(tkinter.END, item)


    # button extract data
    run_button_extract = tkinter.Button(runwindow, text='Extract data', command=extract_data)
    run_button_extract.grid(row=4, column=0, sticky='es')

    # button graph
    run_button_graph = tkinter.Button(runwindow, text='Graph', command=graf_frame)
    run_button_graph.grid(row=4, column=1, sticky='se')

    # button help
    run_button_help = tkinter.Button(runwindow, text='?', command=help_window)
    run_button_help.grid(row=4, column=3, sticky='sw')
    mainWindow.destroy()
    # runwindow.mainloop()


def options_window():
    global def_eos
    global points

    def save_button():
        global def_eos
        global points
        def_eos = entry_default_eos.get()
        points = entry_default_points.get()

    optionswindow = tkinter.Toplevel()
    optionswindow.title('Description Window')
    optionswindow.geometry('400x240')
    optionswindow.minsize(400, 200)
    optionswindow.maxsize(401, 201)
    optionswindow.configure(background='white')
    optionswindow.rowconfigure(0, weight=1)
    optionswindow.rowconfigure(1, weight=1)
    optionswindow.columnconfigure(0, weight=1)
    optionswindow.columnconfigure(1, weight=1)

    # entry frame for eos file

    options_entry_frame = tkinter.LabelFrame(optionswindow, text='eos file name', bg='white', relief='sunken')
    options_entry_frame.grid(row=0, column=0, sticky='nwe')
    entry_default_eos = tkinter.StringVar(options_entry_frame, value=def_eos)
    options_entry = tkinter.Entry(options_entry_frame, bd=3, width='50', textvariable=entry_default_eos)
    options_entry.grid(sticky='n')

    # MAX points computed entry ----------------------------------------

    options_points_frame = tkinter.LabelFrame(optionswindow, text=option_points_txt, bg='white', relief='sunken')
    options_points_frame.grid(row=1, column=0, sticky='nwe')
    entry_default_points = tkinter.StringVar(options_points_frame, value=points)
    option_points_entry = tkinter.Entry(options_points_frame, bd=3, width=5, textvariable=entry_default_points)
    option_points_entry.grid(sticky='n')

    # save button
    save_button = tkinter.Button(optionswindow, text='save', command=save_button)
    save_button.grid(sticky='e')


def help_window():

    helpwindow = tkinter.Toplevel()
    helpwindow.title('Description Window')
    helpwindow.geometry('400x240')
    helpwindow.minsize(400, 240)
    helpwindow.maxsize(401, 241)
    helpwindow.configure(background='white')
    helpwindow.rowconfigure(0, weight=1)
    helpwindow.rowconfigure(1, weight=1)
    helpwindow.columnconfigure(0, weight=1)
    helpwindow.columnconfigure(1, weight=1)

    # text organised based on --input--test
    input_frame = tkinter.LabelFrame(helpwindow, text='Input units', bg='white', relief='sunken')
    input_frame.grid(row=0, column=0, sticky='e')

    input_text = tkinter.Text(input_frame)
    for func in variables.keys():
        input_text.insert('insert', '{}:{}\n'.format(variables[func], variables2[func]))
    input_text.grid(row=0, column=0, sticky='e')

    test_frame = tkinter.LabelFrame(helpwindow, text='Test module', bg='white', relief='sunken')
    test_frame.grid(row=1, column=0, sticky='e')

    test_text = tkinter.Text(test_frame)
    test_text.insert('insert', 'The test task has the following parameters:\n'+test_out)
    test_text.grid(row=0, column=0, sticky='e')

    helpwindow.mainloop()


# the frame_r3_c1_update is called from radiobutton (to blacken entrys)


def frame_r3_c1_up_text():
    global entr3_text
    global entr4_text
    global entry_var_split
    global wanted_task
    global entry_var
    entr3_text = tkinter.Label(frame1, text='           ', bg='white', width='11')
    entr4_text = tkinter.Label(frame1, text='           ', bg='white', width='11')
    entry_var_split = list(entry_var[wanted_task])
    entr3_text = tkinter.Label(frame1, text='{}'.format(variables2[entry_var_split[0]]), bg='white', width='11')
    entr3_text.grid(row=0, column=1, sticky='e')
    entr4_text = tkinter.Label(frame1, text='{}'.format(variables2[entry_var_split[1]]), bg='white', width='11')
    entr4_text.grid(row=1, column=1, sticky='e')


def frame_r3_c1_update():

    global var3
    global var4
    global frame1

    frame1 = tkinter.Frame(mainWindow)
    frame1.grid(row=3, column=1, sticky='e')
    if radiobut.get() == 1:
        var3 = tkinter.Entry(frame1, bd=3, width=5)
        var4 = tkinter.Entry(frame1, bd=3, width=5, state='disabled')
    if radiobut.get() == 2:
        var3 = tkinter.Entry(frame1, bd=3, width=5, state='disabled')
        var4 = tkinter.Entry(frame1, bd=3, width=5)
    if radiobut.get() == 3:
        var3 = tkinter.Entry(frame1, bd=3, width=5, state='disabled')
        var4 = tkinter.Entry(frame1, bd=3, width=5, state='disabled')

    var4.grid(row=1, column=0, sticky='es')
    var3.grid(row=0, column=0, sticky='en')

    frame_r3_c1_up_text()

    return var3, var4, wanted_task


def update_description(*var):
    global task_option_menu_var
    global wanted_task
    global expl_frame
    global expl
    global entry_var_split
    # data_description_update
    wanted_task = task_option_menu_var.get()

    expl_frame = tkinter.LabelFrame(mainWindow, text='Brief explanation', relief='sunken', bg='white')
    expl_frame.grid(row=5, column=1, sticky='nwe', rowspan=2, columnspan=2)
    expl = tkinter.Label(expl_frame, width='72', bg='white', text='{}'.format(tasks_explanation[wanted_task]))
    expl.grid(sticky='nwse')
    frame_r3_c1_up_text()

    return wanted_task, entry_var_split


mainWindow = tkinter.Tk()

mainWindow.title('R.N.S.')
mainWindow.geometry('640x480')
mainWindow.configure(background='white')
mainWindow.minsize(640, 480)
mainWindow.maxsize(641, 481)
# configure
for span in range(0, 11):
    mainWindow.rowconfigure(span, weight=1)
for span in range(0, 5):
    mainWindow.columnconfigure(span, weight=1)

# Buttons

# Options button
options_button = tkinter.Button(mainWindow, text='options', command=options_window)
options_button.grid(row=1, column=2, sticky='e')

# Run button
run_button = tkinter.Button(mainWindow, text='Run', command=run_button_frame)     # add command
run_button.grid(row=10, column=0)

# Add button
add_model_but = tkinter.Button(mainWindow, text='Add model', command=cmd_constructor)
add_model_but.grid(row=10, column=1, sticky='w')

# Help buttons
help_button = tkinter.Button(mainWindow, text='?', command=help_window)
help_button.grid(row=10, column=2, sticky='e')

# Radio button

radio_frame = tkinter.LabelFrame(mainWindow, text='Model sequence', relief='sunken', bg='white')
radio_frame.grid(row=3, column=2, rowspan=1, sticky='nse')
radiobut = tkinter.IntVar()
radio_but = tkinter.Radiobutton(radio_frame, text='variable 1', variable=radiobut, value=1, command=frame_r3_c1_update)
radio_but.grid(row=1)
radio_but = tkinter.Radiobutton(radio_frame, text='variable 2', variable=radiobut, value=2, command=frame_r3_c1_update)
radio_but.grid(row=2)
radio_but = tkinter.Radiobutton(radio_frame, text='both fixed', variable=radiobut, value=3, command=frame_r3_c1_update)
radio_but.grid(row=3)
radiobut.set(3)
radio_but.invoke()

# OptionMenu task

wanted_task = 'model'
list_text = [*tasks_explanation]
task_option_menu_var = tkinter.StringVar(mainWindow)
task_option_menu_var.set(list_text[0])
task_option_menu = tkinter.OptionMenu(mainWindow, task_option_menu_var, *list_text, command=update_description)
task_option_menu.grid(row=3, column=1, sticky='w')
option_menu_label = tkinter.Label(mainWindow, bg='white',  text='Choose task : ').grid(row=3, column=0, sticky='e')
update_description()

# entry

entry_var_split = list(entry_var[wanted_task])
text1 = entry_var[wanted_task]
frame = tkinter.Frame(mainWindow)
frame.grid(row=3, column=1)

var1 = tkinter.Entry(frame, bd=3, width=5)
var1.grid(row=0, column=0, sticky='w')
entr1_text = tkinter.Label(frame, text=':  ', bg='white', width='1')
entr1_text.grid(row=0, column=1, sticky='e')

var2 = tkinter.Entry(frame, bd=3, width=5)
var2.grid(row=1, column=0, sticky='e')
entr2_text = tkinter.Label(frame, text=':  ', bg='white', width='1')
entr2_text.grid(row=1, column=1, sticky='e')

# pop up frames from -- option -- ? -- buttons

mainWindow.mainloop()
