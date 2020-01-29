"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # branchtable of instructions
        self.branchtable = {
            # ALU 
            160: 'ADD',   
            162: 'MUL',        
            # Commands
            1: self.hlt, 
            130: self.ldi,  
            71: self.prn   
        }
        
        self.halt = False
        
        # Program Counter (pc)
        self.pc = 0
         
        # Random Access Memory, 256 bytes (ram)
        self.ram = [0] * 256
        
        # Registers, 8 bytes (reg)
        self.reg = [0] * 8
    
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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.ram[reg_a] *= self.ram[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        
    def hlt(self): # Halt the CPU (and exit the emulator) 
        self.halt = True

    def ldi(self, register, value): # Set the value of a register to an integer
        self.ram_write(register, value)
        
    def prn(self, register): # Print numeric value stored in the given register to console
        print(self.ram_read(register))
        
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
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
            ir = self.ram[self.pc] 
                        
            # instruction bits            
            alu = ir & 0b00100000 # = 32 if ALU instruction
            instruction = self.branchtable[ir] 
            ops = ir >> 6
            
            operand_a = self.ram[self.pc+1] if (ops > 0) else None
            operand_b = self.ram[self.pc+2] if (ops > 1) else None
            
            if alu == 32:
                self.alu(instruction, operand_a, operand_b)
            elif ops == 1:
                instruction(operand_a)
            elif ops == 2:
                instruction(operand_a, operand_b)
            else:
                instruction()
                
            self.pc += (ops+1)
            
            

