#include <string>
#include <vector>

enum Part
{
    Part1 = 0,
    Part2 = 2,
};

void SumUpCalories(const std::string & line, int & calories);
void UpdateMaxCals(const int & cals, std::vector<int> & maxCals, int & index);
void UpdateIndex(const int & cals, std::vector<int> & maxCals, int & index);

void PrintVector(std::vector<int> & vector);
void PrintVectorSum(std::vector<int> & vector);

void Solve(const std::string & filepath, const int & part);
