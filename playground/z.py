data = {
    "tests": [
        {
            "name": "Test 1",
            "subTests": [
                {"name": "var1"},
                {"name": "var2"},
                {"name": "var3"}
            ]
        },
        {
            "name": "Test 2",
            "subTests": [
                {"name": "var4"},
                {"name": "var5"}
            ]
        }
    ]
}

# Parse into a dictionary
test_dict = {}
for main_index, test in enumerate(data["tests"]):
    main_name = test["name"]
    sub_tests = test["subTests"]
    sub_indices = []
    for sub_index, sub_test in enumerate(sub_tests):
        sub_indices.append(sub_index)
    test_dict[main_index] = {
        "main_name": main_name,
        "sub_indices": sub_indices
    }

# Get list of tuples containing main and sub indices
index_tuples = []
for main_index, test_info in test_dict.items():
    main_name = test_info["main_name"]
    sub_indices = test_info["sub_indices"]
    for sub_index in sub_indices:
        index_tuples.append((main_index, sub_index))

print(index_tuples)
