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

// .x efficiency.cpp+("/path/to/your/files")
// /path/to/your/files/000_sometest_p17/...
// /path/to/your/files/001_HREfficiency_50/... <-- commander_HREfficiency.root, defaultMaskFile.dat, testParameters.dat
// /path/to/your/files/002_HREfficiency_100/... <-- "
// /path/to/your/files/003_HREfficiency_150/... <--  "


int eff() {
    
    	cout << "Starting Efficency Script" << endl;

	char chpath[256];
    	getcwd(chpath, 255);
	std::string path = chpath;
    	std::string mod("pa243");
	//std::string mod("yhc691015sn3p35");





	std::string dataPath =  path + "/" + mod + "data";
    	//std::string measurementFolder =  mod + "data";
	std::string configPath = path + "/" + mod; 

	std::string HighRateFileName( "hr" );
    	//std::stringstream ss1(measurementFolder);
    	std::string moduleName = mod;
    	//std::getline(ss1, moduleName, '_');

	//std::string rootFileName("hr10ma.root");
	std::string maskFileName("defaultMaskFile.dat");

	const bool FIDUCIAL_ONLY = true; // don't change
	const bool VERBOSE = true;

	int nTrigPerPixel = 50; // will be read from testParameters.dat
	int nPixels = 4160;
	int nTrig = nTrigPerPixel * nPixels;
	float pixelArea = 0.01 * 0.015; // cm^2
	float triggerDuration = 25e-9; //s

	int nRocs = 16;
	int nDCol = 25;
	
	std::string directoryList = mod;

	std::string outFileName = dataPath + "/efficiency.log";
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
			if (filename.substr(0,2) == HighRateFileName ) {
				if( filename.substr(( filename.length() - 4 ), 4)  == "root" ){
         				fileList.push_back(filename);
					std::cout << "---Added to fileList" << endl;
				}
         		}
      		}
    	}

    	std::vector< std::vector< std::pair< int,int > > > maskedPixels;

    	//cout << "Sort HR File list " << endl;
	//std::sort(fileList.begin(), fileList.end());

	std::vector< std::vector< double > > efficiencies;
	std::vector< std::vector< double > > efficiencyErrors;
	std::vector< std::vector< double > > rates;
	std::vector< std::vector< double > > rateErrors;
        std::vector< std::vector< double > > dcolHits;
        std::vector< std::vector< double > > dcolNumList;
        std::vector< std::vector< double > > dcolUniformity;

	std::vector< double > empty; 

	dcolNumList.push_back(empty);

	for (int i=0;i<(nRocs+1)*6;i++) {
		efficiencies.push_back(empty);
		efficiencyErrors.push_back(empty);
		rates.push_back(empty);
		rateErrors.push_back(empty);
		dcolHits.push_back(empty);
		dcolUniformity.push_back(empty);
	}
	
	for ( int i=1; i < (nDCol+1); i++ ) { dcolNumList[0].push_back(i); }

	cout << "loop over all commander_HREfficiency.root root files" << endl;
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
			//line2 = line2.toLowerCase();
			//std::transform(line2.begin(), line2.end(), line2.begin(), ::tolower);
			if (line2.find("HighRate") != std::string::npos) {
				while (getline(testParameters, line2)) {
					if (line2.size() < 1) break;
					//std::transform(line2.begin(), line2.end(), line2.begin(), ::tolower);
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
	std::cout<< "Going Over HR files: quanity: " << len << endl;	                                
	log << "Double Column's with Efficency < 90 % " << endl;
	for (int i=0; i<len ; ++i) {

		std::string currentRootFile = fileList[i];	
		std::cout << "Working file : " << currentRootFile << endl;

		TFile f(currentRootFile.c_str());
		if (f.IsZombie()) {
			std::cout << "could not read: " << currentRootFile << " .";
			exit(0);
		}
		std::cout << "list keys:" << std::endl;
		TIter next(f.GetListOfKeys());
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
           
			std::cout << "calculating rates and efficiencies" << std::endl;

			for (int iRoc=0;iRoc<nRocs;iRoc++) {

				std::cout << "ROC" << iRoc << std::endl;
				sprintf(xraymapName, "HighRate/highRate_xraymap_C%d_V0;1", iRoc);
				f.GetObject(xraymapName, xraymap);
				if (xraymap == 0) {
					std::cout << "ERROR: x-ray hitmap not found!" << std::endl;
				}
				int nBinsX = xraymap->GetXaxis()->GetNbins();
				int nBinsY = xraymap->GetYaxis()->GetNbins();

				sprintf(calmapName, "HighRate/highRate_C%d_V0;1", iRoc);
				f.GetObject(calmapName, calmap);
				if (calmap == 0) {
					sprintf(calmapName, "HighRate/highRate_calmap_C%d_V0;1", iRoc);
					f.GetObject(calmapName, calmap);
					if (calmap == 0) {
						std::cout << "ERROR: calibration hitmap not found!" << std::endl;
					}
				}

				std::cout << nBinsX << "x" << nBinsY << std::endl;
				//float rate, efficiency;
				for (int doubleColumn = 1; doubleColumn <= 25; doubleColumn++) {
					//std::cout << "reading dc " << doubleColumn << std::endl;

					std::vector<double> hits;
					std::vector<double> xray_hits;
					
					for (int y = 0; y < 160; y++) {

						bool masked = false;
						//std::cout << " Masking " << endl;
						for (int iMaskedPixels=0; iMaskedPixels < maskedPixels[iRoc].size(); iMaskedPixels++) {
							int locFirst = doubleColumn * 2 + (int)(y/80);
							int locSecond = y%80;
							if ( (maskedPixels[iRoc][iMaskedPixels].first == locFirst) && (maskedPixels[iRoc][iMaskedPixels].second == locSecond)) {
								masked = true;
								break;
							}
						}

						if ((!FIDUCIAL_ONLY || ((y % 80) > 0 && (y % 80) < 79)) && !masked) {
							//std::cout << " get " << (doubleColumn * 2 + (int)(y / 80) + 1) << " / " <<  ((y % 80) + 1) << std::endl;

							hits.push_back( calmap->GetBinContent(doubleColumn * 2 + (int)(y / 80) + 1, (y % 80) + 1) );
							xray_hits.push_back( xraymap->GetBinContent(doubleColumn * 2 + (int)(y / 80) + 1, (y % 80) + 1) );

						}
					}

					int nPixelsDC = hits.size();
					double totHits = 0;
					if (nPixelsDC < 1) nPixelsDC = 1;
					double rate = TMath::Mean(nPixelsDC, &xray_hits[0]) / (nTrig * triggerDuration * pixelArea) * 1.0e-6;
					//std::cout << rate << endl;
					double efficiency = TMath::Mean(nPixelsDC, &hits[0]) / nTrigPerPixel;
					//std::cout << efficiency << endl;
					double rateError = TMath::RMS(nPixelsDC, &xray_hits[0]) / std::sqrt(nPixelsDC) / (nTrig * triggerDuration * pixelArea) * 1.0e-6;
					//std::cout << rateError << endl;
					double efficiencyError = TMath::RMS(nPixelsDC, &hits[0]) / std::sqrt(nPixelsDC) / nTrigPerPixel;
					//std::cout << "totaling Hits"  << endl;
					for( int h = 0; h < nPixelsDC; h++){ totHits = totHits + xray_hits[0][h]; }
					
					std::cout << "Assigning vales" << endl;
					efficiencies[iRoc].push_back(efficiency);
					efficiencyErrors[iRoc].push_back(efficiencyError);
					rates[iRoc].push_back(rate);
					rateErrors[iRoc].push_back(rateError);
                                        dcolHits[iRoc].push_back(totHits);

					efficiencies[nRocs*(1+i)+iRoc+1].push_back(efficiency);
                                        efficiencyErrors[nRocs*(1+i)+iRoc+1].push_back(efficiencyError);
                                        rates[nRocs*(1+i)+iRoc+1].push_back(rate);
                                        rateErrors[nRocs*(1+i)+iRoc+1].push_back(rateError);
                                        dcolHits[nRocs*(1+i)+iRoc+1].push_back(totHits);

                                        efficiencies[nRocs].push_back(efficiency);
                                        efficiencyErrors[nRocs].push_back(efficiencyError);
                                        rates[nRocs].push_back(rate);
                                        rateErrors[nRocs].push_back(rateError);
                                        dcolHits[nRocs].push_back(totHits);
					
					efficiencies[nRocs*(2+i)].push_back(efficiency);
                                        efficiencyErrors[nRocs*(2+i)].push_back(efficiencyError);
                                        rates[nRocs*(2+i)].push_back(rate);
                                        rateErrors[nRocs*(2+i)].push_back(rateError);        				
                                        dcolHits[nRocs*(2+i)].push_back(totHits);

					if( efficiency < 0.9 ){	
						log << "Roc: " << iRoc << " dc: " << doubleColumn << " nPixelsDC: " << nPixelsDC << " rate: " << rate << " eff: " << efficiency << std::endl;
					}
					if (VERBOSE) {
						std::cout << "dc " << doubleColumn << " nPixelsDC: " << nPixelsDC << " rate: " << rate << " " << efficiency << std::endl;
					}
				}
			}



	  		//output.open (Form("%s/output_%d.txt",the_path,i), std::ofstream::out);
			//output.close();

		} else {
			std::cout << "high rate test not found";
			return 1;
		}
	}

	for( int ir = 0; ir < nRocs; ir++){
		for( int dc = 0; dc < nDCol; dc++){
			dcolUniformity[ir].push_back( dcolHits[nRocs*(4)+ir+1][dc] / dcolHits[nRocs+ir+1][dc] );
		}			
	}


	std::cout << "Output Phase" << endl;

	std::ofstream outfile("efficiency.csv");

	for (int iRoc=0;iRoc<nRocs;iRoc++) {
		
		std::cout << "Working in ROC " << iRoc << endl;
		TCanvas *c1 = new TCanvas("c1", "efficiency", 200, 10, 700, 500);
		TGraphErrors* TGE = new TGraphErrors(efficiencies[iRoc].size(), &rates[iRoc][0], &efficiencies[iRoc][0], &rateErrors[iRoc][0] , &efficiencyErrors[iRoc][0]);
		char graphTitle[256];
		sprintf(graphTitle, "Fiducial Efficiency vs Rate for %s ROC %d", moduleName.c_str(), iRoc);
		TGE->SetTitle(graphTitle);
		TGE->SetMarkerStyle(3);
		TGE->SetMarkerSize(1);
	//	TGE->GetXaxis->SetTitle("Rate: MHz/cm^2");
	//	TGE->GetYaxis->SetTitle("Efficency 1.00 = 100%");
		TGE->Draw("ap");

		TF1* myfit = new TF1("fitfun", "([0]-[1]*x*x*x)", 70, 170);
		myfit->SetParameter(0, 1);
		myfit->SetParLimits(0, 0.9, 1.1);
		myfit->SetParameter(1, 5e-9);
		myfit->SetParLimits(1, 1e-10, 5e-8);			

		TGE->Fit(myfit, "BR");

		double minimumEfficiency = TMath::MinElement(efficiencies[iRoc].size(), &efficiencies[iRoc][0]);

//		TLegend* leg = new TLegend(0.13,0.3,0.75,0.2);

  // 		leg->SetTextFont(62);
//		leg->SetTextSize(0.03);
		double p0= myfit->GetParameter(0);
		double p1= myfit->GetParameter(1);
		double p0_err = myfit->GetParError(0);
		double p1_err = myfit->GetParError(1);
		double eff_err = sqrt(p0_err * p0_err + pow(120.0,6) * p1_err * p1_err);
//		leg->AddEntry("", Form("eff at 120Mhz/cm2: %f +/- %f", p0 - p1 * 120*120*120, eff_err) );
		outfile << (p0 - p1 * 120*120*120) << std::endl;
		log << "Eff at 120MHz/cm^2 : ROC : " << iRoc << " Eff: " << p0-p1 *120*120*120 << " +/- " << eff_err << endl; 
//   		leg->SetTextFont(62);
//		leg->AddEntry("fitfun",Form("cubic fit: %f - %e *x^3", p0, p1),"l");
//		leg->Draw();

		c1->Modified();
		gPad->Modified();
		char saveFileName[256];
		sprintf(saveFileName, "Efficiency_C%d.png", iRoc);
		c1->SaveAs(saveFileName);
		c1->Clear();
		TGE->Clear();

		myfit->Clear();
		delete myfit;
		delete c1;
//		delete leg;

		cout << "making c2" << endl;
                TCanvas *c2 = new TCanvas("c2", "hitsperdcol", 200, 10, 700, 500);
            	

		cout <<"making th"<< endl;
	//	cout << dcolHits.size() << " " << (nRocs*2)+iRoc+1 << " " << dcolHits[(nRocs*2)+iRoc+1].size() << " "  << dcolNumList[0].size()<<endl;
  	//	cout << dcolUniformity[iRoc].size() << " " << dcolNumList[0].size()<<endl;
		TGraph* Tdcol = new TGraph( dcolNumList[0].size(), &dcolNumList[0][0], &dcolHits[(nRocs*2)+iRoc+1][0] );//        &dcolUniformity[iRoc][0] );\
		cout << "Title and Save" << endl;
		char graphTitle2[256];
                sprintf(graphTitle2, "Hits vs DCol for Module: %s ROC %d", moduleName.c_str(), iRoc);
                Tdcol->SetTitle(graphTitle);
            //    Tdcol->GetXaxis->SetTitle("Double Column");
            //    Tdcol->GetYaxis->SetTitle("Number of Hits");
                Tdcol->SetMarkerStyle(3);
                Tdcol->SetMarkerSize(1);
                Tdcol->Draw("ap");

                c2->Modified();
                gPad->Modified();
		               
		char saveFileName2[256];
		sprintf(saveFileName2, "HitsPerDCol_C%d.png", iRoc);
                c2->SaveAs(saveFileName2);
                c2->Clear();
                Tdcol->Clear();
                delete c2;


	}

        std::cout << "Working on Module" << endl;
      	TCanvas *c1 = new TCanvas("c1", "Efficiency", 200, 10, 700, 500);
        TGraphErrors* TGE = new TGraphErrors( efficiencies[nRocs].size(), &rates[nRocs][0], &efficiencies[nRocs][0], &rateErrors[nRocs][0], &efficiencyErrors[nRocs][0] );
        char graphTitle[256];
        sprintf(graphTitle, "Fiducial Efficiency vs Rate  for %s", moduleName.c_str());
        TGE->SetTitle(graphTitle);
//	TGE->GetXaxis->SetTitle("Rate: MHz/cm^2");
//	TGE->GetYaxis->SetTitle("Efficency 1.00 = 100%");
        TGE->SetMarkerStyle(3);
        TGE->SetMarkerSize(1);
        TGE->Draw("ap");

        TF1* myfit = new TF1("fitfun", "([0]-[1]*x*x*x)", 70, 170);
        myfit->SetParameter(0, 1);
        myfit->SetParLimits(0, 0.9, 1.1);
        myfit->SetParameter(1, 5e-9);
        myfit->SetParLimits(1, 1e-10, 5e-8);

     	TGE->Fit(myfit, "BR");

        double minimumEfficiency = TMath::MinElement(efficiencies[0].size(), &efficiencies[0][0]);

 //       TLegend* leg = new TLegend(0.3,0.4,0.8,0.5);

   //     leg->SetTextFont(62);
     //   leg->SetTextSize(0.03);
        double p0= myfit->GetParameter(0);
        double p1= myfit->GetParameter(1);
        double p0_err = myfit->GetParError(0);
        double p1_err = myfit->GetParError(1);
        double eff_err = sqrt(p0_err * p0_err + pow(120.0,6) * p1_err * p1_err);
//        leg->AddEntry("", Form("eff at 120Mhz/cm2: %f +/- %f", p0 - p1 * 120*120*120, eff_err) );
        outfile << (p0 - p1 * 120*120*120) << std::endl;
        log << "Eff at 120MHz/cm^2 : Mod : " << moduleName << " Eff: " << p0-p1 *120*120*120 << " +/- " << eff_err << endl;
//        leg->SetTextFont(62);
 //       leg->AddEntry("fitfun",Form("cubic fit: %f - %e *x^3", p0, p1),"l");
  //      leg->Draw();

        c1->Modified();
      	gPad->Modified();
 	char saveFileName[256];
  	sprintf(saveFileName, "Efficiency_%s.png",moduleName.c_str());
        c1->SaveAs(saveFileName);
        c1->Clear();
        TGE->Clear();
        myfit->Clear();
       	delete myfit;
        delete c1;
//        delete leg;

	outfile.close();

	return 0;
}
