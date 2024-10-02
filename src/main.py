from ltl_processing import translate_to_ltl, extract_actions, verify_ltl_formula
from plan_generation import generate_plan, complete_plan

def main():
    # Test natural language query
    natural_language_plan = """
    Clean the house by first making a cleaning checklist, then decluttering each room, 
    dusting surfaces, vacuuming or sweeping floors, mopping floors, cleaning windows, 
    scrubbing bathrooms, doing laundry, and finally changing bed linens.
    """
    print("Natural Language Plan:")
    print(natural_language_plan)
    print("\nTranslating to LTL...")
    
    ltl_formula = translate_to_ltl(natural_language_plan)
    print("Translated LTL Formula:")
    print(ltl_formula)

    print("\n" + "=" * 50 + "\n")

    # Test LTL formula
    test_ltl_formula = "G(make_cleaning_checklist -> X(declutter_each_room -> X(dust_surfaces -> X(vacuum_or_sweep_floors -> X(mop_floors -> X(clean_windows -> X(scrub_bathrooms -> X(do_laundry -> X(change_bed_linens)))))))))"
    print("Test LTL Formula:")
    print(test_ltl_formula)

    # Process both formulas
    for i, formula in enumerate([ltl_formula, test_ltl_formula], 1):
        print(f"\nProcessing Formula {i}:")
        print(formula)

        # Extract actions from the LTL formula
        actions = extract_actions(formula)
        print("\nExtracted Actions:")
        print(", ".join(actions))

        # Generate initial plan with missing actions
        initial_plan = generate_plan(actions, include_missing=True, missing_probability=0.3)
        print("\nInitial Plan (with missing actions):")
        print(initial_plan)

        # Complete the plan
        completed_plan = complete_plan(initial_plan)
        print("\nCompleted Plan:")
        print(completed_plan)

        # Note about future LTL verification
        print("\nNote: LTL formula verification will be implemented soon.")
        verification_result = verify_ltl_formula(formula)
        print("Placeholder verification result:", verification_result)

        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()