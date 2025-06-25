from functions.get_files_info import get_files_info

def tests():
    output = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(output)
    print("\n")

    output = get_files_info("calculator", "pkg")
    print("Result for current directory:")
    print(output)
    print("\n")

    output = get_files_info("calculator", "/bin")
    print("Result for current directory:")
    print(output)
    print("\n")

    output = get_files_info("calculator", "../")
    print("Result for current directory:")
    print(output)
    print("\n")

if __name__ == "__main__":
    tests()