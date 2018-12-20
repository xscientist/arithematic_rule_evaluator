from pythonds.basic.stack import Stack

input_data = {
    "unique_id_1": 4,
    "unique_id_2": 6,
    "unique_id_3": 3,
    "value_1": 13,
    "parameterSequence": ["unique_id_1", "unique_id_2", "unique_id_3", "value_1"],
    "ruleId": "rule_00"
}

defined_rules = {
    "rule_00": {
        "ruleInfo": "0 + 1 + 2 - 3",
        "ruleResult": "equals",
        "ruleSequenceLength": 4
    },
    "rule_01": {
        "ruleInfo": "A + B + C - D",
        "ruleResult": "greater",
        "ruleSequenceLength": 4
    },
    "rule_02": {
        "ruleInfo": "A + B + C - D",
        "ruleResult": "lesser",
        "ruleSequenceLength": 4
    },
}


def parameters_to_values_in_postfix(postfix_expression, input_parameter):
    updated_expression = list()
    param_mapper = input_parameter["parameterSequence"]
    for each_expression in postfix_expression:
        try:
            value = int(each_expression)
            updated_expression.append(input_parameter[param_mapper[value]])
        except Exception as e:
            updated_expression.append(each_expression)
    return updated_expression


def rule_to_postfix(infix_rule):
    prec = dict()
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    op_stack = Stack()
    postfix_list = []
    token_list = infix_rule.split()

    for token in token_list:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while (not op_stack.isEmpty()) and \
                    (prec[op_stack.peek()] >= prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.isEmpty():
        postfix_list.append(op_stack.pop())
    return postfix_list


def evaluate_postfix_expression(postfix_expression, expected_result):
    result = None
    result_flag = False
    for i in range(len(postfix_expression)):
        if postfix_expression[i] == "/":
            if result is None:
                result = postfix_expression[i - 1] / postfix_expression[i - 2]
            else:
                result = postfix_expression[i - 1] / result
        elif postfix_expression[i] == "*":
            if result is None:
                result = postfix_expression[i - 1] * postfix_expression[i - 2]
            else:
                result = postfix_expression[i - 1] * result
        elif postfix_expression[i] == "-":
            if result is None:
                result = postfix_expression[i - 1] - postfix_expression[i - 2]
            else:
                result = postfix_expression[i - 1] - result
        elif postfix_expression[i] == "+":
            if result is None:
                result = postfix_expression[i - 1] + postfix_expression[i - 2]
            else:
                result = postfix_expression[i - 1] + result
    if result == 0 and expected_result == "equals":
        result_flag = True
    elif result > 0 and expected_result == "greater":
        result_flag = True
    elif result < 0 and expected_result == "lesser":
        result_flag = True
    elif result >= 0 and expected_result == "gequals":
        result_flag = True
    elif result <= 0 and expected_result == "lequals":
        result_flag = True
    return result_flag


def get_postfix_notation(rule_data, verify_data):
    try:
        rule_param_length = rule_data[verify_data["ruleId"]]["ruleSequenceLength"]
        input_param = verify_data["parameterSequence"]
        if rule_param_length == len(input_param):
            rule = rule_data[verify_data["ruleId"]]["ruleInfo"]
            expected_result = rule_data[verify_data["ruleId"]]["ruleResult"]
            postfix_expression = rule_to_postfix(rule)
            print("POSTFIX-->", postfix_expression)
            postfix_expression = parameters_to_values_in_postfix(postfix_expression=postfix_expression,
                                                                 input_parameter=verify_data)
            print("UPDATED-->", postfix_expression)
            result_data = evaluate_postfix_expression(postfix_expression=postfix_expression,
                                                      expected_result=expected_result)
            print(result_data)
    except Exception as e:
        print("Rule not found :" + str(e))
        raise Exception


if __name__ == '__main__':
    get_postfix_notation(verify_data=input_data, rule_data=defined_rules)
