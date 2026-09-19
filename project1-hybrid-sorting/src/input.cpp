#include "input.hpp"

#include <random>
#include <stdexcept>

namespace sc2001 {

std::vector<int> generateRandomInput(
    std::size_t size,
    int maxValue,
    std::uint32_t seed
) {
    if(maxValue < 1){
        throw std::invalid_argument("maxValue must be at least 1");
    }

    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> distribution(1,maxValue);
    std::vector<int> values(size);

    for(int& value : values){
        value=distribution(generator);
    }

    return values;
}

}  // namespace sc2001

