from PIL import Image, ImageDraw, ImageEnhance
IMDIM=None



def readFromDXF(filename,outfile,d):
    
    global IMDIM
    IMDIM=d
    file = open(filename)
    DXFtxt = file.readlines()
    file.close()
    
    segment = -1
    path = []
    xold = []
    yold = []
    line = 0
    polyline = 0
    vertex = 0

    while line < len(DXFtxt):
        if (DXFtxt[line] == "POLYLINE\n"):
            segment += 1
            polyline = 1
            path.append([])
        elif (DXFtxt[line] == "VERTEX\n"):
            vertex = 1
        elif ((DXFtxt[line].strip() == "10") & (vertex == 1) & (polyline == 1)):
            line += 1
            x = float(DXFtxt[line])
        elif ((DXFtxt[line].strip() == "20") & (vertex == 1) & (polyline == 1)):
            line += 1
            y = float(DXFtxt[line])
            if ((x != xold) | (y != yold)):
                path[segment].append([float(x),float(y)])
                xold = x
                yold = y
        elif (DXFtxt[line] == "SEQEND\n"):
            polyline = 0
            vertex = 0

        line += 1

    x = []
    y = []

    for shape in path:
        for coord in shape:
            x.append(coord[0])
            y.append(coord[1])

    maxx = max(x)
    maxy = max(y) 
    minx = min(x)
    miny = min(y)

    margin = min(minx, miny)
    size = max(maxx, maxy) + margin
    scale = IMDIM / size
    for i in range(len(path)):
        for j in range(len(path[i])):
            path[i][j][0] *= scale
            path[i][j][1] *= scale


    file = open(outfile+"/output.gcode", "w")
    file.write("G1 X0.0 Y0.0\n")
    up = True
    for shape in path:
        for i in range(len(shape)):
             xstr = str(round(shape[i][0],2))
             ystr = str(round(shape[i][1],2))
             file.write("G1 "+"X" + xstr + " Y" + ystr + "\n")
             if up == True:
                file.write("M300 S30.00 (pen down)\n")
                
                up = False
        file.write("M300 S50.00 (pen Up)\n")
        up = True
    file.write("G1 X0.0 Y0.0\n")
    file.write("M18\n")
    file.close()
    print("Done printing")


# readFromDXF("abc.dxf","output.gcode") 