def convert_str_to_int(price_input):
    price_input = price_input.split('.')
    price_input = ''.join(price_input)
    price_input = int(price_input)
    
    return price_input


def convert_int_to_str(price_input):
    price_input = str(price_input)
    list_price = list(price_input)
    index = -1
    number_of_numbers_after_the_comma = len(list_price)//3 # example: 23.123.456 (123.456 is mean numbers_after_the_comma) ==> 2 loop
    number_of_numbers_before_the_comma = len(list_price)%3 # example: 23.123.456 (23 is mean numbers_before_the_comma) ==> 2 loop
    list_numbers_before_the_comma = [] # example: 23.123.456 (list_numbers_before_the_comma mean [2, 3])
    List_of_number_after_being_split =[] # example: 23.123.456 (desired result List_of_number_after_being_split is [[23], [123], [456]])

    if number_of_numbers_before_the_comma > 0:
        for i in range(number_of_numbers_before_the_comma):
            index += 1
            list_numbers_before_the_comma.append(list_price[index]) # group every number_of_numbers_before_the_comma times numbers into a list
        List_of_number_after_being_split.append(list_numbers_before_the_comma)

    for i in range(number_of_numbers_after_the_comma):
        lambda_list = []
        for i in range(3):
            index += 1
            lambda_list.append(list_price[index]) # group every 3 times numbers into a list
        List_of_number_after_being_split.append(lambda_list)

    for i in range(len(List_of_number_after_being_split)):
        List_of_number_after_being_split[i] = ''.join(List_of_number_after_being_split[i]) # convert [[2, 3], [1, 2, 3], [4, 5, 6]] to [[23], [123], [456]]

    final_list = '.'.join(List_of_number_after_being_split)
    return final_list