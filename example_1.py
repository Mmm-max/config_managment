import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Example Graph')

# Add nodes
dot.node('A', 'Node A')
dot.node('B', 'Node B')
dot.node('C', 'Node C')

# Add edges
dot.edges(['AB', 'BC', 'CA'])

# Render the graph to a file
dot.render('output/graph', format='png')

# Print the source code of the graph
print(dot.source)