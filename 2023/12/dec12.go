package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type State struct {
	index     int
	condition int
}

func parseLine(input string) (string, []int) {
	split := strings.Split(input, " ")
	conditionStr := strings.Split(split[1], ",")

	condition := make([]int, len(conditionStr))
	for i, str := range conditionStr {
		condition[i], _ = strconv.Atoi(str)
	}

	return split[0], condition
}

func valid_index(state string, start int, length int) bool {
	// Determine if start and length describe a valid location for a substring of hashes
	if start-1 > 0 && start-1 < len(state) {
		if state[start-1] == '#' {
			return false
		}
	}

	for i := 0; i < length; i++ {
		if start+i >= len(state) {
			return false
		} else if state[start+i] == '.' {
			return false
		}
	}

	if start+length > 0 && start+length < len(state) {
		if state[start+length] == '#' {
			return false
		}
	}

	return true
}

func requiredLength(condition []int) int {
	// Determine the shortest string required for all remaining sets of hashes to be present
	sum := 0
	for _, value := range condition {
		sum += value
	}
	return sum + len(condition)
}

func arrangements(spring string, condition []int, cache *map[State]uint64, state State) uint64 {
	// Count the number of valid arrangements of each line of the input
	if value, found := (*cache)[state]; found {
		return value
	}

	// If all conditions were used, verify that no other hashes have gone unused
	if state.condition >= len(condition) {
		if state.index < len(spring) {
			for _, char := range spring[state.index:] {
				if char == '#' {
					return 0
				}
			}
		}
		return 1
	}

	// Determine range of possible locations for the next hash
	start := state.index
	end := len(spring) - requiredLength(condition[state.condition+1:])
	currentSize := condition[state.condition]

	total := uint64(0)
	for i := start; i < end; i++ {
		if valid_index(spring, i, currentSize) {
			next_state := State{
				index:     i + currentSize + 1,
				condition: state.condition + 1,
			}
			total += arrangements(spring, condition, cache, next_state)
		}

		// You can't skip over hashes; if an index has a hash, stop looking further
		if spring[i] == '#' {
			break
		}
	}

	// cache results
	(*cache)[state] = total
	return total
}

func main() {
	data, err := os.ReadFile("input.txt")
	if err != nil {
		log.Fatalf("Failed to read input file: %s", err)
	}

	lines := strings.Split(string(data), "\n")
	total := uint64(0)
	total_x5 := uint64(0)
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		springs, condition := parseLine(line)
		cache := make(map[State]uint64)
		total += arrangements(springs, condition, &cache, State{0, 0})

		cache_x5 := make(map[State]uint64)

		var condition_x5 []int
		var springs_x5_arr []string
		for i := 0; i < 5; i++ {
			springs_x5_arr = append(springs_x5_arr, springs)
			condition_x5 = append(condition_x5, condition...)
		}
		springs_x5 := strings.Join(springs_x5_arr, "?")
		total_x5 += arrangements(springs_x5, condition_x5, &cache_x5, State{0, 0})
	}

	fmt.Printf("Total arrangements: %d\n", total)
	fmt.Printf("Total arrangements in x5: %d\n", total_x5)
}
