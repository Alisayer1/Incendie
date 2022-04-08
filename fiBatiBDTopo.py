resol=10
chem="B:/Perso/Etudes/MEDSTAR-INTERMED/ModeleRisque/WS/"


shploc=chem+"batiBDtopo.shp"
table = chem+"fiBatiBDTopo.tab"
fBiBDTopo=chem+"fBiBDTopo.tif"

champ = "bati"
outrastbat = chem+"bati.tif"

tifIgnitionsConstantes = "igniSurBati"

try:
	x=0
	chem=param.ws; x+=1
	chemTables=param.chemTables; x+=1
	champPoids=param.champPoidsIgni
	rad=param.radbati
	print("fi"+rad+": param ok")
	
except Exception:
	print(script+": Erreurs parametres "+str(x))
	exit()
	
tifdespoidslocaux = chem+rad+".tif"
shpInitial=chem+rad+".shp"
table = chemTables+"fi"+rad+".tab"
outtif=chem+"fi"+rad+"Norm.tif"
champsOri=["NATURE", "IMPORTANCE"]

calculeRasterDeFacteur(shpInitial, champPoids, champsOri, table, tifdespoidslocaux, outtif, bconvole=True, bcreuse=False, force=True, champSelDesSources="Largeur", seuilDesSources=10, poidsDesSources=0.1)

coefs = litTable(table, False)
if (len(coefs[3]) >0):
	try:
		coef = float(coefs[4])
		if (coef > 0):
			outfi = chem+tifIgnitionsConstantes+rad+".tif"
			lst=litFichierTiff(tifdespoidslocaux)
			rast=lst[0]
			outrast = np.zeros(shape=(lst[2], lst[1]))
			outrast[ ( rast > 0 ) ] = ( coef * rast[ rast > 0 ] )
			genereTiff(outrast, outfi, modeletif=tifdespoidslocaux)

exit(0)

if not isfile(outrastbat):
	if ( estChamp(shploc, champ) ) :
		rasteriseShapeFile(shploc, refrast, outrastbat, champ)
	else:
		print(field +" absent de "+shp)

if isfile(outrastbat):
	tup = litFichierTiff(outrastbat)
	if (len(tup)>0):
		raster=tup[0]
		W = tup[1]
		H = tup[2]
		xul = tup[3]
		yul = tup[4]
		resol = tup[5]

		print("Convolve 5x5")
		weights = np.ones((5, 5))
		#voir outil.py:filtreCirculaire(dim) pour un filtre discoidal
		raster[(raster < 0)]=0
		focal_mean = convolve(raster, weights) / np.sum(weights)
		litValeursRaster(focal_mean, -9999)
		fBi = normalisation(focal_mean)
		genereTiff(fBi, fBiBDTopo, xul, yul, resol)
	
litFichierTiff(fBiBDTopo)
exit(0)

try:
	x=0
	chem=param.ws; x+=1
	chemTables=param.chemTables; x+=1
	champPoids=param.champPoidsIgni
	rad=param.radbati
	print("fi"+rad+": param ok")
	
except Exception:
	print("fi"+rad+": Erreurs parametres "+str(x))
	exit()
outrast = chem+rad+".tif"
shpInitial=chem+"rteBDTOPO.shp"
table = chemTables+"fi"+rad+".tab"
outtif=chem+"fi"+rad+"Norm.tif"
champsOri=["NATURE", "IMPORTANCE"]

calculeRasterDeFacteur(shpInitial, champPoids, champsOri, table, outrast, outtif, bconvole=True, bcreuse=False, force=True, champSelDesSources="Surface", seuilDesSources=100, poidsDesSources=0.1)
