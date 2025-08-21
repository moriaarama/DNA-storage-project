import random as py_random
import numpy as np
from typing import List, Tuple

class DNAFountainEncoder:
    def __init__(self, message: str, frame_size: int = 4):

        self.binary_message = format(int(message, 2), '032b')
        self.frame_size = frame_size
        self.frames = self._split_to_frames()
        
        
    def _split_to_frames(self) -> List[str]:
        """Split the 32-bit message into  L-bit frames-in our case- L=4""" 
        return [self.binary_message[i:i+self.frame_size] 
                for i in range(0, len(self.binary_message), self.frame_size)]
    
    def create_drop(self, seed: int, rank: int) -> Tuple[str, int, List[str]]:
        """
        Create a single drop using the given seed
        Returns: (binary_result, seed, selected_frames)
        binary_result = binary seed + drop value
        """ 
       
        d = rank     #  the provided rank from the exercise table (1)
        
        drop_random = py_random.Random(seed) # select randomly which frames will be chosen to this drop

        # Randomly select exactly d frames without returns- once a frame is selected for a particular drop, it won't be selected again for the same drop.
        selected_indices = drop_random.sample(range(len(self.frames)), d) # random.sample() is without returns
        selected_frames = [self.frames[i] for i in selected_indices]
        
        result = self._xor_frames(selected_frames) # XOR for all selected frames- bit by bit

        seed_binary = format(seed, '04b')
        full_result = seed_binary + result
        return full_result, seed, selected_frames # seed+drop

    
    def _xor_frames(self, frames: List[str]) -> str:
        """XOR all frames bit by bit"""
        # Convert frames to integers for easier XOR operation
        int_frames = [int(frame, 2) for frame in frames]
        result = 0
        for frame in int_frames:# XOR all frames
            result ^= frame
        
        return format(result, f'0{self.frame_size}b')# Convert back to binary string of frame_size length
    
    def to_dna(self, binary: str) -> str:
        """Convert binary string to DNA sequence using the provided mapping"""
        dna_map = {
            '00': 'A',
            '01': 'C',
            '10': 'G',
            '11': 'T'
        }
        
        dna_sequence = ''
        for i in range(0, len(binary), 2):
            pair = binary[i:i+2]
            dna_sequence += dna_map[pair]
            
        return dna_sequence

def create_16_drops(message: str) -> List[Tuple[str, int, List[str]]]:
    """Create 16 drops from the input message and save them to a file"""
    encoder = DNAFountainEncoder(message)
    drops = []

    rank_seed_table = {
        0: 2, 1: 2, 2: 1, 3: 1, 4: 2, 5: 4, 6: 2, 7: 1,
        8: 6, 9: 1, 10: 1, 11: 2, 12: 7, 13: 2, 14: 1, 15: 4
         #seed 0 - rank 2 , seed 1 rank 2 and so on 
    }

    # Create 16 drops with different seeds
    for seed in range(16):
        drop = encoder.create_drop(seed, rank_seed_table[seed])
        drops.append(drop)

    # Write drops to a file
    with open('encoded_drops.txt', 'w') as file:
        for drop in drops:
            dna_sequence = encoder.to_dna(drop[0])
            file.write(f"{dna_sequence}\n")

    return drops



if __name__ == "__main__":
    message = "01000001101011110000010110100101"  # 32-bit example message
           #   0100 0001 1010 1111 0000 0101 1010 0101 returned yayy
    
    drops = create_16_drops(message)
    
    for i, (binary, seed, frames) in enumerate(drops):
        dna = DNAFountainEncoder(message).to_dna(binary)
        print(f"Drop {i+1}:")
        print(f"  Seed: {seed}")
        print(f"  Binary: {binary}")
        print(f"  Selected frames: {frames}")
        print(f"  DNA sequence: {dna}")