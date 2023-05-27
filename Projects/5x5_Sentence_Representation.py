# You can enter a sentence into the function, and if all the characters included are within the 'patterns' dictionary, it will return a 5x5 representation of the sentence. 
# Otherwise, it will inform that it is not contemplated. 
# Derived from an exercise while studying, 
# I thought it would be fun to extend the code to be able to contemplate most characters that can be represented in a 5x5 pattern.


def print_sentence(character):
    patterns = {
        'A': ['  *  ', ' * * ', '*****', '*   *', '*   *'],
        'B': ['**** ', '*   *', '**** ', '*   *', '**** '],
        'C': [' ****', '*    ', '*    ', '*    ', ' ****'],
        'D': ['**** ', '*   *', '*   *', '*   *', '**** '],
        'E': ['*****', '*    ', '*****', '*    ', '*****'],
        'F': ['*****', '*    ', '*****', '*    ', '*    '],
        'G': [' ****', '*    ', '*  **', '*   *', ' ****'],
        'H': ['*   *', '*   *', '*****', '*   *', '*   *'],
        'I': ['*****', '  *  ', '  *  ', '  *  ', '*****'],
        'J': ['*****', '    *', '    *', '*   *', ' *** '],
        'K': ['*   *', '*  * ', '**   ', '*  * ', '*   *'],
        'L': ['*    ', '*    ', '*    ', '*    ', '*****'],
        'M': ['*   *', '** **', '* * *', '*   *', '*   *'],
        'N': ['*   *', '**  *', '* * *', '*  **', '*   *'],
        'O': [' *** ', '*   *', '*   *', '*   *', ' *** '],
        'P': ['**** ', '*   *', '**** ', '*    ', '*    '],
        'Q': [' *** ', '*   *', '*   *', '*  **', ' ** *'],
        'R': ['**** ', '*   *', '**** ', '*  * ', '*   *'],
        'S': [' ****', '*    ', ' *** ', '    *', '**** '],
        'T': ['*****', '  *  ', '  *  ', '  *  ', '  *  '],
        'U': ['*   *', '*   *', '*   *', '*   *', ' *** '],
        'V': ['*   *', '*   *', ' * * ', ' * * ', '  *  '],
        'W': ['*   *', '*   *', '* * *', '** **', '*   *'],
        'X': ['*   *', ' * * ', '  *  ', ' * * ', '*   *'],
        'Y': ['*   *', ' * * ', '  *  ', '  *  ', '  *  '],
        'Z': ['*****', '   * ', '  *  ', ' *   ', '*****'],
        '0': [' *** ', '*   *', '*   *', '*   *', ' *** '],
        '1': ['  *  ', ' **  ', '  *  ', '  *  ', ' *** '],
        '2': [' *** ', '*   *', '   * ', '  *  ', '*****'],
        '3': [' *** ', '    *', '  ** ', '    *', ' *** '],
        '4': ['*   *', '*   *', '*****', '    *', '    *'],
        '5': ['*****', '*    ', '**** ', '    *', '**** '],
        '6': [' ****', '*    ', '*****', '*   *', ' *** '],
        '7': ['*****', '    *', '   * ', '  *  ', '  *  '],
        '8': [' *** ', '*   *', ' *** ', '*   *', ' *** '],
        '9': [' *** ', '*   *', '*****', '    *', '**** '],
        '!': ['  *  ', '  *  ', '  *  ', '     ', '  *  '],
        '?': [' *** ', '*   *', '   * ', '     ', '  *  '],
        '¿': ['     ', '  *  ', '   * ', '*   *', ' *** '],
        '$': ['  *  ', '* * *', ' * * ', '* * *', '  *  '],
        '%': ['*   *', '   * ', '  *  ', ' *   ', '*   *'],
        '&': [' **  ', '*  * ', ' **  ', '*  * ', ' *  *'],
        '/': ['    *', '   * ', '  *  ', ' *   ', '*    '],
        '(': ['  *  ', ' *   ', ' *   ', ' *   ', '  *  '],
        ')': ['  *  ', '   * ', '   * ', '   * ', '  *  '],
        ' ': ['     ', '     ', '     ', '     ', '     '],
    
        # Add more characters here as needed
    }
 # Ensure the input character is uppercase if it is a letter
    if character.isalpha():
        character = character.upper()

    # Check if the character is in the patterns dictionary
    if character in patterns:
        # Return the 5x5 representation of the character
        return patterns[character]
    else:
        print("Character not supported. Please add the pattern for the character in the 'patterns' dictionary.")
        return ['     ', '     ', '     ', '     ', '     ']

def print_sentence(sentence):
    # Split the sentence into individual characters
    characters = list(sentence)

    # Initialize an empty list to store the 5x5 patterns for each character
    pattern_lines = ['' for _ in range(5)]

    # Iterate through each character in the sentence
    for character in characters:
        # Get the 5x5 pattern for the character
        character_pattern = print_big(character)

        # Append the character pattern to the corresponding line
        for i in range(5):
            pattern_lines[i] += character_pattern[i] + ' '

    # Print the final pattern for the entire sentence
    for pattern_line in pattern_lines:
        print(pattern_line)

# Example usage
# print_sentence('Hello World!')
