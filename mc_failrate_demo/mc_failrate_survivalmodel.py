import numpy as np
import matplotlib.pyplot as plt


def simulate_line_with_critical_tool(
    n_wafers,
    n_tools,
    base_fail_rate,
    critical_tool_index,
    critical_tool_fail_rate,
    boosted_fail_rate,
):
    """
    Simulate a production line where a single critical tool affects later
        steps' fail rates.

    Returns:
        final_yield: percentage of wafers that survive all tools
    """
    wafers_alive = np.ones(n_wafers, dtype=bool)
    critical_failed = np.zeros(n_wafers, dtype=bool)

    print(f"\n=== Simulating with critical tool at index {critical_tool_index} ===")
    # print(
    #     f"{'Tool':<5} {'Alive':<21} {'Fails':<21} {'Crit Failed':<21} {'Fail Rates':<30}"
    # )

    for i in range(n_tools):
        if i == critical_tool_index:
            current_fail_rate = np.full(n_wafers, critical_tool_fail_rate)
        elif i > critical_tool_index:
            current_fail_rate = np.where(critical_failed, boosted_fail_rate, base_fail_rate)
        else:
            current_fail_rate = np.full(n_wafers, base_fail_rate)

        # Determine failures at this step
        rand_vals = np.random.rand(n_wafers)
        fails = (rand_vals < current_fail_rate) & wafers_alive

        if i == critical_tool_index:
            # Tag as critical failed, but don't kill wafer
            critical_failed |= fails
        else:
            # Other steps: actual fails kill wafers
            wafers_alive &= ~fails

        # Print debugging info
        # print(
        #     f"{i:<5} "
        #     f"{str(wafers_alive.astype(int)):<15} "
        #     f"{str(fails.astype(int)):<15} "
        #     f"{str(critical_failed.astype(int)):<15} "
        #     f"{str(np.round(current_fail_rate, 2)):<30}"
        # )

    return np.sum(wafers_alive) / n_wafers  # return yield


# Config
n_wafers = 10000
n_tools = 100
base_fail_rate = 0.005  # 2%
boosted_fail_rate = 0.05  # 20% if failed at the critical tool

# Sweep critical tool index from 0 to 99
critical_indices = np.arange(n_tools)
critical_tool_fail_rate = 0.5  # Much higher fail rate for critical tool
final_yields = []

for idx in critical_indices:
    yield_ = simulate_line_with_critical_tool(
        n_wafers=n_wafers,
        n_tools=n_tools,
        base_fail_rate=base_fail_rate,
        critical_tool_index=idx,
        critical_tool_fail_rate=critical_tool_fail_rate,
        boosted_fail_rate=boosted_fail_rate,
    )
    final_yields.append(yield_)

# Convert to fail rate for plotting
final_fail_rates = 1 - np.array(final_yields)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(critical_indices, final_fail_rates, marker="o", linestyle="-")
plt.xlabel("Critical Tool Index (Position in Line)")
plt.ylabel("Total Final Fail Rate")
plt.title("Effect of Critical Tool Position on Final Wafer Fail Rate")
plt.grid(True)
plt.tight_layout()
plt.show()
