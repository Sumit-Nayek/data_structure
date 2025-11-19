import streamlit as st
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
    
    def insert(self, value):
        """Insert a value into the BST"""
        new_node = BSTNode(value)
        
        if self.root is None:
            self.root = new_node
            return True
        
        temp = self.root
        while True:
            if new_node.value == temp.value:
                return False
            
            if new_node.value < temp.value:
                if temp.left is None:
                    temp.left = new_node
                    return True
                temp = temp.left
            else:
                if temp.right is None:
                    temp.right = new_node
                    return True
                temp = temp.right
    
    def contains(self, value):
        """Check if value exists in BST"""
        if self.root is None:
            return False
        
        temp = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        
        return False
    
    def find_min(self):
        """Find minimum value in BST"""
        if self.root is None:
            return None
        
        current = self.root
        while current.left is not None:
            current = current.left
        
        return current.value
    
    def find_max(self):
        """Find maximum value in BST"""
        if self.root is None:
            return None
        
        current = self.root
        while current.right is not None:
            current = current.right
        
        return current.value
    
    def delete(self, value):
        """Delete a value from BST"""
        self.root = self._delete_node(self.root, value)
    
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
    .tree-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 0.5rem 0;
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
        if st.button("🚀 Insert", use_container_width=True):
            if st.session_state.bst.insert(insert_val):
                st.success(f"✅ Value {insert_val} inserted successfully!")
            else:
                st.error(f"❌ Value {insert_val} already exists!")
        
        # Search operation
        st.subheader("Search Node")
        search_val = st.number_input("Enter value to search:", step=1, value=50, key="search")
        if st.button("🔍 Search", use_container_width=True):
            found = st.session_state.bst.contains(search_val)
            if found:
                st.success(f"✅ Value {search_val} found!")
            else:
                st.error(f"❌ Value {search_val} not found!")
        
        # Delete operation
        st.subheader("Delete Node")
        delete_val = st.number_input("Enter value to delete:", step=1, value=50, key="delete")
        if st.button("🗑️ Delete", use_container_width=True):
            st.session_state.bst.delete(delete_val)
            st.success(f"✅ Value {delete_val} deleted!")
        
        st.markdown("---")
        
        # Tree operations
        st.subheader("Tree Operations")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Find Min", use_container_width=True):
                min_val = st.session_state.bst.find_min()
                if min_val is not None:
                    st.info(f"**Minimum Value:** {min_val}")
                else:
                    st.warning("Tree is empty!")
        
        with col2:
            if st.button("📉 Find Max", use_container_width=True):
                max_val = st.session_state.bst.find_max()
                if max_val is not None:
                    st.info(f"**Maximum Value:** {max_val}")
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
            st.success("✅ Demo tree created with values: " + ", ".join(map(str, demo_values)))
        
        if st.button("🧹 Clear Tree", use_container_width=True):
            st.session_state.bst = BinarySearchTree()
            st.session_state.auto_demo_done = False
            st.success("✅ Tree cleared successfully!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔄 Tree Traversals")
        
        if st.session_state.bst.root is not None:
            # Display current tree values
            current_values = st.session_state.bst.inorder_traversal()
            st.info(f"**Current Tree Values (in-order):** {current_values}")
            
            # Traversal buttons
            trav_col1, trav_col2 = st.columns(2)
            
            with trav_col1:
                if st.button("In-order Traversal", key="inorder", use_container_width=True):
                    result = st.session_state.bst.inorder_traversal()
                    st.markdown(f'<div class="success-box"><strong>In-order (Sorted):</strong> {result}</div>', unsafe_allow_html=True)
                
                if st.button("Pre-order Traversal", key="preorder", use_container_width=True):
                    result = st.session_state.bst.preorder_traversal()
                    st.markdown(f'<div class="success-box"><strong>Pre-order:</strong> {result}</div>', unsafe_allow_html=True)
            
            with trav_col2:
                if st.button("Post-order Traversal", key="postorder", use_container_width=True):
                    result = st.session_state.bst.postorder_traversal()
                    st.markdown(f'<div class="success-box"><strong>Post-order:</strong> {result}</div>', unsafe_allow_html=True)
                
                if st.button("Level-order Traversal", key="levelorder", use_container_width=True):
                    result = st.session_state.bst.level_order_traversal()
                    st.markdown(f'<div class="success-box"><strong>Level-order:</strong> {result}</div>', unsafe_allow_html=True)
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
                <p><strong>Total Nodes:</strong> {tree_info['node_count']}</p>
                <p><strong>Min Value:</strong> {tree_info['min_value']}</p>
                <p><strong>Max Value:</strong> {tree_info['max_value']}</p>
                <p><strong>Valid BST:</strong> {'✅' if tree_info['is_valid_bst'] else '❌'}</p>
                <p><strong>Balanced:</strong> {'✅' if tree_info['is_balanced'] else '❌'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("🌱 Tree is empty!")
    
    # Educational content
    st.markdown("---")
    st.header("🎓 BST Learning Guide")
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.subheader("📚 BST Properties")
        st.markdown("""
        - **Binary Tree Structure**: Each node has at most 2 children
        - **Search Property**: Left child < Parent < Right child
        - **Efficient Operations**: O(log n) average case complexity
        - **Sorted Order**: In-order traversal gives sorted values
        - **Dynamic Structure**: Easy to insert and delete nodes
        """)
        
        st.subheader("🎯 Operations Complexity")
        st.markdown("""
        - **Search**: O(h) - depends on tree height
        - **Insert**: O(h) - find position and insert  
        - **Delete**: O(h) - find and reorganize
        - **Traversal**: O(n) - visit all nodes
        - **Min/Max**: O(h) - follow left/right pointers
        """)
    
    with exp_col2:
        st.subheader("🔄 Traversal Types")
        st.markdown("""
        - **In-order**: Left → Root → Right (Gives sorted order)
        - **Pre-order**: Root → Left → Right (Useful for copying trees)
        - **Post-order**: Left → Right → Root (Useful for deletion)
        - **Level-order**: Level by level (Breadth-first search)
        """)
        
        st.subheader("💡 Pro Tips")
        st.markdown("""
        - Keep tree balanced for optimal O(log n) performance
        - Use in-order traversal to get sorted values
        - BSTs are excellent for dynamic data sets
        - Monitor tree height for performance optimization
        - Perfect for range queries and ordered operations
        """)

if __name__ == "__main__":
    main()
