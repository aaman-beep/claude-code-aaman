"""Fill RUN-PROMPT.md for one case, ready to paste into a fresh Claude session in this repo.

  python benchmark/make_prompt.py CP-02        # print the prompt for one case
  python benchmark/make_prompt.py --all         # write benchmark/prompts/<ID>.txt for all 16
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def fill(case, template):
    return (template
            .replace("{{CASE_ID}}", case["id"])
            .replace("{{CATEGORY}}", case["category"])
            .replace("{{GRADE_TYPE}}", case["grade_type"])
            .replace("{{INPUT}}", case["input"])
            .replace("{{PASS_RULE}}", case.get("pass_rule", ""))
            .replace("{{REQUIRED_SKILLS}}", ", ".join(case.get("required_skills", []))))


def main():
    cases = {c["id"]: c for c in json.load(open(os.path.join(HERE, "cases.json")))["cases"]}
    tmpl = open(os.path.join(HERE, "RUN-PROMPT.md")).read()
    # use only the prompt body (after the '---' separator)
    body = tmpl.split("\n---\n", 1)[1].strip() if "\n---\n" in tmpl else tmpl

    if len(sys.argv) == 2 and sys.argv[1] == "--all":
        out = os.path.join(HERE, "prompts")
        os.makedirs(out, exist_ok=True)
        for cid, case in cases.items():
            with open(os.path.join(out, f"{cid}.txt"), "w") as f:
                f.write(fill(case, body))
        print(f"wrote {len(cases)} prompts to {out}/")
    elif len(sys.argv) == 2 and sys.argv[1] in cases:
        print(fill(cases[sys.argv[1]], body))
    else:
        print("usage: make_prompt.py <CASE_ID> | --all\ncases: " + ", ".join(cases))
        sys.exit(1)


if __name__ == "__main__":
    main()
