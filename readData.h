//readData.h
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


