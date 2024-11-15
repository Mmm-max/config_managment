import os
import graphviz

def get_folder_dependencies(folder_path, depth, max_depth, visited, graph):
    if depth > max_depth or folder_path in visited:
        print(f'Stopping analysis for {folder_path}')
        return
    
    visited.add(folder_path)
    all_entries = os.listdir(folder_path)
    subdirectories = [entry for entry in all_entries if os.path.isdir(os.path.join(folder_path, entry))]
    for dirs in os.walk(folder_path):
        # Вычисляем текущую глубину
        current_depth = root.count(os.sep) - folder_path.count(os.sep)
        
        if current_depth > max_depth:
            continue
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            if dir_path not in visited:
                graph.append((root, dir_path))
                get_folder_dependencies(dir_path, depth + 1, max_depth, visited, graph)

def generate_graph(graph):
    dot = graphviz.Digraph(comment='Folder Dependencies Graph')
    
    for parent, child in graph:
        dot.node(parent, parent)
        dot.node(child, child)
        dot.edge(parent, child)
    
    return dot

def main():
    directory = 'temp/repo'  # Укажите путь к вашей папке
    max_depth = 2  # Укажите максимальную глубину анализа
    
    graph = []
    get_folder_dependencies(directory, 0, max_depth, set(), graph)
    dot = generate_graph(graph)
    
    # Save the Graphviz source code to the output file
    output_file = 'output.dot'
    with open(output_file, 'w') as f:
        f.write(dot.source)
    
    # Render the graph to a PNG file
    png_output_file = output_file.replace('.dot', '.png')
    dot.render(png_output_file, format='png', engine='dot')
    
    print(f'Graphviz code written to {output_file}')
    print(f'PNG image written to {png_output_file}')

if __name__ == '__main__':
    main()