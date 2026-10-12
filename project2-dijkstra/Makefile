CXX ?= c++
CPPFLAGS ?= -Iinclude
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -Wpedantic
BUILD := build
CORE := src/graph.cpp src/generation.cpp src/dijkstra_matrix.cpp src/min_heap.cpp src/dijkstra_heap.cpp src/output.cpp src/benchmark.cpp
OBJECTS := $(CORE:src/%.cpp=$(BUILD)/%.o)
TESTS := $(BUILD)/test_graph $(BUILD)/test_matrix $(BUILD)/test_heap $(BUILD)/test_heap_dijkstra $(BUILD)/test_dijkstra $(BUILD)/test_generation

.PHONY: all test test-graph test-matrix test-heap test-heap-dijkstra test-dijkstra test-generation test-cli clean
all: $(BUILD)/dijkstra_benchmark

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/%.o: src/%.cpp | $(BUILD)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(BUILD)/dijkstra_benchmark: $(BUILD)/main.o $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(BUILD)/test_%: tests/test_%.cpp $(OBJECTS) $(wildcard include/*.hpp) $(wildcard tests/*.hpp) | $(BUILD)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(OBJECTS) -o $@

test: $(TESTS) $(BUILD)/dijkstra_benchmark
	@status=0; for test_bin in $(TESTS); do "$$test_bin"; code=$$?; if [ $$code -ne 0 ]; then status=1; fi; done; python3 tests/test_cli.py --binary $(BUILD)/dijkstra_benchmark; code=$$?; if [ $$code -ne 0 ]; then status=1; fi; exit $$status

test-graph: $(BUILD)/test_graph
	"$<"
test-matrix: $(BUILD)/test_matrix
	"$<"
test-heap: $(BUILD)/test_heap
	"$<"
test-heap-dijkstra: $(BUILD)/test_heap_dijkstra
	"$<"
test-dijkstra: $(BUILD)/test_dijkstra
	"$<"
test-generation: $(BUILD)/test_generation
	"$<"

test-cli: $(BUILD)/dijkstra_benchmark
	python3 tests/test_cli.py --binary $(BUILD)/dijkstra_benchmark

clean:
	rm -rf $(BUILD)

-include $(OBJECTS:.o=.d) $(BUILD)/main.d
