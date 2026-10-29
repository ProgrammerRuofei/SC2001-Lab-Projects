CXX ?= c++
CPPFLAGS ?= -Iinclude
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -Wpedantic
BUILD := build
CORE := src/input.cpp src/knapsack.cpp src/output.cpp
OBJECTS := $(CORE:src/%.cpp=$(BUILD)/%.o)

.PHONY: all test check-solution clean
all: $(BUILD)/knapsack

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/%.o: src/%.cpp | $(BUILD)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(BUILD)/knapsack: $(BUILD)/main.o $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(BUILD)/test_%: tests/test_%.cpp $(OBJECTS) $(wildcard include/*.hpp) | $(BUILD)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(OBJECTS) -o $@

test: $(BUILD)/test_framework $(BUILD)/knapsack
	./$(BUILD)/test_framework
	python3 tests/test_cli.py ./$(BUILD)/knapsack

check-solution: $(BUILD)/test_knapsack
	./$(BUILD)/test_knapsack

clean:
	rm -rf $(BUILD)

-include $(OBJECTS:.o=.d) $(BUILD)/main.d
