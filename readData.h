//readData.h
#include "TMath.h"
#include "TimeAnglePair.h"
#include <istream>
#include <fstream>
#include <iterator>
#include <vector>

using namespace RooFit;
using namespace std;

double arctan(double *x, double *par){
	double xx = x[0];
	double p0 = par[0];
	double f = -2*TMath::ATan(-1*p0*xx);
	return f;
}

vector<datumpair> vec_data;
string filenamestem;
