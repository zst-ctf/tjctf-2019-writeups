void entry(undefined8 uParm1,undefined8 uParm2,undefined8 uParm3) {
  undefined8 in_stack_00000000;
  undefined auStack8 [8];
  
  __libc_start_main(FUN_00100a34,in_stack_00000000,&stack0x00000008,FUN_00100b10,FUN_00100b80,uParm3
                    ,auStack8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}


undefined8 FUN_00100a34(void){ 
  // 0xa34
  uint local_14;
  code *local_10;
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  printf("Length: ");
  local_10 = FUN_001009a0;
  local_14 = 0;
  __isoc99_scanf(&DAT_00100ba5,&local_14); // "%u"
  getchar();
  if ((local_14 & 7) == 0) {
    printf("Input: ");
    FUN_001009b3((ulong)local_14);
  }
  else {
    puts("Bad length");
  }
  return 0; // 0xb0f
}

// undefined8 DAT_00301050
// undefined4 DAT_00301058
// undefined4 DAT_0030105c
undefined8 FUN_001009b3(int iParm1){
  ssize_t sVar1;
  undefined local_18 [16];
  
  DAT_00301050 = local_18;
  while (DAT_00301058 < iParm1) {
    sVar1 = read(0,DAT_00301050,(long)(iParm1 - DAT_00301058));
    DAT_0030105c = (int)sVar1;
    DAT_00301058 = DAT_0030105c + DAT_00301058;
    DAT_00301050 = DAT_00301050 + (long)DAT_0030105c;
  }
  return 0;
}


// simplified
undefined8 FUN_001009b3(int iParm1){
  ssize_t sVar1;
  undefined local_18 [16];
  
  buffer = local_18;
  while (count < iParm1) {
    sVar1 = read(0,buffer,(long)(iParm1 - count)); // Returns the number of bytes that were read
    count += sVar1;
    buffer += sVar1;
  }
  return 0;
}


void FUN_001009a0(void){
  system("/bin/sh");
  return;
}




