"""
Code for compressing and decompressing using Huffman compression.
"""

from nodes import HuffmanNode, ReadNode


# ====================
# Helper functions for manipulating bytes


def get_bit(byte, bit_num):
    """ Return bit number bit_num from right in byte.

    @param int byte: a given byte
    @param int bit_num: a specific bit number within the byte
    @rtype: int

    >>> get_bit(0b00000101, 2)
    1
    >>> get_bit(0b00000101, 1)
    0
    """
    return (byte & (1 << bit_num)) >> bit_num


def byte_to_bits(byte):
    """ Return the representation of a byte as a string of bits.

    @param int byte: a given byte
    @rtype: str

    >>> byte_to_bits(14)
    '00001110'
    """
    return "".join([str(get_bit(byte, bit_num))
                    for bit_num in range(7, -1, -1)])


def bits_to_byte(bits):
    """ Return int represented by bits, padded on right.

    @param str bits: a string representation of some bits
    @rtype: int

    >>> bits_to_byte("00000101")
    5
    >>> bits_to_byte("101") == 0b10100000
    True
    """
    return sum([int(bits[pos]) << (7 - pos)
                for pos in range(len(bits))])


# ====================
# Functions for compression


def make_freq_dict(text): #Done 
    """ Return a dictionary that maps each byte in text to its frequency.

    @param bytes text: a bytes object
    @rtype: dict(int,int)

    >>> d = make_freq_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    d = {}
    for i in range(len(text)):
        if text[i] not in d:
            d[text[i]] = 1
        else:
            d[text[i]] += 1
    return d


def huffman_tree(freq_dict): #done
    """ Return the root HuffmanNode of a Huffman tree corresponding
    to frequency dictionary freq_dict.

    @param dict(int,int) freq_dict: a frequency dictionary
    @rtype: HuffmanNode

    >>> freq = {2: 6, 3: 4}
    >>> t = huffman_tree(freq)
    >>> result1 = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> result2 = HuffmanNode(None, HuffmanNode(2), HuffmanNode(3))
    >>> t == result1 or t == result2
    True
    """
    #creates a list of lists where the first item in the tuple is the frequency of the symbol and the second item is the HuffmanNode of the symbol
    node_list = []
    for item in freq_dict:
        node_list.append([freq_dict[item], HuffmanNode(item)])
    
    #create huffman tree
    #if there is only one symbol in freq_dict, returns the HuffmanNode of that symbol with 2 child nodes as the bit for the symbol can be either 0 or 1
    if len(node_list) == 1:
        return HuffmanNode(None, node_list[0][1], node_list[0][1])
    #first sorts freq_dict in ascending order
    #takes 2 symbols in the list with the lowest frequency(which are at the front of the tree) and creates a tree using them
    #and then appends the tree to the list as a list combined with the total frequency of the symbol in the tree
    #repeats until length of list is 1
    #with reference to 'Huffman Coding' section in https://www2.cs.duke.edu/csed/poop/huff/info/  
    while len(node_list) > 1:
        node_list = sorted(node_list, key=lambda x: x[0])
        n_left = node_list.pop(0)
        n_right = node_list.pop(0)
        node_list.append([n_left[0] + n_right[0], HuffmanNode(None, n_left[1], n_right[1])])
    return node_list[0][1]

def get_codes(tree):
    """ Return a dict mapping symbols from Huffman tree to codes.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: dict(int,str)

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    symbol_bits_dict = {}
    
    
    def get_code_preorder(BTNode, symbol_path):
      #if node on left exists, recurse function and add "0" to symbol_bit
      #if node on right exists, recurse function and add "1" to symbol_bit
        if BTNode.left:
            get_code_preorder(BTNode.left, symbol_path + "0")
        if BTNode.right:
            get_code_preorder(BTNode.right, symbol_path + "1")
        if BTNode.is_leaf and BTNode.symbol != None:
            symbol_bits_dict[BTNode.symbol] = symbol_path

    get_code_preorder(tree, "")    
    return symbol_bits_dict
        

def number_nodes(tree):
    """ Number internal nodes in tree according to postorder traversal;
    start numbering at 0.

    @param HuffmanNode tree:  a Huffman tree rooted at node 'tree'
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    L = postorder(tree)
    counter = 0
    for item in L:
      item.number = counter
      counter += 1
    
def postorder(tree):
  if not tree:
    return []
  elif tree.is_leaf():
    return []
  else:
    L = postorder(tree.left) + postorder(tree.right)
    L.append(tree)
    return L
  


def avg_length(tree, freq_dict):
    """ Return the number of bits per symbol required to compress text
    made of the symbols and frequencies in freq_dict, using the Huffman tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: float

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(9)
    >>> tree = HuffmanNode(None, left, right)
    >>> avg_length(tree, freq)
    1.9
    """
    code_dict = get_codes(tree)
    total_bit_length = 0
    total_bits = 0
    for code_key in code_dict:
      #gets length of each bit assigned to the symbol and multiplies it by the number of times the symbol occurs
      total_bit_length += len(code_dict[code_key]) * freq_dict[code_key]
      #
      total_bits += freq_dict[code_key]
    return total_bit_length / total_bits
    


def generate_compressed(text, codes):
    """ Return compressed form of text, using mapping in codes for each symbol.

    @param bytes text: a bytes object
    @param dict(int,str) codes: mapping from symbols to codes
    @rtype: bytes

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    byte_list = []
    txt_to_bit = ""
    for symb in text:
      txt_to_bit += codes[symb]
      if len(txt_to_bit) > 8:
        byte_list.append(bits_to_byte(txt_to_bit[:8]))
        txt_to_bit = txt_to_bit[8:]
    if txt_to_bit != "":
      byte_list.append(bits_to_byte(txt_to_bit))
    return bytes(byte_list)
        
      


def tree_to_bytes(tree):
    """ Return a bytes representation of the Huffman tree rooted at tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes

    The representation should be based on the postorder traversal of tree
    internal nodes, starting from 0.
    Precondition: tree has its nodes numbered.

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(5)
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    """
    if not tree or not (tree.left and tree.right):  #if tree is a leaf, return []
      return bytes([])
    elif tree.left.symbol and tree.right.symbol:
      L = []
      if tree.left and tree.left.is_leaf(): #if left child is a leaf, set 1st byte to 0 and 2nd byte to child's symbol
        L.append(0)
        L.append(tree.left.symbol)
      else:																	#else, set 1st byte to 1 and 2nd byte to node's number
        L.append(1)
        L.append(tree.number)
      if tree.right and tree.right.is_leaf(): 
        L.append(0)
        L.append(tree.right.symbol)
      else:
        L.append(1)
        L.append(tree.number)
      return bytes(L)
    return bytes(tree_to_bytes(tree.left) + tree_to_bytes(tree.right) + node_to_bytes(tree))

def node_to_bytes(tree):
  L = []
  if tree.left:
    if tree.left.is_leaf():  #if left child is a leaf, set 1st byte to 0 and 2nd byte to child's symbol
      L.append(0)
      L.append(tree.left.symbol)
    else:										 #else, set 1st byte to 1 and 2nd byte to the child's number
      L.append(1)
      L.append(tree.left.number)
  if tree.right:						
    if tree.right.is_leaf():
      L.append(0)
      L.append(tree.right.symbol)
    else:
      L.append(1)
      L.append(tree.right.number)
  return bytes(L)


def num_nodes_to_bytes(tree):
    """ Return number of nodes required to represent tree (the root of a
    numbered Huffman tree).

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes
    """
    return bytes([tree.number + 1])


def size_to_bytes(size):
    """ Return the size as a bytes object.

    @param int size: a 32-bit integer to convert to bytes
    @rtype: bytes

    >>> list(size_to_bytes(300))
    [44, 1, 0, 0]
    """
    # little-endian representation of 32-bit (4-byte)
    # int size
    return size.to_bytes(4, "little")


def compress(in_file, out_file):
    """ Compress contents of in_file and store results in out_file.

    @param str in_file: input file to compress
    @param str out_file: output file to store compressed result
    @rtype: NoneType
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = make_freq_dict(text)
    tree = huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (num_nodes_to_bytes(tree) + tree_to_bytes(tree) +
              size_to_bytes(len(text)))
    result += generate_compressed(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression
HuffmanNode(None, HuffmanNode(101, None, None), HuffmanNode(None, HuffmanNode(115, None, None), HuffmanNode(110, None, None)))

def generate_tree_general(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes nothing about the order of the nodes in node_lst.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in 'node_lst'
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), \
HuffmanNode(12, None, None)), \
HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
    """
    if root_index not in range(len(node_lst)):
      return None 
    else:
      a = node_lst[root_index]
      g = HuffmanNode(None, None, None)
      if a.l_type == 1:
        g.left = generate_tree_general(node_lst, a.l_data)        
      if a.r_type == 1:
          g.right = generate_tree_general(node_lst, a.r_data)
      if a.l_type == 0:
          g.left = HuffmanNode(a.l_data, None, None)
      if a.r_type == 0:
          g.right = HuffmanNode(a.r_data, None, None)
    return g


def generate_tree_postorder(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes that node_lst represents a tree in postorder.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in 'node_lst'
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(5, None, None), \
HuffmanNode(7, None, None)), \
HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)))
    """
    if root_index not in range(len(node_lst)):
      return None 
    else:
      a = node_lst[root_index]
      g = HuffmanNode(None, None, None)

      if a.r_type == 0 and a.l_type ==0:
          g.left = HuffmanNode( a.l_data, None, None)
          g.right = HuffmanNode( a.r_data, None, None)
      if a.r_type == 0 and a.l_type ==1:
          g.right = HuffmanNode( a.r_data, None, None)
          g.left = generate_tree_postorder(node_lst, root_index-1)
      if a.r_type ==1 and a.l_type == 0:
          a.left = HuffmanNode( a.l_data, None, None)
          g.right = generate_tree_postorder(node_lst, root_index-1)
      if a.r_type ==1 and a.l_type == 1:
          g.left = generate_tree_postorder(node_lst, root_index-2)
          g.right = generate_tree_postorder(node_lst, root_index-1)
    return g    


def generate_uncompressed(tree, text, size):
    """ Use Huffman tree to decompress size bytes from text.

    @param HuffmanNode tree: a HuffmanNode tree rooted at 'tree'
    @param bytes text: text to decompress
    @param int size: number of bytes to decompress from text.
    @rtype: bytes
    """
    dict_StC = get_codes(tree) #dictionary maps symbols to codes
    dict_CtS = {} #dictionary maps codes to symbols
    for symb in dict_StC:
        dict_CtS[dict_StC[symb]] = symb
        
    text_bits = ""
    for byt in text:
        text_bits += byte_to_bits(byt)

    uncompress_lst = []
    current_bit = ""
    for bit in text_bits:
        current_bit += bit
        if current_bit in dict_CtS and len(uncompress_lst) < size:
            uncompress_lst.append(dict_CtS[current_bit])
            current_bit = ""
##        if len(uncompress_lst) == size:
##            break
        
## DOES NOT WORK \/
##    text_bits = ""
##    for byt in text:
##        text_bits += [byte_to_bits(byt)]
##
##    uncompress_lst = []
##    current_bit = ""
##    i = 0
##    while len(uncompress_lst) != size:
##        current_bit += bit[i]
##        i += 0
##        if current_bit in dict_CtS:
##            uncompress_lst.append(dict_CtS[current_bit])
##            current_bit = ""
    return bytes(uncompress_lst)
            
        
def bytes_to_nodes(buf):
    """ Return a list of ReadNodes corresponding to the bytes in buf.

    @param bytes buf: a bytes object
    @rtype: list[ReadNode]

    >>> bytes_to_nodes(bytes([0, 1, 0, 2]))
    [ReadNode(0, 1, 0, 2)]
    """
    lst = []
    for i in range(0, len(buf), 4):
        l_type = buf[i]
        l_data = buf[i+1]
        r_type = buf[i+2]
        r_data = buf[i+3]
        lst.append(ReadNode(l_type, l_data, r_type, r_data))
    return lst


def bytes_to_size(buf):
    """ Return the size corresponding to the
    given 4-byte little-endian representation.

    @param bytes buf: a bytes object
    @rtype: int

    >>> bytes_to_size(bytes([44, 1, 0, 0]))
    300
    """
    return int.from_bytes(buf, "little")


def uncompress(in_file, out_file):
    """ Uncompress contents of in_file and store results in out_file.

    @param str in_file: input file to uncompress
    @param str out_file: output file that will hold the uncompressed results
    @rtype: NoneType
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_size(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(generate_uncompressed(tree, text, size))


# ====================
# Other functions

def improve_tree(tree, freq_dict):
    """ Improve the tree as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to freq_dict.

    @param HuffmanNode tree: Huffman tree rooted at 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(99), HuffmanNode(100))
    >>> right = HuffmanNode(None, HuffmanNode(101), \
    HuffmanNode(None, HuffmanNode(97), HuffmanNode(98)))
    >>> tree = HuffmanNode(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    actual = huffman_tree(freq_dict)
    
    node_list = postorder_leafnodes(tree)
    actual_list = postorder_leafnodes(actual)
    
    for i in range(len(node_list)):
        if node_list[i] and actual_list[i] and node_list[i].symbol != actual_list[i].symbol:
            for node in node_list:
                if node.symbol == actual_list[i].symbol:
                    node_list[i].symbol, node.symbol = node.symbol, node_list[i].symbol
                    
def postorder_leafnodes(tree):
    if not tree:
        return []
    elif tree.is_leaf():
        return [tree]
    return postorder_leafnodes(tree.left) + postorder_leafnodes(tree.right)


if __name__ == "__main__":
    # TODO: Uncomment these when you have implemented all the functions
    import doctest
    doctest.testmod()

    import time

    mode = input("Press c to compress or u to uncompress: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress(fname, fname + ".huf")
        print("compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "u":
        fname = input("File to uncompress: ")
        start = time.time()
        uncompress(fname, fname + ".orig")
        print("uncompressed {} in {} seconds."
              .format(fname, time.time() - start))
