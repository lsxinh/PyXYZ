### Chapter 4_Shared functions ###
import subprocess
import os
import glob
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
import shlex
import pandas as pd # Reading csv file 
import requests
import os
import glob
import zipfile
import geopandas as gpd # To create GeodataFrame
from shapely.geometry import Point

###############################################################################
def newFolderF(containFolder,newFolder='newFolder'):
    '''
    create new folder
    containFolder: the location of new created foler
    newFolder: new folder name
    Step 1: change dir to containFolder
    Step 2: check if the new folder is existed or not
    Step 3: if not make new folder using os.mkdir
    return the function result to new path.
    '''
    os.chdir(containFolder)
    if os.path.exists(containFolder+"\\"+newFolder): #if newFolder exists
        next
        #print ("Already exists:",containFolder+"\\"+newFolder)
    else:
        os.mkdir(newFolder)
    return containFolder+"\\"+newFolder #return the abspath
##############################################################################################
#a quick python function to view a dem
def ras_qview_gdal(inRas):
    'quick view using gdal - not esthetic'
    ds = gdal.Open(inRas)
    array = ds.GetRasterBand(1).ReadAsArray()
    plt.imshow(array)
    plt.colorbar()
    plt.show()

# ras_qview_gdal(r"D:\Dropbox\write\c4_improve_hUn\data\Qimera\Gtiff\HillShade\S1_RTK_Tide_0.5m_Average_HS_GDAL_MD.tif")

def ras_view_gdal(inRas,Rastitle='Title',
                  RasCmap = 'jet',cb_title='Bathymetry [meter]',grid='on'):
    """view using gdal - better
    done: 
        1. plot data with a good view
        2. cmap='bwr' is good for surface difference
    
    2do: 1. Set the view limit like in chapter 2 for scatter plot of point clound data
    """
    
    # ax = plt.axes()
    fig, ax = plt.subplots(figsize = (10,10))
    ds       = gdal.Open(inRas) #dataset
    ras_band = ds.GetRasterBand(1) #getband
    array    = ras_band.ReadAsArray() #read as np array
    noDatavl = ras_band.GetNoDataValue() #get no data value
    array[array==noDatavl] = np.nan #asign noDatavalues to numpy nan
    print('Max{:.3f}, Min{:.3f}: '.format(np.nanmax(array),np.nanmin(array))) #print out max/min
    #get raster extent
    gt = ds.GetGeoTransform() #geo transform info
    rasterExtent = [gt[0], gt[0] + array.shape[1] * gt[1], 
                    gt[3] + array.shape[0] * gt[5], gt[3]]
    #show the plot
    img = plt.imshow(array,origin='upper',extent=rasterExtent,cmap=RasCmap)
    # ax.set_aspect('equal')
    ax.set_aspect('auto')
    # ax.set_aspect('0.5')
    plt.title(Rastitle)
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    cb = plt.colorbar(img,fraction=0.035) #plot correct color map scale
    cb.set_label(cb_title)
    # gridSize = 20
    # to set the distance between labels (x axis)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(gridSize )) 
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(gridSize ))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    x_tik_r,y_tik_r,tick_s = 0,90,8
    plt.xticks(rotation=x_tik_r,fontsize=tick_s)
    plt.yticks(rotation=y_tik_r,fontsize=tick_s)
    if grid == 'on': plt.grid(grid)
    elif grid == 'off': pass
    plt.show()

# ras_view_gdal(r"D:\Dropbox\write\c4_improve_hUn\data\Qimera\Gtiff\S1_RTK_Tide_0.5m_CUBE.tif",Rastitle='Title',
#                   RasCmap = 'jet',cb_title='Bathymetry [meter]',grid='on')

############################################################################
def clip_bySHPbox_GDAL(inSHP,inRaster,outRaster):
    gdalwarp_File = "C:/OSGeo4W64/bin/gdalwarp.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdalwarp.exe"
    # gdalwarp_File = "gdalwarp"
    print('Running:{gdalwarp_File} ' )
    subprocess.call([gdalwarp_File,'-dstnodata','-9999',
                     '-r','bilinear',
                     '-cutline',inSHP,'-crop_to_cutline',inRaster,outRaster])
##############################################################################
def DEM2HILLSHADE_GDAL_SD(inRaster,outRaster):
    '''
    Hillshade settings:
    gdaldem hillshade inRaster outRaster
            [-z ZFactor (default=1)] [-s scale* (default=1)]
            [-az Azimuth (default=315)] [-alt Altitude (default=45)]
            [-alg ZevenbergenThorne] [-combined | -multidirectional | -igor]
            [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
    '''
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdalwarp_File = "gdaldem"
    print('Running:{gdaldem_File} ' )
    subprocess.call([gdaldem_File,'hillshade',inRaster,outRaster,'-z','2','-of','GTiff','-az','315','-alt','45'])
##############################################################################
def DEM2HILLSHADE_GDAL_SD4(inRaster,outRaster):
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    print('Running:{gdaldem_File} ' )
    msg = [gdaldem_File,'hillshade',inRaster,outRaster,'-z','2','-of','GTiff','-az','315','-alt','45']
    subprocess.call(msg)

# inRaster=r"D:\Dropbox\write\c4_improve_hUn\data\Qimera\Gtiff\S1_RTK_Tide_0.5m_Average.tif"
# outRaster=r"D:\Dropbox\write\c4_improve_hUn\data\Qimera\Gtiff\S1_RTK_Tide_0.5m_Average_t1.tif"
# DEM2HILLSHADE_GDAL_SD(inRaster,outRaster)
##############################################################################
def DEM2HILLSHADE_GDAL_SD2(inRaster,outRaster):
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdaldem_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdaldem_File = "gdaldem" #this gdal may not working
    msg = f'{gdaldem_File} hillshade {inRaster} {outRaster} -z 2 -of GTiff -az 315 -alt 45'
    # subprocess.call(msg.split())
    os.system(msg)
##############################################################################
def DEM2HILLSHADE_GDAL_SD3(inRaster,outRaster):
    # os.chdir(os.path.dirname(inRaster))
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdaldem_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdaldem_File = "gdaldem" #this gdal may not working
    msg = f'{gdaldem_File} hillshade {inRaster} {outRaster} -z 2 -of GTiff -az 315 -alt 45'
    subprocess.call(msg.split())

##############################################################################
def DEM2HILLSHADE_GDAL_MD(inRaster,outRaster):
    '''
    Hillshade settings:
    gdaldem hillshade inRaster outRaster
            [-z ZFactor (default=1)] [-s scale* (default=1)]
            [-az Azimuth (default=315)] [-alt Altitude (default=45)]
            [-alg ZevenbergenThorne] [-combined | -multidirectional | -igor]
            [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
    '''
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdalwarp_File = "gdaldem"
    print('Running:{gdaldem_File} ' )
    subprocess.call([gdaldem_File,'hillshade',inRaster,outRaster,'-z','2','-of','GTiff','-alt','45','-multidirectional'])

##############################################################################
def DEM2HILLSHADE_GDAL_MD2(inRaster,outRaster):
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdaldem_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdaldem_File = "gdaldem" #this gdal may not working
    msg = f'{gdaldem_File} hillshade {inRaster} {outRaster} -z 2 -of GTiff -alt 45 -multidirectional'
    # subprocess.call(msg.split())
    os.system(msg)

##############################################################################
def DEM2HILLSHADE_GDAL_MD3(inRaster,outRaster):
    # os.chdir(os.path.dirname(inRaster))
    gdaldem_File = "C:/OSGeo4W64/bin/gdaldem.exe"
    # gdaldem_File = "C:/Program Files/GDAL/gdaldem.exe"
    # gdaldem_File = "gdaldem" #this gdal may not working
    msg = f'{gdaldem_File} hillshade {inRaster} {outRaster} -z 2 -of GTiff -alt 45 -multidirectional'
    subprocess.call(msg.split())

###############################################################################
def gdalEdit_a_srs(inFile,outEPSG='EPSG:28350'):
    gdalEditFile = 'C:\Program Files\GDAL\gdal_edit.py'
    subprocess.call(['python', gdalEditFile, '-a_srs', outEPSG, inFile])

###############################################################################
def gdalEdit_a_srs2(inFile,outEPSG='EPSG:28350'):
    gdalEditFile = 'C:\Program Files\GDAL\gdal_edit.py'
    msg = f'python {gdalEditFile} -a_srs {outEPSG} {inFile}'
    subprocess.call(msg.split())
###############################################################################
def gdalEdit_a_srs3(inFile,outEPSG='EPSG:28350'):
    gdalEditFile = 'C:\Program Files\GDAL\gdal_edit.py'
    msg = f'python {gdalEditFile} -a_srs {outEPSG} {inFile}'
    os.system(msg)
###############################################################################
def XYZ2SHP(xyz_in_path):
    '''
    input xyz
    output shp file in SHP folder
    '''
    xyz_dirname = os.path.dirname(xyz_in_path)
    os.chdir(xyz_dirname)
    
    #31: add headers to the file 'X' 'Y' 'Z'
    infile = open(xyz_in_path)
    inLines = infile.read()
    infile.close()
    outLines = 'X Y Z\n'+inLines
    outLines = outLines.replace(' ',",")
    outfile_location = xyz_in_path[:-4]+'_ENZ.csv'
    outfile = open(outfile_location,'w')
    outfile.write(outLines)
    outfile.close()
    
    #Create geopandas dataframe
    inXYZdf = pd.read_csv(outfile_location)
    geometry = [Point(lonlat) for lonlat in zip(inXYZdf['X'],inXYZdf['Y'])]
    crs = {'init': 'epsg:28350'}
    geopdf = gpd.GeoDataFrame(inXYZdf,crs=crs,geometry=geometry)
    
    # Plot the map
    geopdf.plot(marker='o', figsize = (6,6),color='g', markersize=5);

    #70 Create a new export folder
    try:
        os.mkdir('SHP')
        os.mkdir('csv')
    except:
        pass
    #71: write to SHP file
    try:
        geopdf.to_file(os.path.join(xyz_dirname,'SHP',os.path.basename(outfile_location)[:-4]+'.shp'))
    except:
        pass
###############################################################################
def getimage_full_info(filename, prefix=""):
	'''get the image full metadata'''
	x = 0
	y = 0
#	odir = newFolderF(os.path.dirname(filename),'Log')
	odir = newFolderF(r'C:\Users\Public','getimage_full_info_log')
	if not os.path.isdir(odir):
		os.makedirs(odir)

	outfilename = os.path.join(odir, prefix + os.path.basename(filename) +'_full_info.txt')
	f = open(outfilename, 'w')
	#subprocess.call(["gdalinfo.exe ", filename], stdout=f)

	#filename = os.path.join(odir, prefix + "gdainfo.stdout.txt")
	#f = open(filename, 'w')

	cmd = "C:/Program Files/GDAL/gdalinfo.exe" + \
		" %s" % (os.path.abspath(filename).replace('\\','/'))
	args = shlex.split(cmd)			

	proc = subprocess.Popen(args, stdout=f, stderr=subprocess.PIPE)	
	proc.wait()

	'''now extract the position informaiton '''
	# Upper Left  (  388264.000, 7514457.000) 
	# Lower Left  (  388264.000, 7514013.400) 
	# Upper Right (  388553.100, 7514457.000) 
	# Lower Right (  388553.100, 7514013.400) 
	# Center      (  388408.550, 7514235.200) 

	p1 = POINT(0,0)
	p2 = POINT(1,1)
	rectangle = RECT(p1, p2)
	top = rectangle.top
	bottom = rectangle.bottom
	left = rectangle.left
	right = rectangle.right
	origin = [0.0000,0.0000]
	center = [0.0000,0.0000]
	pixel_size = [0.0000,0.0000]
	PROJCRS = 'Projection info_not working'
	Proj_ID = 'Proj_ID_not working'
	band1_max = -0.0000
	band1_mean = 0.0000
	band1_min = 0.0000
	band1_std = 0.0000
	noData_V = 'not available'
	gdal_img_object = gdal_img(top, bottom, left, right, center, origin, pixel_size, PROJCRS, Proj_ID, band1_max, band1_mean, band1_min, band1_std, noData_V)

	f = open(outfilename, 'r')
	args_list = list()
	for i,line in enumerate(f):
		#Center      (  389210.865, 7513758.918) 
		if line.startswith('Lower Left'):
			line = line.replace("(", "")
			line = line.replace(")", "")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("\n", "")
			line = line.replace(",", "")
			words = line.split(" ")
			x = float(words[2])
			y = float(words[3])
			ll = POINT(x,y)
			
		if line.startswith('Upper Right'):
			line = line.replace("(", "")
			line = line.replace(")", "")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("\n", "")
			line = line.replace(",", "")
			words = line.split(" ")
			x = float(words[2])
			y = float(words[3])
			ur = POINT(x,y)
			rectangle = RECT(ll, ur)
			top = rectangle.top
			bottom = rectangle.bottom
			left = rectangle.left
			right = rectangle.right
			
		if line.startswith('Center'):
			line = line.replace("(", "")
			line = line.replace(")", "")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("\n", "")
			line = line.replace(",", "")
			words = line.split(" ")
			x = float(words[1])
			y = float(words[2])
#			center = POINT(x,y)
			center = (x,y)
			
		if line.startswith('Origin'):
			line = line.replace('Origin = (','')
			line = line.replace(')','')
			line = line.replace("\n", "")
			words = line.split(",")
			x_ori = float(words[0])
			y_ori = float(words[1])
			# origin = POINT(x_ori,y_ori)
			origin = (x_ori,y_ori)
			
		if line.startswith('Pixel Size'):  
			line = line.replace('Pixel Size = (','')  
			line = line.replace(')','')
			line = line.replace("\n", "")
			words = line.split(",")
			pixel_size = (float(words[0]),float(words[1]))
			
		if i < 10 and 'PROJCRS' in line:
#		if 'PROJCRS' in line:
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace('PROJCRS["', "")
			line = line.replace('",', "")
			line = line.replace("\n", "")
			PROJCRS = line
			
		if i < 44 and 'ID["EPSG",' in line:
#		if 'ID["EPSG",' in line:	 
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' ID["EPSG",', 'EPSG:')
			line = line.replace(']','')
			line = line.replace(']','')
			line = line.replace(']','')
			line = line.replace(',','')
			line = line.replace(',','')
			line = line.replace("\n", "")
			Proj_ID = line
			
		if line.startswith('    STATISTICS_MAXIMUM='):  
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' STATISTICS_MAXIMUM=','')
			line = line.replace("\n", "")
			band1_max = float(line)
			
		if line.startswith('    STATISTICS_MEAN='): 
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' STATISTICS_MEAN=','')
			line = line.replace("\n", "")
			band1_mean = float(line)
			
		if line.startswith('    STATISTICS_MINIMUM='): 
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' STATISTICS_MINIMUM=','')
			line = line.replace("\n", "")
			band1_min = float(line)
			
		if line.startswith('    STATISTICS_STDDEV='): 
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' STATISTICS_STDDEV=','')
			line = line.replace("\n", "")
			band1_std = float(line)
			
		if line.startswith('NoData Value'): 
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace("  ", " ")
			line = line.replace(' NoData Value=','')
			line = line.replace("\n", "")
			noData_V = str(line)

	gdal_img_object = gdal_img(top, bottom, left, right, center, origin, pixel_size, PROJCRS, Proj_ID, band1_max, band1_mean, band1_min, band1_std, noData_V)
	return gdal_img_object
###############################################################################
def check_crs_img_file(filename):
	image_full_info = getimage_full_info(filename, prefix="")
	if 'GDA94' in image_full_info.PROJCRS and 'MGA zone 50' in image_full_info.PROJCRS:
		return True
	elif 'GDA94' not in image_full_info.PROJCRS and 'MGA zone 50' not in image_full_info.PROJCRS:
		return False

##############################################################################
# Define a python function to clip a raster file using gdalwarp
def clip_bySHP_GDAL(inSHP,inRaster,outRaster):
    gdalwarp_File = "C:/OSGeo4W64/bin/gdalwarp.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdalwarp.exe"
    # gdalwarp_File = "gdalwarp"
    print('Running:{gdalwarp_File} ' )
    subprocess.call([gdalwarp_File,'-dstnodata','-9999',
                     '-r','bilinear',
                     '-cutline',inSHP,inRaster,outRaster])
#tested 20201109: gdal from osgeo qgis is working, the 2 others did not.

#clip by box using nodata destination -9999
def clip_byBox_GDAL(x_min,y_min,x_max,y_max,inRas,outRas):
    gdalwarp_File = "C:/OSGeo4W64/bin/gdalwarp.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdalwarp.exe"
    # gdalwarp_File = "gdalwarp"
    print('Running:{}'.format(gdalwarp_File))
    subprocess.call([gdalwarp_File,'-dstnodata','-9999',
                     '-te',str(x_min),str(y_min),str(x_max),str(y_max),
                     inRas,outRas])
# x_min,y_min,x_max,y_max = originX,originY,finalX,finalY
# inRas = line2_RTK_RTK
# outRas = inRas[:-4]+'CropToLine1_'+'.tif'
# clip_byBox_GDAL(x_min,y_min,x_max,y_max,inRas,outRas)
##############################################################################
def raster_coShape_GDAL_v1(inRasBase,inRasDest,outRasDest):
    '''
    get boundaries of inRasBase and crop the inRasDest to outRasDest
    question: can inRasDest be the same as outRasDest?
    funny: using both GDAL python API and GDAL command line through subprocess
    2do: using all python gdal api instead of subprocess
    '''
    #Open raster bands
    inRasBase_band = gdal.Open(inRasBase)
    #GDAl raster data to numpy array
    inRasBase_data = inRasBase_band.GetRasterBand(1).ReadAsArray().astype(np.float32)
    #get inRasBase boundaries based on geotransform
    geotransform = inRasBase_band.GetGeoTransform()
    originX,pixelWidth,empty,finalY,empty2,pixelHeight=geotransform
    cols =  inRasBase_band.RasterXSize
    rows =  inRasBase_band.RasterYSize
    projection = inRasBase_band.GetProjection()
    finalX = originX + pixelWidth * cols
    originY = finalY + pixelHeight * rows
    gdalwarp_File = "C:/OSGeo4W64/bin/gdalwarp.exe"
    # gdalwarp_File = "C:/Program Files/GDAL/gdalwarp.exe"
    # gdalwarp_File = "gdalwarp"
    print('Running:{}'.format(gdalwarp_File))
    subprocess.call([gdalwarp_File,'-dstnodata','-9999',
                     '-te',str(originX),str(originY),str(finalX),str(finalY),
                     inRasDest,outRasDest])

# inRasBase = '201911_Line1_1m_CUBE_PPK_PPK_clipped_GDAL_.tif'
# inRasDest = '201911_Line2_1m_CUBE_PPK_PPK_clipped_GDAL_.tif'
# outRasDest = '201911_Line2_1m_CUBE_PPK_PPK_clipped_GDAL_raster_coShape.tif'
# raster_coShape_GDAL_v1(inRasBase,inRasDest,outRasDest)
#################################################################################
#Define a function to list all Geotiff files in a folder
def nameList_F_withExt(InputFolder,filterString="*"):
    '''
    pathList_F_ext(InputFolder,filterString="*")
    list all files and folders in InputFolder
    return a list of names for every file and folder matching folderString
    file includes extention (ext) information
    '''
    os.chdir(InputFolder) #change working folder
    return glob.glob(filterString)

def pathList_F_ext(InputFolder,filterString="*"):
    """
    pathList_F_ext(InputFolder,filterString="*")
    list all files and folders in InputFolder
    return a list of paths for every file and folder matching folderString
    file includes extention (ext) information
    """
    import glob
    os.chdir(InputFolder) #change working folder
    baseName_FolderList = glob.glob(filterString) #list all the folder list in InputFolder
    pathList = []
    for folder in baseName_FolderList:
        pathList.append(os.path.abspath(folder))
    return pathList

#asign crs
def gdalEdit_a_srs(inFile,outEPSG='EPSG:28350'):
    gdalEditFile = 'C:/Program Files/GDAL/gdal_edit.py'
    gdalEditFile = "C:/Miniconda3/envs/codegis37/Scripts/gdal_edit.py"
    gdalEditFile = "C:/Users/lsxin/AppData/Local/ESRI/conda/envs/arcgispro-py3-clone/Lib/site-packages/osgeo/scripts/gdal_edit.py"
    gdalEditFile = "C:/OSGeo4W64/apps/Python37/Scripts/gdal_edit.py"
    #inFile_sub = os.path.abspath(inFile).replace('\\','/')
    subprocess.call(['python', gdalEditFile, 
                     '-a_srs', outEPSG, inFile])
    # call([python "C:\Program Files\GDAL\gdal_edit.py" -a_srs EPSG:31984 ..\New\BACK_M120_20191020_145813_A096100VA0093.TIF'])
###############################################################################    
def ras_dif_gdal_v1(inRasT1,inRasT2,outRas_dif):
    ''' 
    outRas_dif = inRasT2 - inRasT1
    '''
    inRasT1_band = gdal.Open(inRasT1)
    inRasT2_band = gdal.Open(inRasT2)
    inRasT1_data = inRasT1_band.ReadAsArray().astype(np.float32)
    inRasT2_data = inRasT2_band.ReadAsArray().astype(np.float32)
    outRas_dif_data = inRasT2_data - inRasT1_data
    
    geotransform = inRasT1_band.GetGeoTransform()
    originX,pixelWidth,empty,finalY,empty2,pixelHeight=geotransform
    cols =  inRasT1_band.RasterXSize
    rows =  inRasT1_band.RasterYSize
    projection = inRasT1_band.GetProjection()
    finalX = originX + pixelWidth * cols
    originY = finalY + pixelHeight * rows
    
    rasterSet = gdal.GetDriverByName('GTiff').Create(outRas_dif, 
                                                     cols, rows,1,
                                                     gdal.GDT_Float32)
    rasterSet.SetProjection(projection)
    rasterSet.SetGeoTransform(geotransform)
    rasterSet.GetRasterBand(1).WriteArray(outRas_dif_data)
    rasterSet.GetRasterBand(1).SetNoDataValue(-9999)
    rasterSet = None

###############################################################################    
# Reading a GeoTiff data file using GDAL Python: 
# Solution: create a function that read geotiff file into a numpy array
def readGtif(inGtif):    
    # Creating gdal object
    ds = gdal.Open(inGtif)    
    # Reading number of bands
    numBand = ds.RasterCount    
    # Reading rows and cols size
    col = ds.RasterXSize
    row = ds.RasterYSize    
    # Reading geotransformation and geoprojection
    geotransform = ds.GetGeoTransform()
    geoprojection = ds.GetProjection()
    # Initializing array see CheatSheet#2 for more approaches
    array = np.zeros([row, col, numBand ]) #3d zeros np array
    for i in range(numBand ): #for each band
            band = ds.GetRasterBand(i+1) #read band data
            arr = band.ReadAsArray() #convert to numpy
            array[:, :, i] = arr #assign to 3d numpy array
    #size = arr.shape #this can be neglected similar to row and col    
    #return geotransform, geoprojection, (size[1], size[0]), array
    return geotransform, geoprojection, (row, col), array
# Example:
#geotransform, geoprojection, (row,col), array = readGtif(r'D:/Data_Lib/Raster/Float/sub5_Elev.tif')
