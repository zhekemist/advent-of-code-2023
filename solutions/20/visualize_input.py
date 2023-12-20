"""
Transforms the input into a digraph in the DOT file format.
The output can be visualized with Graphviz, e.g. here: https://dreampuf.github.io/GraphvizOnline
"""


def parse_modules(file_path: str) -> dict[str, list[str]]:
    module_outputs = {}

    for line in open(file_path).readlines():
        module, outputs = line.split(' -> ')
        outputs = outputs.split(', ')
        module_outputs[module] = outputs

    return module_outputs


def main():
    modules = parse_modules("../../input/day_20.txt")

    graph_dot_lines = ["digraph {"]

    for module, module_outputs in modules.items():
        if module[0] == '&':
            node_attr = f' [label="Conjunction_{module[1:]}" color = red]'
        elif module[0] == '%':
            node_attr = f' [label="FlipFlop_{module[1:]}" color = blue]'
        else:
            node_attr = ''

        module = module.strip('&%')
        graph_dot_lines.append(module + node_attr)

        for output in module_outputs:
            output = output.strip('&%')
            graph_dot_lines.append(f'{module} -> {output}')

    graph_dot_lines.append('}')

    print('\n'.join(graph_dot_lines))


if __name__ == '__main__':
    main()
