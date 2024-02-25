| [< Previous (Classes Example)](../Classes/example/README.md) | [Intermediate Python](../../README.md)  | [Next >] |
|--------------------------------------------------------------|-----------------------------------------|----------|

# Introduction to tkinter and GUIs

_Before beginning this section, you should be comfortable with [classes](../Classes/classes.md) and the basics of [inheritance](../Classes/inheritance.md)._

This section will walk you through creating a very basic user interface using python's tkinter library. Although GUIs very
quickly become complex projects, a simple interface can help you monitor a program's progress or change parameters after the
code is already running.

In this example, we will create a basic control for the code in [cryo_sim.py](cryo_sim.py). This code simulates an instrument
with a temperature control (nominally a cryostat), and has three main features:
1. The ability to open/close a "connection" to the instrument with ```open_connection()``` and ```close_connection()```
2. The ability to read the current temperature with ```read_temperature()```
3. The ability to change the temperature setpoint with ```set_setpoint(temperature)```

## Step 0: Planning
As with most projects, the key to coding a GUI starts before any code gets written. It may be helpful to take a piece of paper
and create a sketch of what you want the GUI to look like. What are features or tasks that it needs to accomplish? As layouts
and behaviors increase in complexity, does it make sense to create customized components?

To control our instrument, we're looking for the ability to see the current temperature, change the setpoint, and open & close
the connection. A GUI might be laid out to look something like:

| Temperature      | \<current temperature> |
|------------------|------------------------|
| Change Setpoint: | \<setpoint entry>      |
| Connection:      | \<Open/Close Button>   |

Additionally, we want the temperature to be current, the setpoint to update when we press "enter", and the connection
button to toggle the connection according to its current status. We might even consider changing the button color from
red to green depending on the connection status.

## Basics
Before getting to the work of creating a GUI, it's helpful to understand the steps that the code will go through as the 
GUI gets built. 
1. First, the window gets created as an instance of the ```tkinter.tk.Tk``` class. The window might have
properties defined, such as size, title, or if it's resizeable. 
2. Then, each element (or widget) gets created, often needing to know its "master", or the element that will contain it. 
After the element is created and defined, it gets packed or gridded into its master element. In this sample, we will gridding 
all our componenets into the top-level window. However, there are widgets like tabbed frames or menus that could be sensible
options for your layout.
3. After all the initialization is complete, the window/root element goes into its main loop. This displays the GUI and
then waits for user input. As the user interacts with the GUI, they might cause events (button clicking, typing, mouse 
movement) that the GUI knows means to run a previously-defined function. A bit of multi-threading can be helpful here,
as the GUI will freeze until the function is complete, but be careful: imagine if a user presses enter multiple times,
what is the desired behaviour?
4Finally, when the user indicates the window should close, the root element needs to be destroyed for the window to 
fully close.

When running, the GUI's mainloop command will block code until the window is closed. 

## Step 1: Root Window

### Portability
Take a look at [gui.py](gui.py). The initial structure for the GUI has been defined. We will create our root window as a 
subclass of the ```tkinter.tk.Tk``` class, to be further filled in. First, look at the last few lines of the file.
```python
if __name__ == "__main__":
    cryo = Cryo()
    root = CryoGui(cryo)
    root.mainloop()
```
By subclassing, we keep the code to create and run the GUI compact and portable. The same code could easily run inside 
another script, allowing it to run whatever processes is needed while letting the user actively monitor the instrument. 
In this case, you might want to run ```app.mainloop()``` on a separate thread--just always be aware that the code will 
need to shut down properly, usually with context managers or ```try...finally``` statements.

### Subclass initialization
Next, take a look at the CryoGui ```__init__``` function.
```python
def __init__(self,cryo: Cryo, *args, title="GUI Demo", **kwargs):
    super().__init__(*args,**kwargs)

    self.cryo = cryo

    self.title(title)
    self.resizable(False, False)
    self.protocol("WM_DELETE_WINDOW",self.quit_app)

    self.initialize()
```
The first few lines are basic: initializing the subclass, and storing the pointer to the instrument for later use. For a
GUI, _most_ of the action will happen in ```mainloop()```, after the initialization has finished, so it's important that
all the functions that trigger from events will be able to access that variable.

From there, three lines of code that are specific to the GUI creation. All of these are optional, but useful:
- ```self.title(title)``` / ```root.title(title)``` sets the title of the window
- ```self.resizable(False, False)``` / ```root.resizable(False, False)``` defines if the window is resizable by the user
in the x and y directions
- ```self.protocol("WM_DELETE_WINDOW",self.quit_app)``` tells the code to run the ```quit_app()``` function when the user
closes the window. If not set, then the default is just to destroy the window with ```self.destroy()```. If you wanted 
something like a pop-up to confirm with the user before closing, then you'll want to write your own function. Make sure
it does at some point call ```self.destroy()```, otherwise the window will not close unless the program is force quit.

With that, we're set to start defining elements to add to our window, done in the ```initialization()``` function.

## Step 2: Basic Text
Both the ```tkinter.tk``` and ```tkinter.ttk``` modules contain a number of widgets to use as elements in your GUI. The
[ttk documentation page](https://docs.python.org/3/library/tkinter.ttk.html) says "The basic idea for tkinter.ttk is to 
separate, to the extent possible, the code implementing a widget’s behavior from the code implementing its appearance." 
Meaning, how the element looks and how it behaves are two separate steps. However, not every element will have behaviour.
In this example, we want to start by adding a simple, unchanging label for "Temperature". The ```ttk.Label``` widget easily
handles text. The first argument it takes is the containing element, in this case, the root `Tk` window.
```python
label1 = ttk.Label(self,text="Temperature: ")
```
Properties like background color or font can be configured for the Label, or changed later if desired.

This widget then needs to told where in the containing element it sits. Using ```grid```, the containing element will
act like a table with the widgets filling in the cells where placed.
```python
label1.grid(row=0, column=0)
```

Since this static label will not be changed at any point in the program, we can combine the previous few lines into:
```python
ttk.Label(self,text="Temperature: ").grid(row=0, column=0)
ttk.Label(self,text="Setpoint: ").grid(row=1,column=0)
```

## Step 3: Changing Text
The measurement of the temperature off the device is a different story, as this value will constantly change. We will
still use ```ttk.Label``` to display the value, but (keeping display separated from behavior) we will create a variable
to capture the "behavior" of text that changes and updates on the GUI. This is done using ```tk.StringVar```. As this
variable needs to be modified every time we want to update the value, we will store it as part of the class. Then, the
```ttk.Label``` itself is created similarly to the static label, but using the ```textvariable``` kwarg instead.
```python
self._temperature=tk.StringVar(self,"")
ttk.Label(self,textvariable=self._temperature).grid(row=0,column=1)
```
Now we want to be able to update the `_temperature` variable from the instrument. Since this will be done repeatedly, it's
best to create a function to do that. Once the temperature has been read and formatted as a string, the variable can be 
updated by using `set()`
```python
def update_temperature(self):
    temp = self.cryo.read_temperature()
    formatted_temp = "%.2f C"%temp
    self._temperature.set(formatted_temp)
```
Back in the initializing function, ```self.update_temperature()``` can be called once to initialize the value. We will use this
function later when we update the GUI.

_This is a great place in a real-life situation to implement some error handling. You might need to check that a connection
to the instrument is open before you attempt to read information from it: what should the label say if there is an error?_

## Step 4: User Input
To allow for a user to input a value for the setpoint, we will follow most of the same steps prior. However, instead of 
using the ```ttk.Label``` widget, we will instead use the ```ttk.Entry``` to capture the user input for the setpoint value.
Here, we will again use a ```tk.StringVar``` variable to store the value.
```python
self._setpoint=tk.StringVar(self,"")
entry=ttk.Entry(self,textvariable=self._setpoint)
entry.grid(row=1,column=1)       
```
Like with the temperature, we want to create a function to read the current setpoint. This function will not run regularly
(and in fact, would be annoying to have the value reset midway through typing a new temperature), but it's still useful
when confirming that the value has been set properly.
```python
def update_setpoint(self):
    self._setpoint.set(str(self.cryo.setpoint))
```
Next, we want to write a function to run when we try to set the setpoint. We can get the value stored in the ```tk.StringVar```
using ```get()```. 
```python
def set_setpoint(self,*args):
    setpoint = float(self._setpoint.get())
    self.cryo.set_setpoint(setpoint)
    self.update_setpoint()
```
This function skips all the steps for user input validation: **not recommended outside a tutorial**. A more robust version of
this function might: 
- check that the ```tk.StringVar``` is numerical
- check that the value is within the bounds of the instrument
- check that the setpoint is able to be changed
- check that the value of ```self.cryo.setpoint``` matches the value input by the user.

Additionally, well-written code for the instrument control will _also_ validate the input


## Step 5: Event Binding

Going back to our initialization function, we want to define when ```set_setpoint()``` should run. For this, we will
tell the widget what event should trigger the function. Tkinter recognizes events such as when the user focuses on the widget,
presses a key, or moves the mouse. In this case, we want to run the function when return is pressed, represented by the
"<Return>" event. We bind this event to the widget, and give it the function to run when the event happens.
```python
entry.bind("<Return>",self.set_setpoint)
```
Notice there's no `()` after `self.set_setpoint`. We're not running the function now, we're passing the handle to run later!

## Step 6: Buttons
Adding a button is in a way, simpler than the user input, and reuses many of the elements we've already seen here. The
button should toggle the connection, and read "Connect" if the instrument is disconnected, and "Disconnect" if it's 
connected. This means we need a ```tk.StringVar``` to change the value of the text and a command to run when the button
is pressed. Setting up the event binding can be done when creating the button, as the widget already expects to be clicked.
As before, we will also create a function to read the current status of the connection and display it accordingly.

In the initialization, this gives us:
```python
self.is_connected=tk.StringVar(self,"")
self.update_connection()
button=ttk.Button(self,textvariable=self.is_connected,command=self.toggle_connection)
button.grid(row=2,column=0,columnspan=2)
```
Note that the button is gridded to sit across two columns. This will keep it centered compared to the previous elements.
If you have a more complex layout, consider using 10 or 12 columns and being very liberal with the columnspan argument!
With 12 columns, you can easily split your layout into halves, thirds, and quarters, or go for something like a 3-6-3 
split for a large center element with side columns.


Then, we define the functions to update and toggle the connection:
```python
def update_connection(self):
    string = "Connected" if self.cryo.is_connected else "Disconnected"
    self.is_connected.set(string)

def toggle_connection(self):
    if self.cryo.is_connected:
        self.cryo.close_connection()
    else:
        self.cryo.open_connection()
    self.update_connection()
```
Note that when a function runs as a result of an event, you might see the GUI freezing until it's finished. In this case,
it takes a few seconds to "establish the connection".

Here, with a bit of extra work, it would also be possible to change the color of the button to red/green, to be more visible
to the user.

## Step 7: Quitting

This is a good point to go back to "what happens when the window closes". Think of it like a "finally" statement in an 
exception. Is there anything that needs to be wrapped up, saved, or closed before the program finishes? Should there be 
a pop-up to confirm?You may want to run ```self.cryo.close_connection()``` here, or maybe put that in its own ```try...finally```
statement. Like in exception handling, you want to be smart about how you approach this. If you hit an error and can't reach
the ```self.destroy()``` statement, you'll find yourself force-quitting the program.

# Step 8: Updating

If you run the code at this point, the GUI will pop-up, you'll be able to click the buttons and modify the setpoint. However,
the temperature will not regularly update. You might want the connection status to regularly update as well. There's no
risk for this code, but you could imagine a case where a real instrument might drop the connection. "Manually" updating,
such as binding the update function to an event, becomes cumbersome.

Tkinter has a function ```root.after(ms, function)```, which will run a function some time after the mainloop starts. Adding
a ```refresh_rate``` kwarg to the class, we can then add the following lines to run the update function.
```python
self.refresh=refresh_rate
self.after(self.refresh,self.update)
```
This runs the function once, but we can call it again as part of the update function to create a continuous update:
```python
def update(self):
    self.update_connection()
    self.update_temperature()
    self.after(self.refresh,self.update)
```
We don't want to be updating the setpoint that frequently, as it would interfere with user input. Here, you could again
create a more sophisticated function, especially if you expect the value to be changed through some other method: you 
might check if the cursor is in the Entry element, and update the value if not. Or simply update every 5 seconds and too
bad if that means occasionally needing to retype the value.

With that, you should be able to run the code. Try connecting to the instrument, changing the setpoint, and watching the
temperature change.


### Exercises
- Create a dialog that pops up when there's some invalid input in the setpoint.
- Confirm with the user before closing the window.
- Use the ```sticky``` keyword with the grid function, which takes a combination of "N", "E", "S", and "W" (for north, east,
south, and west) to change the alignment of different widgets. 
- Change the default size of the Entry widget to be more compact.
- If the ```ttk.Button``` widget is switched to ```tk.Button```, you can style the button on Windows. For a MacOS, you
might need to install and use the ```tkmacosx``` version of the same. Create two styles: one for when the instrument is
connected and one for disconnected. Modify the ```update_connection``` function to switch between them using ```button.configure()```.


| [< Previous (Classes Example)](../Classes/example/README.md) | [Intermediate Python](../../README.md)| [Next >] |
|--------------------------------------------------------------|----|----------|
