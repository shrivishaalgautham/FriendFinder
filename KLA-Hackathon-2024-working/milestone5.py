import math
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#change recrusion limit to calculate all indexes
#otherwise the interpreter thinks that the recursion is endless and tries to stop it
sys.setrecursionlimit(20000)

#open the input file
inp= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Milestone5\\Input\\Testcase2.txt",'r')
out= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Output\\Milestone5\\Milestone5Output2.txt",'w')

#read the input content into a dictionary
lines=inp.readlines()
inp_dict = dict()
flag=True
wafer=list()

for line in lines:
    if flag:
        inp_list=line.split(":")
        if inp_list[0]=="WaferCoordinates":
            flag=False

        inp_list[1]=inp_list[1].split("\n")[0]
        if len(inp_list[1].split("x"))==2:
            inp_list[1]=inp_list[1].split("x")
            inp_list[1][0]=int(inp_list[1][0])
            inp_list[1][1]=int(inp_list[1][1])
        elif len(inp_list[1].split(","))==2:
            inp_list[1]=inp_list[1].split(",")
            inp_list[1][0]=(inp_list[1][0].split("(")[1])
            inp_list[1][1]=(inp_list[1][1].split(")")[0])
            if len(inp_list[1][0].split("."))>1:
                inp_list[1][0]=float(inp_list[1][0])
            else:
                inp_list[1][0]=int(inp_list[1][0])
            if len(inp_list[1][1].split("."))>1:
                inp_list[1][1]=float(inp_list[1][1])
            else:
                inp_list[1][1]=int(inp_list[1][1])
        elif len(inp_list[1].split(','))>2:
            inp_list[1]=inp_list[1].split(',')
            for i in range(len(inp_list[1])):
                inp_list[1][i]=int(inp_list[1][i])
        elif len(inp_list[1].split(" "))>1:
            inp_list[1]=inp_list[1].split(" ")
            for i in range(len(inp_list[1])):
                temp=inp_list[1][i].split(",")
                temp[0]=(temp[0].split("(")[1])
                temp[1]=(temp[1].split(")")[0])
                if len(temp[0].split("."))>1:
                    temp[0]=float(temp[0])
                else:
                    temp[0]=int(temp[0])
                if len(temp[1].split("."))>1:
                    temp[1]=float(temp[1])
                else:
                    temp[1]=int(temp[1])
                inp_list[1][i]=temp
        elif (len(inp_list[1].split("\n")))>1:
            print(inp_list[1].split("\n"))
        elif inp_list[1]!='':
            inp_list[1]=float(inp_list[1])

        inp_dict[inp_list[0]]=inp_list[1]
    else:
        inp_list=line.split(",")
        inp_list[0]=float(inp_list[0].split("(")[1])
        inp_list[1]=float(inp_list[1].split(")")[0])
        wafer.append(inp_list)

inp_dict["WaferCoordinates"]=wafer

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

x_dsw=inp_dict["DieStreetWidthAndHeight"][0]
y_dsw=inp_dict["DieStreetWidthAndHeight"][1]

x_rsw=inp_dict["RecticleStreetWidthAndHeight"][0]
y_rsw=inp_dict["RecticleStreetWidthAndHeight"][1]

x_dpr=inp_dict["DiesPerReticle"][1]
y_dpr=inp_dict["DiesPerReticle"][0]

meas_list=inp_dict["WaferCoordinates"]

g_width=inp_dict["GripperWidthAndHeight"][1]
g_height=inp_dict["GripperWidthAndHeight"][0]

g_angles=inp_dict["GripperAngle"]

boundary_radius=wafer_radius-inp_dict["CircularExclusionZone"]

ref_die_point=[x_ref,y_ref]   #center of reference die
start_point=[ref_die_point[0]-(x_die/2),ref_die_point[1]-(y_die/2)]

#plot the wafer as a circle
# fig,ax=plt.subplots()

# cir = plt.Circle((0,0),radius=wafer_radius,edgecolor='b',facecolor='none')
# ax.add_patch(cir)

# cir = plt.Circle((0,0),radius=boundary_radius,edgecolor='y',facecolor='none')
# ax.add_patch(cir)

# ax.set_aspect('equal', adjustable='box')

# #plot vertical and horizontal lines to help visualize the cow
# ax.axvline(x=0, color='red', linestyle='--')
# ax.axhline(y=0, color='green', linestyle='--')

# #adjust scale of the graph
# ax.set_xlim(-wafer_radius-10, wafer_radius+10)
# ax.set_ylim(-wafer_radius-10, wafer_radius+10)

# meas_dict = dict()

# for coord in meas_list:
#     flag = True
    
#     x_temp=x_shift
#     x_dpr_count=1

#     while(coord[0]>x_temp):
#         x_temp+=x_die+x_dsw
#         x_dpr_count+=1
#         if x_dpr_count==x_dpr+1:
#             x_dpr_count=1
#             x_temp+=x_rsw
#         if coord[0]<x_temp:
#             x_temp-=(x_die+x_dsw)
#             if x_dpr_count==1:
#                 x_temp-=x_rsw
#             break
#         flag = False
            

#     while(coord[0]<x_temp and flag):
#         x_temp-=(x_die+x_dsw)
#         x_dpr_count-=1
#         if x_dpr_count==0:
#             x_dpr_count=x_dpr
#             x_temp-=x_rsw
#         if coord[0]>x_temp:
#             break            
        
#     flag = True

#     y_temp=y_shift
#     y_dpr_count=1

#     while(coord[1]>y_temp):
#         y_temp+=y_die+y_dsw
#         y_dpr_count+=1
#         if y_dpr_count==y_dpr+1:
#             y_dpr_count=1
#             y_temp+=y_rsw
#         if coord[1]<y_temp:
#             y_temp-=(y_die+y_dsw)
#             if y_dpr_count==1:
#                 y_temp-=y_rsw
#             break
#         flag = False

#     while(coord[1]<y_temp and flag):
#         y_temp-=(y_die+y_dsw)
#         y_dpr_count-=1
#         if y_dpr_count==0:
#             y_dpr_count=y_dpr
#             y_temp-=y_rsw
#         if coord[1]>y_temp:
#             break

#     if math.dist([0,0],[coord[0],coord[1]]) <= boundary_radius:
#         if (x_temp,y_temp) in meas_dict.keys():
#             meas_dict[(x_temp,y_temp)].append(coord)
#         else:
#             meas_dict[(x_temp,y_temp)]=[coord]

g_coord=list()
g_cen_coord=list()

for angle in g_angles:
    
    cen_x=wafer_radius*math.cos(math.radians(angle))
    cen_y=wafer_radius*math.sin(math.radians(angle))

    g_cen_coord.append([cen_x,cen_y])

    half_width=g_width/2
    half_height=g_height/2

    angle_rad=math.radians(angle)

    tl_x = cen_x + half_width * math.cos(angle_rad+math.pi/2) 
    tl_y = cen_y + half_width * math.sin(angle_rad+math.pi/2) 

    tr_x = cen_x + half_width * math.cos(angle_rad-math.pi/2)
    tr_y = cen_y + half_width * math.sin(angle_rad-math.pi/2)

    bl_x = tl_x + g_height * math.cos(math.pi+angle_rad)
    bl_y = tl_y + g_height * math.sin(math.pi+angle_rad)

    br_x = tr_x + g_height * math.cos(math.pi+angle_rad)
    br_y = tr_y + g_height * math.sin(math.pi+angle_rad)

    g_coord.append([tl_x, tl_y, tr_x, tr_y, bl_x, bl_y, br_x, br_y])

    # rectangle = plt.Polygon([(tl_x, tl_y), (tr_x, tr_y), (br_x, br_y), (bl_x, bl_y)], edgecolor='r', facecolor='none')
    # ax.add_patch(rectangle)

#obtain the reticle die number of the reference die 
x_temp=x_shift
x_dpr_count=1

while(start_point[0]>x_temp):
    x_temp+=x_die+x_dsw
    x_dpr_count+=1
    if x_dpr_count==x_dpr+1:
        x_dpr_count=1
        x_temp+=x_rsw

while(start_point[0]<x_temp):
    x_temp-=(x_die+x_dsw)
    x_dpr_count-=1
    if x_dpr_count==0:
        x_dpr_count=x_dpr
        x_temp-=x_rsw

    
y_temp=y_shift
y_dpr_count=1

while(start_point[1]>y_temp):
    y_temp+=y_die+y_dsw
    y_dpr_count+=1
    if y_dpr_count==y_dpr+1:
        y_dpr_count=1
        y_temp+=y_rsw

while(start_point[1]>y_temp):
    y_temp-=(y_die+y_dsw)
    y_dpr_count-=1
    if y_dpr_count==0:
        y_dpr_count=y_dpr
        y_temp-=y_rsw

die_pos_in_ret=[x_dpr_count,y_dpr_count]

#note all the indexes which are already visited to avoid endless looping recursions
visited=[]

def point_inside_gripper(x,y):
    
    if wafer_radius - math.dist([0,0],[x,y]) > g_height:
        return False
    
    for coord in g_coord:

        # if abs(coord[0]-x) < g_height and abs(coord[1]-y) < g_width:
        #     return True
       
        bl_angle=math.degrees(math.atan2(coord[5],coord[4]))
        tl_angle=math.degrees(math.atan2(coord[1],coord[0]))
        br_angle=math.degrees(math.atan2(coord[7],coord[6]))
        tr_angle=math.degrees(math.atan2(coord[3],coord[2]))

        given_angle=math.degrees(math.atan2(y,x))

        if (given_angle<bl_angle or given_angle<tl_angle) and (given_angle>br_angle or given_angle>tr_angle):
                return True
    return False

def die_num(x_curr,y_curr,x_pos,y_pos,x_pos_ret,y_pos_ret):
    
    visited.append([x_pos,y_pos])

    #calculate distance of all four corners of the die from the center of the wafer
    left_dist=math.dist([0,0],[x_curr,y_curr])
    right_dist=math.dist([0,0],[x_curr+x_die,y_curr])
    top_dist=math.dist([0,0],[x_curr,y_curr+y_die])
    top_right_dist=math.dist([0,0],[x_curr+x_die,y_curr+y_die])

    #if any one distance is lower than the radius of wafer, it atleast partially lies inside the wafer
    if left_dist<wafer_radius or right_dist<wafer_radius or top_dist<wafer_radius or top_right_dist<wafer_radius:

        #plot the die in the graph for visualization
        #rect = Rectangle((x_curr,y_curr),x_die,y_die,edgecolor='r',facecolor='none')
        #ax.add_patch(rect)

        #plot the index of the die
        #text_x = x_curr + x_die / 2
        #text_y = y_curr + y_die / 2
        #ax.text(text_x, text_y, "("+str(x_pos)+","+str(y_pos)+")", color='black', ha='center', va='center')

        if (left_dist<boundary_radius or right_dist<boundary_radius or top_dist<boundary_radius or top_right_dist<boundary_radius):
            
            # if (x_curr,y_curr) in meas_dict.keys():

            #     coords=meas_dict[x_curr,y_curr]

            #     for coord in coords:

            #         if not point_inside_gripper(coord[0],coord[1]):
                
            #             x_temp = abs(x_curr-coord[0])
            #             y_temp = abs(y_curr-coord[1])

            #             #write the output into the file
            #             out.write("("+str(x_pos)+","+str(y_pos)+"):("+str(x_temp)+","+str(y_temp)+")\n")
            #             #print("("+str(x_pos)+","+str(y_pos)+"):("+str(x_temp)+","+str(y_temp)+")")

            #             #plot the dot
            #             #plt.plot(coord[0],coord[1],'ro',markersize=3)
                        
            #             #rect = Rectangle((x_curr,y_curr),x_die,y_die,edgecolor='r',facecolor='none')
            #             #ax.add_patch(rect)

            #             #plot the index of the die
            #             text_x = x_curr + x_die / 2
            #             text_y = y_curr + y_die / 2
            #             #ax.text(text_x, text_y, "("+str(x_pos)+","+str(y_pos)+")", color='black', ha='center', va='center')
                        

            for coord in meas_list:
                
                if  x_curr<=coord[0]<=x_curr+x_die and y_curr<=coord[1]<=y_curr+y_die and (math.dist([0,0],[coord[0],coord[1]])<=boundary_radius) :

                    if not point_inside_gripper(coord[0],coord[1]):

                        x_temp = abs(x_curr-coord[0])
                        y_temp = abs(y_curr-coord[1])

                        #write the output into the file
                        out.write("("+str(x_pos)+","+str(y_pos)+"):("+str(x_temp)+","+str(y_temp)+")\n")
                        #print("("+str(x_pos)+","+str(y_pos)+"):("+str(x_temp)+","+str(y_temp)+")")

                        #plot the dot
                        # rect = Rectangle((x_curr,y_curr),x_die,y_die,edgecolor='r',facecolor='none')
                        # ax.add_patch(rect)

                        #plot the index of the die
                        # text_x = x_curr + x_die / 2
                        # text_y = y_curr + y_die / 2
                        # ax.text(text_x, text_y, "("+str(x_pos)+","+str(y_pos)+")", color='black', ha='center', va='center')
                        # plt.plot(coord[0],coord[1],'ro',markersize=3)

        x_prev=x_next=x_dsw
        x_prev_change=x_next_change=0
        y_prev=y_next=y_dsw
        y_prev_change=y_next_change=0
        
        #set the variables such that reticle street width and height are considered when needed
        if x_pos_ret==1:
            x_prev+=x_rsw
            x_prev_change=x_dpr+1-x_pos_ret
        if x_pos_ret==x_dpr:
            x_next+=x_rsw
            x_next_change=-x_pos_ret
        if y_pos_ret==1:
            y_prev+=y_rsw
            y_prev_change=y_dpr+1-y_pos_ret
        if y_pos_ret==y_dpr:
            y_next+=y_rsw
            y_next_change=-y_pos_ret

        #recursively call the die that is above, below, left and right to the current die
        if [x_pos-1,y_pos] not in visited:
            die_num(x_curr-x_die-x_prev,y_curr,x_pos-1,y_pos,x_pos_ret-1+x_prev_change,y_pos_ret)
                
        if [x_pos,y_pos-1] not in visited:
            die_num(x_curr,y_curr-y_die-y_prev,x_pos,y_pos-1,x_pos_ret,y_pos_ret-1+y_prev_change)

        if [x_pos+1,y_pos] not in visited:
            die_num(x_curr+x_die+x_next,y_curr,x_pos+1,y_pos,x_pos_ret+1+x_next_change,y_pos_ret)

        if [x_pos,y_pos+1] not in visited:
            die_num(x_curr,y_curr+y_die+y_next,x_pos,y_pos+1,x_pos_ret,y_pos_ret+1+y_next_change)
    else:
        return

#start recursion with refernce die and its index as (0,0)
die_num(start_point[0],start_point[1],0,0,die_pos_in_ret[0],die_pos_in_ret[1])

plt.show()

inp.close()
out.close()