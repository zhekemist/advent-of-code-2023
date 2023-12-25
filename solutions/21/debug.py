def print_garden(garden: list[str], marked: set[tuple[int, int]], overwrite_plots: bool = False) -> None:
    print('\n'.join(
        ''.join('O' if (row, col) in marked and (overwrite_plots or plot == '.') else plot
                for col, plot in enumerate(line))
        for row, line in enumerate(garden)
    ))
