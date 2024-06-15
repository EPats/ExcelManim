import re





if __name__ == '__main__':
    # Example usage
    formula = '=IF(A1=1,"Yes",IF(B2<AVERAGE(G8:J10),"No",--TRUE), ,,TEST3(TEST7(TEST8(),)),TEST5(,))'
    parsed_tokens = parse_excel_function(formula)
    for token in parsed_tokens:
        print(token)