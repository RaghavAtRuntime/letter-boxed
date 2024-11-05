# Function to process the letters from each side
def get_letters(side_input):
    """
    Cleans and processes the input letters from each side.

    Args:
        side_input (str): A string of letters from one side of the box.

    Returns:
        dict: A dictionary mapping letters to their side.
    """
    let = ''.join(filter(str.isalpha, side_input))
    let_list = list(let.upper())
    return dict((s, side_input) for s in let_list)


# Function to clean and combine letters from all sides
def clean_letters(l, t, r, b):
    """
    Cleans and combines the letters from the four sides of the puzzle.

    Args:
        l, t, r, b (str): Strings representing the letters on the left, top, right, and bottom sides.

    Returns:
        dict: A dictionary mapping letters to their side.
    """
    left = get_letters(l)
    top = get_letters(t)
    right = get_letters(r)
    bottom = get_letters(b)

    # Combine all letters and their positions
    pos = {**left, **top, **right, **bottom}
    return pos


# Function to get valid words from the dictionary that match the given letters
def get_words(wordfile, pos, chars):
    """
    Gets valid words that match the given set of characters and ensures letters
    are not from the same side consecutively.

    Args:
        wordfile (str): Path to a file containing dictionary words.
        pos (dict): Mapping of letters to their sides.
        chars (set): Set of available characters.

    Returns:
        list: Valid words that meet the criteria.
    """
    with open(wordfile) as word_file:
        actual_words = sorted(set(word.strip().upper() for word in word_file))

    # Filter words that only use available letters
    valid_words = [w for w in actual_words if set(w) <= chars]

    # Remove words that have consecutive letters from the same side
    toss = []
    for word in valid_words:
        letters = list(word)
        for num in range(1, len(letters)):
            if pos[letters[num]] == pos[letters[num - 1]]:
                toss.append(word)
                break

    return [w for w in valid_words if w not in toss]


# Helper function to convert a string to a sorted set (base form)
def to_base(s):
    return ''.join(sorted(set(s)))


# Function to find one-word solutions
def one_word_solution(word_list, chars):
    return [w for w in word_list if set(w) == chars]


# Function to find two-word solutions
def two_word_solution(word_list, chars):
    output = []
    for word in word_list:
        last = word[-1]
        matches = [w for w in word_list if w[0] == last and w != word]
        for match in matches:
            combined = word + match
            if set(combined) == chars:
                output.append([word, match])
    return output


# Function to find three-word solutions
def three_word_solution(word_list, chars):
    ab_combinations = [a + b for a in word_list for b in word_list if a[-1] == b[0]]
    candidates = list(set([to_base(a) + a[-1] for a in ab_combinations]))
    solutions = {a: b for a in candidates for b in word_list if set(a + b) == chars and a[-1] == b[0]}

    ext = [[a + '-' + b, to_base(a + b) + b[-1]] for a in word_list for b in word_list if a != b and a[-1] == b[0]]
    vals = ['-'.join([e[0], solutions[e[1]]]) for e in ext if e[1] in solutions]

    return [v.split('-') for v in vals]


# Map the number of words to corresponding functions
num_map = {
    '1': {'text': 'one', 'function': one_word_solution},
    '2': {'text': 'two', 'function': two_word_solution},
    '3': {'text': 'three', 'function': three_word_solution}
}


# Main function to solve the puzzle
def solve_puzzle(pos, num, wordfile, exclude=[]):
    """
    Solves the Letter Boxed puzzle.

    Args:
        pos (dict): Dictionary of letters mapped to their sides.
        num (str): The number of words in the solution ('1', '2', or '3').
        wordfile (str): Path to a word list file.
        exclude (list): Optionally exclude certain answers.

    Returns:
        tuple: A list of answers and the solution type (one-word, two-word, etc.).
    """
    chars = set(pos.keys())
    wordset = get_words(wordfile, pos, chars)
    answers = num_map[num]['function'](wordset, chars)

    # Exclude any specified answers
    answers = [x for x in answers if x not in exclude]

    return answers, num


def main():
    # Take user input for the sides of the puzzle
    left_side = input("Enter the letters for the left side: ")
    top_side = input("Enter the letters for the top side: ")
    right_side = input("Enter the letters for the right side: ")
    bottom_side = input("Enter the letters for the bottom side: ")

    # Take user input for the number of words in the solution
    while True:
        word_count = input("Enter the number of words in the solution (1, 2, or 3): ")
        if word_count in ['1', '2', '3']:
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    # Clean and process the input letters
    positions = clean_letters(left_side, top_side, right_side, bottom_side)

    # Solve for the specified number of words using a word list
    solution, solution_type = solve_puzzle(positions, word_count, 'words_easy.txt')

    print(f"Solutions ({solution_type}-word):")
    for sol in solution:
        print(' -> '.join(sol))


# Example usage
if __name__ == "__main__":
    main()
