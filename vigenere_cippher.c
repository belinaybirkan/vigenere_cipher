#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define ASCII_START 32
#define ASCII_END 126
#define ASCII_RANGE (ASCII_END - ASCII_START + 1)

void vigenere_cipher (char *text, char *key, int encrypt)
{
	int text_length = strlen(text);
	int key_length = strlen (key);
	if (key_length == 0)
	{
		printf("Error: Key connot be empty.\n");
		return;
	}
	char result[text_length +1];

for (int i=0, j=0; i < text_length; i++)
{
	char current_char =text[i];
	if(current_char >= ASCII_START && current_char <= ASCII_END)
	{
		int shift = key[j % key_length]  - ASCII_START;
		if(!encrypt) shift = -shift;
		
		char new_char = ASCII_START + (current_char - ASCII_START + shift +ASCII_RANGE) % ASCII_RANGE;
		result[i]= new_char;
		j++;
		
	}
	else {
		result[i]= current_char;
	}
	}
	result[text_length]='\0';
	strcpy(text,result);
	
}

	int main(){
		char text[256], key [256],choice;
		printf("Enter text: ");
		if (!fgets(text, sizeof(text),stdin))
		{
			printf("error reading text.\n");
			return 1;
			
		}
		text[strcspn(text,"\n")]='\0';
		printf("enter key:");
		if(!fgets(key,sizeof(key),stdin))
		{
			printf("error reading key.\n");
			return 1;
		}
		key[strcspn(key,"\n")]= '\0';
		if(strlen(key)== 0)
		{
			printf("error: key cannot be empty.\n");
			return 1;
		}
		vigenere_cipher(text,key,1);
		printf("Encrypted text: %s\n",text);
		
		printf("Do you want to decrypt the text? (y/n):");
		scanf(" %c",&choice);
		
		if(choice == 'y' || choice == 'Y'){
			vigenere_cipher(text,key,0);
			printf("Decrypted text: %s\n",text);
		}
			else{
				printf("Exiting without decryption.\n");
			}
			return 0;	
		}
	

