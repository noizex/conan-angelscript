#include <iostream>
#include <angelscript.h>

int main() {
    const char* version = asGetLibraryVersion();
	std::cout << "Angelscript library version: " << version;
}
