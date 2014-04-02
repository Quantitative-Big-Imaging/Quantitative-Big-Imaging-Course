# This source reads a text file and produces a data set
# The file is of the form (where [denotes optional and repeatable]:
# X,Y,Z[,ARRAYNAME]
# x0,y0,z0[,value]
# x1,y1,z1[,value
# ...
#from paraview import vtk
#from random import randint as randi
#pdo=self.GetOutputDataObject(0)
#pdi=self.GetInputDataObject(0,0)
#pdo.CopyAttributes(pdi)
#pdo.Allocate(500,1)
#maxPt=pdi.GetNumberOfPoints()
#for i in range(500):
#	aLine = vtk.vtkLine()
#	aLine.GetPointIds().SetId(0, randi(0, maxPt))
#	aLine.GetPointIds().SetId(1, randi(0, maxPt))
#	pdo.InsertNextCell(aLine.GetCellType(), aLine.GetPointIds())
from paraview import vtk
from paraview.vtk import dataset_adapter as DA
import os,sys
from numpy import array,single,zeros
import numpy
import os,sys
def loadFoam(cObj,cNum):
	cFile='/Users/maderk/Documents/MATLAB/TextureTensor/Foam/ujax/dk31m00/'
	cFile+='bubble_dk31_%02d.csv' % cNum
	filterList=[]
	#filterList+=[('MASK_DISTANCE_MEAN',lambda x: x>180)]
	#filterList+=[('VOLUME',lambda x: x<4000)]
	synList=[]
	synList+=[('Alignment',lambda x: 180/numpy.pi*calcAlignment(x,'PCA1_X','PCA1_Y','PCA1_Z','VOLUME'))]
	synList+=[('ShapeAnisotropy',lambda x: calcAnisotropy(x,'PCA1_S','PCA2_S','PCA3_S'))]
	synList+=[('ShapeOblateness',lambda x: calcOblateness(x,'PCA1_S','PCA2_S','PCA3_S'))]
	synList+=[('PosTheta',lambda x: calcTheta(x,'POS_X','POS_Y',recenter=True))]
	synList+=[('Theta',lambda x: calcTheta(x,'PCA1_X','PCA2_Y',recenter=False))]
	synList+=[('Theta-XZ',lambda x: chkgvlcalcTheta(x,'PCA1_X','PCA2_Z',recenter=False))]
	return ImportCSV(cObj,cFile,filterList,synList)
def initCol(cName,data,keepPoints):
	name=vtk.vtkTypeFloat32Array()
	name.SetNumberOfComponents(1)
	name.SetNumberOfTuples(0)
	name.SetName(cName)
	if keepPoints is None: keepPoints=range(0,len(data))
	for cI in keepPoints: name.InsertNextTuple((data[cI],))
	return name
def initCol3(cName,dat1,dat2,dat3,keepPoints=None):
	name=vtk.vtkTypeFloat32Array()
	name.SetNumberOfComponents(3)
	name.SetNumberOfTuples(0)
	name.SetName(cName)
	if keepPoints is None: keepPoints=range(0,len(dat1))
	for cI in keepPoints: name.InsertNextTuple((dat1[cI],dat2[cI],dat3[cI]))
	print (cName,len(keepPoints))
	return name	
	
def initColTens(cName,dat1,dat2,dat3,dat4,dat5,dat6,dat7,dat8,dat9,keepPoints=None):
	name=vtk.vtkTypeFloat32Array()
	name.SetNumberOfComponents(9)
	name.SetNumberOfTuples(0)
	name.SetName(cName+'_T')
	if keepPoints is None: keepPoints=range(0,len(dat1))
	
	for cI in keepPoints: name.InsertNextTuple((dat1[cI],dat2[cI],dat3[cI],dat4[cI],dat5[cI],dat6[cI],dat7[cI],dat8[cI],dat9[cI]))
	print (cName,len(keepPoints))
	return name	
def getTriplets(allCols,cn1='_X',cn2='_Y',cn3='_Z'):
	xcols=filter(lambda x: (x.find(cn1)>=0),allCols)
	xcols=filter(lambda x: not (x.find('T'+cn1)>=0),xcols)
	repPrefix=lambda x,y,z: z.join(x.split(y))
	goodList=[(repPrefix(curCol,cn1,''),(repPrefix(curCol,cn1,cn1),repPrefix(curCol,cn1,cn2),repPrefix(curCol,cn1,cn3))) for curCol in xcols if ((repPrefix(curCol,cn1,cn2) in allCols) and (repPrefix(curCol,cn1,cn3) in allCols))]	
	return goodList
def getTensors(allCols,cn1=['_XX','_XY','_XZ','_YX','_YY','_YZ','_ZX','_ZY','_ZZ']):
	xcols=filter(lambda x: x.find('T'+cn1[0])>=0,allCols)
	repPrefix=lambda x,y,z: z.join(x.split(y))
	goodList=[]
	for curCol in xcols:
		cRow=[]
		for curEle in cn1:
			cName=repPrefix(curCol,cn1[0],curEle)
			if cName in allCols: cRow+=[cName]
			else: cRow+=['NULL']
		if len(cRow)>2: goodList+=[(repPrefix(curCol,cn1[0],''),tuple(cRow))]
	return goodList
def wtexture(xv,yv,zv,wv):
	""" Since the function will be used alot and is tedious to implement """
	xv=numpy.array(xv)
	yv=numpy.array(yv)
	zv=numpy.array(zv)
	wv=numpy.array(wv)
	
	swv=sum(wv)
	xm=numpy.multiply(xv,wv)/swv
	ym=numpy.multiply(yv,wv)/swv
	zm=numpy.multiply(zv,wv)/swv
	
	xv-=xm
	yv-=ym
	zv-=zm
	
	xv*=wv
	yv*=wv
	zv*=wv
	
	textMat=[[sum(xv*xv)/swv,sum(xv*yv)/swv,sum(xv*zv)/swv]]
	textMat+=[[sum(yv*xv)/swv,sum(yv*yv)/swv,sum(yv*zv)/swv]]
	textMat+=[[sum(zv*xv)/swv,sum(zv*yv)/swv,sum(zv*zv)/swv]]
	return textMat
	DA.numpyTovtkDataArray(numpy.random.rand(50,1))
import numpy as np
class ctexture:
    def __init__(self,textMat):
        self.textMat=textMat
        (self._w,self._v)=np.linalg.eigh(textMat)
        #self._w=np.sqrt(self._w) # No sqrt in texture tensor
    def todict(self,name='TEXTURE',length=1,oDict=None):
    	if oDict is None: oDict={}
    	for (i,cAxI) in enumerate('XYZ'):
    		for (j,cAxJ) in enumerate('XYZ'):
    			oDict[name+'T_'+cAxI+cAxJ]=[self.textMat[i,j]]*length
    	return oDict
    def mean(self):
        return sqrt(self.textMat.trace())
    def v1(self):
        return self._v[:,2]
    def alignment(self):
        return 3.0/2.0*(self._w[2]/sum(self._w)-1.0/3.0)*100
class lacDB_TEXT:
    def __init__(self):
        self.count = 0.0
        self.countn= 0
        self.sumx2 = 0.0
        self.sumx = 0.0
        self.sumxy=0.0
        self.sumxz=0.0
        self.sumy2 = 0.0
        self.sumyz=0.0
        self.sumz2=0.0
        self.text=0
        

    def step(self, valueX,valueY,valueZ,valueW=1.0):
        if valueX is None: return 0
        if valueY is None: return 0
        if valueZ is None: return 0
        if valueW is None: return 0
        self.count+=valueW
        self.countn+=1
        self.sumx+=valueW*valueX
        self.sumy+=valueW*valueY
        self.sumz+=valueW*valueZ
        
        self.sumx2+=valueW*valueX**2
        self.sumxy+=valueW*valueX*valueY
        self.sumxz+=valueW*valueX*valueZ
        self.sumy2+=valueW*valueY**2
        self.sumyz+=valueW*valueY*valueZ
        self.sumz2+=valueW*valueZ**2

    def textMat(self):
        meanx=self.sumx/self.count
        meany=self.sumy/self.count
        meanz=self.sumz/self.count
        
        return np.array([[self.sumx2/self.count-meanx**2,self.sumxy/self.count-meanx*meany,self.sumxz/self.count-meanx*meanz],[self.sumxy/self.count-meanx*meany,self.sumy2/self.count-meany**2,self.sumyz/self.count-meany*meanz],[self.sumxz/self.count-meany*meanz,self.sumyz/self.count-meany*meanz,self.sumz2/self.count-meanz**2]])
        
    def finalize(self):
        if self.countn<2: return 100
        self.text=ctexture(self.textMat())
        return self.text.alignment()
        
def calcAlignment(allcols,cn1,cn2,cn3,cnWeight=None,returnAxis=True,signedAxis=True):
	""" Since the function will be used alot and is tedious to implement """
	ptlist=[]
	ptlist+=[allcols[cn1]]
	ptlist+=[allcols[cn2]]
	ptlist+=[allcols[cn3]]
	ptlist=numpy.array(ptlist)
	ptmag=numpy.sqrt(ptlist[0,:]**2+ptlist[1,:]**2+ptlist[2,:]**2)
	ptlist[0,:]/=ptmag
	ptlist[1,:]/=ptmag
	ptlist[2,:]/=ptmag
	if cnWeight is None:
		textMat=numpy.cov(ptlist)  	
	else:
		xv=ptlist[0,:]
		yv=ptlist[1,:]
		zv=ptlist[2,:]
		wv=numpy.array(allcols[cnWeight])
		textMat=wtexture(xv,yv,zv,wv)
		print (len(xv),len(wv)) 	
		print textMat
	(_w,_v)=numpy.linalg.eigh(textMat)
	print 'Main Direction:'+str(_v[:,2])+', Overall alignment:'+str(3.0/2.0*(_w[2]/sum(_w)-1.0/3.0)*100)
	
	if returnAxis:
		oMat=[]
		sMat=[]
		for cRow in range(3):
			mv=numpy.array([list(_v[:,cRow])]*ptlist.shape[1]).transpose()
			oMat+=[numpy.abs(numpy.sum(numpy.multiply(ptlist,mv),0))]
			sMat+=[numpy.sign(numpy.sum(numpy.multiply(ptlist,mv),0))]
		oAx=numpy.argmax(numpy.array(oMat),0)
		if signedAxis:
			sMat=numpy.array(sMat).transpose()
			return numpy.array(map(lambda x: 2*(x[1]+1)+1*(x[0][x[1]]==1),zip(sMat,oAx)))
		else: 
			return oAx+1
	else:
		mv=numpy.array([list(_v[:,2])]*ptlist.shape[1]).transpose()
		return numpy.arccos(numpy.abs(numpy.sum(numpy.multiply(ptlist,mv),0)))    
def calcAnisotropy(allcols,cn1,cn2,cn3):
	""" Since the function will be used alot and is tedious to implement """
	p1list=numpy.array(allcols[cn1])
	p2list=numpy.array(allcols[cn2])
	p3list=numpy.array(allcols[cn3])	
	return (3.0/2.0*(p1list/(p1list+p2list+p3list)-1.0/3.0)*100)
def calcOblateness(allcols,cn1,cn2,cn3):
	""" Since the function will be used alot and is tedious to implement """
	p1list=numpy.array(allcols[cn1])
	p2list=numpy.array(allcols[cn2])
	p3list=numpy.array(allcols[cn3])	
	return (2*(p1list-p2list)/(p1list-p3list)-1)
def calcTheta(allcols,cnx,cny,cnw=None,recenter=True):
	""" Since the function will be used alot and is tedious to implement """
	p1list=numpy.array(allcols[cnx])
	p2list=numpy.array(allcols[cny])
	if cnw is not None: p3list=numpy.array(allcols[cnw])
	else: p3list=p1list*0+1
	mx=numpy.multiply(p1list,p3list)/sum(p3list)
	my=numpy.multiply(p2list,p3list)/sum(p3list)
	if not recenter:
		mx=0
		my=0
	return 180/numpy.pi*numpy.arctan2(p2list-my,p1list-mx)
def ImportCSV(cObj,filename='',filterList=[],synList=[],outObj=0,fromR=False,csvdelim=True):
	cTable=cObj.GetOutputDataObject(outObj)
	if csvdelim: delim=','
	else: delim='\t'
	(header,cols)=LoadCSVFile(filename,fromR=fromR,delim=delim)
	return ImportData(cTable,cols,filterList,synList)
def ImportDB(cObj,sqlRest='',filterList=[],synList=[],outObj=0):
	cTable=cObj.GetOutputDataObject(outObj)
	if len(sqlRest)>0: sqlRest='WHERE '+sqlRest
	import dbImport as dbi
	cur=dbi.cur
	headerCols=[cCol[0] for cCol in cur.execute('SHOW COLUMNS FROM LACUNA').fetchall()]
	cols={}
	for cCol in headerCols: cols[cCol]=[]
	for cResult in cur.execute('SELECT '+','.join(headerCols)+' FROM LACUNA '+sqlRest):
		for (ccCol,cVal) in zip(headerCols,cResult): cols[ccCol]+=[cVal]
	return ImportData(cTable,cols,filterList,synList)	
def ImportData(output,cols,filterList=[],synList=[]):
	""" Filter list is for adding lambda based filters, synList is for synthetic columns """
	
	
	print 'Importing Next Step...'
	#ncols=lacpa_adddb(None,cols,header,'',False) # formatted and scaled
	#cols=ncols
	print 'Filtering List'
	keepPoints=numpy.array([True]*len(cols.values()[0])) # only
	for (cFiltCol,cFiltFunc) in filterList: keepPoints&=map(cFiltFunc,cols[cFiltCol])
	print 'Keeping - '+str((sum(keepPoints),len(keepPoints)))
	keepPoints=[cValue for (cValue,isKept) in enumerate(keepPoints) if isKept]
	for cKey in cols.keys(): cols[cKey]=numpy.array(cols[cKey])[keepPoints]
	print ' Adding columns'
	for (cName,cData) in cols.items(): output.AddColumn(initCol(cName,cData,None))
	print ' Adding Triplets'
	allTrips=getTriplets(cols.keys())
	print allTrips
	for (cName,cCols) in allTrips: output.AddColumn(initCol3(cName,cols[cCols[0]],cols[cCols[1]],cols[cCols[2]],None))
	print ' Adding Tensors'
	cols['NULL']=0*single(cols.values()[0])
	allTens=getTensors(cols.keys())
	print allTens
	for (cName,cCols) in allTens: output.AddColumn(initColTens(cName,cols[cCols[0]],cols[cCols[1]],cols[cCols[2]],cols[cCols[3]],cols[cCols[4]],cols[cCols[5]],cols[cCols[6]],cols[cCols[7]],cols[cCols[8]],None))
	
	print ' Adding synthetic columns'
	for (cName,cFunc) in synList: output.AddColumn(initCol(cName,cFunc(cols),None))
	return output

def addRowsToTable(output,junkName,outMat,entry_order):
	#globals()['a']=entry_order
	#globals()['b']=outMat
	outArray=numpy.array(outMat)
	outDict={}
	for (cI,cLabel) in enumerate(entry_order): outDict[cLabel]=outArray[:,cI]
	return outDict
from numpy import single
def parseCSV(text,filename='',fromR=False,delim=','):
    def temp_clean(text):
        return (''.join(text.split('/'))).upper().strip()    
    def temp_parse(temp):
        ntemp=[]
        errCount=0
        for val in temp:
            if val.strip().upper()=='NAN':
                cval='0'
                errCount+=1
            else:
                cval=val
            try:
                cval=single(cval)
            except:
                cval=-1
                errCount+=1        
            ntemp+=[cval]
        return (ntemp,errCount) 
    rows=text.split('\n')
    # First row is header
    if fromR:
        fileDict={}
        hRow=0
    else:
        hRow=1
        head1=rows[0]
        head1=''.join(head1.split('//'))
        newStr=[cEle.strip().split(':') for cEle in head1.strip().split(delim)]
        fileDict={}
        for cEle in newStr: 
    	    if len(cEle)==2:
    		    fileDict[temp_clean(cEle[0])]=cEle[1].split('/')[-1].strip()
    fTime=True
    head2=rows[hRow]
    head2=''.join(head2.split('//'))
    head2=[temp_clean(cEle) for cEle in head2.strip().split(delim)]
    # Check for duplicates in header string (and just use the last entry)
    # Generate a dictionary of all header entries
    cleanHeader={}
    for k in range(len(head2)):
        cleanHeader[head2[k]]=k
    # create a new null filled header
    head2=['NULL']*len(head2)
    # use the dictionary to repopulate the head2 entry
    for cKey in cleanHeader.keys(): head2[cleanHeader[cKey]]=cKey  
    outTable={}
    for col in head2: outTable[col]=[]
    for row in rows[2:]:
        temp=row.split(delim)
        try:
            (ntemp,errs)=temp_parse(temp)
            if errs<2:
                if len(ntemp)==len(head2):
                    for k in range(0,len(head2)): outTable[head2[k]]+=[ntemp[k]]     
        except:
            #if fTime: print (len(ntemp),len(head2))
            fTime=False
            temp=[]
    for col in head2: outTable[col]=numpy.array(outTable[col])
    outrows=len(outTable[head2[0]])
    print 'Parsed .. '+str(outrows)+' of '+str(len(rows))
    return (outrows,fileDict,outTable)
def LoadCSVFile(filename,fromR=False,delim=','):
    if True:
        rawtext=''.join(open(filename).readlines())
    else:
        print filename+' is garbage'
    if True:
        (outrows,a,b)=parseCSV(rawtext,fromR=fromR,delim=delim)
        if outrows>2:
            return (a,b)
        else:
            print filename+' is too short!'+str((outrows,a,b))
    else:
        print filename+' is junk:'+rawtext[0:100] 
def getProjNum(*args): return 1
def getSampleNum(*args): return 1
def lacpa_adddb(cur,ptList,oTable,rawFilename,processName=True,tableName='Lacuna',CanalMode=0,projectTitle='None'):
    lacNumOffset=0
    if processName: (filename,lacNumOffset)=processInputName(rawFilename,lacFilename)
    else: filename=rawFilename
    nptList=dict([(cCol.upper(),cDat) for (cCol,cDat) in ptList.items()])
    #ptList=CaseFreeDict(ptList)
    
    dbLen=len(ptList['SCALE_X'])
    if not oTable.has_key('SAMPLE'): 
        oTable['SAMPLE']=''
        print filename+' is missing sample name' 
    dx=numpy.median(ptList['SCALE_X'])
    dy=numpy.median(ptList['SCALE_Y'])
    dz=numpy.median(ptList['SCALE_Z'])
    dr=numpy.sqrt(dx**2+dy**2+dz**2)
    lacTemp={}
    if type(projectTitle) is type(''): cProjNum=getProjNum(cur,projectTitle)
    else: cProjNum=projectTitle
    cSampleNum=getSampleNum(cur,filename,cProjNum)
    lacTemp['SAMPLE_AIM_Number']=(cSampleNum,)*dbLen
    lacTemp['PROJECT']=(cProjNum,)*dbLen
    lacunIds=[lacId+lacNumOffset for lacId in ptList['LACUNA_NUMBER']]
    lacTemp[tableName+'_NUMBER']=tuple(lacunIds)
    # Variables that scale directly with x,y,z voxel size
    lacTemp['VOX_SIZE']=tuple(numpy.abs(ptList['SCALE_X']*1000))
    scaleVars=['POS','STD','PROJ']
    for cVar in scaleVars:
        for cAx in ['X','Y','Z']:
            lacTemp[cVar+'_'+cAx]=tuple(ptList[cVar+'_'+cAx]*ptList['SCALE_'+cAx]) 
    # This doesnt work since I dont save PCA1,2,3 dumb
    # Variables that scale with PCA 1,2,3 voxel size * denotes PCA1, PCA2, PCA3
    pcaScaleVars=['*_S','PROJ_*']
    for cAx in ['PCA1','PCA2','PCA3']:
        cDr=numpy.sqrt((ptList[cAx+'_X']*dx)**2+(ptList[cAx+'_Y']*dy)**2+(ptList[cAx+'_Z']*dz)**2)
        for cVar in pcaScaleVars:
            rcVar=cAx.join(cVar.split('*'))
            lacTemp[rcVar]=tuple(ptList[rcVar]*cDr)
	# Normal Variables 
    normalVars= ['PCA1_X','PCA1_Y','PCA1_Z','PCA2_X','PCA2_Y','PCA2_Z']
    normalVars+=['MASK_GRAD_X','MASK_GRAD_Y','MASK_GRAD_Z','MASK_ANGLE']
    if CanalMode==0: normalVars+=['Canal_ANGLE','Canal_GRAD_X','Canal_GRAD_Y','Canal_GRAD_Z']
    for cVar in normalVars:
        if ptList.has_key(cVar): lacTemp[cVar]=tuple(ptList[cVar])
        elif ((cVar.find('GRAD')>=0) | (cVar.find('ANGLE'))): lacTemp[cVar]=(-1,)*dbLen
        else: print 'Missing important column:'+cVar+', what the frick!'    
    # Variables that require a radial scaling factor
    radialVars=['MASK_DISTANCE_MEAN','MASK_DISTANCE_STD'] # 'MASK_DISTANCE_COV'
    radialVars+=['OBJ_RADIUS','OBJ_RADIUS_STD']
    if CanalMode==0:
        if ptList.has_key(cVar): radialVars+=['Canal_DISTANCE_MEAN','Canal_DISTANCE_STD']
    for cVar in radialVars:
        if ptList.has_key(cVar): lacTemp[cVar]=tuple(numpy.abs(ptList[cVar]*dr))
    # Variables that require a radial cubed scaling factor
    volVars=['VOLUME','VOLUME_BOX']        
    for cVar in volVars:
        lacTemp[cVar]=tuple(numpy.abs(ptList[cVar]*dx*dy*dz))
    if ptList.has_key('SHELL_CNT'):
        lacTemp['VOLUME_LAYER']=tuple(numpy.abs((ptList['VOLUME']-ptList['SHELL_CNT'])*dx*dy*dz))   
    # GrayAnalysis Columns
    if ptList.has_key('MASK'): # new Lacuna method
        lacTemp['MASK_DISTANCE_MEAN']=tuple(numpy.abs(ptList['MASK']*dr))
        lacTemp['MASK_DISTANCE_STD']=tuple(numpy.abs(ptList['MASK_STD']*dr))        
    if ptList.has_key('MASK_WX'):
        lacTemp['MASK_GRAD']=tuple(ptList['MASK'])
        lacTemp['MASK_DISTANCE_STD']=tuple(ptList['MASK_STD']) 
    if ptList.has_key('SHELL_ABSORPTION'):
        lacTemp['SHELL_ABSORPTION']=tuple(ptList['SHELL_ABSORPTION']) 
    if ptList.has_key('SHELL_ABSORPTION_STD'):
        lacTemp['SHELL_ABSORPTION_STD']=tuple(ptList['SHELL_ABSORPTION_STD'])
    else:
        lacTemp['SHELL_ABSORPTION']=(-1,)*dbLen
        lacTemp['SHELL_ABSORPTION_STD']=(-1,)*dbLen
    # Lining Absorption
    if ptList.has_key('LINING_ABSORPTION'):
        lacTemp['LINING_ABSORPTION']=tuple(ptList['LINING_ABSORPTION']) 
    if ptList.has_key('LINING_ABSORPTION_STD'):
        lacTemp['LINING_ABSORPTION_STD']=tuple(ptList['LINING_ABSORPTION_STD'])
    else:
        lacTemp['LINING_ABSORPTION']=(-1,)*dbLen
        lacTemp['LINING_ABSORPTION_STD']=(-1,)*dbLen   
    if CanalMode==0:
        # This doesnt work since I dont save PCA1,2,3 dumb
        # Variables that scale with PCA 1,2,3 voxel size * denotes PCA1, PCA2, PCA3
        for cAx in ['PCA1','PCA2','PCA3']:
            cDr=numpy.sqrt((ptList[cAx+'_X']*dx)**2+(ptList[cAx+'_Y']*dy)**2+(ptList[cAx+'_Z']*dz)**2)
            rcVar='DENSITY_PROJ_'+cAx
            if ptList.has_key('DENSITY_VOLUME_PROJ_'+cAx):
                lacTemp[rcVar]=tuple(ptList[rcVar]*cDr)
            else:
                lacTemp[rcVar]=(-1,)*dbLen
        if ptList.has_key('Canal_NUMBER'):
            lacTemp['Canal_NUMBER']=tuple(ptList['Canal_NUMBER'])
            #lacTemp['Canal_NAME']=tuple([projectTitle+'_'+filename+'_CAN_'+str(int(curCan)) for curCan in ptList['Canal_NUMBER']])
        if ptList.has_key('Canal_NUMBER_STD'):
            lacTemp['Canal_NUMBER_STD']=tuple(ptList['Canal_NUMBER_STD'])
        else:
            lacTemp['Canal_NUMBER_STD']=(-1,)*dbLen
        # Nearest Neighbors
        lacTemp['NEAREST_NEIGHBOR_DISTANCE']=(-1,)*dbLen
        lacTemp['NEAREST_NEIGHBOR_ANGLE']=(-1,)*dbLen
        
        if ptList.has_key('NEIGHBORS'):
            lacTemp['NEAREST_NEIGHBOR_NEIGHBORS']=tuple(ptList['NEIGHBORS'])
        else:
            lacTemp['NEAREST_NEIGHBOR_NEIGHBORS']=(-1,)*dbLen
        # Mask Params
        lacTemp['POS_RADIUS']=(-1,)*dbLen
        lacTemp['MASK_RADIUS']=(-1,)*dbLen
        lacTemp['MASK_RADIUS_MIN']=(-1,)*dbLen
        lacTemp['MASK_RADIUS_MAX']=(-1,)*dbLen
        lacTemp['MASK_RADIUS_MEAN']=(-1,)*dbLen
        lacTemp['MASK_THETA']=(-1,)*dbLen
    if ptList.has_key('THICKNESS'):
        lacTemp['THICKNESS']=tuple(ptList['THICKNESS'])
    else:
        lacTemp['THICKNESS']=(-1,)*dbLen    
    if ptList.has_key('THICKNESS_STD'):
        lacTemp['THICKNESS_STD']=tuple(ptList['THICKNESS_STD'])
    else:
        lacTemp['THICKNESS_STD']=(-1,)*dbLen   
    # Lacuna Density / Volume
    if ptList.has_key('DENSITY_VOLUME'):
        lacTemp['DENSITY_VOLUME']=tuple(numpy.abs(ptList['DENSITY_VOLUME']*dx*dy*dz))    
        lacTemp['DENSITY']=tuple(numpy.abs(1/(ptList['DENSITY_VOLUME']*dx*dy*dz)))
    elif ptList.has_key('DENSITY_VOLUME_CNT'):
        lacTemp['DENSITY_VOLUME']=tuple(numpy.abs(ptList['DENSITY_VOLUME_CNT']*dx*dy*dz))    
        lacTemp['DENSITY']=tuple(numpy.abs(1/(ptList['DENSITY_VOLUME_CNT']*dx*dy*dz)))
    else:
        lacTemp['DENSITY_VOLUME']=(-1,)*dbLen
        lacTemp['DENSITY']=(-1,)*dbLen
    if CanalMode==0:
        # Lacuna Territory Shape
        lacTemp['DISPLACEMENT_MEAN']=(-1,)*dbLen
        if ptList.has_key('NEIGHBOR_AREA'):
            lacTemp['DENSITY_VOLUME_SHELL']=tuple(numpy.abs(ptList['NEIGHBOR_AREA']*dx*dy))
        elif ptList.has_key('MASK_VOLUME_SHELL_CNT'):
            ## Old Definition of Shell
            lacTemp['DENSITY_VOLUME_SHELL']=tuple(numpy.abs(ptList['MASK_VOLUME_SHELL_CNT']*dx*dy*dz))    
        else:
            lacTemp['DENSITY_VOLUME_SHELL']=(-1,)*dbLen
        # Lacuna Territory that is mineralized    
        if ptList.has_key('BONE_VOLUME_CNT'):
            lacTemp['DENSITY_VOLUME_BONE']=tuple(numpy.abs(ptList['BONE_VOLUME_CNT']*dx*dy*dz))    
        else:
            lacTemp['DENSITY_VOLUME_BONE']=(-1,)*dbLen         
        # Lacuna Territory that is part of the mask (for porosity calculations)
        if ptList.has_key('MASK_VOLUME_CNT'):
            lacTemp['DENSITY_VOLUME_MASK']=tuple(numpy.abs(ptList['MASK_VOLUME_CNT']*dx*dy*dz))    
        else:
            lacTemp['DENSITY_VOLUME_MASK']=(-1,)*dbLen
        # PCA1 is a makeshift holding place for STD until the table is once again updated
        terrShapeMap={'DENSITY_VOLUME_C':'DENSITY_','DENSITY_VOLUME_S':'DENSITY_STD_'}
        for cKey in terrShapeMap.keys():
            missingKeys=False
            for cAx in ['X','Y','Z']:
                #print cKey+cAx
                if ptList.has_key(cKey+cAx):
                    #print 'isch da'
                    lacTemp[terrShapeMap[cKey]+cAx]=tuple(ptList[cKey+cAx]*ptList['SCALE_'+cAx])
                else:
                    if cKey=='DENSITY_VOLUME_C': missingKeys=True
                    else:
                        lacTemp[terrShapeMap[cKey]+cAx]=(-1,)*dbLen
            if not missingKeys:
                if cKey=='DENSITY_VOLUME_C':
                    dispMean=numpy.sqrt(((ptList[cKey+'X']-ptList['POS_X'])*dx)**2+((ptList[cKey+'Y']-ptList['POS_Y'])*dy)**2+((ptList[cKey+'Z']-ptList['POS_Z'])*dz)**2)
                    lacTemp['DISPLACEMENT_MEAN']=tuple(dispMean)
                    lacTemp['DISPLACEMENT_X']=tuple((ptList[cKey+'X']-ptList['POS_X'])*dx)
                    lacTemp['DISPLACEMENT_Y']=tuple((ptList[cKey+'Y']-ptList['POS_Y'])*dy)
                    lacTemp['DISPLACEMENT_Z']=tuple((ptList[cKey+'Z']-ptList['POS_Z'])*dz)
    # Polar Coordinates Hints
    # Only really valid for Full Femur, but Lacuna angle can be useful
    mR=numpy.sqrt(((ptList['POS_X']-numpy.mean(ptList['POS_X']))*dx)**2+((ptList['POS_Y']-numpy.mean(ptList['POS_Y']))*dy)**2)
    for cPCA in [1,2]:
        pR=numpy.sqrt(ptList['PCA'+str(cPCA)+'_X']**2+ptList['PCA'+str(cPCA)+'_Y']**2)
        pPhi=180/numpy.pi*numpy.arctan2(ptList['PCA'+str(cPCA)+'_Z'],pR)
        lacTemp['PCA'+str(cPCA)+'_Phi']= tuple(pPhi)
        lacTemp['PCA'+str(cPCA)+'_Theta']=tuple(180/numpy.pi*numpy.arccos(ptList['PCA'+str(cPCA)+'_X']/pR)) # update
    # Junk Angles
    lacTemp['POS_THETA']=(-1,)*dbLen
    lacTemp['MASK_THETA']=(-1,)*dbLen
    lacTemp['POS_DISTANCE']=(-1,)*dbLen
    lacTemp['NEAREST_NEIGHBOR_AVG']=(-1,)*dbLen
    lacTemp['NEAREST_NEIGHBOR_DISTANCE']=(-1,)*dbLen
    lacTemp['NEAREST_NEIGHBOR_DISTANCE']=(-1,)*dbLen
    # Normalize PCA
    pcastot=dr*numpy.sqrt(ptList['PCA1_S']**2+ptList['PCA2_S']**2+ptList['PCA3_S']**2)
    #lacTemp['PCAS_TOTAL']=tuple(pcastot)
    #for tz in lacTemp.keys(): print tz+' '+str(len(lacTemp[tz]))
    outKeys=lacTemp.keys()
    outArr=[lacTemp[cKey] for cKey in outKeys]
    #for cKey in outKeys: print (cKey,len(lacTemp[cKey]))
    outMat=numpy.array(outArr).swapaxes(1,0)
    invalidRows=numpy.sum(numpy.isnan(outMat),1)
    outMat=outMat[numpy.nonzero(invalidRows==0)[0],:]
    globals()['Om']=outMat
    outMat=[tuple(obj) for obj in outMat]
    return None
    return addRowsToTable(cur,tableName,outMat,entry_order=outKeys)
    print filename+' was successfully entered %05d, invalid  %03d' % (lacNumOffset,sum(invalidRows))
class CaseFreeDict:
    """Dictionary, that has case-insensitive keys.
    
    Keys are retained in their original form
    when queried with .keys() or .items().

    Implementation: An internal dictionary maps lowercase
    keys to (key,value) pairs. All key lookups are done
    against the lowercase keys, but all methods that expose
    keys to the user retrieve the original keys."""
    
    def __init__(self, dict=None):
        """Create an empty dictionary, or update from 'dict'."""
        self._dict = {}
        if dict:
            self.update(dict)

    def __getitem__(self, key):
        """Retrieve the value associated with 'key' (in any case)."""
        k = key.lower()
        return self._dict[k][1]

    def __setitem__(self, key, value):
        """Associate 'value' with 'key'. If 'key' already exists, but
        in different case, it will be replaced."""
        k = key.lower()
        self._dict[k] = (key, value)

    def has_key(self, key):
        """Case insensitive test wether 'key' exists."""
        k = key.lower()
        return self._dict.has_key(k)

    def keys(self):
        """List of keys in their original case."""
        return [v[0] for v in self._dict.values()]

    def values(self):
        """List of values."""
        return [v[1] for v in self._dict.values()]

    def items(self):
        """List of (key,value) pairs."""
        return self._dict.values()

    def get(self, key, default=None):
        """Retrieve value associated with 'key' or return default value
        if 'key' doesn't exist."""
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key, default):
        """If 'key' doesn't exists, associate it with the 'default' value.
        Return value associated with 'key'."""
        if not self.has_key(key):
            self[key] = default
        return self[key]

    def update(self, dict):
        """Copy (key,value) pairs from 'dict'."""
        for k,v in dict.items():
            self[k] = v

    def __repr__(self):
        """String representation of the dictionary."""
        items = ", ".join([("%r: %r" % (k,v)) for k,v in self.items()])
        return "{%s}" % items

    def __str__(self):
        """String representation of the dictionary."""
        return repr(self)