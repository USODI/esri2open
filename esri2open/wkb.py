from struct import pack
from sqlite3 import Binary
def pts(c):
    return ["dd",[c.X,c.Y]]
def pt4mp(c):
    return ["Bidd",[1,1,c.X,c.Y]]
def mp(coordinates):
    partCount=coordinates.partCount
    i=0
    out = ["I",[0]]
    while i<partCount:
        pt = coordinates.getPart(i)
        [ptrn,c]=pt4mp(pt)
        out[0]+=ptrn
        out[1][0]+=1
        out[1].extend(c)
        i+=1
    return out
def lineSt(coordinates):
    partCount=coordinates.count
    i=0
    out = ["I",[0]]
    while i<partCount:
        pt = coordinates[i]
        [ptrn,c]=pts(pt)
        out[0]+=ptrn
        out[1][0]+=1
        out[1].extend(c)
        i+=1
    return out
def linearRing(coordinates):
    partCount=coordinates.count
    i=0
    values =[0]
    outnum = "I"
    out = ["I",[0]]
    while i<partCount:
        pt = coordinates[i]
        if pt:
            [ptrn,c]=pts(pt)
            outnum+=ptrn
            values[0]+=1
            values.extend(c)
        else:
            out[0]+=outnum
            out[1][0]+=1
            out[1].extend(values)
            values =[0]
            outnum = "I"
        i+=1
    out[0]+=outnum
    out[1][0]+=1
    out[1].extend(values)
    return out
def multiRing(coordinates):
    partCount=coordinates.partCount
    i=0
    values =[0]
    outnum = "I"
    out = ["I",[0]]
    while i<partCount:
        part = coordinates.getPart(i)
        [ptrn,c]=linearRing(part)
        outnum+=ptrn
        values[0]+=1
        values.extend(c)
        i+=1
    out[0]+=outnum
    out[1][0]+=1
    out[1].extend(values)
    return out
def makePoint(c):
    values = ["<BI",1,1]
    [ptrn,coords] = pts(c.getPart(0))
    values[0]+=ptrn
    values.extend(coords)
    return Binary(pack(*values))
def makeMultiPoint(c):
    values = ["<BI",1,4]
    [ptrn,coords]=mp(c)
    values[0]+=ptrn
    values.extend(coords)
    return Binary(pack(*values))
def makeMultiLineString(c):
    values = ["<BI",1,2]
    [ptrn,coords]=lineSt(c.getPart(0))
    values[0]+=ptrn
    values.extend(coords)
    return Binary(pack(*values))
def makeMultiPolygon(c):
    values = ["<BI",1,3]
    [ptrn,coords]=linearRing(c.getPart(0))
    values[0]+=ptrn
    values.extend(coords)
    return Binary(pack(*values))

def getWKBFunc(type):
    if type == "point":
        return makePoint
    elif type == "multipoint":
        return makeMultiPoint
    elif type == "polyline":
        return makeMultiLineString
    elif type == "polygon":
        return makeMultiPolygon