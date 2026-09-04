// Emit the two guesses per tail for seeds 1..N using the archived toolchain's
// std::mt19937/std::shuffle specification. Each guess is a single byte.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>
int main(int argc,char**argv){
    const int last=argc>1?std::stoi(argv[1]):2000;
    if(last<1||last>100000)return 2;
    for(int seed=1;seed<=last;++seed){
        std::mt19937 engine(seed);
        for(int a=2;a<=12;++a)for(int b=2;b<=12;++b)if(b!=a)
        for(int c=2;c<=12;++c)if(c!=a&&c!=b){
            std::vector<unsigned char> available;
            for(int x=2;x<=12;++x)if(x!=a&&x!=b&&x!=c)available.push_back(x);
            std::shuffle(available.begin(),available.end(),engine);
            std::cout.put(available[0]);std::cout.put(available[1]);
        }
    }
    return std::cout?0:3;
}
