import argparse
import subprocess
import graphviz
import os
import shutil
from git import Repo

def parse_arguments():
    parser = argparse.ArgumentParser(description='Visualize package dependencies.')
    parser.add_argument('--graphviz-path', required=True, help='Path to Graphviz executable')
    parser.add_argument('--package-name', required=True, help='Name of the package to analyze')
    parser.add_argument('--output-file', required=True, help='Path to the output file')
    parser.add_argument('--max-depth', type=int, required=True, help='Maximum depth of dependency analysis')
    parser.add_argument('--repo-url', required=False, help='URL of the repository')
    return parser.parse_args()

def clone_repository(repo_url, clone_path):
    # clone_path = "/workspaces/config_managment_2" + clone_path
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)
    Repo.clone_from(repo_url, clone_path)
    print('Repository cloned successfully.', clone_path)

def get_dependencies(package_name, depth, max_depth, visited, graph, repo_path):
    if depth >= max_depth or package_name in visited:
        print(f'Stopping analysis for {package_name}')
        return
    
    visited.add(package_name)
    result = subprocess.run(['apt-cache', 'depends', package_name], capture_output=True, text=True)
    
    print(f'Analyzing {package_name}...')
    print('result:', result.stdout)
    for line in result.stdout.split('\n'):
        if line.strip().startswith('Depends:'):
            dep = line.split(':')[1].strip()
            graph.append((package_name, dep))
            get_dependencies(dep, depth + 1, max_depth, visited, graph, repo_path)

def generate_graph(graph):
    dot = graphviz.Digraph(comment='Dependencies Graph')
    
    for parent, child in graph:
        dot.node(parent, parent)
        dot.node(child, child)
        dot.edge(parent, child)
    
    return dot

def main():
    args = parse_arguments()
    clone_path = "/workspaces/config_managment_2/tmp/repo"
    if args.repo_url:
        clone_repository(args.repo_url, clone_path)
    
    graph = []
    get_dependencies(args.package_name, 0, args.max_depth, set(), graph, clone_path)
    
    dot = generate_graph(graph)
    
    # Set the path to Graphviz executable
    os.environ["PATH"] += os.pathsep + os.path.dirname(args.graphviz_path)
    
    dot.render(args.output_file, format='png')

if __name__ == '__main__':
    main()