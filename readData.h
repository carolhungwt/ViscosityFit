//readData.h
#include "TMath.h"
#include <istream>
#include <fstream>
#include <iterator>
#include <vector>

using namespace RooFit;
using namespace std;

struct datumpair
{
	double x;	//here x is delta time
	double y;	//here y is delta angle in radian
};

std::istream& operator>>(std::istream& is, datumpair& datum){
	is>>datum.x>>std::ws>>datum.y; // since we assume the datafile follow a format
								   // x [whitespace] y
	return is;
}

double arctan(double *x, double *par){
	double xx = x[0];
	double p0 = par[0];
	double f = -2*TMath::ATan(-1*p0*xx);
	return f;
}

vector<datumpair> vec_data;
TString filenamestem;
