#A2 Part B - Core Decoder 

#A2 Part B.1 - Read and Validate Input 
#Converts hex to binary
def hexToBinary(hex):
    binary = ""
    for char in hex:
        match char: 
            case '0': 
                binary += "0000"
            case '1': 
                binary += '0001'
            case '2': 
                binary += '0010'
            case '3': 
                binary += '0011'
            case '4': 
                binary += '0100'
            case '5': 
                binary += '0101'
            case '6': 
                binary += '0110'
            case '7': 
                binary += '0111'
            case '8': 
                binary += '1000'
            case '9': 
                binary += '1001'
            case 'A':
                binary += '1010'
            case 'B': 
                binary += '1011'
            case 'C': 
                binary += '1100'
            case 'D': 
                binary += '1101'
            case 'E': 
                binary += '1110'
            case 'F': 
                binary += '1111'

    return binary

#A2 Part B.2 - Extract Fields
def binaryToDecimal(binary): 
    decimal = 0
    for i, char in enumerate(reversed(binary)): 
        if char == "1": 
            decimal += 2**i
    return decimal

def extractFields(instruction): 
    #extract opcode
    instruction['opcode'] = instruction['binary'][25:]
    print(f'opcode: {instruction['opcode']}') 

    #A2 Part B.3 Identify Instruction Format
    identifyInstructionType(instruction)

    #extract rest of the fields based on instruction type
    match instruction['format']: 
        case 'R': 
            #extract rd 
            instruction['rd'] = f'x{binaryToDecimal(instruction['binary'][20:25])}'
            print(f'rd: {instruction['rd']}') 

            #extract funct3 
            instruction['funct3'] = instruction['binary'][17:20]
            print(f'funct3: {instruction['funct3']}') 

            #extract rs1
            instruction['rs1'] = f'x{binaryToDecimal(instruction['binary'][12:17])}'
            print(f'rs1: {instruction['rs1']}') 

            #extract rs2
            instruction['rs2'] = f'x{binaryToDecimal(instruction['binary'][7:12])}'
            print(f'rs2: {instruction['rs2']}') 

            #extract funct7 
            instruction['funct7'] = instruction['binary'][0:7]
            print(f'funct7: {instruction['funct7']}')

        case 'I': 
            #extract rd
            instruction['rd'] = f'x{binaryToDecimal(instruction['binary'][20:25])}'
            print(f'rd: {instruction['rd']}')

            #extract funct3
            instruction['funct3'] = instruction['binary'][17:20]
            print(f'funct3: {instruction['funct3']}')

            #extract rs1
            instruction['rs1'] = f'x{binaryToDecimal(instruction['binary'][12:17])}'
            print(f'rs1: {instruction['rs1']}')

            #extract funct7 
            instruction['funct7'] = instruction['binary'][0:7]

        case 'S' | 'B': 
            #extract funct3
            instruction['funct3'] = instruction['binary'][17:20]
            print(f'funct3: {instruction['funct3']}')

            #extract rs1
            instruction['rs1'] = f'x{binaryToDecimal(instruction['binary'][12:17])}'
            print(f'rs1: {instruction['rs1']}')

            #extract rs2
            instruction['rs2'] = f'x{binaryToDecimal(instruction['binary'][7:12])}'
            print(f'rs2: {instruction['rs2']}')

        case 'U' | 'J': 
            #extract rd
            instruction['rd'] = f'x{binaryToDecimal(instruction['binary'][20:25])}'
            print(f'rd: {instruction['rd']}')

#A2 Part B.3 - Identify Instruction Format
def identifyInstructionType(instruction):
    instruction['format'] = ''
    match instruction['opcode']: 
        case '0110011': 
            instruction['format'] = 'R'
        case '0000011' | '0010011' | '1100111' | '1110011': 
            instruction['format'] = 'I'
        case '0100011': 
            instruction['format'] = 'S'
        case '1100011': 
            instruction['format'] = 'B'
        case '0110111'| '0010111': 
            instruction['format'] = 'U'
        case '1101111': 
            instruction['format'] = 'J' 

#A2 Part B.4 - Decode Immeadiates 
#extract immeadiate value from instruction
def extractImmeadiate(binary, instructionType): 
    immeadiate = ''
    match instructionType: 
        case 'I': 
            immeadiate = binary[0:12] 
        case 'S': 
            immeadiate = binary[0:7] + binary[20:25] 
        case 'B': 
            immeadiate = binary[0] + binary[24] + binary[1:7] + binary[20:24] + '0'
        case 'U': 
            immeadiate = binary[0:20]
        case 'J': 
            immeadiate = binary[0] + binary[12:20] + binary[11] + binary[1:11] + '0'

    return immeadiate

#invert bits of binary string
def flipBits(binary): 
    invertedBinary = ''
    for char in binary: 
        if char == '0': 
            invertedBinary += '1'
        else: 
            invertedBinary += '0'

    return invertedBinary

#add one to a binary string to create two's complement binary string
def addOne(invertedBinary): 
    twoComplement = ''
    carry = 1
    
    for char in reversed(invertedBinary): 
        if char == '0' and carry == 1:
            twoComplement += '1'
            carry = 0
        elif char == '1' and carry == 1:
            twoComplement += '0'
            carry = 1
        else:
            twoComplement += char
    
    if carry == 1:
        twoComplement += '1'
    
    return twoComplement[::-1]

#sign extend binary string 
def signExtend(binary): 
    return '1' * (32 - len(binary)) + binary

#decode immeadiate value
def decodeImmeadiate(instruction): 
    #extract immeadiate value based on instruction type
    instruction['immeadiate'] = extractImmeadiate(instruction['binary'], instruction['format']) 
    
    #convert immeadiate to decimal value
    #immeadiate is negative
    if instruction['immeadiate'][0] == '1': 
        #sign extend the immeadiate value 
        instruction['immeadiate'] = signExtend(instruction['immeadiate']) 

        #flip immeadiate bits 
        instruction['immeadiate'] = flipBits(instruction['immeadiate']) 
        
        #add one to inverted immeadiate
        instruction['immeadiate'] = addOne(instruction['immeadiate']) 

        #convert two's complement immeadiate to decimal
        instruction['immeadiate'] = binaryToDecimal(instruction['immeadiate']) * -1

    #immeadiate is positive
    else: 
        instruction['immeadiate'] = binaryToDecimal(instruction['immeadiate'])
    
    #shift U type instructions by 12 bits
    if instruction['format'] == 'U': 
        instruction['immeadiate'] = instruction['immeadiate'] * 4096 

    #display immeadiate decimal value 
    print(f'Immeadiate: {instruction['immeadiate']}')

#A2 Part B.5 - Translate to Assembly
#decode R-type instructions
def translateRtype(instruction):
    #add
    if instruction['funct7'] == '0000000' and instruction['funct3'] == '000': 
        instruction['assembly'] = f'add {instruction['rd']},{instruction['rs1']}, {instruction['rs2']}'
    #sub
    elif instruction['funct7'] == '0100000' and instruction['funct3'] == '000': 
        instruction['assembly'] = f'sub {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}' 
    #xor
    elif instruction['funct7'] == '00000000' and instruction['funct3'] == '100': 
        instruction['assembly'] = f'xor {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #or
    elif instruction['funct7'] == '0000000' and instruction['funct3'] == '110': 
        instruction['assembly'] = f'or {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #and
    elif instruction['funct7'] == '00000000' and instruction['funct3'] == '111':
        instruction['assembly'] = f'and {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #sll
    elif instruction['funct7'] == '0000000' and instruction['funct3'] == '001':
        instruction['assembly'] = f'sll {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #srl
    elif instruction['funct7'] == '0000000' and instruction['funct3'] == '101':
        instruction['assembly'] = f'srl {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #sra
    elif instruction['funct7'] == '0100000' and instruction['funct3'] == '101':
        instruction['assembly'] = f'sra {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #slt
    elif instruction['funct7'] == '0000000' and instruction['funct3'] == '010':
        instruction['assembly'] = f'slt {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #sltu
    elif instruction['funct7'] == '0000000' and instruction['funct3'] == '011':
        instruction['assembly'] = f'sltu {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}'
    #Semester Project
    #mul 
    elif instruction['funct7'] == '0000001' and instruction['funct3'] == '000': 
        instruction['assembly'] = f'mul {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}' 
    #div 
    elif instruction['funct7'] == '0000001' and instruction['funct3'] == '100': 
        instruction['assembly'] = f'div {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}' 
    #mod 
    elif instruction['funct7'] == '0000001' and instruction['funct3'] == '110': 
        instruction['assembly'] = f'mod {instruction['rd']}, {instruction['rs1']}, {instruction['rs2']}' 

def translateItype(instruction): 
    #lw - must check opcode+funct3 before generic funct3 matches
    if instruction['opcode'] == '0000011' and instruction['funct3'] == '010':
        instruction['assembly'] = f'lw {instruction['rd']}, {instruction['immeadiate']}({instruction['rs1']})'
        return 'loads'

    #jalr - must check opcode+funct3 before generic funct3 matches
    elif instruction['opcode'] == '1100111' and instruction['funct3'] == '000': 
        instruction['assembly'] = f'jalr {instruction['rd']}, {instruction['immeadiate']}({instruction['rs1']})'
        return 'jump'

    #addi
    elif instruction['funct3'] == '000': 
        instruction['assembly'] = f'addi {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #xori
    elif instruction['funct3'] == '100': 
        instruction['assembly'] = f'xori {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}' 
        return ''

    #ori
    elif instruction['funct3'] == '110': 
        instruction['assembly'] = f'ori {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #andi
    elif instruction['funct3'] == '111': 
        instruction['assembly'] = f'andi {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #slli
    elif instruction['funct3'] == '001':
        instruction['assembly'] = f'slli {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #srli
    elif instruction['funct3'] == '101':
        instruction['assembly'] = f'srli {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #slti
    elif instruction['funct3'] == '010':
        instruction['assembly'] = f'slti {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

    #sltiu
    elif instruction['funct3'] == '011':
        instruction['assembly'] = f'sltiu {instruction['rd']}, {instruction['rs1']}, {instruction['immeadiate']}'
        return ''

#decode S type instructions 
def translateStype(instruction): 
    #sw
    if instruction['funct3'] == '010':
        instruction['assembly'] = f'sw {instruction['rs2']}, {instruction['immeadiate']}({instruction['rs1']})'

#decode B type instructions 
def translateBtype(instruction, pc): 
    target = pc + instruction['immeadiate']
    #beq
    if instruction['funct3'] == '000': 
        instruction['assembly'] = f'beq {instruction['rs1']}, {instruction['rs2']}, {target}'
    #bne
    elif instruction['funct3'] == '001': 
        instruction['assembly'] = f'bne {instruction['rs1']}, {instruction['rs2']}, {target}' 
    #blt
    elif instruction['funct3'] == '100': 
        instruction['assembly'] = f'blt {instruction['rs1']}, {instruction['rs2']}, {target}'
    #bge
    elif instruction['funct3'] == '101': 
        instruction['assembly'] = f'bge {instruction['rs1']}, {instruction['rs2']}, {target}'
    #bltu
    elif instruction['funct3'] == '110':
        instruction['assembly'] = f'bltu {instruction['rs1']}, {instruction['rs2']}, {target}'
    #bgeu
    elif instruction['funct3'] == '111':
        instruction['assembly'] = f'bgeu {instruction['rs1']}, {instruction['rs2']}, {target}'

#decode U type instruction: 
def translateUtype(instruction): 
    #lui 
    if instruction['opcode'] == '0110111': 
        instruction['assembly'] = f'lui {instruction['rd']},{instruction['immeadiate']}'
    #auipc 
    elif instruction['opcode'] == '0010111': 
        instruction['assembly'] = f'auipc {instruction['rd']}, {instruction['immeadiate']}'

#decode J type instruction: 
def translateJtype(instruction, pc): 
    #jal 
    if instruction['opcode'] == '1101111': 
        target = pc + instruction['immeadiate']
        instruction['assembly'] = f'jal {instruction['rd']}, {target}'

#A3 Part B - Core Simulator 
#A3 Part B.1 Input & PC Rules 
def loadInstructions(path):
    instructions = []
    pc = 0
    with open(path, 'r') as file:
        for lineNum, line in enumerate(file, start=1):
            #ignore empty lines
            if line.strip():
                #validate hex format to exactly 8 characters
                if len(line.strip()) == 8:
                    #build instruction dict using your existing binary pipeline
                    instruction = {
                        'hex':    line.strip(),
                        'binary': hexToBinary(line.strip().upper()),
                        'pc':     pc
                    }
                    pc += 4

                    print(f"Hex value: {instruction['hex']} --> Binary value: {instruction['binary']}")

                    #A2 Part B.2 - extract fields using your existing function
                    extractFields(instruction)

                    #print instruction format
                    print(f"Instruction type: {instruction['format']}")

                    #A2 Part B.4 - decode immediate using your existing function
                    if instruction['format'] != 'R':
                        decodeImmeadiate(instruction)

                    #A2 Part B.5 - translate to assembly using your existing functions
                    if instruction['format'] == 'R':
                        translateRtype(instruction)
                    elif instruction['format'] == 'I':
                        translateItype(instruction)
                    elif instruction['format'] == 'S':
                        translateStype(instruction)
                    elif instruction['format'] == 'B':
                        translateBtype(instruction, instruction['pc'])
                    elif instruction['format'] == 'U':
                        translateUtype(instruction)
                    elif instruction['format'] == 'J':
                        translateJtype(instruction, instruction['pc'])

                    #handle unknown instruction
                    if 'assembly' not in instruction:
                        instruction['assembly'] = '.word 0xXXXXXXXX'

                    print(f"Assembly: {instruction['assembly']}")

                    instructions.append(instruction)
                else:
                    print(f"Invalid hex format on line {lineNum}: {line.strip()}")
    return instructions

#A3 Part B.2 Architectural State (Registers & Memory) 
#initialize registers 
registers = [0] * 32 

#initialize memory 
memory = {} 

#read from register 
def readRegister(register_num): 
	return registers[register_num] & 0xFFFFFFFF

#write to register 
def writeRegister(rd, value): 
	if rd != 0: 
		registers[rd] = value & 0xFFFFFFFF

#A3 Part B.3 Decode --> Execute 
def compareSignedValues(value):
    value &= 0xFFFFFFFF
    return value if value < 0x80000000 else value - 0x100000000

def executeRtype(instruction, pc, stats):
    stats['R'] += 1
    stats['alu'] += 1

    rs1 = readRegister(int(instruction['rs1'][1:]))
    rs2 = readRegister(int(instruction['rs2'][1:]))
    rd  = int(instruction['rd'][1:])
    
    match (instruction['funct7'], instruction['funct3']):
        case ('0000000', '000'): result = rs1 + rs2
        case ('0100000', '000'): result = rs1 - rs2
        case ('0000000', '111'): result = rs1 & rs2
        case ('0000000', '110'): result = rs1 | rs2
        case ('0000000', '100'): result = rs1 ^ rs2
        case ('0000000', '001'): result = rs1 << (rs2 & 0x1F)
        case ('0000000', '101'): result = rs1 >> (rs2 & 0x1F)
        case ('0100000', '101'): result = compareSignedValues(rs1) >> (rs2 & 0x1F)
        case ('0000000', '010'): result = 1 if compareSignedValues(rs1) < compareSignedValues(rs2) else 0
        case ('0000000', '011'): result = 1 if rs1 < rs2 else 0
        #Semester Project 
        #mul 
        case ('0000001', '000'): result = compareSignedValues(rs1) * compareSignedValues(rs2)
        #div 
        case ('0000001', '100'): result = (
                -0x80000000 if (compareSignedValues(rs2) == 0 or
                                (compareSignedValues(rs1) == -0x80000000 and compareSignedValues(rs2) == -1))
                else int(compareSignedValues(rs1) / compareSignedValues(rs2))
            )
        #mod 
        case ('0000001', '110'): result = (
                compareSignedValues(rs1) if (compareSignedValues(rs2) == 0 or
                                             (compareSignedValues(rs1) == -0x80000000 and compareSignedValues(rs2) == -1))
                else compareSignedValues(rs1) % compareSignedValues(rs2)
            ) 
        case _: result = 0
    
    writeRegister(rd, result)
 
    print(f"R-type: {instruction['assembly']} result: {result & 0xFFFFFFFF:#010x}")
    
    return pc + 4

def executeItype(instruction, pc, stats):
    opcode = instruction['opcode']
    
    rs1 = readRegister(int(instruction['rs1'][1:]))
    rd  = int(instruction['rd'][1:])
    immeadiate = instruction['immeadiate']

    #i-type
    if opcode == '0010011':
        stats['I'] += 1
        stats['alu'] += 1
        
        match instruction['funct3']:
            case '000': result = rs1 + immeadiate
            case '111': result = rs1 & immeadiate
            case '110': result = rs1 | immeadiate
            case '100': result = rs1 ^ immeadiate
            case '010': result = 1 if compareSignedValues(rs1) < immeadiate else 0
            case '011': result = 1 if (rs1 & 0xFFFFFFFF) < (immeadiate & 0xFFFFFFFF) else 0
            case '001': result = rs1 << (immeadiate & 0x1F)
            case '101':
                match instruction['funct7']:
                    case '0000000': result = rs1 >> (immeadiate & 0x1F)
                    case '0100000': result = compareSignedValues(rs1) >> (immeadiate & 0x1F)
                    case _: result = 0
            case _: result = 0

        writeRegister(rd, result)

        print(f"I-type ALU: {instruction['assembly']} result: {result & 0xFFFFFFFF:#010x}")

        return pc + 4

    #lw
    elif opcode == '0000011':
        stats['I'] += 1
        stats['load'] += 1
        
        address = (rs1 + immeadiate) & 0xFFFFFFFF

        if address % 4 != 0:
            print(f"HALT: misaligned load at {address:#010x}")
            return None

        value = memory.get(address, 0)
        writeRegister(rd, value)

        print(f"Load: {instruction['assembly']} address: {address:#010x}")
       
        return pc + 4

    #jalr
    elif opcode == '1100111':
        
        stats['J'] += 1
        stats['jump'] += 1
        
        target = (rs1 + immeadiate) & ~1
        
        writeRegister(rd, pc + 4)

        print(f"JALR: {instruction['assembly']} jump to {target:#010x}")
        
        return target

def executeStype(instruction, pc, stats):
    
    stats['S'] += 1
    stats['store'] += 1

    rs1 = readRegister(int(instruction['rs1'][1:]))
    rs2 = readRegister(int(instruction['rs2'][1:]))
    address = (rs1 + instruction['immeadiate']) & 0xFFFFFFFF

    if address % 4 != 0:
        print(f"HALT: misaligned store at {address:#010x}")
        return None
    
    memory[address] = rs2 & 0xFFFFFFFF

    print(f"Store: {instruction['assembly']} address: {address:#010x}")
    return pc + 4

def executeBtype(instruction, pc, stats):
    stats['B'] += 1
    stats['branch'] += 1

    rs1 = readRegister(int(instruction['rs1'][1:]))
    rs2 = readRegister(int(instruction['rs2'][1:]))
    immeadiate = instruction['immeadiate']

    taken = False

    match instruction['funct3']:
        case '000': taken = (rs1 == rs2)
        case '001': taken = (rs1 != rs2)
        case '100': taken = (compareSignedValues(rs1) < compareSignedValues(rs2))
        case '101': taken = (compareSignedValues(rs1) >= compareSignedValues(rs2))
        case '110': taken = (rs1 < rs2)
        case '111': taken = (rs1 >= rs2)

    if taken:
        stats['branchesTaken'] += 1
        nextPC = pc + immeadiate
        print(f"Branch TAKEN: {instruction['assembly']}")
    else:
        stats['branchesNotTaken'] += 1
        nextPC = pc + 4
        print(f"Branch NOT taken: {instruction['assembly']}")

    return nextPC

def executeUtype(instruction, pc, stats):
    stats['U'] += 1

    rd = int(instruction['rd'][1:])
    immeadiate = instruction['immeadiate']

    match instruction['opcode']:
        #lui
        case '0110111':
            writeRegister(rd, immeadiate)
        #auipc
        case '0010111':
            writeRegister(rd, pc + immeadiate)

    print(f"U-type: {instruction['assembly']}")
    
    return pc + 4

def executeJtype(instruction, pc, stats):
    stats['J'] += 1
    stats['jump'] += 1

    rd = int(instruction['rd'][1:])
    immeadiate = instruction['immeadiate']

    writeRegister(rd, pc + 4)
    target = pc + immeadiate

    print(f"JAL: {instruction['assembly']} jump to {target:#010x}")
    
    return target

def execute(instruction, pc, trace, stats):
    nextPC = pc + 4

    match instruction['format']:
        case 'R':
            nextPC = executeRtype(instruction, pc, stats)

        case 'I':
            nextPC = executeItype(instruction, pc, stats)

        case 'S':
            nextPC = executeStype(instruction, pc, stats)

        case 'B':
            nextPC = executeBtype(instruction, pc, stats)

        case 'U':
            nextPC = executeUtype(instruction, pc, stats)

        case 'J':
            nextPC = executeJtype(instruction, pc, stats)

        case _:
            stats['UNKNOWN'] += 1
            print(f"HALT: unknown instruction at PC {pc:#010x}")
            return None

    registers[0] = 0

    trace.append(
        f'Step:\n'
        f'PC: {pc:#010x}\n'
        f'INSTUCTION: {instruction["hex"]}\n'
        f'ASSEMBLY: {instruction["assembly"]}\n'
        f'NEXT PC : {nextPC & 0xFFFFFFFF:#010x}\n\n'
    )

    return nextPC & 0xFFFFFFFF

def main():
    #A3 Part B.1 Input & PC Rules
    instructions = loadInstructions('hex_inst.txt')
    if not instructions:
        print('ERROR: no valid instructions loaded.')
        retur


    #A3 Part C.2 Statistics Summary 
    stats = {
        'R': 0, 'I': 0, 'S': 0, 'B': 0, 'U': 0, 'J': 0, 'UNKNOWN': 0,
        'alu': 0, 'load': 0, 'store': 0, 'branch': 0, 'jump': 0,
        'branchesTaken': 0, 'branchesNotTaken': 0
    }

    #Part B.1 - PC starts at 0
    pc          = 0
    step        = 0
    maxSteps   = 100
    trace = ['RISCV Trace\n\n']

    #A3 Part B.5 Stop Condition
    while step < maxSteps:
        index = pc // 4

        if index < 0 or index >= len(instructions):
            print('PC out of range')
            break

        if pc % 4 != 0:
            print(f'HALT: PC misaligned at {pc:#010x}')
            break

        instruction = instructions[index]

        #A3 Part B.4 Decode --> Execute
        result = execute(instruction, pc, trace, stats)
        if result is None:
            break

        pc   = result
        step += 1

    else:
        print(f'HALT: maxSteps={maxSteps} reached')

    #A3 Part C Extensions 
    #A3 Part C.1 Output Files
    with open('sim_trace.txt', 'w') as f:
        f.writelines(trace)

    with open('final_state.txt', 'w') as f:
        f.write(f'Final PC: {pc:#010x}\n\n')

        f.write('Registers:\n')
        for i in range(32):
            f.write(f'  x{i:02} = {registers[i]:#010x} ({compareSignedValues(registers[i])})\n')

        f.write('\nMemory:\n')
        if not memory:
            f.write('No writes to memory\n')
        else:
            for address in sorted(memory):
                f.write(f'  [{address:#010x}] = {memory[address]:#010x} ({compareSignedValues(memory[address])})\n')

        #Part C.2 - statistics summary
        f.write(f'Executed instructions: {step}\n\n')
        f.write('By format:\n')
        for k in ['R', 'I', 'S', 'B', 'U', 'J', 'UNKNOWN']:
            f.write(f'  {k}: {stats[k]}\n')
        f.write('\nBy category:\n')
        for k in ['alu', 'load', 'store', 'branch', 'jump', 'UNKNOWN']:
            f.write(f'  {k}: {stats[k]}\n')
        f.write(f'\nBranches taken    : {stats["branchesNotTaken"]}\n')
        f.write(f'Branches not taken: {stats["branchesTaken"]}\n')


    print(f'\nTotal executed instructions: {step}')
    print(f'By format:   R={stats["R"]}  I={stats["I"]}  S={stats["S"]}  B={stats["B"]}  U={stats["U"]}  J={stats["J"]}  UNKNOWN={stats["UNKNOWN"]}')
    print(f'By category: ALU={stats["alu"]}  LOAD={stats["load"]}  STORE={stats["store"]}  BRANCH={stats["branch"]}  JUMP={stats["jump"]}')
    print(f'Branches taken: {stats["branchesTaken"]} | Not taken: {stats["branchesNotTaken"]}')


if __name__ == '__main__':
    main()
