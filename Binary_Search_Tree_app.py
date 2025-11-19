import streamlit as st
import graphviz
import pandas as pd
import time
from collections import deque

class BSTNode:
    """Node class for Binary Search Tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class BinarySearchTree:
    """Binary Search Tree implementation for Streamlit"""
    
    def __init__(self):
        self.root = None
        self.operations_history = []
    
    def log_operation(self, operation, value=None, result=None, details=None):
        """Log operations for history tracking"""
        log_entry = {
            'operation': operation,
            'value': value,
            'result': result,
            'details': details,
            'timestamp': time.time()
        }
        self.operations_history.append(log_entry)
    
    def insert(self, value):
        """Insert a value into the BST"""
        new_node = BSTNode(value)
        
        if self.root is None:
            self.root = new_node
            self.log_operation("INSERT", value, "Success", "Inserted as root")
            return True
        
        temp = self.root
        path = [f"Root({temp.value})"]
        while True:
            if new_node.value == temp.value:
                self.log_operation("INSERT", value, "Failed", "Duplicate value")
                return False
            
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    new_node.parent = temp
                    path.append(f"Left({value})")
                    self.log_operation("INSERT", value, "Success", f"Path: {' → '.join(path)}")
                    return True
                temp = temp.left
                path.append(f"Left({temp.value})")
            else:
                if temp.right is None:
                    temp.right = new_node
                    new_node.parent = temp
                    path.append(f"Right({value})")
                    self.log_operation("INSERT", value, "Success", f"Path: {' → '.join(path)}")
                    return True
                temp = temp.right
                path.append(f"Right({temp.value})")
    
    def contains(self, value):
        """Check if value exists in BST"""
        if self.root is None:
            self.log_operation("SEARCH", value, "Not Found", "Tree is empty")
            return False
        
        temp = self.root
        path = [f"Root({temp.value})"]
        while temp is not None:
            if value < temp.value:
                temp = temp.left
                if temp:
                    path.append(f"Left({temp.value})")
            elif value > temp.value:
                temp = temp.right
                if temp:
                    path.append(f"Right({temp.value})")
            else:
                self.log_operation("SEARCH", value, "Found", f"Path: {' → '.join(path)}")
                return True
        
        self.log_operation("SEARCH", value, "Not Found", f"Path: {' → '.join(path)}")
        return False
    
    def find_min(self):
        """Find minimum value in BST"""
        if self.root is None:
            self.log_operation("FIND_MIN", None, "Failed", "Tree is empty")
            return None
        
        current = self.root
        path = [f"Root({current.value})"]
        while current.left is not None:
            current = current.left
            path.append(f"Left({current.value})")
        
        self.log_operation("FIND_MIN", None, f"Min: {current.value}", f"Path: {' → '.join(path)}")
        return current.value
    
    def find_max(self):
        """Find maximum value in BST"""
        if self.root is None:
            self.log_operation("FIND_MAX", None, "Failed", "Tree is empty")
            return None
        
        current = self.root
        path = [f"Root({current.value})"]
        while current.right is not None:
            current = current.right
            path.append(f"Right({current.value})")
        
        self.log_operation("FIND_MAX", None, f"Max: {current.value}", f"Path: {' → '.join(path)}")
        return current.value
    
    def delete(self, value):
        """Delete a value from BST"""
        self.root, deleted = self._delete_node(self.root, value)
        if deleted:
            self.log_operation("DELETE", value, "Success", "Node deleted successfully")
        else:
            self.log_operation("DELETE", value, "Failed", "Value not found")
    
    def _delete_node(self, node, value):
        """Recursive helper for delete"""
        if node is None:
            return node, False
        
        if value < node.value:
            node.left, deleted = self._delete_node(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_node(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            
            # Node with two children
            min_node = self._find_min_node(node.right)
            node.value = min_node.value
            node.right, _ = self._delete_node(node.right, min_node.value)
            return node, True
        
        return node, deleted
    
    def _find_min_node(self, node):
        """Find node with minimum value in subtree"""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def inorder_traversal(self):
        """In-order traversal"""
        result = []
        
        def traverse(node):
            if node:
                traverse(node.left)
                result.append(node.value)
                traverse(node.right)
        
        traverse(self.root)
        self.log_operation("TRAVERSAL", "INORDER", f"Result: {result}", "Left → Root → Right")
        return result
    
    def preorder_traversal(self):
        """Pre-order traversal"""
        result = []
        
        def traverse(node):
            if node:
                result.append(node.value)
                traverse(node.left)
                traverse(node.right)
        
        traverse(self.root)
        self.log_operation("TRAVERSAL", "PREORDER", f"Result: {result}", "Root → Left → Right")
        return result
    
    def postorder_traversal(self):
        """Post-order traversal"""
        result = []
        
        def traverse(node):
            if node:
                traverse(node.left)
                traverse(node.right)
                result.append(node.value)
        
        traverse(self.root)
        self.log_operation("TRAVERSAL", "POSTORDER", f"Result: {result}", "Left → Right → Root")
        return result
    
    def level_order_traversal(self):
        """Level-order traversal"""
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        self.log_operation("TRAVERSAL", "LEVELORDER", f"Result: {result}", "Breadth-first level by level")
        return result
    
    def height(self):
        """Calculate tree height"""
        def calc_height(node):
            if node is None:
                return 0
            return 1 + max(calc_height(node.left), calc_height(node.right))
        
        return calc_height(self.root)
    
    def get_tree_info(self):
        """Get comprehensive tree information"""
        if self.root is None:
            return {
                'root': None,
                'height': 0,
                'node_count': 0,
                'min_value': None,
                'max_value': None,
                'is_valid_bst': True,
                'is_balanced': True
            }
        
        node_count = len(self.inorder_traversal())
        min_val = self.find_min()
        max_val = self.find_max()
        
        return {
            'root': self.root.value,
            'height': self.height(),
            'node_count': node_count,
            'min_value': min_val,
            'max_value': max_val,
            'is_valid_bst': self._is_valid_bst(),
            'is_balanced': self._is_balanced()
        }
    
    def _is_valid_bst(self):
        """Check if tree is a valid BST"""
        def validate(node, min_val=float('-inf'), max_val=float('inf')):
            if node is None:
                return True
            if node.value <= min_val or node.value >= max_val:
                return False
            return (validate(node.left, min_val, node.value) and 
                    validate(node.right, node.value, max_val))
        
        return validate(self.root)
    
    def _is_balanced(self):
        """Check if tree is balanced"""
        def check_balance(node):
            if node is None:
                return True, 0
            
            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)
            
            balanced = (left_balanced and right_balanced and 
                       abs(left_height - right_height) <= 1)
            
            return balanced, 1 + max(left_height, right_height)
        
        balanced, _ = check_balance(self.root)
        return balanced
    
    def visualize_graphviz(self):
        """Create Graphviz visualization of the tree"""
        dot = graphviz.Digraph()
        dot.attr('node', shape='circle')
        
        if self.root is None:
            dot.node('empty', 'Empty Tree', shape='plaintext')
            return dot
        
        # Add nodes and edges recursively
        def add_nodes_edges(node, parent_id=None, direction=''):
            if node is None:
                return
            
            node_id = f'node_{node.value}'
            dot.node(node_id, str(node.value))
            
            if parent_id:
                dot.edge(parent_id, node_id, label=direction)
            
            add_nodes_edges(node.left, node_id, 'L')
            add_nodes_edges(node.right, node_id, 'R')
        
        add_nodes_edges(self.root)
        return dot

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'bst' not in st.session_state:
        st.session_state.bst = BinarySearchTree()
    if 'auto_demo_done' not in st.session_state:
        st.session_state.auto_demo_done = False

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="BST Visualization",
        page_icon="🌳",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .operation-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .tree-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🌳 Binary Search Tree Simulator</h1>', unsafe_allow_html=True)
    
    # Sidebar for operations
    with st.sidebar:
        st.header("🎯 BST Operations")
        
        # Insert operation
        st.subheader("Insert Node")
        insert_val = st.number_input("Enter value to insert:", step=1, value=50)
        if st.button("🚀 Insert", use_container_width=True):
            st.session_state.bst.insert(insert_val)
            st.rerun()
        
        # Search operation
        st.subheader("Search Node")
        search_val = st.number_input("Enter value to search:", step=1, value=50)
        if st.button("🔍 Search", use_container_width=True):
            found = st.session_state.bst.contains(search_val)
            if found:
                st.success(f"✅ Value {search_val} found!")
            else:
                st.error(f"❌ Value {search_val} not found!")
        
        # Delete operation
        st.subheader("Delete Node")
        delete_val = st.number_input("Enter value to delete:", step=1, value=50)
        if st.button("🗑️ Delete", use_container_width=True):
            st.session_state.bst.delete(delete_val)
            st.rerun()
        
        st.markdown("---")
        
        # Tree operations
        st.subheader("Tree Operations")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Find Min", use_container_width=True):
                min_val = st.session_state.bst.find_min()
                if min_val is not None:
                    st.info(f"Minimum: {min_val}")
                else:
                    st.warning("Tree is empty!")
        
        with col2:
            if st.button("📉 Find Max", use_container_width=True):
                max_val = st.session_state.bst.find_max()
                if max_val is not None:
                    st.info(f"Maximum: {max_val}")
                else:
                    st.warning("Tree is empty!")
        
        # Demo operations
        st.markdown("---")
        st.subheader("Demo Operations")
        demo_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
        
        if st.button("🎮 Auto Demo", use_container_width=True):
            st.session_state.bst = BinarySearchTree()
            for val in demo_values:
                st.session_state.bst.insert(val)
            st.session_state.auto_demo_done = True
            st.rerun()
        
        if st.button("🧹 Clear Tree", use_container_width=True):
            st.session_state.bst = BinarySearchTree()
            st.session_state.auto_demo_done = False
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌳 Tree Visualization")
        
        # Graphviz visualization
        dot = st.session_state.bst.visualize_graphviz()
        st.graphviz_chart(dot, use_container_width=True)
        
        # Tree traversals
        st.header("🔄 Tree Traversals")
        if st.session_state.bst.root is not None:
            trav_col1, trav_col2, trav_col3, trav_col4 = st.columns(4)
            
            with trav_col1:
                if st.button("In-order"):
                    result = st.session_state.bst.inorder_traversal()
                    st.write(f"**In-order:** {result}")
            
            with trav_col2:
                if st.button("Pre-order"):
                    result = st.session_state.bst.preorder_traversal()
                    st.write(f"**Pre-order:** {result}")
            
            with trav_col3:
                if st.button("Post-order"):
                    result = st.session_state.bst.postorder_traversal()
                    st.write(f"**Post-order:** {result}")
            
            with trav_col4:
                if st.button("Level-order"):
                    result = st.session_state.bst.level_order_traversal()
                    st.write(f"**Level-order:** {result}")
        else:
            st.info("🌱 Tree is empty. Insert some values to see traversals!")
    
    with col2:
        st.header("📊 Tree Information")
        
        tree_info = st.session_state.bst.get_tree_info()
        
        if tree_info['root'] is not None:
            st.markdown(f"""
            <div class="tree-info">
                <h3>🌲 Tree Stats</h3>
                <p><strong>Root:</strong> {tree_info['root']}</p>
                <p><strong>Height:</strong> {tree_info['height']}</p>
                <p><strong>Nodes:</strong> {tree_info['node_count']}</p>
                <p><strong>Min Value:</strong> {tree_info['min_value']}</p>
                <p><strong>Max Value:</strong> {tree_info['max_value']}</p>
                <p><strong>Valid BST:</strong> {'✅' if tree_info['is_valid_bst'] else '❌'}</p>
                <p><strong>Balanced:</strong> {'✅' if tree_info['is_balanced'] else '❌'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("🌱 Tree is empty!")
        
        # Operations history
        st.header("📝 Recent Operations")
        if st.session_state.bst.operations_history:
            recent_ops = st.session_state.bst.operations_history[-8:]  # Last 8 operations
            
            for op in reversed(recent_ops):
                with st.container():
                    st.markdown(f"""
                    <div class="operation-card">
                        <strong>{op['operation']}</strong> {f"({op['value']})" if op['value'] else ""}<br>
                        <small>Result: {op['result']}</small><br>
                        <small style="color: #666;">{op['details']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No operations yet!")
    
    # Demo explanation
    if st.session_state.auto_demo_done:
        st.markdown("---")
        st.header("🎓 BST Learning Guide")
        
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            st.subheader("📚 BST Properties")
            st.markdown("""
            - **Binary Tree**: Each node has at most 2 children
            - **Search Property**: Left child < Parent < Right child
            - **Efficient Operations**: O(h) time complexity
            - **Balanced vs Unbalanced**: Height affects performance
            """)
            
            st.subheader("🎯 Operations Complexity")
            st.markdown("""
            - **Search**: O(h) - depends on tree height
            - **Insert**: O(h) - find position and insert
            - **Delete**: O(h) - find and reorganize
            - **Traversal**: O(n) - visit all nodes
            """)
        
        with exp_col2:
            st.subheader("🔄 Traversal Types")
            st.markdown("""
            - **In-order**: Left → Root → Right (Sorted order)
            - **Pre-order**: Root → Left → Right (Copying trees)
            - **Post-order**: Left → Right → Root (Deletion)
            - **Level-order**: Level by level (Breadth-first)
            """)
            
            st.subheader("💡 Pro Tips")
            st.markdown("""
            - Keep tree balanced for optimal performance
            - Use in-order traversal to get sorted values
            - BSTs are great for dynamic data sets
            - Watch tree height for performance monitoring
            """)

if __name__ == "__main__":
    main()
