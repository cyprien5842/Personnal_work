#include <maya/MIOStream.h>
#include <maya/MSimple.h>

DeclareSimpleCommand(helloWorld, PLUGIN_COMPANY, "4.5");

MStatus helloWorld::doIt(const MArgList&)
{
	cout << "Hello World" << endl;
	
	return MS::kSuccess;
	
}
