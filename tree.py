from graphviz import Digraph, Source
import streamlit as st
import graphviz


class GraphGenerator:
    @classmethod
    def is_valid_dot(self, dot_string):
        try:
            graphviz.Source(dot_string)
            return True
        except graphviz.backend.CalledProcessError:
            st.write("error hui")
            return False

    # Replace `query` with your DOT code
    def generate_and_render_graph(
        self,
        query,
        filename_prefix="graph",
        format="png",
        cleanup=True,
        rankdir="TB",
    ):
        """
        Generate and render a graph using Graphviz.

        Parameters:
        - query (str): The DOT language code representing the graph.
        - filename_prefix (str): Prefix for the filename of the rendered graph.
        - format (str): The format in which the graph should be rendered (e.g., 'png').
        - cleanup (bool): Whether to remove intermediate files after rendering.
        - rankdir (str): Layout direction ('TB' for top-to-bottom, 'LR' for left-to-right).
        """
        # Create a Digraph object
        if GraphGenerator.is_valid_dot(query):
            # Display the graph using st.graphviz_chart
            st.graphviz_chart(query)
        return True


# Create a GraphGenerator object
graph = GraphGenerator()
