#include <fstream>
#include <iostream>
#include <algorithm>
#include <functional>

#include "main.h"

/**function definitions **/
void SumUpCalories(const std::string & line, int & calories)
{
    if (!line.empty())
    {
        calories += std::stoi(line);
    }
    else
    {
        calories = 0;
    }
}

void UpdateMaxCals(const int & cals, std::vector<int> & maxCals, int & index)
{
    if (cals > maxCals.at(index))
    {
        maxCals.at(index) = cals;
        std::sort(maxCals.begin(), maxCals.end(), std::greater<int>());
    }

    UpdateIndex(cals, maxCals, index);

}

void UpdateIndex(const int & cals, std::vector<int> & maxCals, int & index)
{
    auto iterator = std::find(maxCals.begin(), maxCals.end(), cals);

    if (iterator != maxCals.end())
    {
        index = iterator - maxCals.begin();
    }
    else
    {
        index = maxCals.size() - 1;
    }
}

void PrintVector(std::vector<int> & vector)
{
    std::cout << "[";
    for (int & elem : vector)
    {
        std::cout << elem << ", ";
    }
    std::cout << "]" << std::endl;
}

void PrintVectorSum(std::vector<int> & vector)
{
    int sum {0};
    for (int & v : vector)
    {
        sum += v;
    }
    std::cout << sum << std::endl;
}

void Solve(const std::string & filepath, const Part & NUM_BACKUPS)
{
    std::cout << std::endl;

    int currentCalories {0};
    std::vector<int> maxCalories(NUM_BACKUPS + 1, 0);
    int index {NUM_BACKUPS};

    std::ifstream file(filepath);
    std::string line;

    while (std::getline(file, line))
    {
        SumUpCalories(line, currentCalories);
        UpdateMaxCals(currentCalories, maxCalories, index);
    }
    file.close();

    PrintVector(maxCalories);
    PrintVectorSum(maxCalories);

}

/** constants **/
// const std::string FILEPATH {"input_short.txt"};
const std::string FILEPATH {"input.txt"};

int main()
{
    Solve(FILEPATH, Part1);
    Solve(FILEPATH, Part2);

    return 0;
}