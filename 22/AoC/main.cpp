#include <deque>
#include <map>
#include <set>
#include <vector>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cassert>

#define CASE 2

typedef long number_t;
typedef int16_t diff_t;

inline number_t evolve(number_t number) {
    number_t new_number = (number ^ (number << 6)) & 0b0111111111111111111111111;
    new_number = (new_number ^ (new_number >> 5));
    return (new_number ^ (new_number << 11)) & 0b0111111111111111111111111;
}

std::vector<number_t> readFile(const std::string& filename) {
    std::vector<number_t> numbers;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return numbers; // Return empty vector on failure
    }

    std::string line;
    while (std::getline(file, line)) {
        int number;
        std::istringstream iss(line);
        if (iss >> number) {
            numbers.push_back(number);
        } else {
            std::cerr << "Warning: Invalid integer in line: " << line << std::endl;
        }
    }

    file.close();
    return numbers;
}

std::set<std::vector<diff_t>> all_diffs;

number_t part_1(std::vector<number_t> initial_secret_numbers) {
    number_t answer1 = 0;
    for (auto number: initial_secret_numbers) {
        std::deque<diff_t> diff_deque;
        number_t previous;
        for (int j = 0; j < 3; ++j) {
            previous = number;
            number = evolve(number);
            diff_deque.push_back((number % 10) - (previous % 10));
        }
        for (int j = 3; j < 2000; ++j) {
            previous = number;
            number = evolve(number);
            diff_deque.push_back((number % 10) - (previous % 10));
            // Create a std::Vector from diff_deque
            std::vector<diff_t> diff_vector(diff_deque.begin(), diff_deque.end());
            all_diffs.insert(diff_vector);
            diff_deque.pop_front();
        }
//        printf("Number: %ld\n", number);
        answer1 += number;
    }

//    for (auto it = all_diffs.begin(); it != all_diffs.end(); ++it) {
//        //print the vector pointed to by it
//        for (auto it2 = it->begin(); it2 != it->end(); ++it2) {
//            std::cout << (int)*it2 << " ";
//        }
//        std::cout << std::endl;
//    }
    return answer1;
}

number_t match_diff(std::vector<number_t> initial_secret_numbers, std::vector<diff_t> current_diff) {
    int total_bananas = 0;
    std::deque<diff_t> diff_deque;
    number_t previous;
    for (auto number: initial_secret_numbers) {
        diff_deque.clear();
        for (int j = 0; j < 3; ++j) {
            previous = number;
            number = evolve(number);
            diff_deque.push_back((number % 10) - (previous % 10));
        }

        for (int j = 3; j < 2000; ++j) {
            previous = number;
            number = evolve(number);
            diff_deque.push_back((number % 10) - (previous % 10));
            assert(diff_deque.size() == 4);
            // Compare the vector current_diff with the current diff_deque
            if (std::equal(current_diff.begin(), current_diff.end(), diff_deque.begin())) {
                total_bananas += number % 10;
                break;
            }
            diff_deque.pop_front();
        }
    }
    return total_bananas;
}

void run_tests() {
    int test_evolutions[] = {123, 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254};
    for (int i = 0; i < 10; ++i) {
        if (evolve(test_evolutions[i]) != test_evolutions[i + 1]) {
            fprintf(stderr, "Test evolution failed at index %d\n", i);
            abort();
        }
    }
    
    std::vector<number_t> initial_secret_numbers = readFile("/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22_test_case_1.txt");
    
    assert(part_1(initial_secret_numbers) == 37327623);
    
    
    initial_secret_numbers = readFile("/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22.txt");
    assert(part_1(initial_secret_numbers) == 17724064040);
    
    initial_secret_numbers = readFile("/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22_test_case_2.txt");
    assert(match_diff(initial_secret_numbers, {-2, 1, -1, 3}) == 23);
}


int main(void) {
    const char* input_file;

//    run_tests();
    all_diffs.clear();
    
    size_t expected_size;
    switch (CASE) {
        case 0:
            input_file = "/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22_test_case_1.txt";
            expected_size = 4;
            break;
        case 1:
            input_file = "/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22_test_case_2.txt";
            expected_size = 4;
            break;
        case 2:
            input_file = "/Users/AndrewParker/dev/git/hormyajp/advent_of_code_2024/input22.txt";
            expected_size = 2098;
            break;
        default:
            fprintf(stderr, "Unknown case\n");
            return 1;
    }
    
    // Read the input file using C++ into a vector of numbers. Each line in the file is an integer
    std::vector<number_t> initial_secret_numbers = readFile(input_file);
    assert(initial_secret_numbers.size() == expected_size);
    
    clock_t start = clock();
    number_t answer1 = part_1(initial_secret_numbers);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken for part 1: %f seconds\n", time_taken);
    printf("Part 1: %ld\n", answer1);


    printf("Number of unique differences: %lu\n", all_diffs.size());
    number_t best_bananas = 0;
    std::vector<diff_t> best_banana_diff;
    int x = 0;
    for (const auto& current_diff : all_diffs) {
        x++;
        if (x % 100 == 0) {
            printf("x: %d\n", x);
        }
        
        number_t total_bananas = match_diff(initial_secret_numbers, current_diff);
        if (total_bananas > best_bananas) {
            best_bananas = total_bananas;
            // Copy the contets of diff_deque into best_banana_diff
            best_banana_diff = std::vector<diff_t>(current_diff.begin(), current_diff.end());
        }
    }
        
    printf("Part 2: %ld\n", best_bananas);
    printf("Best banana diff: ");
    for (auto it = best_banana_diff.begin(); it != best_banana_diff.end(); ++it) {
        std::cout << (int)*it << " ";
    }
        
    
    return 0;
}
