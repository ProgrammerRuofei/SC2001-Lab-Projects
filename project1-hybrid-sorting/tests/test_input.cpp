#include "input.hpp"

#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    bool passed=true;

    const auto check=[&passed](bool condition,const char* name){
        if(!condition){
            std::cerr<<"FAIL: "<<name<<'\n';
            passed=false;
        }
    };

    const std::vector<int> values=
        sc2001::generateRandomInput(1000,100,2001);

    check(values.size()==1000,"requested size");
    check(
        std::all_of(
            values.begin(),
            values.end(),
            [](int value){
                return value>=1 && value<=100;
            }
        ),
        "values within [1, maxValue]"
    );

    const std::vector<int> repeated=
        sc2001::generateRandomInput(1000,100,2001);
    check(values==repeated,"same seed reproduces the same input");

    const std::vector<int> differentSeed=
        sc2001::generateRandomInput(1000,100,2002);
    check(values!=differentSeed,"different seeds produce different input");

    check(
        sc2001::generateRandomInput(0,100,2001).empty(),
        "zero-size input"
    );
    check(
        sc2001::generateRandomInput(5,1,2001)==std::vector<int>(5,1),
        "maxValue of one"
    );

    for(int invalidMaximum : {0,-1}){
        bool rejected=false;

        try{
            sc2001::generateRandomInput(5,invalidMaximum,2001);
        }
        catch(const std::invalid_argument&){
            rejected=true;
        }

        check(rejected,"reject nonpositive maxValue");
    }

    if(!passed){
        return 1;
    }

    std::cout<<"PASS: all random-input tests\n";
    return 0;
}

