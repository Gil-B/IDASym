#include <Windows.h>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <memory>
#include "IDASym.h"

using namespace std;

class EXT_CLASS : public ExtExtension
{
public:
    EXT_COMMAND_METHOD(idasym);
};

EXT_DECLARE_GLOBALS();

EXT_COMMAND(idasym, "Loads symbols from .sym file", "{;e64;MODULE;module}{;x;inputpath;input file path}")
{
	ULONG64 imageBase;
	imageBase = GetUnnamedArgU64(0);
	Out("%08I64x\n", imageBase);
	string inputFilename = GetUnnamedArgStr(1);
	string line;
	try {
		ifstream ifs;
		ifs.open(inputFilename);
		while (getline(ifs, line))
		{
			const char* name = strchr(line.c_str(), ';') + 1;
			char* end = NULL;
			unsigned long offset = strtoul(line.c_str(), &end, 16);
			unsigned long size = strtoul(end, NULL, 16);

			dprintf("%08I64x %s\n", imageBase + offset, name);
			m_Symbols3->AddSyntheticSymbol(imageBase + offset, size, name, DEBUG_ADDSYNTHSYM_DEFAULT, NULL);
		}

	}
	catch (...) 
	{
		dprintf("An error has occurred\n");
		return;
	}
}