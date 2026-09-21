#include "input.hpp"
#include "sorting.hpp"

#include <algorithm>
#include <cstdint>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {

long long parseInteger(const char* text,const char* name) {
    std::size_t parsedCharacters=0;

    try{
        const long long value=std::stoll(text,&parsedCharacters);

        if(parsedCharacters != std::string(text).size()){
            throw std::invalid_argument("contains non-integer characters");
        }

        return value;
    }
    catch(const std::exception&){
        throw std::invalid_argument(std::string(name)+" must be an integer");
    }
}

void printUsage(const char* programName) {
    std::cerr
        <<"Usage: "<<programName
        <<" <hybrid|merge> <n> <S> <x> <seed> [timing-repetitions]\n"
        <<"  hybrid requires S >= 1\n"
        <<"  merge requires S = 0 because S is not used\n"
        <<"  timing-repetitions defaults to 1\n";
}

}  // namespace

int main(int argc,char* argv[]) {
    if(argc != 6 && argc != 7){
        printUsage(argv[0]);
        return 1;
    }

    try{
        const std::string algorithm=argv[1];
        const long long parsedN=parseInteger(argv[2],"n");
        const long long parsedThreshold=parseInteger(argv[3],"S");
        const long long parsedMaximum=parseInteger(argv[4],"x");
        const long long parsedSeed=parseInteger(argv[5],"seed");
        const long long parsedRepetitions=
            argc == 7 ? parseInteger(argv[6],"timing-repetitions") : 1;

        if(algorithm != "hybrid" && algorithm != "merge"){
            throw std::invalid_argument(
                "algorithm must be either hybrid or merge"
            );
        }
        if(parsedN < 1 || parsedN > std::numeric_limits<int>::max()){
            throw std::invalid_argument("n must be between 1 and INT_MAX");
        }
        if(parsedMaximum < 1 ||
           parsedMaximum > std::numeric_limits<int>::max()){
            throw std::invalid_argument("x must be between 1 and INT_MAX");
        }
        if(parsedSeed < 0 ||
           parsedSeed > std::numeric_limits<std::uint32_t>::max()){
            throw std::invalid_argument(
                "seed must fit in an unsigned 32-bit integer"
            );
        }
        if(parsedRepetitions < 1 ||
           parsedRepetitions > std::numeric_limits<int>::max()){
            throw std::invalid_argument(
                "timing-repetitions must be between 1 and INT_MAX"
            );
        }
        if(algorithm == "hybrid" &&
           (parsedThreshold < 1 ||
            parsedThreshold > std::numeric_limits<int>::max())){
            throw std::invalid_argument(
                "hybrid threshold S must be between 1 and INT_MAX"
            );
        }
        if(algorithm == "merge" && parsedThreshold != 0){
            throw std::invalid_argument("merge requires S = 0");
        }

        const std::size_t n=static_cast<std::size_t>(parsedN);
        const int threshold=static_cast<int>(parsedThreshold);
        const int maxValue=static_cast<int>(parsedMaximum);
        const std::uint32_t seed=static_cast<std::uint32_t>(parsedSeed);
        const int repetitions=static_cast<int>(parsedRepetitions);

        const std::vector<int> originalValues=
            sc2001::generateRandomInput(n,maxValue,seed);
        sc2001::ComparisonCount keyComparisons=0;
        std::clock_t totalTicks=0;

        for(int repetition=0;repetition<repetitions;++repetition){
            std::vector<int> values=originalValues;
            sc2001::ComparisonCount currentComparisons=0;
            const std::clock_t start=std::clock();

            if(algorithm == "hybrid"){
                sc2001::hybridMergeSort(
                    values,
                    0,
                    static_cast<int>(values.size())-1,
                    threshold,
                    currentComparisons
                );
            }
            else{
                sc2001::mergeSort(
                    values,
                    0,
                    static_cast<int>(values.size())-1,
                    currentComparisons
                );
            }

            const std::clock_t finish=std::clock();
            if(start == static_cast<std::clock_t>(-1) ||
               finish == static_cast<std::clock_t>(-1)){
                throw std::runtime_error("CPU time is unavailable");
            }
            if(!std::is_sorted(values.begin(),values.end())){
                throw std::runtime_error("sorting correctness check failed");
            }
            if(repetition == 0){
                keyComparisons=currentComparisons;
            }
            else if(currentComparisons != keyComparisons){
                throw std::runtime_error(
                    "key-comparison count changed between repetitions"
                );
            }
            totalTicks+=finish-start;
        }

        const double cpuSeconds=
            static_cast<double>(totalTicks)/
            (static_cast<double>(CLOCKS_PER_SEC)*repetitions);
        const int outputThreshold=
            algorithm == "hybrid" ? threshold : 0;

        std::cout
            <<algorithm<<','
            <<n<<','
            <<outputThreshold<<','
            <<maxValue<<','
            <<seed<<','
            <<repetitions<<','
            <<keyComparisons<<','
            <<std::fixed<<std::setprecision(9)<<cpuSeconds<<'\n';
    }
    catch(const std::exception& error){
        std::cerr<<"ERROR: "<<error.what()<<'\n';
        printUsage(argv[0]);
        return 1;
    }

    return 0;
}
