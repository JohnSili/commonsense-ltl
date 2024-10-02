import re
import random
from g4f.client import Client

def translate_to_ltl(instructions):
    """
    Translates natural language instructions into a Linear Temporal Logic (LTL) formula
    using a language model.

    Args:
        instructions (str): A string containing natural language instructions for a task.

    Returns:
        str: A string representing the LTL formula translated from the instructions.

    Raises:
        Exception: If there's an error in communicating with the language model.
    """
    client = Client()

    prompt = """
    LTL Expression Translator with Linear Dependencies

    Atomic Propositions:
    Describe your atomic propositions using alphanumeric identifiers or double-quoted strings. 
    Remember, identifiers starting with F, G, or X (e.g., "GFa") are interpreted differently. 
    Use double quotes ("GFa") if you want to refer to such propositions directly.

    Boolean Constants:
    Use 1 or 0, or true or false (case insensitive).

    Boolean Operators:
    - and: &, &&, /\
    - or: |, ||, /, +
    - implies: ->, -->, =>
    - equivalent: <->, <-->, <=>
    - not: ! (prefix), ~ (prefix)
    - exclusive or: ^, xor

    Temporal Operators:
    Binary Operators:
    - Strong until: U
    - Weak until: W
    - Strong release: M
    - Weak release: R, V

    Unary Operators (prefix):
    - Next: X
    - Eventually: F, <>
    - Globally: G, []

    Additional Syntax:
    For specifying polarity (compatibility with Wring), use =1 or =0 after atomic propositions 
    (e.g., a=0 U b=1 is equivalent to !a U b).

    Instructions for LTL Translation:
    Translate the following natural language instructions into a Linear Temporal Logic (LTL) formula 
    with strict linear dependencies between actions. Each action should follow the previous one in a 
    clear sequence using the "Next" (X) operator to ensure that every action occurs only after the 
    previous one is completed. No parallel or branching actions are allowed, and all steps should 
    form a strictly linear chain of dependencies.

    Rules:
    1. Replace each action with an atomic proposition.
    2. Use the "Next" operator (X) to indicate that one action follows another.
    3. Ensure that each step strictly depends on the previous step.

    Translate the following instructions into a strictly linear LTL formula:

    {}
    """.format(instructions)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        ltl_formula = response.choices[0].message.content
        return ltl_formula.strip()
    except Exception as e:
        raise Exception(f"Error in translating instructions to LTL: {str(e)}")


def extract_actions(formula):
    """
    Extracts individual actions from the provided formula string.

    The function looks for words in the formula that start with letters and may include underscores.
    It then filters out logical operators "G" and "X" from the list of actions.

    Args:
        formula (str): The input formula containing actions and logical operators.

    Returns:
        list: A list of actions (words) from the formula, excluding logical operators.
    """

    # Regex pattern to match words (actions) in the formula
    pattern = r'\b\w+\b'

    # Finding all matches based on the pattern
    matches = re.findall(pattern, formula)

    # Removing logical operators "G" and "X"
    actions = [match for match in matches if match not in ["G", "X"]]

    return actions


def replace_random_actions(actions):
    """
    Randomly replaces actions with '{missing actions}' while ensuring at least two actions remain.

    The function iteratively replaces random actions in the list with the placeholder
    '{missing actions}', avoiding the first and last actions. This process continues until 
    only two actions remain unreplaced.

    Args:
        actions (list): A list of actions to process.

    Returns:
        list: The list of actions with random actions replaced by '{missing actions}'.
    """
    iteration = 0
    # Filter out actions that have already been replaced
    remaining_actions = [action for action in actions if action != '{missing actions}']

    # Continue replacing actions randomly until at least two actions remain
    while len(remaining_actions) > 2:
        # Choose a random index for replacement, excluding the first and last actions
        index = random.randint(1, len(actions) - 2)
        if actions[index] != '{missing actions}':
            actions[index] = '{missing actions}'

        # Update the list of remaining unreplaced actions
        remaining_actions = [action for action in actions if action != '{missing actions}']

        # Print the current state of the action list for debugging
        iteration += 1
        print(f"Iteration {iteration}: {' -> '.join(actions)}")

    return actions

def verify_ltl_formula(formula):
    """
    Placeholder function for verifying the given LTL formula.
    The actual implementation will be added soon.

    Args:
        formula (str): The LTL formula to be verified.

    Returns:
        dict: A placeholder dictionary with verification results.
    """
    print("Note: LTL formula verification will be implemented soon.")
    return {
        "is_valid": None,
        "message": "Verification not implemented yet",
        "latex": "",
        "tree": {}
    }



def create_plan(formula):
    """
    Generates a plan by extracting actions from the formula and randomly replacing some of them.

    The function first extracts all actions from the input formula, then replaces random actions
    with a placeholder while ensuring that at least two actions remain. The final list of actions
    is returned as a formatted string with arrows between each action.

    Args:
        formula (str): The input formula containing logical operations and actions.

    Returns:
        str: A string representing the final plan, with random actions replaced by placeholders.
    """
    actions = extract_actions(formula)
    replaced_actions = replace_random_actions(actions)
    plan_str = ' -> '.join(replaced_actions)
    return plan_str

formula = "G(make_cleaning_checklist -> X(declutter_each_room -> X(dust_surfaces -> X(vacuum_or_sweep_floors -> X(mop_floors -> X(clean_windows -> X(scrub_bathrooms -> X(do_laundry -> X(change_bed_linens)))))))))"
plan = create_plan(formula)

print("\nFinal Plan:")
print(plan)