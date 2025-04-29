import numpy as np
import matplotlib.pyplot as plt


def simulate_line_with_multiple_fails(
    n_wafers,
    n_tools,
    base_fail_rate,
    critical_tool_index,
    critical_tool_fail_rate,
    boosted_fail_rate,
):
    """
    Simulate a production line where wafers can fail multiple times,
    accumulating failure counts instead of being killed.
    A single critical tool flags wafers for subsequent boosted fail rates.

    Returns:
        avg_failures: average number of failures per wafer
        total_failures: total number of fails across all wafers
    """
    fail_counts = np.zeros(n_wafers, dtype=int)
    critical_failed = np.zeros(n_wafers, dtype=bool)

    for i in range(n_tools):
        if i == critical_tool_index:
            current_fail_rate = np.full(n_wafers, critical_tool_fail_rate)
        elif i > critical_tool_index:
            current_fail_rate = np.where(critical_failed, boosted_fail_rate, base_fail_rate)
        else:
            current_fail_rate = np.full(n_wafers, base_fail_rate)

        fails = np.random.rand(n_wafers) < current_fail_rate
        fail_counts += fails
        if i == critical_tool_index:
            critical_failed |= fails

    return fail_counts.mean(), fail_counts.sum()


# Config
n_wafers = 10000
n_tools = 100
base_fail_rate = 0.005
boosted_fail_rate = 0.05
critical_tool_fail_rate = 0.5

# Run simulations
critical_indices = np.arange(n_tools)
average_failures = []
total_fails = []

for idx in critical_indices:
    avg, total = simulate_line_with_multiple_fails(
        n_wafers, n_tools, base_fail_rate, idx, critical_tool_fail_rate, boosted_fail_rate
    )
    average_failures.append(avg)
    total_fails.append(total)


# === Plot: Total Failures Only ===
plt.figure(figsize=(10, 6))
plt.plot(critical_indices, total_fails, marker="o", linestyle="-", color="orange")
plt.xlabel("Critical Tool Index (Position in Line)")
plt.ylabel("Total Failures (All Wafers)")
plt.title("Effect of Critical Tool Position on Total Wafer Failures")
plt.grid(True)
plt.tight_layout()

# === Optional Plot: Average Failures Per Wafer ===
# Uncomment this section if you want to visualize the average as well

plt.figure(figsize=(10, 6))
plt.plot(critical_indices, average_failures, marker="o", linestyle="-", color="blue")
plt.xlabel("Critical Tool Index (Position in Line)")
plt.ylabel("Average Failures per Wafer")
plt.title("Effect of Critical Tool Position on Average Failures per Wafer")
plt.grid(True)
plt.tight_layout()
plt.show()
