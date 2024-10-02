import random


from g4f.client import Client

def complete_plan(incomplete_plan):
    """
    Complete a partially defined plan by filling in missing actions using AI-generated suggestions.

    This function takes an incomplete plan with placeholders for missing actions and uses
    a language model to generate logical and contextually appropriate actions to complete the plan.
    The function is specifically designed for plans related to household tasks, such as cleaning.

    Args:
        incomplete_plan (str): A string representing an incomplete plan. Actions in the plan
                               should be separated by ' -> '. Missing actions should be
                               represented by the placeholder '{missing actions}'.

    Returns:
        str: A string representing the completed plan with AI-generated actions replacing
             the '{missing actions}' placeholders.

    Example:
        incomplete_plan = "make_cleaning_checklist -> {missing actions} -> vacuum_floors"
        complete_plan(incomplete_plan)
        "make_cleaning_checklist -> gather_cleaning_supplies -> dust_surfaces -> vacuum_floors"

    Note:
        - This function relies on the g4f library and requires an active internet connection.
        - The quality and appropriateness of the generated actions depend on the AI model used.
    """
    client = Client()

    prompt = """

The process of executing the action associated with the task - {Task} is represented, each action is separated by -> (where the arrow means transition between actions), here is the plan


{ProcessedPlan}


replace the missing actions based on your own view of the world, apply logical knowledge of the world and general knowledge of everyday actions, where things are, apply this knowledge and submit the corrected plan with additions.
    """.format(incomplete_plan)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        completed_plan = response.choices[0].message.content
        return completed_plan.strip()
    except Exception as e:
        raise Exception(f"Error in completing the plan: {str(e)}")



def generate_plan(actions, include_missing=True, missing_probability=0.3):
    """
    Generates a plan from a list of actions, optionally including 'missing actions' placeholders.

    This function takes a list of actions and creates a plan by joining the actions
    with ' -> ' separators. It can also randomly insert '{missing actions}' placeholders
    to simulate incomplete plans for testing purposes.

    Args:
        actions (list): A list of actions extracted from an LTL formula.
        include_missing (bool): If True, may include '{missing actions}' placeholders. Default is True.
        missing_probability (float): The probability of inserting a 'missing actions' placeholder
                                     between any two actions. Should be between 0 and 1. Default is 0.3.

    Returns:
        str: A string representing the generated plan, with actions separated by ' -> '
             and possibly including '{missing actions}' placeholders.

    Example:
        >>> actions = ['make_bed', 'vacuum_floor', 'dust_surfaces', 'take_out_trash']
        >>> generate_plan(actions)
        'make_bed -> {missing actions} -> vacuum_floor -> dust_surfaces -> {missing actions} -> take_out_trash'

    Note:
        - The function always keeps the first and last actions intact.
        - If include_missing is False, the function simply joins all actions without any missing placeholders.
    """
    if not actions:
        return ""

    if len(actions) == 1:
        return actions[0]

    if not include_missing:
        return " -> ".join(actions)

    plan = [actions[0]]  # Start with the first action

    for action in actions[1:-1]:  # Process middle actions
        if random.random() < missing_probability:
            plan.append("{missing actions}")
        plan.append(action)

    plan.append(actions[-1])  # End with the last action

    return " -> ".join(plan)