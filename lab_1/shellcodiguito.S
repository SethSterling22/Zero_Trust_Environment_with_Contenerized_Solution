#include <sys/syscall.h>

#define STRING  "test.txt"
#define STRLEN  8

.globl main
        .type   main, @function

 main:
        jmp     calladdr

 popladdr:
        popq    %rcx
        xorq    %rax,%rax               /* get a 64-bit zero value */
        movb    %al, 8(%rcx)      /* null-terminate our string */
       
        movb    $SYS_unlink,%al         /* set up the syscall number - cambio de execv a unlink */
	movq    %rcx,%rdi               /* syscall arg 1: string pathname */
        syscall                         /* invoke syscall */


	xorq	%rax, %rax
        movb    $SYS_exit, %al            /* set up the syscall number */
                       /* syscall arg 1: 0 */
        syscall                         /* invoke syscall */

 calladdr:
        call    popladdr
        .ascii  STRING
