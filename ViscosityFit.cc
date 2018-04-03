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
	TCanvas *c1 = new TCanvas("","",500,400);
	c1->cd();
	tg.SetLineColor(1);
	tg.SetLineWidth(2);
	tg.SetMarkerStyle(5);
	tg.SetTitle(filenamestem);
	tg.GetXaxis()->SetTitle("Time(s)");
	tg.GetYaxis()->SetTitle("#Phi(rad)");
	tg.Draw("");
	c1->SaveAs("~/www/"+filenamestem+".pdf");

}

void dofit(){
	TimeAnglePair *obj1 = new TimeAnglePair(filenamestem, vec_data);
	TGraph* tg = obj1->getTGraph();

	TF1 *fit = new TF1("arctanfit",arctan,0.,0.2,1);
	fit->SetParameter(0,8);
	fit->SetParNames("k");
	tg->Fit(fit,"R");
	fit->SetLineColor(2);
	fit->SetLineWidth(2);
	
	drawgraph(*tg);
//	RooArgList dependents;
//	const char* arctanform = "-2*TMath::ATan(-[0]*[1])";
//	RooFormulaVar* 2arctan = new RooFormulaVar("2arctan","2arctan",arctanform,dependents);
}

void ViscosityFit(){
	dofit();
}
