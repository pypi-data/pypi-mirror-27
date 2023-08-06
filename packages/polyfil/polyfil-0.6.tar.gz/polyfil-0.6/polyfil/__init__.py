from cv2 import imread,IMREAD_UNCHANGED, imwrite
import numpy as np


class simplePolyFill:

    def __init__(self, tmpcnrs, imarray):
        self.cnrs=tmpcnrs
        self.minn=np.empty
        self.maxn=np.array((0,0), dtype=np.int16)
        self.extremes=np.zeros((2,2), dtype=np.int16)
        self.fillarea=None
        self.xdif=0
        self.ct=0
        self.image=np.asarray(imarray)
        self.dotdot=None

    def buildOrderedNodes(self):
        tmpcnrs=self.cnrs
        ncnrs=len(tmpcnrs)
        cnrs=np.zeros((ncnrs+1,2), dtype=np.int16)
        if tmpcnrs[0][1]<=tmpcnrs[ncnrs-1][1]:
            cnrs[0:ncnrs]=tmpcnrs[0:ncnrs]
        else:
            shf=np.zeros((2,ncnrs-2))
            initcmp=tmpcnrs[0]
            shf=tmpcnrs[1:ncnrs-1]
            cnrs[0]=tmpcnrs[ncnrs-1]
            cnrs[1]=initcmp
            cnrs[2:ncnrs]=shf
        cnrs[ncnrs]=cnrs[0]
        self.minn=tmpcnrs[0]
        self.cnrs=cnrs


    def extremeCorners(self):
        tmpcnrs=self.cnrs
        nnodes=len(tmpcnrs)-1
        minn=self.minn
        maxn=self.maxn
        for node in range(nnodes):
            tx,ty=tmpcnrs[node]
            if minn[0]>tx:
                minn[0]=tx
            if maxn[0]<tx:
                maxn[0]=tx
            if minn[1]>ty:
                minn[1]=ty
            if maxn[1]<ty:
                maxn[1]=ty
        self.minn,self.maxn=minn,maxn

    def bresenham(self, idx):
        p0, p1=self.cnrs[idx],self.cnrs[idx+1]
        x0,y0=p0
        dx, dy=p1-p0
        xsign, ysign = (1 if dx>0 else -1), (1 if dy>0 else -1)
        dx, dy= abs(dx), abs(dy)
        if dx>dy:
            xx,xy,yx,yy=xsign,0,0,ysign
        else:
            dx, dy=dy, dx
            xx,xy,yx,yy=0,ysign, xsign, 0
        pk=2*dy-dx
        y=0
        line=np.zeros((dx+1,2), dtype=np.uint16)
        for i in range(dx+1):
            line[i]=x0+i*xx+y*yx,y0+i*xy+y*yy
            if pk>0:
                y+=1
                pk-=2*dx
            pk+=2*dy
        return line, dx+1
    def polygon(self):
        nvertexes=len(self.cnrs)-1
        prepoint=self.minn[1]
        maxnpoint=self.maxn[1]
        self.xdif=self.maxn[0]-self.minn[0]
        ct0, ct1=2, 0
        walls=np.zeros((maxnpoint,2), dtype=np.uint16)
        for vtx in range(nvertexes):
            linea, npoints=self.bresenham(vtx)
            iter=np.zeros((npoints, 1))
            it = np.nditer(iter, flags=['multi_index'], op_flags=['readwrite'])
            while not it.finished:
                r=it.multi_index[0]
                nx,ny=linea[r]
                if prepoint>ny:
                    walls[ct1-ct0][1]=nx
                    ct0+=1
                if prepoint<ny:
                    walls[ct1][0]=nx
                    ct1+=1
                prepoint=linea[r][1]
                self.image[ny][nx]=[0,0,0,255]
                it.iternext()
        self.fillarea=walls[0:ct1-1]
        self.ct=ct1-1
    def polygonFill(self):
        iter=np.zeros((self.ct, 1))
        it = np.nditer(iter, flags=['multi_index'], op_flags=['readwrite'])
        maxsize=(self.xdif)*(self.ct)
        dotdot=np.zeros((maxsize,2))
        difac=0
        inity=self.cnrs[0][1]+1
        image=self.image
        while not it.finished:
            r=it.multi_index[0]
            fila=self.fillarea[r]
            dif=fila[1]-fila[0]
            for px in range(dif):
                dotdot[difac+px]=[fila[0]+px,inity+r]
                image[inity+r][fila[0]+px]=[0,0,0,255]
            difac+=dif
            self.image=image
            it.iternext()
        return dotdot[0:difac]

    def getPixelsCoords(self):
        self.buildOrderedNodes()
        self.extremeCorners()
        self.polygon()
        dotdot=self.polygonFill()
        return dotdot

    def plotFillArea(self, name):
        imwrite(name,self.image)
