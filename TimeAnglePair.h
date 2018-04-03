//TimeAnglePair.h
#ifndef TIMEANGLEPAIR
#define TIMEANGLEPAIR

#include <vector>
#include <string>
#include <iterator>
#include "TGraph.h"

//template<typename T> 
struct datumpair
{
	double x;
	double y;

//	const double& operator[](std::size_t var)const{return var==0? x: y;}
};

std::istream& operator>>(std::istream& is, datumpair& datum){ //overload the operator >>
	is>>datum.x>>std::ws>>datum.y; // since we assume the datafile follow a format
								   // x [whitespace] y
	return is;
}


class TimeAnglePair{
protected:
	std::string objname;
	std::vector<datumpair> data;	

public:
	TimeAnglePair();
	TimeAnglePair(std::string objname_, const std::vector<datumpair> &data_);
	~TimeAnglePair();

	string GetName(){return objname;}
	vector<double> getXs(){std::vector<double> Xs; for(unsigned int ix=0; ix<data.size();ix++){Xs.push_back(data[ix].x);}
	return Xs;}
	vector<double> getYs(){std::vector<double> Ys; for(unsigned int iy=0; iy<data.size();iy++){Ys.push_back(data[iy].y);}
	return Ys;}
	TGraph* getTGraph(){
		vector<double> xdata = getXs();
		vector<double> ydata = getYs();
		TGraph* g1 = new TGraph(data.size(),xdata.data(),ydata.data());
		return g1;}
};

inline TimeAnglePair::TimeAnglePair(std::string objname_, const std::vector<datumpair> &data_)
{
	objname = objname_;
	data = data_;
}

#endif

