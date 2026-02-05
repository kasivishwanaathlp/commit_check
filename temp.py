errors = []

for key, rule in VALIDATION_RULES.items():
    value = config[key]

    if not rule(value):
        errors.append(f"{key} has invalid value: {value}")

if errors:
    raise ValueError("\n".join(errors))