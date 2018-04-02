//#include "readData.h"

vector<double> getData(TString var){
	vector<double> coldata;
	if(var=="x"||var=="X"){
	  for(int n=0; n<vec_data.size(); n++){
	    coldata.push_back(vec_data[n].x);}
	}else if(var=="y"||var=="Y"){
	  for(int n=0; n<vec_data.size(); n++){
            coldata.push_back(vec_data[n].y);}
	}
	return coldata;
}

void drawgraph(TGraph& tg){
	TCanvas *c1 = new TCanvas("","",1000,800);
	c1->cd();
	tg.SetLineColor(1);
	tg.SetLineWidth(2);
	tg.SetMarkerStyle(5);
	tg.Draw("");
	c1->SaveAs("~/www/test_plot.png");

}

void dofit(){
	vector<double> xdata = getData("x");
	vector<double> ydata = getData("y");
	TGraph* tg = new TGraph(xdata.size(), xdata.data(), ydata.data());
	drawgraph(*tg);
	
	RooArgList dependents;
	const char* arctanform = "-2*TMath::ATan(-[0]*[1])";
//	RooFormulaVar* 2arctan = new RooFormulaVar("2arctan","2arctan",arctanform,dependents);
}

void ViscosityFit(){
	dofit();
}
