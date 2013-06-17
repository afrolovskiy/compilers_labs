class Factorial{
    public static void main(String[] a){
	System.out.println(new Fac().ComputeFac(10));
    }
}


class Fac {
    int f1;
    boolean f2;
    int[] f3;

    public int ComputeFac(int num, int test){
	int num_aux ;
  
	if (num < 1)
	    num_aux = 1 ;
	else 
	    num_aux = num * (this.ComputeFac(num-1)) ;
    
	return num_aux ;
    }

}
