// The classes are basically the same as the BinaryTree 
// file except the visitor classes and the accept method
// in the Tree class

class TreeVisitor{
    public static void main(String[] a){
	System.out.println(new TV().Start());
    }
}

class Tree{
    Tree left;
    Tree right;
    int key ;
    boolean has_left ;
    boolean has_right ;
    Tree my_null ;

    public boolean Init(int v_key){
	key = v_key ;
	has_left = false ;
	has_right = false ;
	return true ;
    }
}
