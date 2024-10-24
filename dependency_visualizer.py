import argparse
import subprocess
import graphviz

def parse_arguments():
    parser = argparse.ArgumentParser(description='Visualize package dependencies.')
    parser.add_argument('--graphviz-path', required=True, help='Path to Graphviz executable')
    parser.add_argument('--package-name', required=True, help='Name of the package to analyze')
    parser.add_argument('--output-file', required=True, help='Path to the output file')
    parser.add_argument('--max-depth', type=int, required=True, help='Maximum depth of dependency analysis')
    parser.add_argument('--repo-url', required=False, help='URL of the repository')
    return parser.parse_args()

def get_dependencies(package_name, depth, max_depth, visited, graph):
    if depth > max_depth or package_name in visited:
        return
    
    visited.add(package_name)
    result = subprocess.run(['apt-cache', 'depends', package_name], capture_output=True, text=True)
    
    print(f'Analyzing {package_name}...')
    print(result.stdout)
    for line in result.stdout.split('\n'):
        if line.strip().startswith('Depends:'):
            dep = line.split(':')[1].strip()
            graph.append((package_name, dep))
            get_dependencies(dep, depth + 1, max_depth, visited, graph)

def generate_graph(graph):
    dot = graphviz.Digraph(comment='Dependencies Graph')
    
    for parent, child in graph:
        dot.node(parent, parent)
        dot.node(child, child)
        dot.edge(parent, child)
    
    return dot

def main():
    args = parse_arguments()
    
    graph = []
    get_dependencies(args.package_name, 0, args.max_depth, set(), graph)
    dot = generate_graph(graph)
    
    # Save the Graphviz source code to the output file
    with open(args.output_file, 'w') as f:
        f.write(dot.source)
    
    # Render the graph to a PNG file
    png_output_file = args.output_file.replace('.dot', '.png')
    dot.render(png_output_file, format='png', engine='dot')
    
    print(f'Graphviz code written to {args.output_file}')
    print(f'PNG image written to {png_output_file}')

if __name__ == '__main__':
    main()