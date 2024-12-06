import math
import sys

sys.setrecursionlimit(20000)
#open the input file
inp= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Milestone3\\Input\\Testcase1.txt",'r')
out= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Output\\Milestone3\\Milestone3AlternateOutput1.txt",'w')

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

x_dsw=inp_dict["DieStreetWidthAndHeight"][0]
y_dsw=inp_dict["DieStreetWidthAndHeight"][1]

x_rsw=inp_dict["RecticleStreetWidthAndHeight"][0]
y_rsw=inp_dict["RecticleStreetWidthAndHeight"][1]

x_dpr=inp_dict["DiesPerReticle"][0]
y_dpr=inp_dict["DiesPerReticle"][1]

ref_die_point=[x_ref,y_ref]   #center of reference die
start_point=[ref_die_point[0]-(x_die/2),ref_die_point[1]-(y_die/2)]

x_temp=0
x_dpr_count=1

while(start_point[0]>x_temp):
    x_temp+=x_die+x_dsw
    x_dpr_count+=1
    if x_dpr_count==x_dpr:
        x_dpr_count=1
        x_temp+=x_rsw

y_temp=0
y_dpr_count=1

while(start_point[1]>y_temp):
    y_temp+=y_die+y_dsw
    y_dpr_count+=1
    if y_dpr_count==y_dpr:
        y_dpr_count=1
        y_temp+=y_rsw

die_pos_in_ret=[x_dpr_count,y_dpr_count]
print(die_pos_in_ret)
visited=[]

def die_num(x_curr,y_curr,x_pos,y_pos,x_pos_ret,y_pos_ret):
    
    visited.append([x_pos,y_pos])

    left_dist=math.dist([0,0],[x_curr,y_curr])
    right_dist=math.dist([0,0],[x_curr+x_die,y_curr])
    top_dist=math.dist([0,0],[x_curr,y_curr+y_die])
    top_right_dist=math.dist([0,0],[x_curr+x_die,y_curr+y_die])


    if left_dist<wafer_radius or right_dist<wafer_radius or top_dist<wafer_radius or top_right_dist<wafer_radius:

        out.write("("+str(x_pos)+","+str(y_pos)+"):("+str(x_curr)+","+str(y_curr)+")\n")

        if [x_pos-1,y_pos] not in visited:
            if x_pos_ret==1:
                die_num(x_curr-x_die-x_rsw-x_dsw, y_curr, x_pos-1, y_pos, x_dpr, y_pos_ret)
            else:
                die_num(x_curr-x_die-x_dsw,y_curr, x_pos-1, y_pos, x_pos_ret-1, y_pos_ret)

        if [x_pos+1,y_pos] not in visited:
            if x_pos_ret==x_dpr:
                die_num(x_curr+x_die+x_rsw+x_dsw, y_curr, x_pos+1, y_pos, 1, y_pos_ret)
            else:
                die_num(x_curr+x_die+x_dsw,y_curr, x_pos+1, y_pos, x_pos_ret+1, y_pos_ret)

        if [x_pos,y_pos-1] not in visited:
            if x_pos_ret==1:
                die_num(x_curr, y_curr-y_die-y_dsw-y_rsw, x_pos, y_pos-1, x_pos_ret, y_dpr)
            else:
                die_num(x_curr, y_curr-y_die-y_dsw, x_pos, y_pos-1, x_pos_ret, y_pos_ret-1)
            
        if [x_pos,y_pos+1] not in visited:
            if x_pos_ret==y_dpr:
                die_num(x_curr, y_curr+y_die+y_dsw+y_rsw, x_pos, y_pos+1, x_pos_ret, 1)
            else:
                die_num(x_curr, y_curr-y_die-y_dsw, x_pos, y_pos+1, x_pos_ret, y_pos_ret+1)
            
    else:
        return


die_num(start_point[0],start_point[1],0,0,die_pos_in_ret[0],die_pos_in_ret[1])

inp.close()
out.close()