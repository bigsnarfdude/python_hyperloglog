from HLLMonoid import HLLMonoid
from Generators import Generator
import random
from typing import List, Tuple
import matplotlib.pyplot as plt

def test_hll_accuracy(sample_sizes: List[int], range_size: int) -> List[Tuple[int, float, float]]:
    results = []
    for size in sample_sizes:
        # Generate random numbers
        numbers = Generator.random_numbers(size, range_size)
        actual_unique = len(set(numbers))
        
        # Create HLL estimate
        hll = HLLMonoid.load_list_int(numbers)
        estimated_unique = hll.count()
        
        # Calculate error percentage
        error_percent = abs(actual_unique - estimated_unique) / actual_unique * 100
        results.append((size, actual_unique, error_percent))
        
        print(f"\nSample size: {size:,}")
        print(f"Actual unique values: {actual_unique:,}")
        print(f"HLL estimated unique values: {int(estimated_unique):,}")
        print(f"Error percentage: {error_percent:.2f}%")
    
    return results

def plot_results(results: List[Tuple[int, float, float]]):
    plt.figure(figsize=(10, 6))
    
    sample_sizes = [r[0] for r in results]
    errors = [r[2] for r in results]
    
    plt.semilogx(sample_sizes, errors, 'bo-')
    plt.grid(True)
    plt.xlabel('Sample Size')
    plt.ylabel('Error Percentage')
    plt.title('HyperLogLog Accuracy vs Sample Size')
    
    return plt

# Test with different sample sizes
sample_sizes = [100, 1000, 10000, 100000, 1000000]
range_size = 1000000  # Range for random number generation

results = test_hll_accuracy(sample_sizes, range_size)
plot = plot_results(results)
plot.show()

# Additional test with overlap detection
def test_overlap_accuracy():
    # Generate two sets with known overlap
    set1 = set(Generator.random_numbers(100000, 1000000))
    set2 = set(Generator.random_numbers(100000, 1000000))
    
    # Create intersection
    overlap_size = 20000
    overlap = random.sample(list(set1), overlap_size)
    set2.update(overlap)
    
    # Convert to HLL
    hll1 = HLLMonoid.load_list_int(list(set1))
    hll2 = HLLMonoid.load_list_int(list(set2))
    
    # Merge HLLs
    hll1.merge(hll2)
    
    actual_union = len(set1.union(set2))
    estimated_union = hll1.count()
    
    print("\nOverlap Detection Test:")
    print(f"Actual union size: {actual_union:,}")
    print(f"HLL estimated union size: {int(estimated_union):,}")
    print(f"Error percentage: {abs(actual_union - estimated_union) / actual_union * 100:.2f}%")

test_overlap_accuracy()
