public void crackleAndPop(){
	for(int i = 1 ; i<= 100 ; i++){
		if((i % 5 == 0 )&& (i % 3 == 0)){
			System.out.println("CracklePop");
		} else if(i % 3 == 0){
			System.out.println("Crackle");
		} else if(i % 5 == 0){
			System.out.println("Pop");
		}
	}
}