import math

#open the input file
inp= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Milestone1\\Input\\Testcase4.txt",'r')
out= open("C:\\Users\\rammu\\OneDrive\\Desktop\\MSc SS\\6th sem\\kla-hackathon\\Workshop2024\\Output\\Milestone1\\Milestone1Output4.txt",'w')

#read the input content into a dictionary
lines=inp.readlines()
inp_dict = dict()

for line in lines:
    inp_list=line.split(":")
    inp_dict[inp_list[0]]=int(inp_list[1].split("\n")[0])

#initial setup to start calculations
initial_point=(0,0)
wafer_diameter=inp_dict["WaferDiameter"]
wafer_radius=wafer_diameter/2
total_points=inp_dict["NumberOfPoints"]
radians=math.radians(inp_dict["Angle"])
x_point=(-wafer_radius)*math.cos(radians)
y_point=(-wafer_radius)*math.sin(radians)
start_point=[x_point,y_point]
dist=wafer_diameter/(total_points-1)


def calculate_nextpt(curr_point,radians,dist):
    next_x=curr_point[0]+dist*math.cos(radians)
    next_y=curr_point[1]+dist*math.sin(radians)
    return[next_x,next_y]

curr_pt=start_point
for i in range(total_points):
    out.write("("+str(curr_pt[0])+","+str(curr_pt[1])+")\n")
    #print(i,curr_pt)
    curr_pt=calculate_nextpt(curr_pt,radians,dist)
    

inp.close()
out.close()
    
