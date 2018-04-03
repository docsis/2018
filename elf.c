//gcc -std=c11 elf.c -o elf
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <unistd.h>
#include <elf.h>


static FILE *infile;
static Elf64_Ehdr ehdr;
static Elf64_Shdr *shdr;
static Elf64_Sym *syms;
static int syms_num;
static Elf64_Phdr *phdr;
static int phdr_num;
static char *strtab;
static char *sectstr;	/* sh string table */

struct section {
	int id;
	char *data;
	int len;
};

static struct section sects[100];


void die(char *s)
{
	printf("%s\n", s);
	exit(1);
}

char *printsht(int type)
{
	if (type == SHT_PROGBITS)
		return "PROGBITS";
	else if (type == SHT_SYMTAB)
		return "SYMTAB";
	else if (type == SHT_STRTAB)
		return "STRTAB";
	else if (type == SHT_RELA)
		return "RELA";
	else if (type == SHT_NULL)
		return "NULL";
	else if (type == SHT_NOTE)
		return "NOTE";
	else if (type == SHT_INIT_ARRAY)
		return "INIT_ARRAY";
	else if (type == SHT_DYNAMIC)
		return "DYNAMIC";
	else if (type == SHT_NOBITS)
		return "NOBITS";

	return "";
}

void *rd_alloc(int off, int siz, char *s)
{
	void *buf;

	fprintf(stderr, "%06x %04x %s\n", off, siz+off, s);

	fseek(infile, off, SEEK_SET);
	buf = malloc(siz);
	if (!buf)
		die("no mem");
	
	if (fread(buf, siz, 1, infile) != 1)
		die("read error");

	return buf; 
}

void prehdr(void)
{
	printf("\n----- elf header ------\n");
	printf("e_shnum %d\n", ehdr.e_shnum);
	printf("e_phoff %d\n", ehdr.e_phoff);
	printf("e_shoff %d\n", ehdr.e_shoff);

}

void prshr(void)
{
	printf("\n----- section header ------\n");
	printf("idx:    type       name\n");
	for (int i=0; i < ehdr.e_shnum; i++) {
		printf("%02d:  %08x %10s %s\n", i, shdr[i].sh_type,
			printsht(shdr[i].sh_type), sectstr+shdr[i].sh_name);
	}

}

void prsyms(void)
{
	printf("\n----- symbol table ------\n");
	for (int i=0; i<syms_num; i++) {
		printf("%02d: %08llx %s\n", i, syms[i].st_value, &strtab[syms[i].st_name]);
	}
}

void prphdr(void)
{
	if (phdr) {
		printf("\n----- program header ------\n");
		for (int i=0; i<phdr_num; i++)
			printf("p_vaddr %08llx %llx\n", phdr[i].p_vaddr, phdr[i].p_paddr);
	}
}

void parse_file(void)
{

	fread(&ehdr, sizeof(ehdr), 1, infile); 

	shdr = rd_alloc(ehdr.e_shoff, sizeof(Elf64_Shdr) * ehdr.e_shnum, "shdr");

	if (ehdr.e_phoff) {
		phdr = rd_alloc(ehdr.e_phoff, sizeof(Elf64_Phdr)*ehdr.e_phnum, "phdr");
		phdr_num = ehdr.e_phnum;
	}

	for (int i=1; i < ehdr.e_shnum; i++) {
		if (shdr[i].sh_type == SHT_STRTAB) {
			if (i == ehdr.e_shstrndx) {
				sectstr = rd_alloc(shdr[i].sh_offset, shdr[i].sh_size, "sc_strtab_h");
				sects[i].data = sectstr;
			} else {
				strtab = rd_alloc(shdr[i].sh_offset, shdr[i].sh_size, "sc_strtab");
				sects[i].data = strtab;
			}
			sects[i].len = shdr[i].sh_size;
		} else if (shdr[i].sh_type == SHT_SYMTAB) {
			syms = rd_alloc(shdr[i].sh_offset, shdr[i].sh_size, "sc_symtab");
			syms_num = shdr[i].sh_size/sizeof(Elf64_Sym);
			sects[i].data = syms;
		} else {
			sects[i].data = rd_alloc(shdr[i].sh_offset, shdr[i].sh_size, "sc_");
		}

		sects[i].len = shdr[i].sh_size;
	}
}

int main(int argc, char *argv[])
{
	if (argc > 1) {
		infile = fopen(argv[1], "rb");
		if (!infile)
			die("file open error");
	} else {
		die("file name");
	}

	parse_file();

	prehdr();
	prphdr();
	prshr();
	prsyms();

	return 0;
}
