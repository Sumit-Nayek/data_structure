import streamlit as st
from collections import deque

class BSTNode:
    """Node class for Binary Search Tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Added for AVL tree

class BinarySearchTree:
    """Binary Search Tree implementation with AVL balancing"""
    
    def __init__(self):
        self.root = None
        self.avl_mode = False
    
    def set_avl_mode(self, enabled):
        """Enable or disable AVL balancing"""
        self.avl_mode = enabled
    
    def get_height(self, node):
        """Get height of a node"""
        if not node:
            return 0
        return node.height
    
    def update_height(self, node):
        """Update height of a node"""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def get_balance(self, node):
        """Get balance factor of a node"""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def rotate_right(self, y):
        """Right rotation for AVL balancing"""
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        self.update_height(y)
        self.update_height(x)
        
        return x
    
    def rotate_left(self, x):
        """Left rotation for AVL balancing"""
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        self.update_height(x)
        self.update_height(y)
        
        return y
    
    def balance_node(self, node):
        """Balance a node using AVL rotations"""
        if not node:
            return node
        
        # Update height
        self.update_height(node)
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        
        # Right Right Case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        
        # Left Right Case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # Right Left Case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    def _insert(self, node, value):
        """Recursive insert helper"""
        if not node:
            return BSTNode(value)
        
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node  # Duplicate values not allowed
        
        # AVL balancing if enabled
        if self.avl_mode:
            return self.balance_node(node)
        
        return node
    
    def insert(self, value):
        """Insert a value into the BST/AVL tree"""
        self.root = self._insert(self.root, value)
        return True
    
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
    
    def _delete(self, node, value):
        """Recursive delete helper"""
        if not node:
            return node
        
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children
            min_node = self._find_min_node(node.right)
            node.value = min_node.value
            node.right = self._delete(node.right, min_node.value)
        
        # AVL balancing if enabled
        if self.avl_mode:
            return self.balance_node(node)
        
        return node
    
    def delete(self, value):
        """Delete a value from BST"""
        self.root = self._delete(self.root, value)
    
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
                'is_balanced': True,
                'balance_factor': 0,
                'tree_type': 'AVL' if self.avl_mode else 'BST'
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
            'is_balanced': self._is_balanced(),
            'balance_factor': self.get_balance(self.root),
            'tree_type': 'AVL' if self.avl_mode else 'BST'
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
        """Check if tree is balanced (AVL property)"""
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
    if 'avl_enabled' not in st.session_state:
        st.session_state.avl_enabled = False

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="BST & AVL Tree Simulator",
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
    .avl-info {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
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
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🌳 BST & AVL Tree Simulator</h1>', unsafe_allow_html=True)
    
    # AVL Mode Toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        avl_enabled = st.toggle("🔄 Enable AVL Tree Balancing", 
                               value=st.session_state.avl_enabled,
                               help="When enabled, tree automatically balances after each operation")
        
        if avl_enabled != st.session_state.avl_enabled:
            st.session_state.avl_enabled = avl_enabled
            st.session_state.bst.set_avl_mode(avl_enabled)
            st.rerun()
    
    # Sidebar for operations
    with st.sidebar:
        st.header("🎯 Tree Operations")
        
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
        
        demo_option = st.selectbox(
            "Choose demo sequence:",
            ["Balanced Sequence", "Sorted Sequence", "Random Sequence", "Unbalanced Sequence"]
        )
        
        if st.button("🎮 Run Demo", use_container_width=True):
            st.session_state.bst = BinarySearchTree()
            st.session_state.bst.set_avl_mode(st.session_state.avl_enabled)
            
            if demo_option == "Balanced Sequence":
                # Balanced insertion sequence
                values = [50, 25, 75, 15, 35, 65, 85]
                sequence_info = "Root-first, then level-by-level insertion"
            elif demo_option == "Sorted Sequence":
                # Worst-case for BST, best case for AVL to show balancing
                values = [10, 20, 30, 40, 50, 60, 70]
                sequence_info = "Sorted ascending order - worst case for BST"
            elif demo_option == "Random Sequence":
                # Random values
                values = [42, 23, 67, 15, 38, 55, 89]
                sequence_info = "Random insertion order"
            else:  # Unbalanced Sequence
                # Creates a skewed tree
                values = [10, 20, 30, 40, 50, 60, 70] if not st.session_state.avl_enabled else [50, 60, 70, 80, 90, 100]
                sequence_info = "Creates highly unbalanced tree (shows AVL power)"
            
            for val in values:
                st.session_state.bst.insert(val)
            
            st.session_state.auto_demo_done = True
            st.success(f"✅ Demo created with {demo_option}!")
            st.info(f"**Sequence:** {values}")
            st.info(f"**Pattern:** {sequence_info}")
        
        if st.button("🧹 Clear Tree", use_container_width=True):
            st.session_state.bst = BinarySearchTree()
            st.session_state.bst.set_avl_mode(st.session_state.avl_enabled)
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
            info_style = "avl-info" if st.session_state.avl_enabled else "tree-info"
            st.markdown(f"""
            <div class="{info_style}">
                <h3>🌲 {tree_info['tree_type']} Tree Stats</h3>
                <p><strong>Root:</strong> {tree_info['root']}</p>
                <p><strong>Height:</strong> {tree_info['height']}</p>
                <p><strong>Total Nodes:</strong> {tree_info['node_count']}</p>
                <p><strong>Min Value:</strong> {tree_info['min_value']}</p>
                <p><strong>Max Value:</strong> {tree_info['max_value']}</p>
                <p><strong>Balance Factor:</strong> {tree_info['balance_factor']}</p>
                <p><strong>Valid BST:</strong> {'✅' if tree_info['is_valid_bst'] else '❌'}</p>
                <p><strong>Balanced:</strong> {'✅' if tree_info['is_balanced'] else '❌'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("🌱 Tree is empty!")
    
    # Educational content
    st.markdown("---")
    st.header("🎓 BST & AVL Tree Learning Guide")
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.subheader("📚 BST Properties")
        st.markdown("""
        - **Binary Tree Structure**: Each node has at most 2 children
        - **Search Property**: Left child < Parent < Right child
        - **Efficient Operations**: O(log n) average case
        - **Worst Case**: O(n) for skewed trees
        - **No Auto-balancing**: Can become unbalanced
        """)
        
        st.subheader("🔄 AVL Tree Properties")
        st.markdown("""
        - **Self-balancing**: Automatically maintains balance
        - **Balance Factor**: |left_height - right_height| ≤ 1
        - **Rotations**: Uses single/double rotations
        - **Guaranteed Performance**: O(log n) worst case
        - **Overhead**: Extra height/balance calculations
        """)
    
    with exp_col2:
        st.subheader("🎯 AVL Rotations")
        st.markdown("""
        **Four Rotation Cases:**
        1. **Left-Left**: Right rotation
        2. **Right-Right**: Left rotation  
        3. **Left-Right**: Left then Right rotation
        4. **Right-Left**: Right then Left rotation
        
        **When Rotations Occur:**
        - After insertions that cause imbalance
        - After deletions that cause imbalance
        - Balance factor becomes ±2
        """)
        
        st.subheader("💡 Demo Sequences")
        st.markdown("""
        **Balanced Sequence**: Shows ideal BST structure
        **Sorted Sequence**: Worst-case for BST, shows AVL power
        **Random Sequence**: Typical real-world scenario
        **Unbalanced Sequence**: Demonstrates AVL balancing
        """)

if __name__ == "__main__":
    main()
