#include"TCanvas.h"
#include"TGraphErrors.h"
#include"TFile.h"
#include"TF1.h"
#include"TCanvas.h"
#include"TH1.h"
#include"TH2.h"
#include"TLegend.h"
#include"TArrow.h"
#include"TLatex.h"
#include"TSystemDirectory.h"
#include"TDirectory.h"
#include"TKey.h"

#include <fstream>
#include <iostream>
#include <cstdio>
#include <unistd.h>
#include <utility>
#include <vector>
#include <algorithm>
#include <sstream>
#include <functional>
#include <string>
#include <numeric>

int eff(){
    
    	cout << "Starting Efficency Script" << endl;

	char chpath[256];
    	getcwd(chpath, 255);
	std::string path = chpath;
    	std::string mod("mh143");//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
	// <<<<<< change folder/module name to run in 
	//std::string mod("yhc691015sn3p35");

	std::string dataPath =  path + "/" + mod + "data";
    	//std::string measurementFolder =  mod + "data";
	std::string configPath = path + "/" + mod; 
	std::string HighRateSaveFileName( "Results_"+ mod );
	std::string HighRateFileName( "hr" );//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 
	int namelength = HighRateFileName.length();
	// <<<<<<<<<<<<<<<<<<<  change Highrate File name to use
    	//  assumes something like hr08ma_pa225_082715.root
    	//  10 or 08 or 06 or 04 or 02 required after hr
    	//      --   looks for a root file  with "HighRateFileName" followed by 10 or 08 or ect....
    	//      --   so will parse hr10****.root and hr08**********.root ect...  with above settings
    	std::string moduleName = mod;

	std::string maskFileName("defaultMaskFile.dat");

	const bool FIDUCIAL_ONLY = true; // don't change
	const bool VERBOSE = true;

	int nTrigPerPixel = 50; // will be read from testParameters.dat
	int nPixels = 4160;
	int nTrig = nTrigPerPixel * nPixels;
	float pixelArea = 0.01 * 0.015; // cm^2
	float triggerDuration = 25e-9; //s

	const int nRocs = 16;
	const int nDCol = 25;
	
	double worstDCol[nRocs];
	for( int i = 0; i<nRocs; i++) worstDCol[i] = 0;
	double worstDColEff[nRocs];
        for( int i = 0; i<nRocs; i++) worstDColEff[i] = 1.0;

	std::string directoryList = mod;

	std::string outFileName = dataPath + "/" + HighRateFileName + "Efficiency.log";
        std::ofstream log(outFileName.c_str());


	cout << "search for HREfficiency folders in elComandante folder structure" << endl;
    	log << "High Rate Efficency Log File Module: "<< mod << endl << endl;
	TSystemDirectory dir(dataPath.c_str(), dataPath.c_str());
    	TList *files = dir.GetListOfFiles();
    	std::vector<std::string> fileList;
    	if (files) {
      		TSystemFile *file;
      		TString fname;
      		TIter next(files);
      		while (file=(TSystemFile*)next()) {
        		fname = file->GetName();
			std::cout << fname << endl;
         		std::string filename = fname.Data();
			if (filename.substr(0,namelength) == HighRateFileName ) {
				if( filename.substr(( filename.length() - 4 ), 4)  == "root" ){
         				fileList.push_back(filename);
					std::cout << "---Added to fileList" << endl;
				}
         		}
      		}
    	}


        std::vector<double> ylist;
        ylist.push_back(1.0);
        ylist.push_back(0.8);
        ylist.push_back(0.6);
        ylist.push_back(0.4);
        ylist.push_back(0.2);

	std::cout << " Declaring vectors" << endl;

    	std::vector< std::vector< std::pair< int,int > > > maskedPixels;
	std::vector< std::vector< double > > efficiencies;
	std::vector< std::vector< double > > efficiencyErrors;
	std::vector< std::vector< double > > rates;
	std::vector< std::vector< double > > rateErrors;
        std::vector< std::vector< std::vector< double > > > byAmpEfficiencies;
        std::vector< std::vector< std::vector< double > > > byAmpEfficiencyErrors;
        std::vector< std::vector< std::vector< double > > > byAmpRates;
        std::vector< std::vector< std::vector< double > > > byAmpRateErrors;
	std::vector< std::vector< std::vector< double > > > dcolHits;
	std::vector< std::vector< std::vector< double > > > dcolHitErrors;
	std::vector< std::vector< std::vector< double > > > dcolRates;
        std::vector< std::vector< std::vector< double > > > dcolRateErrors;
        std::vector< std::vector< std::vector< double > > > dcolEff;
        std::vector< std::vector< std::vector< double > > > dcolEffErrors;

	std::vector< std::vector< double > > lineList;

	std::vector< std::vector< double > > bigempty; 
	std::vector< double > empty;

	std::cout << " Line Lists" << endl;
	for( int i=0; i <4; i++ ){
		lineList.push_back(empty);
	}

	for( int i = 0; i<201;i++){
		lineList[1].push_back(.98);
		lineList[0].push_back(i);
	}

	for( int i = 0; i<= 100; i++ ){
		lineList[3].push_back(i/100);
		lineList[2].push_back(120.0);
	} 

	std::cout << "byamp inits" << endl;

	for (int i=0;i<=5;i++){
		byAmpEfficiencies.push_back(bigempty);
                byAmpEfficiencyErrors.push_back(bigempty);
                byAmpRates.push_back(bigempty);
                byAmpRateErrors.push_back(bigempty);
	}

	std::cout << "initilizing 2 tier" << endl;

	for( int i=0; i<=5; i++){
		for( int j=0;j<=nRocs;j++){
                        byAmpEfficiencies[i].push_back(empty);
                        byAmpEfficiencyErrors[i].push_back(empty);
                        byAmpRates[i].push_back(empty);
                        byAmpRateErrors[i].push_back(empty);
                }
	}
	
        std::cout << "initilizing 1 tier" << endl;

	for (int i=0;i<=nRocs;i++) {
		efficiencies.push_back(empty);
		efficiencyErrors.push_back(empty);
		rates.push_back(empty);
		rateErrors.push_back(empty);
		dcolHits.push_back(bigempty);
         	dcolHitErrors.push_back(bigempty);
	        dcolRates.push_back(bigempty);
                dcolRateErrors.push_back(bigempty);
                dcolEff.push_back(bigempty);
                dcolEffErrors.push_back(bigempty);
	}
	

	for( int i=0; i<=nRocs; i++){
		for( int j=0; j<=nDCol; j++){
			dcolHits[i].push_back(empty);
			dcolHitErrors[i].push_back(empty);
	                dcolRates[i].push_back(empty);
	                dcolRateErrors[i].push_back(empty);
                	dcolEff[i].push_back(empty);
                	dcolEffErrors[i].push_back(empty);
		}
	}


	std::cout << "loop over all commander_HREfficiency.root root files" << endl;
	for (int i=0;i<1;++i) {
		chdir(path.c_str());
		std::cout << "looking in directory <" << directoryList << ">" << std::endl;
		std::cout << "From " << path << endl;
		std::string parmFile = directoryList + "/testParameters.dat";
		cout << "For " << parmFile << endl;
		std::ifstream testParameters(parmFile.c_str());
		std::string line2;
		cout << "Getting line" << endl;
	
		while (getline(testParameters, line2)) {
			cout << line2 << endl;
			if (line2.find("HighRate") != std::string::npos) {
				while (getline(testParameters, line2)) {
					if (line2.size() < 1) break;
					size_t pos = line2.find("Ntrig");
					std::cout << line2 << " " << pos << endl;
					if (pos != std::string::npos) {
						nTrigPerPixel = atoi(line2.substr(pos+6).c_str());
						nTrig = nTrigPerPixel * nPixels;
						std::cout << ">" << line2 << "< pos:" << pos << std::endl;
						std::cout << "number of triggers per pixel: " << nTrigPerPixel << std::endl;
					}
				}

			}
		}
		testParameters.close();


		// read masked pixels
	    	maskedPixels.clear();
		for (int j=0;j<nRocs;j++) {
			std::vector< std::pair<int,int> > rocMaskedPixels;
			maskedPixels.push_back(rocMaskedPixels);
		}
		std::ifstream maskFile;
		char maskFilePath[256];
		sprintf(maskFilePath, "%s/%s/%s", path.c_str(), directoryList.c_str(), maskFileName.c_str());
		maskFile.open(maskFilePath, std::ifstream::in);
		if (!maskFile) {
			std::cout << "ERROR: mask file <" << maskFilePath << "> can't be opened!"<<std::endl;
		}
		std::string line;
		std::vector< std::string > tokens;
		while(getline(maskFile, line)) {
			if (line[0] != '#') {
				std::stringstream ss(line); 
	    			std::string buf;
	    			tokens.clear();
				while (ss >> buf) {
					tokens.push_back(buf);
				}
				std::cout << "tok0 <" << tokens[0] << "> ";
				if (tokens[0] == "pix" && tokens.size() >= 4) {
					int roc = atoi(tokens[1].c_str());
					int col = atoi(tokens[2].c_str());
					int row = atoi(tokens[3].c_str());
					std::cout << "mask pixel " << roc << " " << col << " " << row << std::endl;
					maskedPixels[roc].push_back(std::make_pair(col, row));
				}
			}
		}
		maskFile.close();
	}

	chdir( dataPath.c_str() );
        int len = fileList.size();
	std::string blank(" ");
	std::vector< std::string > listTFile;
	listTFile.push_back( blank );
        listTFile.push_back( blank );
        listTFile.push_back( blank );
        listTFile.push_back( blank );
        listTFile.push_back( blank );

	cout << "Sorting T file list " << endl;

	for( int i=0; i<len; i++){

		std::string currentRootFile = fileList[i];		
		std::string fileRate = currentRootFile.substr(namelength,2);
		std::cout<< " Looking for: " << fileRate << endl;
		if(fileRate == "10") { rateIndex = 0;}
		else if( fileRate == "08"){ rateIndex = 1;}
		else if( fileRate == "06"){ rateIndex = 2;}
		else if( fileRate == "04"){ rateIndex = 3;}
		else if( fileRate == "02"){ rateIndex = 4;}
		else {
			std::cout << "could not read rate: " << currentRootFile << " .";
			exit(0);
		}
		listTFile[rateIndex]=currentRootFile;
	}

	std::cout<< "Processing  HR files: quanity: " << len << endl;	                                
	log << "Double Column's with Efficency < 90 % " << endl;
	for (int i=0; i<len ; ++i) {

		int rateIndex = 0;		
                int dColModCount = 0;

		std::string currentRootFile = listTFile[i];	
		std::cout << "Working file : " << currentRootFile << endl;

		TFile curTfile(currentRootFile.c_str());
		if (curTfile.IsZombie()) {
			std::cout << "could not read: " << currentRootFile << " .";
			exit(0);
		}

		std::cout << "list keys:" << std::endl;
		TIter next(curTfile.GetListOfKeys());
		bool highRateFound = false;
	
		TKey *obj;
		while ( obj = (TKey*)next() ) {
			if (strcmp(obj->GetTitle(),"HighRate") == 0) highRateFound = true;
			if (VERBOSE) {
				std::cout << obj->GetTitle() << std::endl;
			}
		}
		if (highRateFound) {
			std::cout << "highRate test found, reading data..." << std::endl;
			TH2D* xraymap;
			TH2D* calmap;
			char calmapName[256];
			char xraymapName[256];
			std::ofstream output;
           
//			std::cout << "calculating rates and efficiencies" << std::endl;

			for (int iRoc=0;iRoc<nRocs;iRoc++) {

//				std::cout << "ROC" << iRoc << std::endl;
				sprintf(xraymapName, "HighRate/highRate_xraymap_C%d_V0;1", iRoc);
				curTfile.GetObject(xraymapName, xraymap);
				if (xraymap == 0) {
					std::cout << "ERROR: x-ray hitmap not found!" << std::endl;
				}
				int nBinsX = xraymap->GetXaxis()->GetNbins();
				int nBinsY = xraymap->GetYaxis()->GetNbins();
				
				sprintf(calmapName, "HighRate/highRate_C%d_V0;1", iRoc);
				curTfile.GetObject(calmapName, calmap);
				if (calmap == 0) {
					sprintf(calmapName, "HighRate/highRate_calmap_C%d_V0;1", iRoc);
					curTfile.GetObject(calmapName, calmap);
					if (calmap == 0) {
						std::cout << "ERROR: calibration hitmap not found!" << std::endl;
					}
				}

//				std::cout << nBinsX << "x" << nBinsY << std::endl;
				for (int dcol = 0; dcol < nDCol; dcol++) {
//					std::cout << "reading dc " << dcol << std::endl;

					std::vector<double> hits;
					std::vector<double> xray_hits;
					double totCHits = 0;
					double totXHits = 0;						
					double totXHitErrors = 0;					

//					std::cout<<"Getting data from Histograms" << endl;

					for (int y = 0; y < 160; y++) {

						bool masked = false;
						//std::cout << " Masking " << endl;
						for (int iMaskedPixels=0; iMaskedPixels < maskedPixels[iRoc].size(); iMaskedPixels++) {
							int locFirst = dcol * 2 + (int)(y/80);
							int locSecond = y%80;
							if ( (maskedPixels[iRoc][iMaskedPixels].first == locFirst) && (maskedPixels[iRoc][iMaskedPixels].second == locSecond)) {
								masked = true;
								break;
							}
						}

						if ((!FIDUCIAL_ONLY || ((y % 80) > 0 && (y % 80) < 79)) && !masked) {
							//std::cout << " get " << (dcol * 2 + (int)(y / 80) + 1) << " / " <<  ((y % 80) + 1) << std::endl;
							double trans =0;
							trans =  calmap->GetBinContent(dcol * 2 + (int)(y / 80) + 1, (y % 80) + 1);
							hits.push_back(trans);
							totCHits += trans;
							trans = xraymap->GetBinContent(dcol * 2 + (int)(y / 80) + 1, (y % 80) + 1);
							xray_hits.push_back( trans );
							totXHits += trans;
							totXHitErrors += trans/100;
						}
					}

					int nPixelsDC = hits.size();
					double totHits = 0;
					if (nPixelsDC < 1) nPixelsDC = 1;
					double rate = TMath::Mean(nPixelsDC, &xray_hits[0]) / (nTrig * triggerDuration * pixelArea) * 1.0e-6;
					double efficiency = TMath::Mean(nPixelsDC, &hits[0]) / nTrigPerPixel;
					double rateError = TMath::RMS(nPixelsDC, &xray_hits[0]) / std::sqrt(nPixelsDC) / (nTrig * triggerDuration * pixelArea) * 1.0e-6;
					double efficiencyError = TMath::RMS(nPixelsDC, &hits[0]) / std::sqrt(nPixelsDC) / nTrigPerPixel;
					
//					std::cout << "Assigning vales" << endl;
					efficiencies[iRoc].push_back(efficiency);
					efficiencyErrors[iRoc].push_back(efficiencyError);
					rates[iRoc].push_back(rate);
					rateErrors[iRoc].push_back(rateError);
                                        dcolHits[iRoc][dcol].push_back(totXHits);
                                        dcolHitErrors[iRoc][dcol].push_back(std::sqrt(totXHits));
					dcolEff[iRoc][dcol].push_back(efficiency);
					dcolEffErrors[iRoc][dcol].push_back(efficiencyError);
					dcolRates[iRoc][dcol].push_back(rate);
                                        dcolRateErrors[iRoc][dcol].push_back(rateError);

                                        efficiencies[nRocs].push_back(efficiency);
                                        efficiencyErrors[nRocs].push_back(efficiencyError);
                                        rates[nRocs].push_back(rate);
                                        rateErrors[nRocs].push_back(rateError);
					dcolRates[nRocs][0].push_back(rate);
					dcolRates[nRocs][1].push_back(dColModCount);		
			
					byAmpEfficiencies[rateIndex][iRoc].push_back(efficiency);
                                        byAmpEfficiencyErrors[rateIndex][iRoc].push_back(efficiencyError);
                                        byAmpRates[rateIndex][iRoc].push_back(rate);
					byAmpRateErrors[rateIndex][iRoc].push_back(rateError);
					
					dColModCount++;		

					if( (worstDColEff[iRoc] < efficiency) && ( rate < 125) ) { worstDColEff[iRoc] = efficiency; worstDCol[iRoc] = dcol; }

					if( efficiency < 0.98 ){	
						log << "Roc: " << iRoc << " dc: " << dcol << " nPixelsDC: " << nPixelsDC << " rate: " << rate << " eff: " << efficiency << std::endl;
					}
					if (VERBOSE) {
//						std::cout << "dc " << dcol << " nPixelsDC: " << nPixelsDC << " rate: " << rate << " " << efficiency << std::endl;
				}
//					std::cout<<"next dcol"<<endl;
				}
//				std::cout << "next roc" << endl;
			}
//			std::cout<<"next file"<<endl;
		} else {
//			std::cout << "high rate test not found" << std::endl;
			return 1;
		}
//	std:cout << "end of Data Collection" << endl;
	}

	std::cout << "Output Phase" << std::endl;

	std::ofstream outfile("efficiency.csv");
        std::vector<double> slopes;
        std::vector<double> slope_err;

	for (int iRoc=0;iRoc<nRocs;iRoc++) {
		
		std::cout << "Working in ROC " << iRoc << endl;
		TCanvas *c1 = new TCanvas("c1", "efficiency", 200, 10, 700, 500);
		c1->Range(0,0,1, 300);
		TGraphErrors* TGE = new TGraphErrors( rates[iRoc].size(), &rates[iRoc][0], &efficiencies[iRoc][0], &rateErrors[iRoc][0] , &efficiencyErrors[iRoc][0] ) ;
		TGraph* tge2 = new TGraph( lineList[0].size(), &lineList[0][0], &lineList[1][0] );
                TGraph* tge3 = new TGraph( lineList[2].size(), &lineList[2][0], &lineList[3][0] );

		char graphTitle[256];
		sprintf(graphTitle, "Fiducial Efficiency vs Rate for %s ROC %d", moduleName.c_str(), iRoc);
		TGE->SetTitle(graphTitle);
		TGE->SetMarkerStyle(3);
		TGE->SetMarkerSize(1);
		TGE->GetXaxis()->SetTitle("Rate: MHz/cm^2");
		TGE->GetYaxis()->SetTitle("Efficency 1.00 = 100%");
		TGE->Draw("ap");
		
		tge2->SetMarkerColor( kRed );
		tge2->SetMarkerStyle(21);
 
		tge3->SetMarkerColor( kRed );
		tge3->SetMarkerStyle(21);

		TF1* myfit = new TF1("fitfun", "([0]-[1]*x*x*x)", 70, 170);
		myfit->SetParameter(0, 1);
		myfit->SetParLimits(0, 0.9, 1.1);
		myfit->SetParameter(1, 5e-9);
		myfit->SetParLimits(1, 1e-10, 5e-8);			
	
		tge2->Draw("same");
		tge3->Draw("same");	
		TGE->Fit(myfit, "BR");
		c1->Update();
		
		double p0= myfit->GetParameter(0);
		double p1= myfit->GetParameter(1);
		double p0_err = myfit->GetParError(0);
		double p1_err = myfit->GetParError(1);
		double eff_err = sqrt(p0_err * p0_err + pow(120.0,6) * p1_err * p1_err);
		outfile << (p0 - p1 * 120*120*120) << std::endl;
		log << "Eff at 120MHz/cm^2 : ROC : " << iRoc << " Eff: " << p0-p1 *120*120*120 << " +/- " << eff_err << endl; 

		c1->Modified();
		gPad->Modified();
		char saveFileName[256];
		sprintf(saveFileName, "%s_Eff_C%d.png",HighRateSaveFileName.c_str(), iRoc);
		c1->SaveAs(saveFileName);
		c1->Clear();
		TGE->Clear();

		myfit->Clear();
		delete myfit;
		delete c1;

		TCanvas *c1 = new TCanvas("c1", "worst_dcol", 200, 10, 700, 500);
                c1->Range(0,0,1, 300);
		int use = worstDCol[iRoc];
                TGraphErrors* TGE = new TGraphErrors(dcolEff[iRoc][use].size(), &dcolRates[iRoc][use][0], &dcolEff[iRoc][use][0], &dcolRateErrors[iRoc][use][0] , &dcolEffErrors[iRoc][use][0]);
                TGraph* tge2 = new TGraph( lineList[0].size(), &lineList[0][0], &lineList[1][0] );
                TGraph* tge3 = new TGraph( lineList[2].size(), &lineList[2][0], &lineList[3][0] );
		
		char graphTitle[256];
                sprintf(graphTitle, "Fiducial Efficiency vs Rate for %s ROC %d DC %d", moduleName.c_str(), iRoc, use);
                TGE->SetTitle(graphTitle);
                TGE->SetMarkerStyle(3);
                TGE->SetMarkerSize(1);
                TGE->GetXaxis()->SetTitle("Rate: MHz/cm^2");
                TGE->GetYaxis()->SetTitle("Efficency 1.00 = 100%");
                TGE->Draw("ap");

                tge2->SetMarkerColor( kRed );
                tge2->SetMarkerStyle(21);
 
                tge3->SetMarkerColor( kRed );
                tge3->SetMarkerStyle(21);

                TF1* myfit = new TF1("fitfun", "([0]-[1]*x*x*x)", 70, 170);
                myfit->SetParameter(0, 1);
                myfit->SetParLimits(0, 0.9, 1.1);
                myfit->SetParameter(1, 5e-9);
                myfit->SetParLimits(1, 1e-10, 5e-8);

                tge2->Draw("same");
                tge3->Draw("same");
                TGE->Fit(myfit, "BR");
                c1->Update();

                c1->Modified();
                gPad->Modified();
                char saveFileName[256];
                sprintf(saveFileName, "%s_Eff_C%d_DC%d.png",HighRateSaveFileName.c_str(), iRoc, use);
                c1->SaveAs(saveFileName);
                c1->Clear();
                TGE->Clear();

                myfit->Clear();
                delete myfit;
                delete c1;

		
	}

        std::cout << "Working on Module" << endl;
      	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	TCanvas *c1 = new TCanvas("c1", "Efficiency", 200, 10, 700, 500);
        TGraphErrors* TGE = new TGraphErrors( efficiencies[nRocs].size(), &rates[nRocs][0], &efficiencies[nRocs][0], &rateErrors[nRocs][0], &efficiencyErrors[nRocs][0] );
        TGraph* tge2 = new TGraph( lineList[0].size(), &lineList[0][0], &lineList[1][0] );
        TGraph* tge3 = new TGraph( lineList[2].size(), &lineList[2][0], &lineList[3][0] );

	char graphTitle[256];
        sprintf(graphTitle, "%s Fiducial Efficiency vs Rate  for %s", HighRateFileName.c_str() , moduleName.c_str());
        TGE->SetTitle(graphTitle);
	TGE->GetXaxis()->SetTitle("Rate: MHz/cm^2");
	TGE->GetYaxis()->SetTitle("Efficency 1.00 = 100%");
        TGE->SetMarkerStyle(7);
        TGE->SetMarkerSize(1);
        TGE->Draw("ap");


        tge2->SetMarkerColor(2 );
        tge2->SetMarkerStyle(21);

        tge3->SetMarkerColor(2 );
        tge3->SetMarkerStyle(21);

        TF1* myfit = new TF1("fitfun", "([0]-[1]*x*x*x)", 40, 120);
        myfit->SetParameter(0, 1);
        myfit->SetParLimits(0, 0.9, 1.1);
        myfit->SetParameter(1, 5e-9);
        myfit->SetParLimits(1, 1e-10, 5e-8);

        tge2->Draw("same");
        tge3->Draw("same");
        TGE->Fit(myfit, "BR");
        c1->Update();

        double p0= myfit->GetParameter(0);
        double p1= myfit->GetParameter(1);
        double p0_err = myfit->GetParError(0);
        double p1_err = myfit->GetParError(1);
        double eff_err = sqrt(p0_err * p0_err + pow(120.0,6) * p1_err * p1_err);
        
	outfile << (p0 - p1 * 120*120*120) << std::endl;
	log << "High Rate Run: " << HighRateFileName << endl;
        log << "Efficency at 120MHz/cm^2 : " << moduleName << " Eff: " << p0-p1 *120*120*120 << " +/- " << eff_err << endl;

        c1->Modified();
      	gPad->Modified();
 	char saveFileName[256];
  	sprintf(saveFileName, "%s_Eff_%s.png",HighRateSaveFileName.c_str(), moduleName.c_str());
        c1->SaveAs(saveFileName);
        c1->Clear();
        TGE->Clear();
        myfit->Clear();
       	delete myfit;
        delete c1;
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	TCanvas *c2 = new TCanvas("c2", "DColRate", 200, 10, 700, 500);
        TGraph* tg1 = new TGraph( dcolRates[nRocs][1].size(), &dcolRates[nRocs][1][0], &dcolRates[nRocs][0][0] );
        char graphTitle[256];
        sprintf(graphTitle, "%s Rate by DCol for %s", HighRateFileName.c_str() , moduleName.c_str());
        tg1->SetTitle(graphTitle);
        tg1->GetXaxis()->SetTitle("DCol Number");
        tg1->GetYaxis()->SetTitle("Rate: MHa/cm^2");
        tg1->SetMarkerStyle(7);
        tg1->SetMarkerSize(1);
        tg1->Draw("ap");

        char saveFileName3[256];
        sprintf(saveFileName3, "%s_Rate_by_DCol_%s.png",HighRateSaveFileName.c_str(), moduleName.c_str());
        c2->SaveAs(saveFileName3);
        c2->Clear();
        tg1->Clear();
        delete c2;
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	outfile.close();
	std::cout <<"Thats all folks!!!" << endl; 
	return 0;


}

