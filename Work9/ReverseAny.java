package unit_two;

import java.util.Scanner;

public class ReverseAny {

	public static void main(String[] args) {
		
		Scanner input = new Scanner(System.in);
		int num = input.nextInt();
		int reversed = 0;
		
		while(num != 0) {
			
			reversed = reversed * 10 + num % 10;
			num /= 10;
		}
		
		System.out.println(reversed);
		input.close();
	}

}
