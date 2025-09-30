	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0	sdk_version 26, 0
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	wzr, [x29, #-4]
	stur	w0, [x29, #-8]
	str	x1, [sp, #16]
	ldr	x8, [sp, #16]
	ldr	x8, [x8, #8]
	str	x8, [sp, #8]
	ldr	x8, [sp, #8]
	ldrsb	w8, [x8]
	subs	w8, w8, #97
	b.ne	LBB0_2
	b	LBB0_1
LBB0_1:
	b	LBB0_3
LBB0_2:
	adrp	x0, l_.str@PAGE
	add	x0, x0, l_.str@PAGEOFF
	bl	_puts
	mov	w8, #-1                         ; =0xffffffff
	stur	w8, [x29, #-4]
	b	LBB0_15
LBB0_3:                                 ; =>This Inner Loop Header: Depth=1
	ldr	x8, [sp, #8]
	add	x8, x8, #1
	str	x8, [sp, #8]
	ldr	x8, [sp, #8]
	ldrsb	w8, [x8]
	subs	w8, w8, #46
	b.ne	LBB0_5
	b	LBB0_4
LBB0_4:                                 ;   in Loop: Header=BB0_3 Depth=1
	ldr	x8, [sp, #8]
	add	x8, x8, #1
	str	x8, [sp, #8]
	b	LBB0_8
LBB0_5:                                 ;   in Loop: Header=BB0_3 Depth=1
	ldr	x8, [sp, #8]
	ldrsb	w8, [x8]
	cbnz	w8, LBB0_7
	b	LBB0_6
LBB0_6:
	adrp	x0, l_.str@PAGE
	add	x0, x0, l_.str@PAGEOFF
	bl	_puts
	mov	w8, #-1                         ; =0xffffffff
	stur	w8, [x29, #-4]
	b	LBB0_15
LBB0_7:                                 ;   in Loop: Header=BB0_3 Depth=1
	b	LBB0_3
LBB0_8:                                 ;   in Loop: Header=BB0_3 Depth=1
	ldr	x8, [sp, #8]
	ldrsb	w8, [x8]
	subs	w8, w8, #99
	b.ne	LBB0_10
	b	LBB0_9
LBB0_9:                                 ;   in Loop: Header=BB0_3 Depth=1
	b	LBB0_11
LBB0_10:                                ;   in Loop: Header=BB0_3 Depth=1
	b	LBB0_3
LBB0_11:                                ;   in Loop: Header=BB0_3 Depth=1
	ldr	x8, [sp, #8]
	add	x8, x8, #1
	str	x8, [sp, #8]
	ldr	x8, [sp, #8]
	ldrsb	w8, [x8]
	cbnz	w8, LBB0_13
	b	LBB0_12
LBB0_12:
	b	LBB0_14
LBB0_13:                                ;   in Loop: Header=BB0_3 Depth=1
	b	LBB0_3
LBB0_14:
	adrp	x0, l_.str.1@PAGE
	add	x0, x0, l_.str.1@PAGEOFF
	bl	_puts
	stur	wzr, [x29, #-4]
	b	LBB0_15
LBB0_15:
	ldur	w0, [x29, #-4]
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"reject!"

l_.str.1:                               ; @.str.1
	.asciz	"accept!\n"

.subsections_via_symbols
