print('MDToolbox')
print('Version 0.07. This is the latest version.')
print('Updated on 10_20_2017 by Axel.')
print('Contact : axel.poyet@cern.ch')


### IMPORTANT
### Each method can have parameters, but all parameters should have a custom value 
### (so you can run simply MD1Toolbox.method() to see the output without knowing the correct syntax)
### Each method should have a short description

import sys
sys.path.append('/eos/user/s/sterbini/MD_ANALYSIS/public/')
print('Importing toolbox from Guido.')
from myToolbox import *
import tarfile

class MDToolbox:

###===========================================================================================================================###
###                                                    GET FUNCTIONS                                                          ###
###===========================================================================================================================###

    @staticmethod    
    def getRightWireVariables():
        """The IP5 Right Wire Variables (1 power supply, 5 motors, 4 temperatures gauges, 1 vacuum gauges, 
        relay status and voltages on the two wires (internal and external))"""
        variablesWireR=['RPMC.UL557.RBBCW.R5B2:I_MEAS',
                'RPMC.UL557.RBBCW.R5B2:I_REF',
                'RPMC.UL557.RBBCW.R5B2:V_MEAS',
                'RPMC.UL557.RBBCW.R5B2:V_REF',
                'RPMC.UL557.RBBCW.R5B2:STATE',
                'TCTPH.4R5.B2:MEAS_MOTOR_LD',
                'TCTPH.4R5.B2:MEAS_MOTOR_LU',
                'TCTPH.4R5.B2:MEAS_MOTOR_RD',
                'TCTPH.4R5.B2:MEAS_MOTOR_RU',
                'TCTPH.4R5.B2:MEAS_V_MOTOR_POS',
                'TCTPH_4R5_B2_TTRD.POSST',
                'TCTPH_4R5_B2_TTRU.POSST',
                'TCTPH_4R5_B2_TTLD.POSST',
                'TCTPH_4R5_B2_TTLU.POSST',
                'BBCWE.R5.B2:RELAY_STATUS',
                'BBCWE.R5.B2:VOLTAGE',
                'BBCWI.R5.B2:RELAY_STATUS',
                'BBCWI.R5.B2:VOLTAGE',
                'VGPB.935.4R5.R.PR',
                'LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS',
                'LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS']
        return variablesWireR
    
    @staticmethod    
    def getLeftWireVariables():
        """The IP5 Right Wire Variables (1 power supply, 5 motors, 4 temperatures gauges, 1 vacuum gauges, 
        relay status and voltages on the two wires (internal and external))"""
        variablesWireL=['RPMC.USC55.RBBCW.L5B2:I_MEAS',
                    'RPMC.USC55.RBBCW.L5B2:I_REF',
                    'RPMC.USC55.RBBCW.L5B2:V_MEAS',
                    'RPMC.USC55.RBBCW.L5B2:V_REF',
                    'RPMC.USC55.RBBCW.L5B2:STATE',
                    'TCL.4L5.B2:MEAS_MOTOR_LD',
                    'TCL.4L5.B2:MEAS_MOTOR_LU',
                    'TCL.4L5.B2:MEAS_MOTOR_RD',
                    'TCL.4L5.B2:MEAS_MOTOR_RU',
                    'TCL.4L5.B2:MEAS_V_MOTOR_POS',
                    'TCL_4L5_B2_TTRD.POSST',
                    'TCL_4L5_B2_TTRU.POSST',
                    'TCL_4L5_B2_TTLD.POSST',
                    'TCL_4L5_B2_TTLU.POSST',
                    'BBCWI.L5.B2:RELAY_STATUS', 
                    'BBCWI.L5.B2:VOLTAGE',
                    'BBCWE.L5.B2:RELAY_STATUS',
                    'BBCWE.L5.B2:VOLTAGE',
                    'VGPB.935.4L5.R.PR',
                    'LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS',
                    'LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS']
        return variablesWireL
    
    
    @staticmethod
    def getGlobalBeamVariables():
        """About the beam, we are mainly interested in the tune, the energy and the intensity. This function only returns these different variables.
        """
        globalBeamVariables = ['LHC.BOFSU:OFC_ENERGY','LHC.BQBBQ.CONTINUOUS.B2:TUNE_H','LHC.BQBBQ.CONTINUOUS.B2:TUNE_V','LHC.BQBBQ.CONTINUOUS.B1:TUNE_H','LHC.BQBBQ.CONTINUOUS.B1:TUNE_V','LHC.BCTFR.B6R4.B1:BEAM_INTENSITY','LHC.BCTFR.B6R4.B2:BEAM_INTENSITY']
        
        return globalBeamVariables
    
    
    @staticmethod    
    def getOptics(
        myFile='/eos/user/s/sterbini/MD_ANALYSIS/2017/LHCOptics/newStudies/collisionAt40cm/lhcb2_thin.twiss'):
        """to load the optics from a TFS file.
        myFile: '/eos/user/s/sterbini/MD_ANALYSIS/2017/LHCOptics/newStudies/collisionAt40cm/lhcb2_thin.twiss'
        """
        globalDF=myToolbox.fromTFStoDF(myFile)
        optics=globalDF.iloc[0]['TABLE'].copy()
        return {'globalDF':globalDF, 'opticsDF':optics}
    
    @staticmethod
    def getFillingPattern():
        """ This functions returns the variables needed to download the filling pattern """
        
        fillingPatternVariables = ['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN','LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN']
        return fillingPatternVariables
    
    @staticmethod
    def getFBCTVariables():
        """ FBCT variables in cals.
        """
        FBCTvariables = ['LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY','LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY']
        return FBCTvariables
    
    @staticmethod
    def getVerticalVariables():
        variables = ['LHC.BPTDV.A4R5.B2:CALIBCORRECTEDPOS',
                                  'LHC.BPTUV.A4R5.B2:CALIBCORRECTEDPOS',
                                  'TCTPV.4R5.B2:MEAS_MOTOR_RD',
                                  'TCTPV.4R5.B2:MEAS_MOTOR_RU',
                                  'TCTPV.4R5.B2:MEAS_MOTOR_LD',
                                  'TCTPV.4R5.B2:MEAS_MOTOR_LU',
                                  'TCL.4L5.B2:MEAS_V_MOTOR_POS',
                                  'TCTPH.4R5.B2:MEAS_V_MOTOR_POS']
        return variables
    
    @staticmethod
    def getTCTPHRawVariables():
        """ Raw data variables from cals for TCTPH.
        """
        variables = ['LHC.BPTDH.A4R5.B2:CALIBRAWVALV1',
                     'LHC.BPTDH.A4R5.B2:CALIBRAWVALV2',
                     'LHC.BPTUH.A4R5.B2:CALIBRAWVALV1',
                     'LHC.BPTUH.A4R5.B2:CALIBRAWVALV2',
                     'TCTPH.4R5.B2:MEAS_V_LVDT_POS'
                    ]
        return variables
    
    @staticmethod
    def getTCLRawVariables():
        """ Raw data variables from cals for TCL.
        """
        variables = ['LHC.BPTDH.A4L5.B2:CALIBRAWVALV1',
                     'LHC.BPTDH.A4L5.B2:CALIBRAWVALV2',
                     'LHC.BPTUH.A4L5.B2:CALIBRAWVALV1',
                     'LHC.BPTUH.A4L5.B2:CALIBRAWVALV2',
                     'TCL.4L5.B2:MEAS_V_LVDT_POS'
                    ]
        return variables
    
    @staticmethod
    def getLumiBBBVariables():
        """ BBB Luminosity at IP1 and IP5
        """
        variables = ['ATLAS:BUNCH_LUMI_INST',
                     'CMS:BUNCH_LUMI_INST'
                    ]
        return variables
    
    @staticmethod
    def getOctupoleVariables():
        """ Current in lattice octupoles
        """
        variables = ['RPMBB.RR17.ROF.A12B1:I_REF',
                     'RPMBB.RR17.ROF.A12B2:I_REF',
                     'RPMBB.RR17.ROD.A12B1:I_REF',
                     'RPMBB.RR17.ROD.A12B2:I_REF']
        return variables
    
    @staticmethod
    def getCrossingAngle():
        """ Crossing angle in IP1/5 variables
        """
        variables = ['LHC.RUNCONFIG:IP1-XING-V-MURAD',
                     'LHC.RUNCONFIG:IP5-XING-H-MURAD']
        return variables
    
    @staticmethod
    def getADTObsBoxTriggers(t1,t2,beam='B2',plane='H'):
        variable = ['CGWRTD.SR4.ADT-'+plane+beam+'.OUT:DESC']
        trigger = myToolbox.cals2pnd(variable,t1,t2)
        ts = pnd.DatetimeIndex(trigger.index)
        return ts.to_pydatetime()
    
        
        
###===========================================================================================================================###
###                                             INITIALIZE AND ADD FUNCTIONS                                                  ###
###===========================================================================================================================###

    
    @staticmethod    
    def initializeDF(variables=['RPMC.UL557.RBBCW.R5B2:I_MEAS','RPMC.USC55.RBBCW.L5B2:I_MEAS'], LastMinuteToConsider=2,startTime = datetime.datetime.now()):
        """To initialize the DF a simple schematic of the wires setup in IP5.
        variables=self.getLeftWireVariables()+self.getRightWireVariables()
        LastMinuteToConsider=2
        """
        return myToolbox.cals2pnd(variables,startTime
                                  -datetime.timedelta(minutes=LastMinuteToConsider),startTime)
    
    
    
    @staticmethod    
    def addRowsFromCals(myDF, deltaTime=datetime.timedelta(minutes=2)):
        """This method extend in time a pandas dataframe using the CALS database.
        It returns a new pandas dataframe. It has 2 arguments:
        myDF: the initial dataframe
        deltaTime:  the delta of time to apply (e.g. deltaTime=datetime.timedelta(minutes=2))"""
        aux=myToolbox.cals2pnd(list(myDF),myDF.index[-1],myDF.index[-1]+deltaTime )
        myDF=pnd.concat([myDF,aux])
        return myDF
    
    @staticmethod    
    def addColumnsFromCals(myDF, listOfVariables):
        """This method add a list of variables to a pandas dataframe using the CALS database.
        It returns a new pandas dataframe. It has 2 arguments:
        myDF: the initial dataframe
        listOfVariable:  the list of variables to add"""
        aux=myToolbox.cals2pnd(listOfVariables,myDF.index[0],myDF.index[-1])
        myDF=pnd.concat([myDF,aux])
        return myDF
    
    @staticmethod
    def refreshData(raw_data, minutesToAdd=2):
        raw_data = MD1Toolbox.addRowsFromCals(raw_data,deltaTime=datetime.timedelta(minutes=minutesToAdd))
        return raw_data
    
    
###====================================================================================================================###
###                                                                                                                    ###
###                                                     BB FUNCTIONS                                                   ###
###                                                                                                                    ###
###====================================================================================================================###


    @staticmethod
    def prepareOpticsFromMADX(B1,B2,B1_survey,B2_survey):
        """The purpose of this function is to prepare the useful dataframes for BB studies. 
        It has to follow the getOptics function from this same toolbox. 
        The input shall be DFs, as the output. 
        """
        B1_survey_BBLR_IP1 = B1_survey['opticsDF'][B1_survey['opticsDF']['NAME'].str.contains('BBLR_IP1')].copy()
        B1_IP1_s=0.0
        B1_survey_BBLR_IP1 = B1_survey_BBLR_IP1.drop([B1_IP1_s])
        B1_survey_BBLR_IP1['S wrt IP1'] = B1_survey_BBLR_IP1['S']-B1_IP1_s
        
        B1_survey_BBLR_IP5 = B1_survey['opticsDF'][B1_survey['opticsDF']['NAME'].str.contains('BBLR_IP5')].copy()
        B1_IP5_s=13329.28923
        B1_survey_BBLR_IP5 = B1_survey_BBLR_IP5.drop([B1_IP5_s])
        B1_survey_BBLR_IP5['S wrt IP5'] = B1_survey_BBLR_IP5['S']-B1_IP5_s


        B2_survey_BBLR_IP1 = B2_survey['opticsDF'][B2_survey['opticsDF']['NAME'].str.contains('BBLR_IP1')].copy()
        B2_IP1_s=0.0
        B2_survey_BBLR_IP1 = B2_survey_BBLR_IP1.drop([B2_IP1_s])
        B2_survey_BBLR_IP1['S wrt IP1'] = B2_survey_BBLR_IP1['S']-B2_IP1_s
        
        B2_survey_BBLR_IP5 = B2_survey['opticsDF'][B2_survey['opticsDF']['NAME'].str.contains('BBLR_IP5')].copy()
        B2_IP5_s=13329.59397
        B2_survey_BBLR_IP5 = B2_survey_BBLR_IP5.drop([B2_IP5_s])
        B2_survey_BBLR_IP5['S wrt IP5'] = B2_survey_BBLR_IP5['S']-B2_IP5_s

        
        
        #BBLR PARAMETERS 
        
        B1_BBLR_IP1 = B1['opticsDF'][B1['opticsDF']['NAME'].str.contains('BBLR_IP1')].copy()
        B1_BBLR_IP1 = B1_BBLR_IP1.drop([B1_IP1_s])
        B1_BBLR_IP1['S wrt IP1'] = B1_BBLR_IP1['S']-B1_IP1_s
        
        B1_BBLR_IP5 = B1['opticsDF'][B1['opticsDF']['NAME'].str.contains('BBLR_IP5')].copy()
        B1_BBLR_IP5 = B1_BBLR_IP5.drop([13329.28923])
        B1_BBLR_IP5['S wrt IP5'] = B1_BBLR_IP5['S']-B1_IP5_s


        B2_BBLR_IP1 = B2['opticsDF'][B2['opticsDF']['NAME'].str.contains('BBLR_IP1')].copy()
        B2_BBLR_IP1 = B2_BBLR_IP1.drop([B2_IP1_s])
        B2_BBLR_IP1['S wrt IP1'] = B2_BBLR_IP1['S']-B2_IP1_s
        
        B2_BBLR_IP5 = B2['opticsDF'][B2['opticsDF']['NAME'].str.contains('BBLR_IP5')].copy()
        B2_BBLR_IP5 = B2_BBLR_IP5.drop([13329.59397])
        B2_BBLR_IP5['S wrt IP5'] = B2_BBLR_IP5['S']-B2_IP5_s
        
        
        
        nbMADX = len(B1_BBLR_IP1)/2
        
        LRname = np.arange(-nbMADX,nbMADX+1)
        LRname = np.delete(LRname,nbMADX)
        LRname = LRname[::-1]
        B2_BBLR_IP1.index = LRname
        B2_BBLR_IP5.index = LRname
        B1_BBLR_IP1.index = LRname
        B1_BBLR_IP5.index = LRname
        
        a = np.concatenate([np.arange(-nbMADX,0)[::-1],np.arange(1,nbMADX+1)[::-1]])
        B2_BBLR_IP1 = B2_BBLR_IP1.reindex(a)
        B2_BBLR_IP1.index = B2_BBLR_IP5.index
        B1_BBLR_IP1 = B1_BBLR_IP1.reindex(a)
        B1_BBLR_IP1.index = B1_BBLR_IP5.index
        
        beamSep1_IP1 = np.abs(B1_survey_BBLR_IP1['Y'].values-B2_survey_BBLR_IP1['Y'].values)
        beamSep1_IP5 = np.abs(B1_survey_BBLR_IP5['X'].values-B2_survey_BBLR_IP5['X'].values)
        
        beamSep2_IP1 = np.abs(B1_BBLR_IP1['Y'].values - B2_BBLR_IP1['Y'].values)
        beamSep2_IP5 = np.abs(B1_BBLR_IP5['X'].values - B2_BBLR_IP5['X'].values)
        
        B2_BBLR_IP1['BEAM SEP bump']=beamSep2_IP1
        B2_BBLR_IP1['BEAM SEP reference orbit']=beamSep1_IP1
        B2_BBLR_IP1['BEAM SEP'] = B2_BBLR_IP1['BEAM SEP bump']+B2_BBLR_IP1['BEAM SEP reference orbit']
        B2_BBLR_IP1['BEAM SEP ALG'] = B2_BBLR_IP1['BEAM SEP']
        B2_BBLR_IP1['BEAM SEP ALG'].iloc[range(nbMADX)]=-B2_BBLR_IP1['BEAM SEP ALG'].iloc[range(nbMADX)]
        
        B2_BBLR_IP5['BEAM SEP bump']=beamSep2_IP5
        B2_BBLR_IP5['BEAM SEP reference orbit']=beamSep1_IP5
        B2_BBLR_IP5['BEAM SEP'] = B2_BBLR_IP5['BEAM SEP bump']+B2_BBLR_IP5['BEAM SEP reference orbit']
        B2_BBLR_IP5['BEAM SEP ALG'] = B2_BBLR_IP5['BEAM SEP']
        B2_BBLR_IP5['BEAM SEP ALG'].iloc[range(nbMADX)]=-B2_BBLR_IP5['BEAM SEP ALG'].iloc[range(nbMADX)]
        
        



        return B1_BBLR_IP1, B1_BBLR_IP5, B2_BBLR_IP1, B2_BBLR_IP5, B1_survey_BBLR_IP1, B1_survey_BBLR_IP5, B2_survey_BBLR_IP1, B2_survey_BBLR_IP5
    
    
    @staticmethod
    def getEncountersFromBBMatrix(B1_bunches,B2_bunches,BBMatrixLHC,nbLR,B2_BBLR):
        listofLR = []
        nbLRPerBunch = []
        beamIndex = []
        for i in B2_bunches:
            tmp = []
            beamInd = []
            for j in np.arange(nbLR):
                if (BBMatrixLHC[i+j][i]==10) & (len(np.where(B1_bunches==(i+j))[0])==1):
                                            tmp.append(j)
                                            beamInd.append(i+j)
                if (BBMatrixLHC[i-j][i]==10) & (len(np.where(B1_bunches==(i-j))[0])==1):
                                            tmp.append(-j)
                                            beamInd.append(i-j)
            beamInd_sort = sorted(beamInd)
            #beamInd_sort.append('Sum')
            listofLR.append(sorted(tmp))
            nbLRPerBunch.append(len(tmp))
            beamIndex.append(sorted(beamInd_sort))

        encountersDF = pnd.DataFrame(index=B2_bunches)
        encountersDF['Nb of encounters'] = nbLRPerBunch
        encountersDF['Index for Optics'] = listofLR
        encountersDF['Index for Beam Param.'] = beamIndex
        encountersDF['Index'] = np.arange(len(B2_bunches))
        

        return encountersDF
    
    @staticmethod
    def computeRDT(bunch,listOfencountersDF,encountersDF,MUX_IP5,MUY_IP5,p,q):
        aux = listOfencountersDF[encountersDF.loc[bunch]['Indice']]
        cp = (aux['BETX']**(np.abs(p)/2.)*aux['BETY']**(np.abs(q)/2.))/aux['BEAM SEP ALG']**(np.abs(p)+np.abs(q))*np.exp(1j*2*np.pi*(p*(aux['MUX']-MUX_IP5+q*(aux['MUY']-MUY_IP5))))
        return cp.sum()
            
        
        
###===========================================================================================================================###
###                                                  COMPUTE FUNCTIONS                                                        ###
###===========================================================================================================================###


    @staticmethod    
    def computeDistancesInMM(myDF):
        """To obtain the distances between the wires and the beam, in mm, from PUs and positions of the jaws.
        Input : 
         - myDF : panda DataFrame = original DF containing row data. 
         
        Out put : 
         - myDF_resample : panda DF = modified DF containing resampling data and calculated distances.
         
        NB : To keep original data, a copy is made. 
        NB2 : Calibration to be checked.
        """
        myDF_resample = pnd.DataFrame()
        calibrationFactor = 1.
        posWireL_mm = 3
        posWireR_mm = -3
         #Right Wire

        myDF_resample['LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] =-myDF['LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')*calibrationFactor
        myDF_resample['LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] =-myDF['LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')*calibrationFactor
        myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RD resampled [mm]'] =myDF['TCTPH.4R5.B2:MEAS_MOTOR_RD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RU resampled [mm]'] =myDF['TCTPH.4R5.B2:MEAS_MOTOR_RU'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_LD resampled [mm]'] =myDF['TCTPH.4R5.B2:MEAS_MOTOR_LD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_LU resampled [mm]'] =myDF['TCTPH.4R5.B2:MEAS_MOTOR_LU'].resample('1s').mean().fillna(method='ffill')

            #Left Wire 

        myDF_resample['LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] =-myDF['LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')*calibrationFactor
        myDF_resample['LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] =-myDF['LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')*calibrationFactor
        myDF_resample['TCL.4L5.B2:MEAS_MOTOR_RD resampled [mm]'] =myDF['TCL.4L5.B2:MEAS_MOTOR_RD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCL.4L5.B2:MEAS_MOTOR_RU resampled [mm]'] =myDF['TCL.4L5.B2:MEAS_MOTOR_RU'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LD resampled [mm]'] =myDF['TCL.4L5.B2:MEAS_MOTOR_LD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LU resampled [mm]'] =myDF['TCL.4L5.B2:MEAS_MOTOR_LU'].resample('1s').mean().fillna(method='ffill')
        
            #Vertical 

        myDF_resample['LHC.BPTDV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] = myDF['LHC.BPTDV.A4R5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['LHC.BPTUV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'] = myDF['LHC.BPTUV.A4R5.B2:CALIBCORRECTEDPOS'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_RD resampled [mm]'] =myDF['TCTPV.4R5.B2:MEAS_MOTOR_RD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_RU resampled [mm]'] =myDF['TCTPV.4R5.B2:MEAS_MOTOR_RU'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_LD resampled [mm]'] =myDF['TCTPV.4R5.B2:MEAS_MOTOR_LD'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_LU resampled [mm]'] =myDF['TCTPV.4R5.B2:MEAS_MOTOR_LU'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['Average PU [mm]'] = (myDF_resample['LHC.BPTUV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+myDF_resample['LHC.BPTDV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'])/2
        myDF_resample['TCTPH.4R5.B2:MEAS_V_MOTOR_POS resampled [mm]'] = myDF['TCTPH.4R5.B2:MEAS_V_MOTOR_POS'].resample('1s').mean().fillna(method='ffill')
        myDF_resample['TCL.4L5.B2:MEAS_V_MOTOR_POS resampled [mm]'] = myDF['TCL.4L5.B2:MEAS_V_MOTOR_POS'].resample('1s').mean().fillna(method='ffill')



        #Distances calculation 

            #Right Wire 

        myDF_resample['Beam Position Downstream (WRT R Tank) [mm]'] = myDF_resample['LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RD resampled [mm]']+myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_LD resampled [mm]'])/2
        myDF_resample['Beam Position Upstream (WRT R Tank) [mm]'] = myDF_resample['LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RU resampled [mm]']+myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_LU resampled [mm]'])/2
        myDF_resample['Average Beam Position (WRT R Tank) [mm]'] = (myDF_resample['Beam Position Upstream (WRT R Tank) [mm]']+myDF_resample['Beam Position Downstream (WRT R Tank) [mm]'])/2
        myDF_resample['Distance Right Wire Beam Downstream [mm]'] = myDF_resample['Beam Position Downstream (WRT R Tank) [mm]']-myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RD resampled [mm]']-posWireR_mm   # NB ALWAYS positive
        myDF_resample['Distance Right Wire Beam Upstream [mm]'] = myDF_resample['Beam Position Upstream (WRT R Tank) [mm]']-myDF_resample['TCTPH.4R5.B2:MEAS_MOTOR_RU resampled [mm]']-posWireR_mm       # NB ALWAYS positive
        myDF_resample['Average Distance Right Wire Beam [mm]'] = (myDF_resample['Distance Right Wire Beam Downstream [mm]']+myDF_resample['Distance Right Wire Beam Upstream [mm]'])/2

            #Left Wire

        myDF_resample['Beam Position Downstream (WRT L Tank) [mm]'] = myDF_resample['LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCL.4L5.B2:MEAS_MOTOR_RD resampled [mm]']+myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LD resampled [mm]'])/2
        myDF_resample['Beam Position Upstream (WRT L Tank) [mm]'] = myDF_resample['LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCL.4L5.B2:MEAS_MOTOR_RU resampled [mm]']+myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LU resampled [mm]'])/2
        myDF_resample['Average Beam Position (WRT L Tank) [mm]'] = (myDF_resample['Beam Position Downstream (WRT L Tank) [mm]']+myDF_resample['Beam Position Upstream (WRT L Tank) [mm]'])/2
        myDF_resample['Distance Left Wire Beam Downstream [mm]'] = myDF_resample['Beam Position Downstream (WRT L Tank) [mm]']-myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LD resampled [mm]']-posWireL_mm         # NB ALWAYS negative
        myDF_resample['Distance Left Wire Beam Upstream [mm]'] = myDF_resample['Beam Position Upstream (WRT L Tank) [mm]']-myDF_resample['TCL.4L5.B2:MEAS_MOTOR_LU resampled [mm]']-posWireL_mm              # NB ALWAYS negative
        myDF_resample['Average Distance Left Wire Beam [mm]'] = (myDF_resample['Distance Left Wire Beam Upstream [mm]']+myDF_resample['Distance Left Wire Beam Downstream [mm]'])/2
        
            #Vertical

        myDF_resample['Beam Position Downstream [mm]'] = myDF_resample['LHC.BPTDV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_RD resampled [mm]']+myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_LD resampled [mm]'])/2
        myDF_resample['Beam Position Upstream [mm]'] = myDF_resample['LHC.BPTUV.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+(myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_RU resampled [mm]']+myDF_resample['TCTPV.4R5.B2:MEAS_MOTOR_LU resampled [mm]'])/2
        myDF_resample['Average Beam Position [mm]'] = (myDF_resample['Beam Position Downstream [mm]']+myDF_resample['Beam Position Upstream [mm]'])/2


        return myDF_resample
    
    
    @staticmethod
    def computeLifetimeFromFBCT(FBCT):
        """Calculating the life time bunch by bunch from FBCT.
        
        NB : recquire to have imported the intensity from FBCT before. 
        
        Input : 
        - FBCT : panda DataFrame = DF containing raw data about FBCT
        
        Outputs : 
        - Lifetime_FBCT_DF = panda DataFrame = DF containing BBB lifetime 
        """      
        Lifetime_FBCT_DF = pnd.DataFrame()
        
        for i in FBCT.columns:
            Lifetime_FBCT_DF[i] = -1./((FBCT[i].dropna()/1e10).resample('30s').mean().diff()/30./(FBCT[i].dropna()/1e10).resample('30s').mean())/3600.
                   
        return Lifetime_FBCT_DF
        
        
    @staticmethod
    def computeIntensityBBBFromFBCT(fill,FBCT):
        """ Download intensity bunch by bunch from FBCT. 
        Need the filling pattern as an input, the raw data from FBCT in cals. 
        Returns a DF containing all bunches intensities for both the beams.
        """
        intensityFromFBCT = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            intensityFromFBCT['slot '+str(fill[0][i])+'_B1'] = FBCT['LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            intensityFromFBCT['slot '+str(fill[1][i])+'_B2'] = FBCT['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY'].dropna().apply(lambda x:x[fill[1][i]])
        return intensityFromFBCT


    
    @staticmethod
    def computeFillingPatternFromFBCT(variables,startTime=datetime.datetime.now()):
        """This function returns a 2D array containing both the two filling pattern for B1 and B2
        Input : 
        - variables from cals
        Output : 
        - array = filling pattern for both the two beams.
        
        NB : to get B1 filling, array[0], for beam 2, array[1]
        """
        fill = myToolbox.cals2pnd(variables,startTime-datetime.timedelta(minutes=1),startTime)
        slotsB1 = np.where(fill['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'][0])
        slotsB2 = np.where(fill['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'][0])
        B1fill = fill['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'][0]
        B2fill = fill['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'][0]
        return np.array([slotsB1[0],slotsB2[0]]), B1fill, B2fill
    
    @staticmethod
    def computeIntensityBBBCompleteScheme(FBCT):
        """ The aim of this function is to return a data frame containing the intensity, bunch by bunch.
        The empty buckets are filled with NaN, which will be useful for the vistar function. 
        
        Input : 
        - FBCT : panda DF = DF containing the FBCT data ALREADY FORMATED
        
        Output : 
        - intensitySeparated : panda.DataFrame = DF with the full scheme
        """
        LHCFill = np.arange(3564)
        columns = []
        for i in LHCFill:
            columns.append('slot '+str(i)+'_B1')
        for i in LHCFill:
            columns.append('slot '+str(i)+'_B2')


        intensitySeparate = pnd.DataFrame(np.nan,index=FBCT.index, columns=columns)

        for i in FBCT.columns:
            intensitySeparate[i] = FBCT[i]
            
        return intensitySeparate
    
    @staticmethod
    def computeVerticalAlignmentDF_notCalibrated(raw_data,TCTPH_variables, TCL_variables,myThreshold = 0.5):
        """ Creation of a data frame containing resampling data from TCTPH and TCL
        --> FOR VERTICAL ALIGNMENT CHECK !!
        """             
        verticalAlignmentDataDF = pnd.DataFrame()
       
        verticalAlignmentDataDF['TCTPH.4R5.B2:MEAS_V_LVDT_POS_resampled'] = raw_data['TCTPH.4R5.B2:MEAS_V_LVDT_POS'].resample('1s').mean().fillna(method='ffill')
        verticalAlignmentDataDF['TCL.4L5.B2:MEAS_V_LVDT_POS_resampled'] = raw_data['TCL.4L5.B2:MEAS_V_LVDT_POS'].resample('1s').mean().fillna(method='ffill')
        for i in TCTPH_variables[:4]:
            verticalAlignmentDataDF[i+'_resampled'] = raw_data[i].mask(raw_data[i]<.5).resample('1s').mean().fillna(method='ffill')
        for i in TCL_variables[:4]:
            verticalAlignmentDataDF[i+'_resampled'] = raw_data[i].mask(raw_data[i]<.5).resample('1s').mean().fillna(method='ffill')
            
     
    @staticmethod
    def computeVerticalAlignmentDF(raw_data,TCTPH_variables, TCL_variables,myThreshold = 0.5):
        """ Creation of a data frame containing resampling data from TCTPH and TCL
        --> FOR VERTICAL ALIGNMENT CHECK !!
        """             
        verticalAlignmentDataDF = pnd.DataFrame()
       
        #verticalAlignmentDataDF['TCTPH.4R5.B2:MEAS_V_LVDT_POS_resampled'] = raw_data['TCTPH.4R5.B2:MEAS_V_LVDT_POS'].resample('1s').mean().fillna(method='ffill')
        #verticalAlignmentDataDF['TCL.4L5.B2:MEAS_V_LVDT_POS_resampled'] = raw_data['TCL.4L5.B2:MEAS_V_LVDT_POS'].resample('1s').mean().fillna(method='ffill')
        for i in TCTPH_variables:
            verticalAlignmentDataDF[i+'_resampled'] = raw_data[i].resample('1s').mean().fillna(method='ffill')
        for i in TCL_variables:
            verticalAlignmentDataDF[i+'_resampled'] = raw_data[i].resample('1s').mean().fillna(method='ffill')
            

        
        
                        
                 
        return verticalAlignmentDataDF
    
    @staticmethod
    def computeDataFrameSize_MB(myDF):
        return myDF.memory_usage(deep='True').sum()/1024./1024.
    
    @staticmethod
    def computeLumiBBB(fill,raw_data):
        cms = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            cms['slot '+str(fill[0][i])+'_B1'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            cms['slot '+str(fill[1][i])+'_B2'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        CMS_DF = cms.resample('1s').mean().fillna(method='ffill')*1e30

        t1 = CMS_DF.index[0].strftime("%H:%M:%S")
        t2 = CMS_DF.index[-1].strftime("%H:%M:%S")

        atlas = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            atlas['slot '+str(fill[0][i])+'_B1'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            atlas['slot '+str(fill[1][i])+'_B2'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        ATLAS_DF = atlas.resample('1s').mean().fillna(method='ffill').between_time(t1,t2)/1000*1e30

        return CMS_DF + ATLAS_DF
    
    @staticmethod
    def computeRatioLumiBBB(fill,raw_data):
        cms = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            cms['slot '+str(fill[0][i])+'_B1'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            cms['slot '+str(fill[1][i])+'_B2'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        CMS_DF = cms.resample('60s').mean().fillna(method='ffill')*1e30

        t1 = CMS_DF.index[0].strftime("%H:%M:%S")
        t2 = CMS_DF.index[-1].strftime("%H:%M:%S")

        atlas = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            atlas['slot '+str(fill[0][i])+'_B1'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            atlas['slot '+str(fill[1][i])+'_B2'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        ATLAS_DF = atlas.resample('60s').mean().fillna(method='ffill').between_time(t1,t2)/1000*1e30
        
        ratio = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            ratio['slot '+str(fill[0][i])+'_B1'] = ATLAS_DF['slot '+str(fill[0][i])+'_B1']/CMS_DF['slot '+str(fill[0][i])+'_B1']
        for i in np.arange(len(fill[1])):
            ratio['slot '+str(fill[1][i])+'_B2'] = ATLAS_DF['slot '+str(fill[1][i])+'_B2']/CMS_DF['slot '+str(fill[1][i])+'_B2']
        return ratio
    
    @staticmethod
    def computeLumiBBBFromATLASandCMS(fill,raw_data):
        cms = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            cms['slot '+str(fill[0][i])+'_B1'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            cms['slot '+str(fill[1][i])+'_B2'] = raw_data['CMS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        CMS_DF = cms.resample('1s').mean().fillna(method='ffill')*1e30

        t1 = CMS_DF.index[0].strftime("%H:%M")
        t2 = CMS_DF.index[-1].strftime("%H:%M")

        atlas = pnd.DataFrame()
        for i in np.arange(len(fill[0])):
            atlas['slot '+str(fill[0][i])+'_B1'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[0][i]])
        for i in np.arange(len(fill[1])):
            atlas['slot '+str(fill[1][i])+'_B2'] = raw_data['ATLAS:BUNCH_LUMI_INST'].dropna().apply(lambda x:x[fill[1][i]])

        ATLAS_DF = atlas.resample('1s').mean().fillna(method='ffill').between_time(t1,t2)/1000*1e30
        
        return CMS_DF, ATLAS_DF

       
    
    @staticmethod
    def computeEffCrossSection(LUMI_DF, FBCT, sample=60.):
        slots = LUMI_DF.columns.values
        t1 = LUMI_DF.index[0].strftime("%H:%M")
        t2 = LUMI_DF.index[-1].strftime("%H:%M")
        effXSection = pnd.DataFrame(index = (FBCT.between_time(t1,t2)/1e10).dropna().resample(str(sample)[0:-2]+'s').mean().diff().index)
        for i in slots:
            dI_dt = (FBCT.between_time(t1,t2)[i]).resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').diff().values/sample
            lumi = LUMI_DF.between_time(t1,t2)[i].resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').values
            effXSection[i] = - dI_dt/lumi*1e27

        return effXSection
    
    @staticmethod
    def computeEffCrossSection_NEW(LUMI_DF, FBCT, sample=60.):
        slots = LUMI_DF.columns.values
        FBCT = FBCT.reindex(LUMI_DF.index,method='ffill')
        effXSection = pnd.DataFrame(index = (FBCT/1e10).dropna().resample(str(sample)[0:-2]+'s').mean().diff().index)
        for i in slots:
            dI_dt = FBCT[i].resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').diff().values/sample
            lumi = LUMI_DF[i].resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').values
            effXSection[i] = - dI_dt/lumi*1e27

        return effXSection
    
    @staticmethod
    def computeEffCrossSectionFromATLAS(ATLAS_DF, FBCT, sample=60.):
        slots = ATLAS_DF.columns.values
        t1 = ATLAS_DF.index[0].strftime("%H:%M:%S")
        t2 = ATLAS_DF.index[-1].strftime("%H:%M:%S")
        effXSection = pnd.DataFrame(index = (FBCT.between_time(t1,t2)/1e10).dropna().resample(str(sample)[0:-2]+'s').mean().diff().index)
        for i in slots:
            dI_dt = (FBCT.between_time(t1,t2)[i]).resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').diff().values/sample
            lumi = 2*ATLAS_DF.between_time(t1,t2)[i].resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').values
            effXSection[i] = - dI_dt/lumi*1e27

        return effXSection
    
    @staticmethod
    def computeEffCrossSectionFromCMS(CMS_DF, FBCT, sample=60.):
        slots = CMS_DF.columns.values
        t1 = CMS_DF.index[0].strftime("%H:%M:%S")
        t2 = CMS_DF.index[-1].strftime("%H:%M:%S")
        effXSection = pnd.DataFrame(index = (FBCT.between_time(t1,t2)/1e10).dropna().resample(str(sample)[0:-2]+'s').mean().diff().index)
        for i in slots:
            dI_dt = (FBCT.between_time(t1,t2)[i]).resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').diff().values/sample
            lumi = 2*CMS_DF.between_time(t1,t2)[i].resample(str(sample)[0:-2]+'s').mean().fillna(method='ffill').values
            effXSection[i] = - dI_dt/lumi*1e27
        return effXSection


    
    @staticmethod
    def computeLossesRatio(lifetimeBBB,HO=0,LR=224):
        losses = pnd.DataFrame()
        slots = lifetimeBBB.columns.values
        for i in slots:
            losses[i] = 1/lifetimeBBB[i]
        ratio = losses['slot '+str(HO)+'_B2']/losses['slot '+str(LR)+'_B2']
        return ratio
    

        
        
    
    
###===========================================================================================================================###
###                                                    WIRES & TRICKS                                                         ###
###===========================================================================================================================###


    @staticmethod    
    def plotWiresIP5(myColorRE='gray', myColorRI='k',myColorLE='gray',myColorLI='k'):
        """To plot a simple schematic of the wires setup in IP5.
        Arguments and default values:
        myColorRE='gray', color of the right external wire
        myColorRI='k', color of the right internal wire
        myColorLE='gray', color of the left external wire
        myColorLI='k', color of the left internal wire
        """
        plt.plot([-1,1],[-1,1],'b',lw=3)
        plt.plot([1,4],[1,1],'b',lw=3)
        plt.plot([-4,-1],[-1,-1],'b',lw=3)
        plt.plot(np.array([-3.2,-3])+.6,[-0.94,-1],'b',lw=3)
        plt.plot(np.array([-3.2,-3])+.6,[-1.06,-1],'b',lw=3)
        plt.plot(np.array([3,3.2])-.6,np.array([1.06,1]),'b',lw=3)
        plt.plot(np.array([3,3.2])-.6,np.array([.94,1]),'b',lw=3)

        plt.plot([-1,1],[1,-1],'r',lw=3)
        plt.plot([1,4],[-1,-1],'r',lw=3)
        plt.plot([-4,-1],[1,1],'r',lw=3)
        plt.plot(np.array([-3,-3.2])+.6,np.array([-0.94,-1])+2,'r',lw=3)
        plt.plot(np.array([-3,-3.2])+.6,np.array([-1.06,-1])+2,'r',lw=3)
        plt.plot(np.array([3.2,3])-.6,np.array([1.06,1])-2,'r',lw=3)
        plt.plot(np.array([3.2,3])-.6,np.array([.94,1])-2,'r',lw=3)

        plt.plot(np.array([2.0,3.4])-.2,[-1.3,-1.3],myColorRE,lw=3)
        plt.plot(np.array([2.6,2.8])-.2,[-1.3+.06,-1.3],myColorRE,lw=3)
        plt.plot(np.array([2.6,2.8])-.2,[-1.3-.06,-1.3],myColorRE,lw=3)

        plt.plot(np.array([2.0,3.4])-.2,[-0.7,-0.7],myColorRI,lw=3)
        plt.plot(np.array([2.6,2.8])-.2,[-0.7,-0.7+.06],myColorRI,lw=3)
        plt.plot(np.array([2.6,2.8])-.2,[-0.7,-0.7-.06],myColorRI,lw=3)

        plt.plot(np.array([-1.8,-3.2]),[1.3,1.3],myColorLE,lw=3)
        plt.plot(np.array([-3,-3.2])+.6,np.array([1.3,1.3+.06]),myColorLE,lw=3)
        plt.plot(np.array([-3,-3.2])+.6,np.array([1.3,1.3-.06]),myColorLE,lw=3)

        plt.plot(np.array([-1.8,-3.2]),[0.7,0.7],myColorLI,lw=3)
        plt.plot(np.array([-3.2,-3.])+.6,np.array([0.7,0.7+.06]),myColorLI,lw=3)
        plt.plot(np.array([-3.2,-3.])+.6,np.array([0.7,0.7-.06]),myColorLI,lw=3)

        plt.xlim([-5,5])
        plt.ylim([-2,2])
        plt.text(4.15, 1, 'B1', color='b', verticalalignment='center')
        plt.text(4.15, -1, 'B2',color='r', verticalalignment='center')
        plt.text(-4.15, -1, 'B1',color='b', verticalalignment='center',horizontalalignment='right')
        plt.text(-4.15, 1, 'B2', color='r', verticalalignment='center',horizontalalignment='right')

        plt.text(-1.5, .7, '+', color=myColorLI, verticalalignment='center',horizontalalignment='center')
        plt.text(-2.5, .4, 'BBCWI.4L5', color=myColorLI, verticalalignment='center',horizontalalignment='center')

        plt.text(-3.5, 1.3, '+', color=myColorLE, verticalalignment='center',horizontalalignment='center')
        plt.text(-2.5, 1.6, 'BBCWE.4L5', color=myColorLE, verticalalignment='center',horizontalalignment='center')

        plt.text(1.5, .4-2+.3, '+', color=myColorRE, verticalalignment='center',horizontalalignment='center')
        plt.text(2.5, .4-2, 'BBCWE.4R5', color=myColorRE, verticalalignment='center',horizontalalignment='center')

        plt.text(3.5, 1.6-2-.3, '+', color=myColorRI, verticalalignment='center',horizontalalignment='center')
        plt.text(2.5, 1.6-2, 'BBCWI.4R5', color=myColorRI, verticalalignment='center',horizontalalignment='center')
        plt.text(0, 0, 'IP5', color=myColorRI, verticalalignment='center',horizontalalignment='center',
                 bbox=dict(facecolor='w', edgecolor='b', boxstyle='round'))

        plt.axis('off');
        
    @staticmethod    
    def tricks():   
        """Just printing some tricks"""
        print('========================================')
        print('fill,fillDetails=myToolbox.LHCFillsByTime2pnd(datetime.datetime(2017,5,14,23),datetime.datetime(2017,5,20))')

        
        

###===========================================================================================================================###
###                                                     VISTAR                                                                ###
###===========================================================================================================================###


    @staticmethod
    def vistarFillingPattern(B1fill,B2fill,theory=1):
        """Plot the current filling pattern.
        Input : 
        - Bfill : narray = data about filling of B1 and B2
        
        No output. Only plots. 
        """


        B1 = plt.figure()
        ax1=B1.add_subplot(111)
        plt.step(B1fill,'b',where='post')
        plt.ylabel('Current Filling')
        #ax2=B1.add_subplot(212,sharex=ax1)
        #if theory==1:
        #    theoSlotsB1 = np.append([0,100],np.arange(200,248))
        #elif theory==2:
        #    theoSlotsB1 = np.append([0,100],[np.arange(200,248),np.arange(300,348),np.arange(400,448)])
        #for i in theoSlotsB1:
        #    plt.plot([i,i],plt.ylim(),'b')
        #plt.ylabel('Theoretical Filling')
        plt.xlabel('# SLOTS B1')
        #plt.xlim([0,500])
        plt.ylim([0,1.1])
        plt.yticks([0,1],['EMPTY','FILLED'])
        plt.tight_layout()

        B2 = plt.figure()
        ax1=B2.add_subplot(111)
        plt.step(B2fill,'r',where='post')
        plt.ylabel('Current Filling')
        #ax2=B2.add_subplot(212,sharex=ax1)
        #if theory==1:
        #    theoSlotsB2 = np.array([20,100,224])
        #elif theory==2:
        #    theoSlotsB2 = np.append([20,100],[np.arange(200,248),np.arange(300,348),np.arange(400,448)])
        #for i in theoSlotsB2:
        #    plt.plot([i,i],plt.ylim(),'r')
        #plt.ylabel('Theoretical Filling')
        #plt.xlim([0,500])
        plt.ylim([0,1.1])
        plt.xlabel('# SLOTS B2')
        plt.yticks([0,1],['EMPTY','FILLED'])
        plt.tight_layout()
    
    
    
    @staticmethod
    def vistarWireCURRENT(raw_data, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """Plot the current in both the wires.
        """
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux1=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        fig = plt.figure(figsize=(10,8))
        
        ax1 = fig.add_subplot(211)
        plt.step(aux1['RPMC.USC55.RBBCW.L5B2:I_MEAS'].dropna(),'b',lw=3,label='I LEFT')
        plt.ylim([-10,360])
        plt.ylabel('Current [A]')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax2 = fig.add_subplot(212)
        plt.step(aux1['RPMC.UL557.RBBCW.R5B2:I_MEAS'].dropna(),'r',lw=3,label='I RIGHT')
        plt.ylim([-10,360])
        plt.ylabel('Current [A]')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax2.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        
        
        
        
    @staticmethod
    def vistarWirePOSITIONS(distances_mm, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """ Monitor the position of the jaws/wires/beam.
        """
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux2=distances_mm.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        fig = plt.figure(figsize=(20,20))
        
        ax1 = fig.add_subplot(621)
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_RD resampled [mm]'],lw=3,label='RD')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_RU resampled [mm]'],lw=3,label='RU')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_LD resampled [mm]'],lw=3,label='LD')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_LU resampled [mm]'],lw=3,label='LU')
        plt.plot(aux2['Beam Position Upstream (WRT L Tank) [mm]'],'r',lw=3,label='UX')
        plt.plot(aux2['Beam Position Downstream (WRT L Tank) [mm]'],'b',lw=3,label='DX')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT THE TANK')
        plt.grid()
        plt.title('LEFT WIRE')
        plt.legend(loc='best',frameon=True)
        
        ax2 = fig.add_subplot(622)
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_RD resampled [mm]'],lw=3,label='RD')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_RU resampled [mm]'],lw=3,label='RU')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_LD resampled [mm]'],lw=3,label='LD')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_LU resampled [mm]'],lw=3,label='LU')
        plt.plot(aux2['Beam Position Upstream (WRT R Tank) [mm]'],'r',lw=3,label='UX')
        plt.plot(aux2['Beam Position Downstream (WRT R Tank) [mm]'],'b',lw=3,label='DX')
        plt.ylabel('[mm] WRT THE TANK')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax2.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.title('RIGHT WIRE')
        plt.legend(loc='best',frameon=True)
        
        ax3 = fig.add_subplot(623,sharex=ax1)
        plt.plot(-aux2['Average Distance Left Wire Beam [mm]'],lw=3,label='Beam Position')
        plt.plot(plt.xlim(),[12.7,12.7],'--g',lw=3,label='REF 15 sig')
        plt.plot(plt.xlim(),[6.9,6.9],'--k',lw=3,label='REF 6 sig')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        plt.ylabel('[mm] WRT B2')
        myFmt =mdates.DateFormatter('%H:%M')
        ax3.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax4 = fig.add_subplot(624,sharex=ax2)
        plt.plot(-aux2['Average Distance Right Wire Beam [mm]'],lw=3,label='Beam Position')
        plt.plot(plt.xlim(),[-10.4,-10.4],'--g',lw=3,label='REF 9 &\sigma&')
        plt.plot(plt.xlim(),[-7.95,-7.95],'--k',lw=3,label='REF 6 &\sigma&')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax4.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT B2')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax5 = fig.add_subplot(625,sharex=ax1)
        plt.plot((aux2['LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+aux2['LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'])/2,'r',lw=3,label='(XD+XU)/2')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        plt.ylabel('[mm] WRT JAWS')
        myFmt =mdates.DateFormatter('%H:%M')
        ax5.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax6 = fig.add_subplot(626,sharex=ax2)
        plt.plot((aux2['LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+aux2['LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'])/2,'r',lw=3,label='(XD+XU)/2')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax6.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT JAWS')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        
        
        
        
    @staticmethod
    def vistarWireTEMP_PRESS(raw_data, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """ Monitor the temperature of the jaws and the pressure inside the vacuum chamber
        """
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux1=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        fig = plt.figure(figsize=(20,15))
        
        ax1 = fig.add_subplot(421)
        plt.plot(aux1['VGPB.935.4L5.R.PR'],lw=2,label='Pressure')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mbar]')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax2 = fig.add_subplot(422)
        plt.plot(aux1['VGPB.935.4R5.R.PR'],lw=2,label='Pressure')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax2.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mbar]')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax3 = fig.add_subplot(423,sharex=ax1)
        plt.step(aux1['TCL_4L5_B2_TTRD.POSST'].dropna(),'b',lw=3,where='post',label='T RD')
        plt.step(aux1['TCL_4L5_B2_TTRU.POSST'].dropna(),'r',lw=3,where='post',label='T RU')
        plt.step(aux1['TCL_4L5_B2_TTLD.POSST'].dropna(),'m',lw=3,where='post',label='T LD')
        plt.step(aux1['TCL_4L5_B2_TTLU.POSST'].dropna(),'c',lw=3,where='post',label='T LU')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax3.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[deg]')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax4 = fig.add_subplot(424,sharex=ax2)
        plt.step(aux1['TCTPH_4R5_B2_TTRD.POSST'].dropna(),'b',lw=3,where='post',label='T RD')
        plt.step(aux1['TCTPH_4R5_B2_TTRU.POSST'].dropna(),'r',lw=3,where='post',label='T RU')
        plt.step(aux1['TCTPH_4R5_B2_TTLD.POSST'].dropna(),'m',lw=3,where='post',label='T LD')
        plt.step(aux1['TCTPH_4R5_B2_TTLU.POSST'].dropna(),'c',lw=3,where='post',label='T LU')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax4.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[deg]')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        

        
    @staticmethod    
    def vistarWiresStateDashboard(myDF,myDistances, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """To have an overview of the wires states. 
        Input : 
        - my DF : panda DataFrame = raw data
        - myDistances : panda DF = calculated distances
        
        No Output. Only plots. 
        
        """
        
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux1=myDF.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        aux2=myDistances.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        fig = plt.figure(figsize=(20,40))
        
        ax1 = fig.add_subplot(821)
        plt.step(aux1['RPMC.USC55.RBBCW.L5B2:I_MEAS'].dropna(),'b',lw=3,label='I LEFT')
        plt.ylim([-10,360])
        plt.ylabel('Current [A]')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.title('LEFT WIRE')
        plt.legend(loc='best',frameon=True)
        
        ax2 = fig.add_subplot(822)
        plt.step(aux1['RPMC.UL557.RBBCW.R5B2:I_MEAS'].dropna(),'r',lw=3,label='I RIGHT')
        plt.ylim([-10,360])
        plt.ylabel('Current [A]')
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax2.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.title('RIGHT WIRE')
        plt.legend(loc='best',frameon=True)

        ax3 = fig.add_subplot(823,sharex=ax1)
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_RD resampled [mm]'],lw=3,label='MOTOR_RD')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_RU resampled [mm]'],lw=3,label='MOTOR_RU')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_LD resampled [mm]'],lw=3,label='MOTOR_LD')
        plt.plot(aux2['TCL.4L5.B2:MEAS_MOTOR_LU resampled [mm]'],lw=3,label='MOTOR_LU')
        plt.plot(aux2['Beam Position Upstream (WRT L Tank) [mm]'],'r',lw=3,label='UX')
        plt.plot(aux2['Beam Position Downstream (WRT L Tank) [mm]'],'b',lw=3,label='DX')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax3.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT THE TANK')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax4 = fig.add_subplot(824,sharex=ax2)
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_RD resampled [mm]'],lw=3,label='MOTOR_RD')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_RU resampled [mm]'],lw=3,label='MOTOR_RU')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_LD resampled [mm]'],lw=3,label='MOTOR_LD')
        plt.plot(aux2['TCTPH.4R5.B2:MEAS_MOTOR_LU resampled [mm]'],lw=3,label='MOTOR_LU')
        plt.plot(aux2['Beam Position Upstream (WRT R Tank) [mm]'],'r',lw=3,label='UX')
        plt.plot(aux2['Beam Position Downstream (WRT R Tank) [mm]'],'b',lw=3,label='DX')
        plt.ylabel('[mm] WRT THE TANK')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax4.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax5 = fig.add_subplot(825,sharex=ax1)
        plt.plot(-aux2['Average Distance Left Wire Beam [mm]'],lw=3,label='BEAM/WIRE SEP.')
        plt.plot(plt.xlim(),[12.7,12.7],'--g',lw=3,label='REF 15 &\sigma&')
        plt.plot(plt.xlim(),[6.9,6.9],'--k',lw=3,label='REF 6 &\sigma&')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        plt.ylabel('[mm] WRT B2')
        myFmt =mdates.DateFormatter('%H:%M')
        ax5.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax6 = fig.add_subplot(826,sharex=ax2)
        plt.plot(-aux2['Average Distance Right Wire Beam [mm]'],lw=3,label='BEAM/WIRE SEP.')
        plt.plot(plt.xlim(),[-10.4,-10.4],'--g',lw=3,label='REF 9 &\sigma&')
        plt.plot(plt.xlim(),[-7.95,-7.95],'--k',lw=3,label='REF 6 &\sigma&')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax6.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT B2')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        
        ax7 = fig.add_subplot(827,sharex=ax1)
        plt.plot((aux2['LHC.BPTDH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+aux2['LHC.BPTUH.A4L5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'])/2,'r',lw=3,label='(XD+XU)/2')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        plt.ylabel('[mm] WRT JAWS')
        myFmt =mdates.DateFormatter('%H:%M')
        ax5.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        
        ax8 = fig.add_subplot(828,sharex=ax2)
        plt.plot((aux2['LHC.BPTDH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]']+aux2['LHC.BPTUH.A4R5.B2:CALIBCORRECTEDPOS resampled and calibrated [mm]'])/2,'r',lw=3,label='(XD+XU)/2')
        t = np.arange(aux2.index[0],aux2.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax6.xaxis.set_major_formatter(myFmt);
        plt.ylabel('[mm] WRT JAWS')
        plt.grid()
        plt.legend(loc='best',frameon=True)
        plt.xlabel('[hh:mm]')
        

        plt.tight_layout()
        
        
    
    @staticmethod
    def vistarLHCDashBoard(BDF, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """Gives an overview of the situation of both the two beams in the LHC
        Input : 
        - BDF : panda DataFrame = DF containing beams data
        - deltaTimeToConsider_in_minutes : int type = nb of minutes needed
        No output, returns plots.
        
        NB : still a problem with the energy to be solved. 
        """
        
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        fig = plt.figure(figsize=(15,15))
        aux = BDF.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))

        ax1 = fig.add_subplot(411)
        plt.step(aux['LHC.BOFSU:OFC_ENERGY'].fillna(method='bfill'),'k',lw=3)
        plt.ylabel('Energy [GeV]')
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.ylim([0,7000])
        plt.legend(loc='best',frameon=True)


        ax2 = fig.add_subplot(412,sharex=ax1)
        plt.plot(aux['LHC.BCTFR.B6R4.B1:BEAM_INTENSITY'].dropna(),'b',lw=3)
        plt.plot(aux['LHC.BCTFR.B6R4.B2:BEAM_INTENSITY'].dropna(),'r',lw=3)
        plt.ylabel('Intensity')
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax2.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)

        ax3 = fig.add_subplot(413,sharex=ax1)
        plt.plot(aux['LHC.BQBBQ.CONTINUOUS.B2:TUNE_H'],'.r',alpha=0.1)
        plt.plot(aux['LHC.BQBBQ.CONTINUOUS.B1:TUNE_H'],'.b',alpha=0.1)
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax3.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)

        ax4 = fig.add_subplot(414,sharex=ax1)
        plt.plot(aux['LHC.BQBBQ.CONTINUOUS.B2:TUNE_V'],'.r',alpha=0.1)
        plt.plot(aux['LHC.BQBBQ.CONTINUOUS.B1:TUNE_V'],'.b',alpha=0.1)
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        ax4.xaxis.set_major_formatter(myFmt);
        plt.grid()
        plt.legend(loc='best',frameon=True)

        plt.tight_layout()
        
        
        
    @staticmethod
    def vistarBBBLifetime(Lifetime_FBCT_DF, fill, deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now(),beam='B2'):
        """ Vistar for the bunch by bunch lifetime.
        
        Input : 
        - Lifetime_FBCT_DF = panda DataFrame = DF containing BBB lifetime 
        
        No output. Plots only. 
        
        WARNING : NEED TO FIND A WAY TO SELECT ONLY SOME BUNCHES.
        """
        
        
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        
        aux = Lifetime_FBCT_DF.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))

        fig = plt.figure(figsize=(20,20))
        b2 = fig.add_subplot(212)
        t = np.arange(Lifetime_FBCT_DF.index[0],Lifetime_FBCT_DF.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t);
        myFmt =mdates.DateFormatter('%H:%M')
        b2.xaxis.set_major_formatter(myFmt);
        if beam == 'B2':
            slots_B2 = []
            for i in np.arange(len(fill[1])):
                slots_B2.append('slot '+str(fill[1][i])+'_B2')
            for n in slots_B2:
                plt.plot(aux[n],'-^',label=n)
        elif beam == 'B1':
            slots_B1 = []
            for i in np.arange(len(fill[0])):
                slots_B1.append('slot '+str(fill[0][i])+'_B1')
            for n in slots_B1:
                plt.plot(aux[n],'-^',label=n)
                
        plt.xlabel('[hh:mm]')
        #plt.ylim([0,200])
        plt.ylabel('B2 Lifetime [h]')
        plt.legend(loc='best',frameon=True)
        plt.grid()
        
    
    @staticmethod
    def vistarIntensityBBB(intensityWithSeparation,B1 = False, B2 = True, xlim=[0,3563]):
    
        if B1:
            dfB1 = intensityWithSeparation[np.where(intensityWithSeparation.columns.str.contains("_B1"))[0]].resample('60s').mean()/intensityWithSeparation[np.where(intensityWithSeparation.columns.str.contains("_B1"))[0]].iloc[0]
            fig1 = plt.figure(figsize=(20,8))
            plt.pcolor(dfB1,cmap = plt.cm.plasma,vmin=np.nanmin(dfB1), vmax=np.nanmax(dfB1))
            cbar = plt.colorbar()
            cbar.set_label('Normalized Intensity')
            plt.xlim(xlim)
            plt.xlabel('# SLOTS B1')
            plt.ylabel('Time [min]')


        if B2:
            dfB2 = intensityWithSeparation[np.where(intensityWithSeparation.columns.str.contains("_B2"))[0]].resample('60s').mean()/intensityWithSeparation[np.where(intensityWithSeparation.columns.str.contains("_B2"))[0]].iloc[0]
            fig2 = plt.figure(figsize=(20,8))
            plt.pcolor(dfB2,cmap = plt.cm.plasma,vmin=np.nanmin(dfB2), vmax=np.nanmax(dfB2))
            cbar = plt.colorbar()
            cbar.set_label('Normalized Intensity')
            plt.xlim(xlim)
            plt.xlabel('# SLOTS B2')
            plt.ylabel('Time [min]')
            
            
    @staticmethod
    def vistarBBCWCompensation_XSection(raw_data,Xsection,fill,deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now(),mode='wire',ylim=[-10,200]):
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        aux1=Xsection.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        slots = aux1.columns.values

        fig = plt.figure(figsize=(20,10))

        ax = fig.add_subplot(111)
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./12)).astype(datetime.datetime)
        plt.xticks(t)
        myFmt =mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
   
        slots_B2 = []
        for i in np.arange(len(fill[1])):
            slots_B2.append('slot '+str(fill[1][i])+'_B2')
        for n in slots_B2:
            plt.plot(aux1[n],'-^',label=n)
        slots_B1 = []
        for i in np.arange(len(fill[0])):
            slots_B1.append('slot '+str(fill[0][i])+'_B1')
        for n in slots_B1:
            plt.plot(aux1[n],'-^',label=n)
        
        plt.legend(loc='upper left',frameon=True)
        plt.grid(linestyle='--')
        ax.plot(plt.xlim(),[80,80],'--k',label='$\\sigma_{pp} = 80 mb$')
        ax.set_ylim(ylim)
        ax.set_ylabel('Eff Cross-Section [mb]')
        ax.set_xlabel('[hh:mm]')
        
        if mode=='wire':
            ax1 = ax.twinx()
            ax1.step(raw_data['RPMC.UL557.RBBCW.R5B2:I_MEAS'],'r',lw=3)
            ax1.step(raw_data['RPMC.USC55.RBBCW.L5B2:I_MEAS'],'b',lw=3)
            ax1.set_ylabel('Wire Current [A]')
            ax1.set_ylim([-10,360])
            ax1.yaxis.label.set_color('r')
            ax1.tick_params(axis='y', colors='r')
        elif mode=='octupole':
            ax1 = ax.twinx()
            ax1.step(raw_data['RPMBB.RR17.ROF.A12B1:I_REF'],'-',where='post',lw=3)
            ax1.step(raw_data['RPMBB.RR17.ROF.A12B2:I_REF'],'-',where='post',lw=3)
            ax1.step(raw_data['RPMBB.RR17.ROD.A12B1:I_REF'],'-',where='post',lw=3)
            ax1.step(raw_data['RPMBB.RR17.ROD.A12B2:I_REF'],'-',where='post',lw=3)
            ax1.set_ylabel('Octupole Current [A]')
            ax1.set_ylim([-600,600])
            ax1.tick_params(axis='y', colors='k')
        plt.legend(loc='lower left',frameon=True)
        
        plt.xlim(t1,t2)
        return fig
        
        
    @staticmethod
    def vistarBBCWCompensation_lifetime(raw_data,lifetime,fill,deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now(),mode='wire',ylim=[0,100]):
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        aux1=lifetime.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        slots = aux1.columns.values

        fig = plt.figure(figsize=(20,10))

        ax = fig.add_subplot(111)
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./12)).astype(datetime.datetime)
        plt.xticks(t)
        myFmt =mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        slots_B2 = []
        for i in np.arange(len(fill[1])):
            slots_B2.append('slot '+str(fill[1][i])+'_B2')
        for n in slots_B2:
            plt.plot(aux1[n],'-^',label=n)
        slots_B1 = []
        for i in np.arange(len(fill[0])):
            slots_B1.append('slot '+str(fill[0][i])+'_B1')
        for n in slots_B1:
            plt.plot(aux1[n],'-^',label=n)       
        plt.legend(loc='upper left',frameon=True)
        plt.grid(linestyle='--')
        ax.set_ylim(ylim)
        ax.set_ylabel('Lifetime [h]')
        ax.set_xlabel('[hh:mm]')
        
        if mode=='wire':
            ax1 = ax.twinx()
            ax1.step(aux['RPMC.UL557.RBBCW.R5B2:I_MEAS'],'r',lw=3)
            ax1.step(aux['RPMC.USC55.RBBCW.L5B2:I_MEAS'],'b',lw=3)
            ax1.set_ylabel('Wire Current [A]')
            ax1.set_ylim([-10,360])
            ax1.yaxis.label.set_color('r')
            ax1.tick_params(axis='y', colors='r')
        elif mode=='octupole':
            ax1 = ax.twinx()
            ax1.step(aux['RPMBB.RR17.ROF.A12B1:I_REF'],'-',where='post',lw=3)
            ax1.step(aux['RPMBB.RR17.ROF.A12B2:I_REF'],'-',where='post',lw=3)
            ax1.step(aux['RPMBB.RR17.ROD.A12B1:I_REF'],'-',where='post',lw=3)
            ax1.step(aux['RPMBB.RR17.ROD.A12B2:I_REF'],'-',where='post',lw=3)            
            ax1.set_ylabel('Octupole Current [A]')
            ax1.set_ylim([-600,600])
            ax1.tick_params(axis='y', colors='k')
        plt.legend(loc='lower left',frameon=True)
        
        plt.xlim(t1,t2)
        
        
    @staticmethod
    def vistarBBCWCompensation_losses(raw_data,ratio,deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        aux1=ratio.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        slots = aux1.columns.values

        fig = plt.figure(figsize=(20,10))

        ax = fig.add_subplot(111)
        t = np.arange(aux1.index[0],aux1.index[-1], datetime.timedelta(hours=1./12)).astype(datetime.datetime)
        plt.xticks(t)
        myFmt =mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        ax.plot(ratio,lw=3)
        plt.legend(loc='upper left',frameon=True)
        plt.grid(linestyle='--')
        ax.set_ylim([0,2])
        ax.set_ylabel('Ratio Losses')
        ax.set_xlabel('[hh:mm]')
        ax1 = ax.twinx()
        ax1.step(raw_data['RPMC.UL557.RBBCW.R5B2:I_MEAS'],'r',lw=3)
        ax1.step(raw_data['RPMC.USC55.RBBCW.L5B2:I_MEAS'],'b',lw=3)
        ax1.set_ylabel('Wire Current [A]')
        ax1.set_ylim([-10,360])
        ax1.yaxis.label.set_color('r')
        ax1.tick_params(axis='y', colors='r')
        
        plt.xlim(t1,t2)
        
        
    @staticmethod
    def vistarOctupoles(raw_data,deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """ Display the current in the octupoles
        """
        fig = plt.figure()
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        ax = fig.add_subplot(111)
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t)
        myFmt =mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        ax.step(aux['RPMBB.RR17.ROF.A12B1:I_REF'],'-',where='post',lw=3)
        ax.step(aux['RPMBB.RR17.ROF.A12B2:I_REF'],'-',where='post',lw=3)
        ax.step(aux['RPMBB.RR17.ROD.A12B1:I_REF'],'-',where='post',lw=3)
        ax.step(aux['RPMBB.RR17.ROD.A12B2:I_REF'],'-',where='post',lw=3)
        
        plt.ylim([-600,600])
        plt.xlim([t1,t2])
        plt.ylabel('Octupole Current [A]')
        plt.xlabel('[hh:mm]')
        plt.legend(loc='best',frameon=True)
        
        
    @staticmethod
    def vistarCrossingAngle(raw_data,deltaTimeToConsider_in_minutes=60,startTime=datetime.datetime.now()):
        """ Display the current in the octupoles
        """
        fig = plt.figure()
        t1=startTime-datetime.timedelta(minutes=deltaTimeToConsider_in_minutes)
        t2=startTime
        aux=raw_data.between_time(datetime.date.strftime(t1,format="%H:%M"),datetime.date.strftime(t2,format="%H:%M"))
        ax = fig.add_subplot(111)
        t = np.arange(aux.index[0],aux.index[-1], datetime.timedelta(hours=1./6)).astype(datetime.datetime)
        plt.xticks(t)
        myFmt =mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        ax.step(aux['LHC.RUNCONFIG:IP5-XING-H-MURAD'],'-',where='post',lw=3,label='IP5')
        ax.step(aux['LHC.RUNCONFIG:IP1-XING-V-MURAD'],'-',where='post',lw=3,label='IP1')
        
        plt.ylim([0,200])
        plt.xlim([t1,t2])
        plt.ylabel('Half Crossing Angle [$\\mu$rad]')
        plt.xlabel('[hh:mm]')
        plt.legend(loc='best',frameon=True)
        
        

            
###===========================================================================================================================###
###                                                     CHECKS                                                                ###
###===========================================================================================================================###


    @staticmethod
    def checkVerticalAlignment(verticalAlignementDF,t1,t2,TCTPH=True,plot=False):
        """ Use this function to check the vertical alignement. 
        For TCTPH, set TCTPH=True. For TCL, TCTPH = False.
        Please fill the times as 'HH:MM'.
        Plot=True to see the plots. 
        """

        aux = verticalAlignementDF.between_time(t1,t2)

        if TCTPH:
            #DOWNSTREAM
            xD = aux['TCTPH.4R5.B2:MEAS_V_LVDT_POS_resampled'].values
            #myFilter1 = aux['LHC.BPTDH.A4R5.B2:HORRAWVALUEV1_resampled']>0
            #myFilter2 = aux['LHC.BPTDH.A4R5.B2:HORRAWVALUEV2_resampled']>0
            yD = aux['LHC.BPTDH.A4R5.B2:CALIBRAWVALV1_resampled'] + aux['LHC.BPTDH.A4R5.B2:CALIBRAWVALV2_resampled']
            #yD = yD.fillna(method='ffill')
            #yD.iloc[0] = yD.iloc[1]
            yD = yD.values

            pD = np.polyfit(xD,yD,deg=2)

            fitD = pD[2] + pD[1]*xD + pD[0]*(xD**2)

            valMaxD = xD[(np.where(fitD == fitD.max()))[0]]

            print('TCTPH DOWNSTREAM : Max reached in y = {}'.format(float(valMaxD))+' mm')

            #UPSTREAM
            #myFilter1 = aux['LHC.BPTUH.A4R5.B2:HORRAWVALUEV1_resampled']>0
            #myFilter2 = aux['LHC.BPTUH.A4R5.B2:HORRAWVALUEV2_resampled']>0
            xU = aux['TCTPH.4R5.B2:MEAS_V_LVDT_POS_resampled'].values
            yU = aux['LHC.BPTUH.A4R5.B2:CALIBRAWVALV1_resampled'] + aux['LHC.BPTUH.A4R5.B2:CALIBRAWVALV2_resampled']
            #yU = yU.fillna(method='ffill')
            #yU.iloc[0] = yU.iloc[1]
            yU = yU.values

            pU = np.polyfit(xU,yU,deg=2)

            fitU = pU[2] + pU[1]*xU + pU[0]*(xU**2)

            valMaxU = xU[(np.where(fitU == fitU.max()))[0]]

            print('TCTPH UPSTREAM : Max reached in y = {}'.format(float(valMaxU))+' mm')

            #AVERAGE
            valMaxAverage = (valMaxU + valMaxD)/2
            diff = valMaxU-valMaxD
            print('TCTPH AVERAGE : Max reached in y = {}'.format(float(valMaxAverage))+' mm')
            print('TCTPH DIFFERENCE U/D : {}'.format(diff)+' mm')
            print('TCTPH V MOTORS : APPLY THE OFFSET = {}'.format(-float(valMaxAverage))+' mm')

        else:
            #DOWNSTREAM
            xD = aux['TCL.4L5.B2:MEAS_V_LVDT_POS_resampled'].values
            #myFilter1 = aux['LHC.BPTDH.A4L5.B2:HORRAWVALUEV1_resampled']>0
            #myFilter2 = aux['LHC.BPTDH.A4L5.B2:HORRAWVALUEV2_resampled']>0
            yD = aux['LHC.BPTDH.A4L5.B2:CALIBRAWVALV1_resampled'] + aux['LHC.BPTDH.A4L5.B2:CALIBRAWVALV2_resampled']
            #yD = yD.fillna(method='ffill')
            #yD.iloc[0] = yD.iloc[1]
            yD = yD.values

            pD = np.polyfit(xD,yD,deg=2)

            fitD = pD[2] + pD[1]*xD + pD[0]*(xD**2)

            valMaxD = xD[(np.where(fitD == fitD.max()))[0]]

            print('TCL DOWNSTREAM : Max reached in y = {}'.format(float(valMaxD))+' mm')

            #UPSTREAM
            #myFilter1 = aux['LHC.BPTUH.A4L5.B2:HORRAWVALUEV1_resampled']>0
            #myFilter2 = aux['LHC.BPTUH.A4L5.B2:HORRAWVALUEV2_resampled']>0
            xU = aux['TCL.4L5.B2:MEAS_V_LVDT_POS_resampled'].values
            yU = aux['LHC.BPTUH.A4L5.B2:CALIBRAWVALV1_resampled'] + aux['LHC.BPTUH.A4L5.B2:CALIBRAWVALV2_resampled']
            #yU = yU.fillna(method='ffill')
            #yU.iloc[0] = yU.iloc[1]
            yU = yU.values

            pU = np.polyfit(xU,yU,deg=2)

            fitU = pU[2] + pU[1]*xU + pU[0]*(xU**2)

            valMaxU = xU[(np.where(fitU == fitU.max()))[0]]

            print('TCL UPSTREAM : Max reached in y = {}'.format(float(valMaxU))+' mm')

            #AVERAGE
            valMaxAverage = (valMaxU + valMaxD)/2
            diff = valMaxU-valMaxD
            print('TCL AVERAGE : Max reached in y = {}'.format(float(valMaxAverage))+' mm')
            print('TCL DIFFERENCE U/D : {}'.format(diff)+' mm')
            print('TCL V MOTORS : APPLY THE OFFSET = {}'.format(-float(valMaxAverage))+' mm')

        if plot:
            figD = plt.figure()
            plt.plot(xD,yD,'ro',lw=2,label='Measured')
            plt.plot(xD,fitD,'b-',lw=2,label='Fit')
            plt.xlabel('5th-axis position [mm]')
            plt.ylabel('PUs reading [mm]')
            plt.title('DOWNSTREAM')
            plt.legend(loc='best',frameon=True)

            figU = plt.figure()
            plt.plot(xU,yU,'ro',lw=2,label='Measured')
            plt.plot(xU,fitU,'b-',lw=2,label='Fit')
            plt.xlabel('5th-axis position [mm]')
            plt.ylabel('PUs reading [mm]')
            plt.title('UPSTREAM')
            plt.legend(loc='best',frameon=True)

    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
### TO BE DONE
    
    
    @staticmethod    
    def computeDistancesInSigma(myDF):
        return myDF
    
  
    
    
        
        
    
    
        
    






   