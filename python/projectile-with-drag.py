from math import pi
import numpy as np
import matplotlib.pyplot as plt
import vpython as vp
from math import exp

# global variables
gravitational_acceleration = 9.8
mass = 10  # change later
diameter = 2
viscosity = .01

drag_coefficient = 3 * pi * viscosity * diameter
terminal_velocity = mass * gravitational_acceleration / drag_coefficient
tao = mass / drag_coefficient
time_values = np.linspace(0, 2, 100)
initial_position = vp.vector(0, 0, 0)
initial_velocity = vp.vector(5, 5, 5)
# make a definition statement for your equation
print(drag_coefficient)
print(tao)
print(terminal_velocity)


def x_position(t):
    return initial_velocity.x * tao * (1 - exp(-t / tao))


def y_position(t):
    return (initial_velocity.y + terminal_velocity) * tao * (1 - exp(-t / tao)) - terminal_velocity * t


# while t <2:
#     x_position = initial_velocity.x * tao * (1 - exp(-t / tao)) - terminal_velocity * t
#     y_position = (initial_velocity.y + terminal_velocity) * tao * (1 - exp(-t / tao)) - terminal_velocity * t
#     print(f'x at t = {t} ={x_position}')
#     print(f'y at t = {t} ={y_position}')
#     t += t + .1

# generate arrays to plug into your def statement, you can use for loops or linear_algebra code
# for computing these arrays depending on your problem

# for loop
# x_values = # here you can use np.range(), or np.linspace() this will most likely be time for many of you
# argument_values = [] # you will use this to plug in as an argument into your def
#                      # statement and it depends on the x_value above
# for i in x_values:
#     # compute argument values with an equation
#     # append y values to empty list
#
# # linalg
# x_values = # here you can use np.range(), or np.linspace() this will most likely be time for many of you
# argument_values = # <definition of this argument as a function of x_values>
#     # ie.) y = x^2 : argument_values = (x_values)**2 , this will return an array

# do this for your various variables
x_position_list = [x_position(t) for t in time_values]
y_position_list = [y_position(t) for t in time_values]
print(y_position_list)
# plotting
plt.plot(x_position_list, y_position_list)
#     # main plot(x values, y values, color, label)
# plt.xlabel('x values')                                                 # x label
# plt.ylabel('y values')                                                 # y label
# plt.legend(["function"], loc="lower right")                            # legend (key)
# plt.title('your project name')                                         # title of graph
# # plt.savefig('plot of <your graph>')                                    # saves graph as a png
plt.show()  # display the graph

# # Draft code comments
#
# Does the code run without error?
# If any error occurs, can you suggest a potential fix?
# The code runs without error; however, there is an error in one of the packages. I don't believe there is a potential fix for this.
# How understandable is the output of the code?
# Point out any parts you do not understand.
# The code is very understandable; however, there are no units. I am assuming that m/s**2 is the unit for gravity and that mass is in grams and diameter is in meters but it is unclear. The variable 't' is hard to understand since there is no def, maybe it represents time.
# How readable is the code itself?
# Say where formatting or commenting would make the code more readable or where PEP-8 is violated.
# The code itself is very readable and very well formatted.
# How clearly do the code comments describe the problem it is trying to solve?
# Identify places that would benefit from a clearer comment.
# The code comments are pretty clear, but I was unsure what was being solved for. Toward the top of the comments it said "while 't'<2" but again t is not defined.
# How clearly do the variable names relate to the concepts they concretize?
# Point out any variables you don't recognize, and/or suggest better names. Check for PEP-8 compliance.
# The variable names are mostly clear, but again variable 't' is my biggest complaint.
# How well does the range of variables capture the problem described?
# Identify extraneous regions that could be left out or important regions that should be included.
# The range is of variable are capture very well, but the position_x and position_y is unclear. There are no lables on x or y-axis so I'm not sure what the values represent.
# To what degree does the script follow a functional programming paradigm, packaging all major components of the script
# into separately defined functions that pass information among them in a small number of lines? Identify ways in which
# the functionalization of the code could be improved.
# How clearly do the visualizations show the solutions to the problem?
# The script is has a very functional programming paradigm. There is not too much lines of code and everything is well kept. The visualization shows the solutions to the problem but it is little unclear what the problem is, the only way I know what the problem is about is by looking at the .py file name.
# Say if there is extraneous whitespace or the co-domain or domain of the data should be changed or any other ways the
# visualizations could be more effective
# titles on x and y-axis would be beneficial, a title would also be helpful to state what is being solved for. Including units on each of the axis would also help understand the graph more.
