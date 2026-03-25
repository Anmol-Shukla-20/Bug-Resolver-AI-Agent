from agent.issue_parser import parse_issue
from agent.fix_generator import generate_fix
from agent.test_generator import generate_tests

def run_agent(issue_text):
    parsed = parse_issue(issue_text)
    
    fix = generate_fix(parsed)
    tests = generate_tests(parsed)
    
    print("\n=== FIX SUGGESTION ===\n")
    print(fix)

    print("\n=== GENERATED TESTS ===\n")
    print(tests)

if __name__ == "__main__":
    issue = input("Enter issue: ")
    run_agent(issue)