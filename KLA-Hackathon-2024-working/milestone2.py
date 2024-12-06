import math
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.setrecursionlimit(20000)
#open the input file
inp= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Milestone2\\Input\\Testcase3.txt",'r')
out= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Output\\Milestone2\\Milestone2Output3.txt",'w')

#read the input content into a dictionary
lines=inp.readlines()
inp_dict = dict()

for line in lines:
    inp_list=line.split(":")
    inp_list[1]=inp_list[1].split("\n")[0]
    if len(inp_list[1].split("x"))==2:
        inp_list[1]=inp_list[1].split("x")
        inp_list[1][0]=int(inp_list[1][0])
        inp_list[1][1]=int(inp_list[1][1])
    elif len(inp_list[1].split(","))==2:
        inp_list[1]=inp_list[1].split(",")
        inp_list[1][0]=int(inp_list[1][0].split("(")[1])
        inp_list[1][1]=int(inp_list[1][1].split(")")[0])
    else:
        inp_list[1]=int(inp_list[1])

    inp_dict[inp_list[0]]=inp_list[1]
    

print(inp_dict)

#initial setup to start calculations
x_die=inp_dict["DieSize"][0]
y_die=inp_dict["DieSize"][1]

x_ref=inp_dict["ReferenceDie"][0]
y_ref=inp_dict["ReferenceDie"][1]

x_shift=inp_dict["DieShiftVector"][0]
y_shift=inp_dict["DieShiftVector"][1]

initial_point=(0,0)
wafer_diameter=inp_dict["WaferDiameter"]
wafer_radius=wafer_diameter/2

#plot the wafer as a circle
fig,ax=plt.subplots()

cir = plt.Circle((0,0),radius=wafer_radius,edgecolor='b',facecolor='none')
ax.add_patch(cir)

ax.set_aspect('equal', adjustable='box')

#plot vertical and horizontal lines to help visualize the cow
ax.axvline(x=0, color='red', linestyle='--')
ax.axhline(y=0, color='green', linestyle='--')

#adjust scale of the graph
ax.set_xlim(-wafer_radius-10, wafer_radius+10)
ax.set_ylim(-wafer_radius-10, wafer_radius+10)

ref_die_point=[x_ref,y_ref]   #center of reference die
start_point=[ref_die_point[0]-(x_die/2),ref_die_point[1]-(y_die/2)]

visited=[]

def die_num(x_curr,y_curr,x_pos,y_pos):

    visited.append([x_pos,y_pos])

    left_dist=math.dist([0,0],[x_curr,y_curr])
    right_dist=math.dist([0,0],[x_curr+x_die,y_curr])
    top_dist=math.dist([0,0],[x_curr,y_curr+y_die])
    top_right_dist=math.dist([0,0],[x_curr+x_die,y_curr+y_die])

    bottom_mid_dist=math.dist([0,0],[x_curr+(x_die/2),y_curr])
    left_mid_dist=math.dist([0,0],[x_curr,y_curr+(y_die/2)])
    top_mid_dist=math.dist([0,0],[x_curr+(x_die/2),y_curr+y_die])
    right_mid_dist=math.dist([0,0],[x_curr+x_die,y_curr+(y_die/2)])


    if (left_dist<wafer_radius or right_dist<wafer_radius or top_dist<wafer_radius or top_right_dist<wafer_radius) or (bottom_mid_dist<wafer_radius or left_mid_dist<wafer_radius or top_mid_dist<wafer_radius or right_mid_dist<wafer_radius):

        out.write("("+str(x_pos)+","+str(y_pos)+"):("+str(x_curr)+","+str(y_curr)+")\n")

        #plot the die in the graph for visualization
        rect = Rectangle((x_curr,y_curr),x_die,y_die,edgecolor='r',facecolor='none')
        ax.add_patch(rect)

        #plot the index of the die
        text_x = x_curr + x_die / 2
        text_y = y_curr + y_die / 2
        ax.text(text_x, text_y, "("+str(x_pos)+","+str(y_pos)+")", color='black', ha='center', va='center')

        if [x_pos-1,y_pos] not in visited:
            die_num(x_curr-x_die,y_curr,x_pos-1,y_pos)
        if [x_pos+1,y_pos] not in visited:
            die_num(x_curr+x_die,y_curr,x_pos+1,y_pos)
        if [x_pos,y_pos-1] not in visited:
            die_num(x_curr,y_curr-y_die,x_pos,y_pos-1)
        if [x_pos,y_pos+1] not in visited:
            die_num(x_curr,y_curr+y_die,x_pos,y_pos+1)
    else:
        return


die_num(start_point[0],start_point[1],0,0)

plt.show()

inp.close()
out.close()