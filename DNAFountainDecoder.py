from typing import List, Dict, Set

class DNAFountainDecoder:
    def __init__(self):
        self.dna_map = {
            'A': '00',
            'C': '01',
            'G': '10',
            'T': '11'
        }
        self.frame_size = 4
        self.drops = []
        self.decoded_frames = {}  # Dictionary to store position -> frame mapping
        self.rank_seed_table = {
            0: 2, 1: 2, 2: 1, 3: 1, 4: 2, 5: 4, 6: 2, 7: 1,
            8: 6, 9: 1, 10: 1, 11: 2, 12: 7, 13: 2, 14: 1, 15: 4
        }
        
    def load_dna_sequences(self, filename: str) -> None:
        """Load DNA sequences from file and convert them to drops"""
        with open(filename, 'r') as file:
            for line in file:
                dna_sequence = line.strip()
                binary = self.dna_to_binary(dna_sequence)
                
                # Extract seed and data
                seed_binary = binary[:4]
                data_binary = binary[4:]  # Last 4 bits are the frame data

                
                seed = int(seed_binary, 2)
                self.drops.append({
                    'seed': seed,
                    'value': data_binary,
                    'positions': self.get_frame_positions(seed)
                })
                print(f"Loaded drop: seed={seed}, positions={self.get_frame_positions(seed)}, value={data_binary}")

    def dna_to_binary(self, dna_sequence: str) -> str:
        """Convert DNA sequence back to binary"""
        return ''.join(self.dna_map[nucleotide] for nucleotide in dna_sequence)
    
    def get_frame_positions(self, seed: int) -> List[int]:
        """Get frame positions for this drop based on seed"""
        import random
        random.seed(seed)
        num_positions = self.rank_seed_table[seed % 16]  # Use modulo 16 to wrap around if seed > 15
        return random.sample(range(8), num_positions)  # Choose from

    
    def xor_binary(self, bin1: str, bin2: str) -> str:
        """XOR two binary strings"""
        if len(bin1) != len(bin2):
            raise ValueError("Binary strings must be same length")
        result = ''
        for b1, b2 in zip(bin1, bin2):
            result += '1' if b1 != b2 else '0'
        return result



    def decode_step_by_step(self) -> str:
        print("\nStarting step-by-step decoding:")
        
        # Step 1: Process single-frame drops
        print("\nStep 1: Processing single-frame drops")
        for drop in self.drops:
            if len(drop['positions']) == 1:
                position = drop['positions'][0]
                self.decoded_frames[position] = drop['value']
                print(f"Decoded frame at position {position}: {drop['value']}")
        
        # Step 2: Process multi-frame drops
        print("\nStep 2: Processing multi-frame drops")
        iterations = 0
        while len(self.decoded_frames) < 8 and iterations < 10:
            iterations += 1
            print(f"\nIteration {iterations}")
            for drop in self.drops:
                positions = drop['positions']
                if len(positions) > 1:
                    known_positions = [pos for pos in positions if pos in self.decoded_frames]
                    unknown_positions = [pos for pos in positions if pos not in self.decoded_frames]
                    print(f"Processing drop: positions={positions}, known={known_positions}, unknown={unknown_positions}")
                    if len(unknown_positions) == 1:
                        value = drop['value']
                        for pos in known_positions:
                            value = self.xor_binary(value, self.decoded_frames[pos])
                        self.decoded_frames[unknown_positions[0]] = value
                        print(f"Decoded frame at position {unknown_positions[0]}: {value}")
        
        # Combine frames in order
        final_message = ''
        for i in range(8):
            if i in self.decoded_frames:
                final_message += self.decoded_frames[i]
            else:
                print(f"Warning: Missing frame at position {i}")
                final_message += '0000'  # Placeholder for missing frames
        
        print("\nDecoded frames:")
        for i in range(8):
            print(f"Frame {i}: {self.decoded_frames.get(i, 'Missing')}")
        
        return final_message



def decode_with_details(input_file: str) -> str:
    decoder = DNAFountainDecoder()
    decoder.load_dna_sequences(input_file)
    return decoder.decode_step_by_step()


if __name__ == "__main__":
    decoded_message = decode_with_details("encoded_drops.txt")
    print(f"\nFinal decoded message: {decoded_message}")