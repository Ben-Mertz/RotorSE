------- OpenFAST INPUT FILE -------------------------------------------
AeroElasticSE FAST driver
---------------------- SIMULATION CONTROL --------------------------------------
True                   Echo        - Echo input data to <RootName>.ech (flag)
"FATAL"                AbortLevel  - Error level when simulation should abort (string) {"WARNING", "SEVERE", "FATAL"}
360.0                  TMax        - Total run time (s)
0.01                   DT          - Recommended module time step (s)
2                      InterpOrder - Interpolation order for input/output time history (-) {1=linear, 2=quadratic}
0                      NumCrctn    - Number of correction iterations (-) {0=explicit calculation, i.e., no corrections}
99999.0                DT_UJac     - Time between calls to get Jacobians (s)
1000000.0              UJacSclFact - Scaling factor used in Jacobians (-)
---------------------- FEATURE SWITCHES AND FLAGS ------------------------------
1                      CompElast   - 
1                      CompInflow  - 
2                      CompAero    - 
1                      CompServo   - 
0                      CompHydro   - 
0                      CompSub     - 
0                      CompMooring - 
0                      CompIce     - 
---------------------- INPUT FILES ---------------------------------------------
"RotorSE_FAST_BAR_005a_1_ElastoDyn.dat" EDFile      - Name of file containing ElastoDyn input parameters (quoted string)
"../5MW_Baseline/NRELOffshrBsline5MW_BeamDyn.dat" BDBldFile(1) - Name of file containing BeamDyn input parameters for blade 1 (quoted string)
"../5MW_Baseline/NRELOffshrBsline5MW_BeamDyn.dat" BDBldFile(2) - Name of file containing BeamDyn input parameters for blade 2 (quoted string)
"../5MW_Baseline/NRELOffshrBsline5MW_BeamDyn.dat" BDBldFile(3) - Name of file containing BeamDyn input parameters for blade 3 (quoted string)
"RotorSE_FAST_BAR_005a_1_InflowFile.dat" InflowFile  - Name of file containing inflow wind input parameters (quoted string)
"RotorSE_FAST_BAR_005a_1_AeroDyn15.dat" AeroFile    - Name of file containing aerodynamic input parameters (quoted string)
"RotorSE_FAST_BAR_005a_1_ServoDyn.dat" ServoFile   - Name of file containing control and electrical-drive input parameters (quoted string)
"unused"               HydroFile   - Name of file containing hydrodynamic input parameters (quoted string)
"unused"               SubFile     - Name of file containing sub-structural input parameters (quoted string)
"unused"               MooringFile - Name of file containing mooring system input parameters (quoted string)
"unused"               IceFile     - Name of file containing ice input parameters (quoted string)
---------------------- OUTPUT --------------------------------------------------
True                   SumPrint    - Print summary data to "<RootName>.sum" (flag)
5.0                    SttsTime    - Amount of time between screen status messages (s)
99999.0                ChkptTime   - Amount of time between creating checkpoint files for potential restart (s)
"default"              DT_Out      - Time step for tabular output (s) (or "default")
120.0                  TStart      - Time to begin tabular output (s)
2                      OutFileFmt  - Format for tabular (time-marching) output file (switch) {1: text file [<RootName>.out], 2: binary file [<RootName>.outb], 3: both}
True                   TabDelim    - Use tab delimiters in text tabular output file? (flag) {uses spaces if false}
"ES10.3E2"             OutFmt      - Format used for text tabular output, excluding the time channel.  Resulting field should be 10 characters. (quoted string)
---------------------- LINEARIZATION -------------------------------------------
False                  Linearize   - Linearization analysis (flag)
2                      NLinTimes   - Number of times to linearize (-) [>=1] [unused if Linearize=False]
30, 60                 LinTimes    - List of times at which to linearize (s) [1 to NLinTimes] [unused if Linearize=False]
1                      LinInputs   - Inputs included in linearization (switch) {0=none; 1=standard; 2=all module inputs (debug)} [unused if Linearize=False]
1                      LinOutputs  - Outputs included in linearization (switch) {0=none; 1=from OutList(s); 2=all module outputs (debug)} [unused if Linearize=False]
False                  LinOutJac   - Include full Jacobians in linearization output (for debug) (flag) [unused if Linearize=False; used only if LinInputs=LinOutputs=2]
False                  LinOutMod   - Write module-level linearization output files in addition to output for full system? (flag) [unused if Linearize=False]
---------------------- VISUALIZATION ------------------------------------------
0                      WrVTK       - VTK visualization data output: (switch) {0=none; 1=initialization data only; 2=animation}
1                      VTK_type    - Type of VTK visualization data: (switch) {1=surfaces; 2=basic meshes (lines/points); 3=all meshes (debug)} [unused if WrVTK=0]
True                   VTK_fields  - Write mesh fields to VTK data files? (flag) {true/false} [unused if WrVTK=0]
15.0                   VTK_fps     - Frame rate for VTK output (frames per second){will use closest integer multiple of DT} [used only if WrVTK=2]
