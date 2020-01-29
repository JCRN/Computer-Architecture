"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # branchtable of instructions
        self.branchtable = {
            # ALU 
            101: 'INC',
            102: 'DEC',
            105: 'NOT',
            160: 'ADD',
            161: 'SUB',   
            162: 'MUL',
            163: 'DIV',
            164: 'MOD', 
            168: 'AND', 
            170: 'OR', 
            171: 'XOR', 
            172: 'SHL',  
            173: 'SHR',  
            # Commands
            1: self.hlt,
            69: self.push, 
            70: self.pop, 
            71: self.prn,  
            130: self.ldi, 
        }
        
        # Random Access Memory, 256 bytes (ram)
        self.ram = [0] * 256
        
        # Registers, 8 bytes (reg)
        self.reg = [0] * 8
        
        ### Internal Registers ###
        # Interrupt Mask (im)
        self.IM = 0
        
        # Interrupt Status (is)
        self.IS = 0
        
        # Program Counter (pc)
        self.PC = 0    
        
        # Stack Pointer
        self.SP = self.ram[0xF4]     
        
        # Reserved Registers
        self.reg[5] = self.IM # interrupt mask
        self.reg[6] = self.IS # interrupt status
        self.reg[7] = self.SP # stack pointer
    
        self.halt = False
        
    def load(self):
        """Load a program into memory."""
        
        if len(sys.argv) != 2:
            print('Usage: file.py filename', file=sys.stderr)
            sys.exit(2)
            
        try:
            address = 0
            
            with open(sys.argv[1]) as file:
                for line in file:                    
                    comment_split = line.split('#')  # Ignore comments                  
                    instruction = comment_split[0].strip()   # Strip out whitespace                 
                    if instruction == '':                    # Ignore blank lines
                        continue                     
                    self.ram_write(address, int(instruction[:8], 2))
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)


    def alu(self, op=None, reg_a=None, reg_b=None):
        """ALU operations."""
        
        if op == 'INC':
            self.reg[reg_a] += 1
        elif op == 'DEC':
            self.reg[reg_a] -= 1
        elif op == 'NOT':
            self.reg[reg_a] ~= self.reg[reg_a]
        elif op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'SUB': 
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            try:
                self.reg[reg_a] /= self.reg[reg_b]
            except ZeroDivisionError:
                print('Error: dividing by zero!')
                self.halt()
        elif op == 'MOD':
            try:
                self.reg[reg_a] %= self.reg[reg_b]
            except ZeroDivisionError:
                print('Error: dividing by zero!')
                self.halt() 
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        
    def hlt(self): # Halt the CPU (and exit the emulator) 
        self.halt = True
        
    def push(self, register): # Push the value in given register on the stack
        self.SP -= 1
        self.ram_write(self.SP, register)
        
    def pop(self, register):
        self.reg[register] = self.ram_read(self.SP)
        self.SP += 1        

    def prn(self, register): # Print numeric value stored in the given register to console
        print(self.reg[register])
    
    def ldi(self, register, value): # Set the value of a register to an integer
        self.reg[register] = value        
        
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def ram_read(self, mar): # memory address register - contains the address that is being read or written to
        return self.ram[mar]
    
    def ram_write(self, mar, mdr): # memory data register - contains the data that was read or the data to write
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        while not self.halt:
            
            # self.trace()
            
            # Instruction register (ir)
            ir = self.ram[self.PC] 
                        
            # instruction bits            
            alu = ir & 32 # bitmask, 32 if ALU instruction
            instruction = self.branchtable[ir] 
            ops = ir >> 6
            
            operand_a = self.ram[self.PC+1] if (ops > 0) else None
            operand_b = self.ram[self.PC+2] if (ops > 1) else None
            
            if alu == 32:
                self.alu(instruction, operand_a, operand_b)
            elif ops == 1:
                instruction(operand_a)
            elif ops == 2:
                instruction(operand_a, operand_b)
            else:
                instruction()
                
            self.PC += (ops+1)
            
            

