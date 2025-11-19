import streamlit as st
import pandas as pd
import time
from collections import deque

class BSTNode:
    """Node class for Binary Search Tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

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
                    path.append(f"Left({value})")
                    self.log_operation("INSERT", value, "Success", f"Path: {' → '.join(path)}")
                    return True
                temp = temp.left
                path.append(f"Left({temp.value})")
            else:
                if temp.right is None:
                    temp.right = new_node
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
        self.root = self._delete_node(self.root, value)
        self.log_operation("DELETE", value, "Success", "Node deleted successfully")
    
    def _delete_node(self, node, value):
        """Recursive helper for delete"""
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete_node(node.left, value)
        elif value > node.value:
            node.right = self._delete_node(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children
            min_node = self._find_min_node(node.right)
            node.value = min_node.value
            node.right = self._delete_node(node.right, min_node.value)
        
        return node
    
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
        
        inorder = self.inorder_traversal()
        node_count = len(inorder)
        min_val = min(inorder) if inorder else None
        max_val = max(inorder) if inorder else None
        
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
    
    def visualize_tree(self):
        """Create a text-based visualization of the tree"""
        if self.root is None:
            return "🌳 Tree is empty!"
        
        # Get all nodes by level
        levels = []
        queue = deque([(self.root, 0)])
        
        while queue:
            node, level = queue.popleft()
            if level >= len(levels):
                levels.append([])
            
            if node:
                levels[level].append(str(node.value))
                queue.append((node.left, level + 1))
                queue.append((node.right, level + 1))
            else:
                levels[level].append(" ")
                # Still add placeholders for children to maintain structure
                if level < 4:  # Limit depth for display
                    queue.append((None, level + 1))
                    queue.append((None, level + 1))
        
        # Build the visualization
        lines = []
        for i, level in enumerate(levels):
            if any(node != " " for node in level):
                indent = "  " * (2 ** (len(levels) - i - 1) - 1)
                line = indent + ("  " * (2 ** (len(levels) - i - 1)))
                
                for j, node in enumerate(level):
                    if node != " ":
                        line += f"{node:^3}"
                    else:
                        line += "   "
                    # Add spacing between nodes
                    if j < len(level) - 1:
                        line += " " * (2 ** (len(levels) - i) - 1)
                
                lines.append(line)
                
                # Add connecting lines for next level
                if i < len(levels) - 1 and any(n != " " for n in levels[i]):
                    connector_line = indent + ("  " * (2 ** (len(levels) - i - 1)))
                    for j in range(len(level)):
                        if level[j] != " ":
                            connector_line += " / \\ "
                        else:
                            connector_line += "     "
                        if j < len(level) - 1:
                            connector_line += " " * (2 ** (len(levels) - i) - 5)
                    lines.append(connector_line)
        
        return "\n".join(lines)
    
    def get_tree_structure(self):
        """Get a simple tree structure representation"""
        if self.root is None:
            return "Empty Tree"
        
        def build_structure(node, prefix="", is_left=True):
            if node is None:
                return ""
            
            result = ""
            result += prefix
            result += "└── " if is_left else "┌── "
            result += str(node.value) + "\n"
            
            # Process children
            if node.left or node.right:
                if node.left:
                    result += build_structure(node.left, prefix + ("    " if is_left else "│   "), True)
                if node.right:
                    result += build_structure(node.right, prefix + ("    " if is_left else "│   "), False)
            
            return result
        
        return build_structure(self.root)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'bst' not in st.session_state:
        st.session_state.bst = BinarySearchTree()
    if 'auto_demo_done' not in st.session_state:
        st.session_state.auto_demo_done = False
    if 'last_operation' not in st.session_state:
        st.session_state.last_operation = None

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
    .tree-visualization {
        font-family: 'Courier New', monospace;
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #2E8B57;
        white-space: pre;
        overflow-x: auto;
        font-size: 14px;
        line-height: 1.4;
    }
    .history-item {
        padding: 0.5rem;
        border-left: 3px solid #2E8B57;
        background-color: #f8f9fa;
        margin-bottom: 0.5rem;
        border-radius: 5px;
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
        insert_val = st.number_input("Enter value to insert:", step=1, value=50, key="insert")
        if st.button("🚀 Insert", use_container_width=True, key="insert_btn"):
            st.session_state.bst.insert(insert_val)
            st.session_state.last_operation = f"INSERT {insert_val}"
            st.rerun()
        
        # Search operation
        st.subheader("Search Node")
        search_val = st.number_input("Enter value to search:", step=1, value=50, key="search")
        if st.button("🔍 Search", use_container_width=True, key="search_btn"):
            found = st.session_state.bst.contains(search_val)
            st.session_state.last_operation = f"SEARCH {search_val}"
            st.rerun()
        
        # Delete operation
        st.subheader("Delete Node")
        delete_val = st.number_input("Enter value to delete:", step=1, value=50, key="delete")
        if st.button("🗑️ Delete", use_container_width=True, key="delete_btn"):
            st.session_state.bst.delete(delete_val)
            st.session_state.last_operation = f"DELETE {delete_val}"
            st.rerun()
        
        st.markdown("---")
        
        # Tree operations
        st.subheader("Tree Operations")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Find Min", use_container_width=True, key="min_btn"):
                min_val = st.session_state.bst.find_min()
                st.session_state.last_operation = "FIND_MIN"
                st.rerun()
        
        with col2:
            if st.button("📉 Find Max", use_container_width=True, key="max_btn"):
                max_val = st.session_state.bst.find_max()
                st.session_state.last_operation = "FIND_MAX"
                st.rerun()
        
        # Demo operations
        st.markdown("---")
        st.subheader("Demo Operations")
        demo_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
        
        if st.button("🎮 Auto Demo", use_container_width=True, key="demo_btn"):
            st.session_state.bst = BinarySearchTree()
            for val in demo_values:
                st.session_state.bst.insert(val)
            st.session_state.auto_demo_done = True
            st.session_state.last_operation = "DEMO"
            st.rerun()
        
        if st.button("🧹 Clear Tree", use_container_width=True, key="clear_btn"):
            st.session_state.bst = BinarySearchTree()
            st.session_state.auto_demo_done = False
            st.session_state.last_operation = "CLEAR"
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌳 Tree Visualization")
        
        # Text-based tree visualization
        tree_structure = st.session_state.bst.get_tree_structure()
        st.markdown("### Tree Structure:")
        st.markdown(f'<div class="tree-visualization">{tree_structure}</div>', unsafe_allow_html=True)
        
        # Alternative simple visualization
        st.markdown("### Simple View:")
        if st.session_state.bst.root:
            simple_view = f"Root: {st.session_state.bst.root.value}"
            if st.session_state.bst.root.left:
                simple_view += f" | Left: {st.session_state.bst.root.left.value}"
            if st.session_state.bst.root.right:
                simple_view += f" | Right: {st.session_state.bst.root.right.value}"
            st.code(simple_view)
        
        # Tree traversals
        st.header("🔄 Tree Traversals")
        if st.session_state.bst.root is not None:
            # Display all traversals at once
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.subheader("In-order")
                st.code(f"{st.session_state.bst.inorder_traversal()}")
            
            with col2:
                st.subheader("Pre-order")
                st.code(f"{st.session_state.bst.preorder_traversal()}")
            
            with col3:
                st.subheader("Post-order")
                st.code(f"{st.session_state.bst.postorder_traversal()}")
            
            with col4:
                st.subheader("Level-order")
                st.code(f"{st.session_state.bst.level_order_traversal()}")
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
        st.header("📝 Operations History")
        if st.session_state.bst.operations_history:
            # Show last 10 operations
            recent_ops = st.session_state.bst.operations_history[-10:]
            
            for i, op in enumerate(reversed(recent_ops)):
                with st.container():
                    st.markdown(f"""
                    <div class="history-item">
                        <strong>{op['operation']}</strong> 
                        {f"<strong>({op['value']})</strong>" if op['value'] is not None else ""}<br>
                        <small>Status: {op['result']}</small><br>
                        <small style="color: #666;">{op['details']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No operations yet. Start by inserting values!")
    
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
