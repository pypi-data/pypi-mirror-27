#### magnetmatter ####
Material Science Research Data Visualization.
FullProf .prf, .out and .pcr files are read and informations on 
	refined parameters, 
	phases, 
	appearent crystalline sizes
	phase fractions 
are hardcoded next to the graph of "Yobs", "Ycal" and "Yobs-Ycal".

#### HOW TO INSTALL ####
This installation assumes that you have a plain python (version > 3.0) installed that can be accessed through the command prompt.
If on Ubuntu/MacTos, python 2.7 will be preinstalled. Then use "python3" and "pip3" for all purposes.

	pip install magnetmatter

#### HOW TO USE ####
once it has been installed along with dependencies ("numpy", "pandas", "matplotlib", it may take a while, be patient), type python/python3 in command prompt. then type
    
    import magnetmatter as mogens

this may also take a while to load everything. Type now

    path = r"C:\give\a\valid\path\to\folder\with\datasubfolders\"
    mogens.plot_prf(path)

The default printed size is 8 cm (two plots fit into a docx document). other options include:

	mogens.plot_prf(path, printsize = "two_in_docx") # 8  cm wide
	mogens.plot_prf(path, printsize = "one_in_docx") # 15 cm wide
	mogens.plot_prf(path, printsize = "two_in_ppt")  # 17 cm wide
	mogens.plot_prf(path, printsize = "one_in_ppt")  # 32 cm wide
	
The files are saved as .png in the "path" folder.

#### HOW SHOULD FILES BE ORGANIZED ####
The script goes into each subfolder and looks for an .out, a .pcr and a .prf file. 
If no such files are found (or if indeed multiple files are found), the script will skip the respective folder.

./
│   CoKa_BB_ISx.irf
│   CoKa_PB_ISxmm.irf
│   FS_17nm_R1D1.png
│   FS_8nm_R1D1.png
│
├───FS_17nm_R1D1
│   │   size_bigger_10nm.dat
│   │   size_bigger_10nm.ras
│   │   size_bigger_10nm_Theta_2-Theta.asc
│   │   size_bigger_10nm_Theta_2-Theta.raw
│   │   _gFe2O3_Fe3O4_.out
│   │   _gFe2O3_Fe3O4_.pcr
│   │   _gFe2O3_Fe3O4_.prf
│   │   _gFe2O3_Fe3O4_.sum
│   │   _gFe2O3_Fe3O4_1.fst
│   │   _gFe2O3_Fe3O4_1.mic
│   │   _gFe2O3_Fe3O4_2.fst
│   │   _gFe2O3_Fe3O4_2.mic
│   │
│   └───backup
│           _gFe2O3_Fe3O4_.pcr
│
└───FS_8nm_R1D1
    │   size_smaller_10nm.dat
    │   size_smaller_10nm.ras
    │   size_smaller_10nm_Theta_2-Theta.asc
    │   size_smaller_10nm_Theta_2-Theta.raw
    │   _gFe2O3_Fe3O4_.out
    │   _gFe2O3_Fe3O4_.pcr
    │   _gFe2O3_Fe3O4_.prf
    │   _gFe2O3_Fe3O4_.sum
    │   _gFe2O3_Fe3O4_1.fst
    │   _gFe2O3_Fe3O4_1.mic
    │   _gFe2O3_Fe3O4_2.fst
    │   _gFe2O3_Fe3O4_2.mic
    │
    └───backup
            _gFe2O3_Fe3O4_.pcr
 			
#### NEW FORMAT OF PCR FILE ####
The new FullProf .pcr format is expected. 
Make sure that you have this format by using the FullProf toolbar: 

	"EdPCR">>"output">>unclick"Classical Output Format for a Single Pattern in PCR".
