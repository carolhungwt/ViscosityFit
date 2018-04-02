//readData.cc
#include "readData.h"

vector<datumpair> ReadDataFile(TString filename){
	int numentry=7;
	std::vector<datumpair> datum;

	ifstream data;
	data.open(filename);
	if(data.is_open()){
		//https://stackoverflow.com/questions/7868936/read-file-line-by-line
		std::copy(std::istream_iterator<datumpair>(data),
				  std::istream_iterator<datumpair>(),std::back_inserter(datum));
		}else{
			std::cerr<<"Couldn't open "<<filename<<" for reading. \n"<<endl;
		}
	return datum;
}


void readData(TString filename){
//	vector<datumpair> vec_data;
	vec_data = ReadDataFile(filename);
//	cout<<vec_data[3].x<<endl;	
}
