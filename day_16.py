# https://adventofcode.com/2021/day/16
from collections import defaultdict

def parse_input():
    # Parse file input

    with open("input/16.txt") as f:

        lines = []
        for line in f.readlines():
            line = line.rstrip()
            lines.append(line)
            
        return lines


class Decoder():
    def __init__(self): 
        self.version_number_total = 0 

    def convert_hex_to_bin(self, hex): 
        int_val = int(hex, 16)
        expected_final_length = len(hex) * 4
        # print(bin(int_val))
        bin_val = bin(int_val)[2:].zfill(expected_final_length)
        # print(bin_val)
        return bin_val

    def decode_literal_value(packet, depth=0): 
        tab_space = ''.join(['    ' for _ in range(depth + 1)])

    def reset_decoder(self): 
        self.__init__()

    def decode_packet(self, packet, depth=0):
        tab_space = ''.join(['    ' for _ in range(depth + 1)])

        if not packet:
            raise Exception("Empty packet passed in!")

        # print(f"{tab_space}Decoding new packet {packet}")

        packet_version = int(packet[:3],2)
        packet_type_id = int(packet[3:6],2)

        # if packet_version == 6:
        #     print(packet)

        self.version_number_total += packet_version

        print(f"{tab_space}packet_version: {packet_version}")
        print(f"{tab_space}packet_type_id: {packet_type_id}")

        if packet_type_id == 4: 
            # This is a literal value. 
            # This encodes a single binary number
            # Padded with 0s until its length is a mul of 4 bits
            print(f"{tab_space}Packet is a literal value")
            finished = False 
            starting_idx = 6
            number = []
            while not finished:
                bit_group = packet[starting_idx:starting_idx + 5]
                if bit_group[0] == "0": 
                    # We're at the end of the encoding. 
                    finished = True 
                
                print(bit_group)
                number.append(bit_group[1:])
                starting_idx += 5

            number = int("".join(number), 2) 
            print(f"{tab_space}Literal value is {number}")
            # print(f"{tab_space} {packet}")


            # This works for the samples: 
            # print(f"{tab_space}Next packet will be {packet[starting_idx:]}")
            return number, packet[starting_idx:]

            # I need packet size decisioning to work with nesting though. 
            if packet[starting_idx:] and int(packet[starting_idx:], 2):
                # print(f"{tab_space}Next packet will be {packet[starting_idx:]}")
                return number, packet[starting_idx:]
            

            print(f"{tab_space}Reducing the start idx")
            return number, packet
        else: 
            # This packet is an operator. 
            print(f"{tab_space}Packet is an operator")
            header_len = 6 # TODO should be dynamic 
            length_type_id = packet[header_len]
            start_idx = header_len + 1
            print(f"{tab_space}length_type_id: {length_type_id}")

            if length_type_id == "0": 
                # The next 15 bits represent the total length of the sub packets. 

                total_length = int(packet[start_idx: start_idx + 15], 2)
                print(f"{tab_space}Packet contains packets of total_length {total_length}")
                if total_length == 106:
                    print(packet)
                start_idx += 15
                numbers = [] 
                distance_traveled = 0 
                packet = packet[start_idx:]
                current_size = len(packet) 
                while distance_traveled != total_length:
                    # infinite loop. 
                    print(f"{tab_space}Decoding subpacket")
                    number, next_packet = self.decode_packet(packet, depth + 1)

                    #IMPORTANT TODO - IF WE GET THE SAME PACKET BACK THAT'S A PROBLEM. 

                    if next_packet == packet: 
                        # We got the same packet back. 
                        raise Exception(f"{next_packet} is the same as {packet}")


                    print("Something is wrong here maybe?")
                    print(packet[:current_size - len(next_packet)])

                    packet = next_packet

                    # print(f"{tab_space}We got back {packet}")
                    distance_traveled += current_size - len(packet)
                    current_size = len(packet)
                    numbers.append(number) 

                    print(f"{tab_space}We have traveled {distance_traveled}, and are trying to reach {total_length}")

                    if distance_traveled > total_length: 
                        raise Exception(f"We have traveled {distance_traveled}, and are trying to reach {total_length}")


                print(numbers)

                return numbers, packet

                # TODO - I don't understand how the packet sizes are determind
                # continue 
            else: 
                # The next 11 bits reprsent the number of sub packets 
                number_sub_packets = int(packet[start_idx: start_idx + 11], 2)
                # print(packet[start_idx: start_idx + 11])
                start_idx += 11
                print(f"{tab_space}There are {number_sub_packets} sub packets")
                # print(start_idx + (11*0))
                # print(start_idx + 11*(0+1))
                outputs = []
                packet = packet[start_idx:]
                for idx in range(number_sub_packets):
                    # print(sub_packets)
                    # sub_packets.append(packet[start_idx: start_idx + 11])
                    print(f"{tab_space}---Evaluating subpacket {idx}---")

                    # TODO - I DON'T KNOW HOW FAR TO SEARCH AHEAD 
                    # print(f"1st: Sending {packet}")
                    output, packet = self.decode_packet(packet, depth +1)
                    
                    # print(f"2nd: Got back {packet}")
                    outputs.append(output) 



                if packet[start_idx:] and int(packet[start_idx:],2):
                    print("Trimming")
                    packet = packet[start_idx:]
                return outputs, packet

        print("Done?")



packet = parse_input()[0]
decoder = Decoder() 
# bin_packet = "11101110000000001101010000001100100000100011000001100000"

# This packet fails 

def test_sample_problems(): 
    hex_packets = [
        "8A004A801A8002F478",
        "620080001611562C8802118E34",
        "C0015000016115A2E0802F182340",
        "A0016C880162017C3686B18A3D4780",
    ]
    final_answers = []
    expected_answers = [16,12,23,31]
    decoder = Decoder() 

    for hex in hex_packets: 
        bin_packet = decoder.convert_hex_to_bin(hex)
        decoder.decode_packet(bin_packet)
        final_answers.append(decoder.version_number_total)
        decoder.reset_decoder()


    for answer in final_answers:
        print(f"Final answer: {answer}")


    assert final_answers == expected_answers


decoder = Decoder() 
# bin_packet = "01010100000000011010101110000000000000100001010100000100101000100111010001011110000100000000011110100010000111000001110010000110001010000000000111110101010010101101000001110110010110111110100000110011110110001011100111110100110011101000010101100100101110011011111001101100010111001100000000010001111000000000110101011100000000000001000010011000111100010001101000100011001000001000000000111001000101010010000111100100011110011001111111000101101110110011111011100001101010001100000000010000101000000000101011100010010101101111010010010110001110110011001100111001000111011110111001010111110110100111010010001111010111011100110000000001000111010000000001000110000110100100111111011100100000100011110010010000000001100101100100111000011111011010000000001010010010011111010100100010011010100101010011101100001101111000011000010101000000000010101001000111101100110110010010010010000111000010000000010010001101101000000000110011010010011011100001010110000100011001101100110100110001110110101111011000111110110101000010110110110000100110011011101010110011100100000000000100001001001000100000111000100000000101000100111011011000100110100001111111001110001010000100111011110010111110111100010010011101111000001010100110000000001011011100000000001010101001001000111101010011111001010110011010000011001001010011110111010000001010100101101001110100001011010011000000000101101101000000000101010000000000000100001011100010110111000011100010001001100000100000000011001100011001011000011100010000010001100101010000111100110000000001001111000000000001010101111001101110101000100001001101110101000101101001011001101101000000000000000101110110000011011000100000000100011100011100011001100011000100110100001010010010111000111101110011111100110011010010001010111001000000000110000011110011000111110010000110110000000001011110011001011111111001101111000110101000110101110000100010000000000000000110111101001101100111110100001000000010000000001010000111100100010100101110011000010011011001101001000110100100110010011010011001011001110101000000000110101001110000001011100100111000111011110011111001111010100101111011100011001001100000000010101100101111101010110111000001110011010000000001000110011001000100011001100100010010100110111110111100100000101111100100000000001010110111001101000011001100011101001001100001111100001000000000100000000110010010010001011001101100100100100100110111110110010110011001000010000000001011010000100111100101100011100000000001101000001001010010100100000111001110010100101001000001110101001000000000110101011111010000000001001110011000100001010010100111101111100000101100111011111110110100110110100110011111010001101001110010000111000101111110011001100111010101000110011000000000011111111110011001111011111010000001010111001001111010000100111000101111001100000000001001010111001000100100101100100101011000010011100110101001111001110011011000110111011100000000101101100011001101001100011000110111000110011110011100011101011010001001101101011111100100011111011110111111111110011111011011101110001100111101010111010111001010111110001000010000000000010011101111001100000000011000100000100001000100011110001100011001100000000011100100010100001000111111110001001001001000000000010000101110001110011100011100101000001011100100000000101000010010000000000000100001000100010001111000011011110001100011000100000000011001100011011101000110001110001011001000000000000010000101110000101100100011011011000001010101010000000001000110011101001000101001001100100011011100000000100100100100101111100000111100111111000110110101001001111101100010011110010011011011000101001010110100100101001110111111110000110000110000000001001110010001111110000001010100000000001010100101001110011011101010011100010010111010110110111000000000010101001001101001001010100000000100101100110111001111001000001111001101011111110111110110001101011010100111001100110001110001111100100110000110100000100000000011010101101011000000000101011001010110011101001111101111100100101011001110100111110111110010010101111011000001100100001000000000110111000110100000000010010000001001011011010110011011111000000101111001011011010110011011111000000100111001101001001100100010001100010000000000100000011100100100111111010011100000110010010000000001110100010100101101001010001101001101000111111110100000000010001100110101011110001100110100100010010010111001000110000001111101001100011100101001111010010111010100001000110000000001011111100000000001011111001001010110100111010001110110010010110110001001010010111111111001110110111110101100010011000101111111011101101110101001100100000000100101111011001011111011111101110000010010110100000000010001000100000000011010100001111111000100001110001001100000100000000011100100000110011000010110010000011110011100000000001100011100000000001110010000000010111000110100010000000000100001000000001010010010010111000000000011010000000000100100001010010000000010000101101100110000000000111100010000000000101001000000000110100010000010000000010111011101010100000000001010001100000000001011001000000001000000101101010000000000110101100000000010110011000110000000001000011111001100000000001110000100000000001010100100111100110101100000010101100100000000100100000011001010000101101101000000000110101010100010000000001110010001111001100001000101000100110000000000000001000011011000110100010001010101100000111010001000000000110011000010110010010011100111010011110100011010010000011100011001101110110001000000"
packet = parse_input()[0]
bin_packet = decoder.convert_hex_to_bin(packet)
# bin_packet = "110000100000000011110100010000111000001110010000110001010000000000111"

decoder.decode_packet(bin_packet)
print("Final answer:")
print(decoder.version_number_total)

