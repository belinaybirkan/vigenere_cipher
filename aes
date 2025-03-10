#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>

#define BLOCK_SIZE 16

void handleErrors() {
    fprintf(stderr, "Error occurred!\n");
    exit(1);
}

void encrypt_decrypt(const unsigned char *input, int input_len, unsigned char *key, unsigned char *iv, unsigned char *output, int encrypt, const char *mode) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    const EVP_CIPHER *cipher;
    int len, output_len = 0;

    if (strcmp(mode, "ECB") == 0)
        cipher = EVP_aes_128_ecb();
    else if (strcmp(mode, "CBC") == 0)
        cipher = EVP_aes_128_cbc();
    else if (strcmp(mode, "CFB") == 0)
        cipher = EVP_aes_128_cfb();
    else {
        fprintf(stderr, "Invalid mode!\n");
        exit(1);
    }

    EVP_CipherInit_ex(ctx, cipher, NULL, key, iv, encrypt);
    EVP_CipherUpdate(ctx, output, &len, input, input_len);
    output_len += len;
    EVP_CipherFinal_ex(ctx, output + output_len, &len);
    output_len += len;

    EVP_CIPHER_CTX_free(ctx);
}

void save_to_file(const char *filename, unsigned char *data, int len) {
    FILE *file = fopen(filename, "wb");
    fwrite(data, 1, len, file);
    fclose(file);
}

int read_from_file(const char *filename, unsigned char *buffer) {
    FILE *file = fopen(filename, "rb");
    if (!file) return -1;
    int len = fread(buffer, 1, 1024, file);
    fclose(file);
    return len;
}

int main() {
    unsigned char key[16], iv[16], input[1024], output[1024];
    char mode[4], choice;

    RAND_bytes(key, sizeof(key));
    RAND_bytes(iv, sizeof(iv));

    printf("Enter mode (ECB/CBC/CFB): ");
    scanf("%s", mode);

    printf("Encrypt (E) or Decrypt (D)? ");
    scanf(" %c", &choice);

    if (choice == 'E') {
        printf("Enter plaintext: ");
        scanf("%s", input);
        encrypt_decrypt(input, strlen((char *)input), key, iv, output, 1, mode);
        save_to_file("ciphertext.txt", output, strlen((char *)input));
        printf("Encrypted data saved to file.\n");
    } else if (choice == 'D') {
        int len = read_from_file("ciphertext.txt", input);
        if (len == -1) {
            fprintf(stderr, "Error reading file!\n");
            return 1;
        }
        encrypt_decrypt(input, len, key, iv, output, 0, mode);
        output[len] = '\0';
        printf("Decrypted text: %s\n", output);
    } else {
        printf("Invalid choice!\n");
    }
    return 0;
}
