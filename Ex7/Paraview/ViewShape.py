from optparse import OptionParser
import os,sys,inspect
scriptFullPath=os.path.abspath(inspect.getfile(inspect.currentframe()))
scriptFullDir=os.path.dirname(scriptFullPath)
print scriptFullPath+' is running in directory:'+scriptFullDir
opTool=OptionParser()
opTool.add_option('-p','--pvpath',dest='pvpath',help='The path to the paraview tools script')
opTool.add_option('-c','--csvfile',dest='csvfile',help='The path of the csv file to load')
opTool.add_option('-i','--imagefile',dest='imfile',help='The path of the rendered image to save')
opTool.add_option('-s','--statefile',dest='statefile',help='The path of the state-file to save')
opTool.add_option('-t','--hastwoheader',dest='hoh',default=True,action='store_false',help='Does the file have two header lines')
opTool.add_option('','--tab',dest='csv',default=True,action='store_false',help='Use tab delimited files instead of comma')
opTool.add_option('-x','--xcolname',dest='xColName',help='The name of the x position column')
opTool.add_option('-y','--ycolname',dest='yColName',help='The name of the y position column')
opTool.add_option('-z','--zcolname',dest='zColName',help='The name of the z position column')
opTool.set_description('Creates a paraview dataset from a given CSV file')
opTool.set_defaults(pvpath=scriptFullDir,xColName='POS_X',yColName='POS_Y',zColName='POS_Z',imfile='viewshape.png')
# parse and load the arguments
(opt,args)=opTool.parse_args()
outputImageName=opt.imfile
outputStateName=opt.statefile
pvtoolsPath=opt.pvpath
csvPath=opt.csvfile
hasOnlyOneHeader=str(opt.hoh)
xColName=opt.xColName
yColName=opt.yColName
zColName=opt.zColName
if not opt.csv: csvdelim="False"
else: csvdelim="True"


# start paraview

try: paraview.simple
except: from paraview.simple import *
from paraview import servermanager as sm
paraview.simple._DisableFirstRenderCameraReset()

ProgrammableSource1 = ProgrammableSource()

RenderView1 = GetRenderView()

ProgrammableSource1.OutputDataSetType = 'vtkTable'
ProgrammableSource1.PythonPath = ''
ProgrammableSource1.ScriptRequestInformation = ''
ProgrammableSource1.Script = "import os,sys\naPath='"+pvtoolsPath+"'\nif aPath not in sys.path: sys.path.append(aPath)\nimport pvtools as pvtools\nfilterList=[]\n#filterList+=[('MASK_DISTANCE_MEAN',lambda x: x>0)]\n#filterList+=[('VOLUME',lambda x: x<4000)]\nsynList=[]\n#synList+=[('Alignment',lambda x: 180/numpy.pi*pvtools.calcAlignment(x,'DIR_X','DIR_Y','DIR_Z'))]\n#synList+=[('Anisotropy',lambda x: pvtools.calcAnisotropy(x,'PCA1_S','PCA2_S','PCA3_S'))]\nimport numpy\ncFile='"+csvPath+"'\npvtools.ImportCSV(self,cFile,filterList,synList,fromR="+hasOnlyOneHeader+",csvdelim="+csvdelim+")\n"
AnimationScene1 = GetAnimationScene()
AnimationScene1.ViewModules = []

Delete(RenderView1)
SpreadSheetView1 = CreateView( "SpreadSheetView" )

AnimationScene1.ViewModules = SpreadSheetView1



RenameSource("Load Shape Analysis", ProgrammableSource1)
LoadShapeAnalysis = ProgrammableSource1
del ProgrammableSource1

TableToPoints1 = TableToPoints()

TableToPoints1.XColumn = 'PCA1_Z'
TableToPoints1.ZColumn = 'PCA1_Z'
TableToPoints1.YColumn = 'PCA1_Z'

# Set the columns correctly so points can be visualized
TableToPoints1.XColumn = xColName
TableToPoints1.ZColumn = yColName
TableToPoints1.YColumn = zColName


RenameSource("To Points", TableToPoints1)
ToPoints = TableToPoints1
del TableToPoints1
Glyph1 = Glyph( GlyphType="Arrow", GlyphTransform="Transform2" )

Glyph1.Scalars = ['POINTS', 'Anisotropy']
Glyph1.SetScaleFactor = 97.025130224227908
Glyph1.Vectors = ['POINTS', 'MASK_GRAD']
Glyph1.GlyphTransform = "Transform2"
Glyph1.GlyphType = "Arrow"

Glyph1.SetScaleFactor = 97.025126417927396
Glyph1.Vectors = ['POINTS', 'PCA1']

DataRepresentation3 = Show()


RenderView2 = CreateRenderView()
RenderView2.CompressorConfig = 'vtkSquirtCompressor 0 3'
RenderView2.UseLight = 1
RenderView2.CameraPosition = [-2.4390328368769287, 0.10220142036508373, 6.6816073198010404]
RenderView2.LightSwitch = 0
RenderView2.CameraClippingRange = [4.4624027214322766, 10.468053324286563]
RenderView2.CameraViewUp = [0.00012411430305431584, 0.99988372184732821, -0.015248848493401374]
RenderView2.Background = [0.31999694819562063, 0.34000152590218968, 0.42999923704890519]
RenderView2.CameraParallelScale = 1.848717442275589

AnimationScene1.ViewModules = [ SpreadSheetView1, RenderView2 ]

DataRepresentation4 = Show()
DataRepresentation4.ScaleFactor = 108.14910964965821
DataRepresentation4.SelectionPointFieldDataArrayName = 'Anisotropy'
DataRepresentation4.EdgeColor = [0.0, 0.0, 0.50000762951094835]

a1_Anisotropy_PVLookupTable = GetLookupTableForArray( "Anisotropy", 1, RGBPoints=[2.728503942489624, 0.23000000000000001, 0.29899999999999999, 0.754, 34.332071185112, 0.86499999999999999, 0.86499999999999999, 0.86499999999999999, 65.935638427734375, 0.70599999999999996, 0.016, 0.14999999999999999], VectorMode='Magnitude', NanColor=[0.25, 0.0, 0.0], ColorSpace='Diverging', ScalarRangeInitialized=1.0 )

a1_Anisotropy_PiecewiseFunction = CreatePiecewiseFunction( Points=[2.728503942489624, 0.0, 0.5, 0.0, 65.935638427734375, 1.0, 0.5, 0.0] )

DataRepresentation4.ColorArrayName = ('POINT_DATA', 'THICKNESS')

RenderView2.CameraViewUp = [-0.51993293227740078, 0.38433446627998352, -0.76286090734989442]
RenderView2.CameraPosition = [2298.3755267380275, -345.95007779394399, -1426.4492404529071]
RenderView2.CameraClippingRange = [1175.1576924833901, 4232.2804652982086]
RenderView2.CameraFocalPoint = [497.38994979858444, 403.08729743957525, 178.39455223083485]
RenderView2.CameraParallelScale = 794.29468863596412
RenderView2.CenterOfRotation = [497.38994979858398, 403.0872974395752, 178.39455223083496]

a1_NEIGHBORS_PVLookupTable = GetLookupTableForArray( "NEIGHBORS", 1, RGBPoints=[0.0, 0.23000000000000001, 0.29899999999999999, 0.754, 16.5, 0.86499999999999999, 0.86499999999999999, 0.86499999999999999, 33.0, 0.70599999999999996, 0.016, 0.14999999999999999], VectorMode='Magnitude', NanColor=[0.25, 0.0, 0.0], ColorSpace='Diverging', ScalarRangeInitialized=1.0 )

a1_NEIGHBORS_PiecewiseFunction = CreatePiecewiseFunction( Points=[0.0, 0.0, 0.5, 0.0, 33.0, 1.0, 0.5, 0.0] )

a1_THICKNESS_PVLookupTable = GetLookupTableForArray( "THICKNESS", 1, RGBPoints=[0.73925554752349854, 0.23000000000000001, 0.29899999999999999, 0.754, 2.0352964997291565, 0.86499999999999999, 0.86499999999999999, 0.86499999999999999, 3.3313374519348145, 0.70599999999999996, 0.016, 0.14999999999999999], VectorMode='Magnitude', NanColor=[0.25, 0.0, 0.0], ColorSpace='Diverging', ScalarRangeInitialized=1.0 )

a1_THICKNESS_PiecewiseFunction = CreatePiecewiseFunction( Points=[0.73925554752349854, 0.0, 0.5, 0.0, 3.3313374519348145, 1.0, 0.5, 0.0] )

Glyph1.Scalars = ['POINTS', 'PCA1_S']
Glyph1.SetScaleFactor = 1.77245266628994
Glyph1.ScaleMode = 'scalar'

a1_Anisotropy_PVLookupTable.ScalarOpacityFunction = a1_Anisotropy_PiecewiseFunction

DataRepresentation4.LookupTable = a1_THICKNESS_PVLookupTable

a1_NEIGHBORS_PVLookupTable.ScalarOpacityFunction = a1_NEIGHBORS_PiecewiseFunction

a1_THICKNESS_PVLookupTable.ScalarOpacityFunction = a1_THICKNESS_PiecewiseFunction

Glyph1.GlyphType = "Sphere"

RenderView2.CameraViewUp = [0.70245334438796803, 0.49646391511954041, -0.5099832153535413]
RenderView2.CameraFocalPoint = [497.38994979858415, 403.08729743957571, 178.39455223083505]
RenderView2.CameraClippingRange = [1521.8072855436326, 3778.1925641411135]
RenderView2.CameraPosition = [-606.23366850569721, -265.84044756719146, -1992.9368867340388]

Render()
WriteImage(outputImageName)
if outputStateName is not None: sm.SaveState(outputStateName)
