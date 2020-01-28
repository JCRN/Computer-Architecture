"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # Instructions
        self.instructions = {
            0b10000010: 'LDI', # Load Immediate
            0b01000111: 'PRN', # Print
            0b00000001: 'HLT'  # Halt     
        }
        
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
        else:
            filename = sys.argv[1]
            
        try:
            address = 0
            
            with open(filename) as program:
                for instruction in program:                    
                    comment_split = line.split('#')  # Ignore comments                  
                    num = comment_split[0].strip()   # Strip out whitespace                 
                    if num == '':
                        continue                     # Ignore blank lines
                    instruction = int(num, 2)        # Cast to binary integer                    
                    self.ram[address] = instruction
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
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        
    def hlt(self): # Halt the CPU (and exit the emulator) 
        return False

    def ldi(self, register, value): # Set the value of a register to an integer
        self.ram_write(register, value)
        self.pc += 3
        
    def prn(self, register): # Print numeric value stored in the given register to console
        print(self.ram_read(register))
        self.pc += 2
        
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
        running = True
        while running:
            
            # Instruction register (ir)
            ir = self.ram[self.pc]  
            
            # Next 2 registers (in case the instruction requires them)          
            operand_a = self.ram[self.pc+1]
            operand_b = self.ram[self.pc+2]
            
            instruction = self.instructions[ir]
            
            if instruction == 'LDI':
                self.ldi(operand_a, operand_b)
            
            elif instruction == 'PRN':
                self.prn(operand_a)
                
            elif instruction == 'HLT':
                running = self.hlt()    
            
            else:
                print(f'Command not found.')
