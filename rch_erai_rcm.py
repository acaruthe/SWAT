###########################################
#############HEADER#######################
# This python code will read in multiple output.rch files from SWAT, subset the data based on subbasins of choice, and create new text files containing data  
#    corresponding to teach subbasin
#
#  by: alex caruthers 
##########################################
#########################################

## need numpy, matplotlib and pandas 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

###########################################
#
# output.rch files can be read in using fixed-width columns. set the headers for each column, which pandas will use as the column/variable name
# then create a list of "tuples" or pairs whih correspond to the starting and ending space of each column
#
###########################################
    
 
##### set headers for column names 
heds = (["deadspc","SUB", "GIS",  "MONTH", "AREAkm2", "FLOW_INcms", "FLOW_OUTcms", "EVAPcms",  "TLOSScms", "SED_INtons", "SED_OUTtons", "SEDCONCmg/L ", "ORGN_INkg", "ORGN_OUTkg", "ORGP_INkg", "ORGP_OUTkg" , "NO3_INkg" ,   "NO3_OUTkg"   , "NH4_INkg" ,  "NH4_OUTkg"   , "NO2_INkg"  , "NO2_OUTkg" ,  "MINP_INkg" , "MINP_OUTkg" , "CHLA_INkg" , "CHLA_OUTkg"  , "CBOD_INkg"  , "CBOD_OUTkg"  , "DISOX_INkg"  ,"DISOX_OUTkg" , "SOLPST_INmg" , "SOLPST_OUTmg" , "SORPST_INmg" , "SORPST_OUTmg" , "REACTPSTmg"   ,  "VOLPSTmg"  , "SETTLPSTmg" , "RESUSP_PSTmg" , "DIFFUSEPSTmg" , "REACBEDPSTmg" , "BURYPSTmg"  , "BED_PSTmg", "BACTP_OUTct" ,"BACTLP_OUTct" , "CMETAL1kg" ,  "CMETAL2kg",  "CMETAL3kg" , "TOT Nkg", "TOT_Pkg" , "NO3ConcMg/l",  "WTMPdegc"  ])

## create the tuples for the start/end of each column in  # of spaces 
s = 12
t = 14
w = 12 

s66 = np.repeat(s,5) #the first n columns are 12 spaces each
t2 = np.repeat(t,1)  # there is n columns that are 14 spaces each 
s11 =np.repeat(s,41) # the remaining columns are 12 spaces 

col_array1 = np.append([7,5,8,5],s66) # the first 4 columns are 7, 5, 8, 5 spaces, then add the first repeating 12

col_array2 = np.append(col_array1,t2) # add the repeating 14 spaces 

col_array = np.append(col_array2,s11) # add the remaining 12 spaces 


col = list(col_array) # create a "list" of this data 

## create tuples  -> create the pairs of start/end space 
istart = [0 for x in range(len(col_array))] #make the original start space 0
iend  = [0 for x in range(len(col_array))]  # make og end space 0 

for i in range(len(col_array)): 
    print(i)
    if i==0: #for the first start space, begin at 0
        istart[i] = 0
        iend[i] = col_array[i] # the first column ends at space 7, or col_array[i]
    else:
        istart[i] = istart[i-1] + col_array[i-1] #the start space is the previous start space plus the previous end space (aka, the past end)
        iend[i] = iend[i-1] + col_array[i]      # the end space is the start date plus col_array[i]



col_tuple = list(zip(istart,iend)) #create the pairs! of istart,iend 
print(col_tuple) # double check this worked !

#### read in each data file -> file name, header = 0; names =header names, colspecs = list of start/end spaces, skiprows = number of lines to skip for headers in file 
names = heds

df_prism_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_PRISM_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_erai_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAI_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_eraiwrf12_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIWRF12km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_eraiwrf25_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIWRF25km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_eraiwrf50_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIWRF50km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_erairegcm12_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIRegCM12km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_erairegcm25_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIRegCM25km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

df_erairegcm50_raw = pd.read_fwf('SWAToutput_UMRB_ISU/output_ERAIRegCM50km_cal_8910.rch', header=0, names=names, colspecs=col_tuple, skiprows=8)

#######################################################################################################################
#
# Now that the files have been read, we need to create a date column 
# The text files are 2-d, but we want them to either be 3d, or separated by subbasin 
# Files have month, year as separate columns; also yearly averages after each year (mon=1-12,year)
# Also a set of averages for full simulation at the end 
#
####################################################################################################################

########################
#
# lets start by removing the yearly averages and the averages for the simulation 
# remove all the lines where month is greater than 12 
#
##############################################


df_prism = df_prism_raw.drop(df_prism_raw[df_prism_raw.MONTH > 12].index)
df_erai = df_erai_raw.drop(df_erai_raw[df_erai_raw.MONTH > 12].index)
df_eraiwrf12 = df_eraiwrf12_raw.drop(df_eraiwrf12_raw[df_eraiwrf12_raw.MONTH > 12].index)
df_eraiwrf25 = df_eraiwrf25_raw.drop(df_eraiwrf25_raw[df_eraiwrf25_raw.MONTH > 12].index)
df_eraiwrf50 = df_eraiwrf50_raw.drop(df_eraiwrf50_raw[df_eraiwrf50_raw.MONTH > 12].index)
df_erairegcm12 = df_erairegcm12_raw.drop(df_erairegcm12_raw[df_erairegcm12_raw.MONTH > 12].index)
df_erairegcm25 = df_erairegcm25_raw.drop(df_erairegcm25_raw[df_erairegcm25_raw.MONTH > 12].index)
df_erairegcm50 = df_erairegcm50_raw.drop(df_erairegcm50_raw[df_erairegcm50_raw.MONTH > 12].index)


##############################################
# add year to data frame
# 119 subbasins, 12 months of data plus the stupid yearly averages 
# so year repeats every 119 * 12 = 1428
# so 1991-2010 repeats 1547 times


yrs = [] # create new array for years

for i in range(1991,2011,1): #repeat the year for 119 subbasins * 13 (12 months plus 1 annual average)
       yr1 = np.repeat(i,1428)
       yrs = np.append(yrs,yr1)

# now append this to the dataframes

df_prism['YEAR'] = yrs
df_erai['YEAR'] = yrs
df_eraiwrf12['YEAR'] = yrs
df_eraiwrf25['YEAR'] = yrs
df_eraiwrf50['YEAR'] = yrs
df_erairegcm12['YEAR'] = yrs
df_erairegcm25['YEAR'] = yrs
df_erairegcm50['YEAR'] = yrs

######### create a new column thats YYYYMM 
#### the last date is just number of years in simulation, which doesnt fit the YYYY-MM format, so coerce to fix that error
##### NOTE -> will need to fix this in order to use subbasin averages -> maybe send to a different file? 

###                   create datetime       year    month        needs a day       coerce to fix the last rows     YYYY-MM
df_prism['DATE'] = pd.to_datetime(df_prism[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_erai['DATE'] = pd.to_datetime(df_erai[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_eraiwrf12['DATE'] = pd.to_datetime(df_eraiwrf12[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_eraiwrf25['DATE'] = pd.to_datetime(df_eraiwrf25[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_eraiwrf50['DATE'] = pd.to_datetime(df_eraiwrf50[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_erairegcm12['DATE'] = pd.to_datetime(df_erairegcm12[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_erairegcm25['DATE'] = pd.to_datetime(df_erairegcm25[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')
df_erairegcm50['DATE'] = pd.to_datetime(df_erairegcm50[['YEAR','MONTH']].assign(Day=1), errors = "coerce").dt.strftime('%Y%m')


############################################################################################################################################3
#
# Now we can subbset the data based on subbasin ! Use SUB = 100 as test, Grafton 
#
#####################################################################
#rearrange data using dataframe multi-index; using SUBBASIN and DATE

#pd.MultiIndex.from_frame(df_prism, names = ['SUB', 'DATE'])

print(df_prism)



grafton_prism_raw = df_prism[df_prism["SUB"] == 100]  #.to_xarray()


grafton_prism = grafton_prism_raw.set_index(['DATE'])

print(grafton_prism)

print(grafton_prism["FLOW_OUTcms"])


grafton_prism.plot( y = 'FLOW_OUTcms', use_index=True)
plt.show()



