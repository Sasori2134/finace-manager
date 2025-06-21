def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validation_dictionary(field,word):
    match field:
        case "CharField":
            return {
                'invalid' : f'You Have To Include Valid {word}',
                'blank' : f'You Have To Include Valid {word}',
                'min_length' : f'{word} Has To Be More Than One Character',
                'max_length' : f"{word} Can't Be More Than Fifty Characters Long"
            }
        case "DecimalField":
            return {
            'invalid' : f'You Have To Include Valid {word}',
            'blank' : f'You Have To Include {word}',
            'min_value' : f'{word} Has To Be More Than 0',
            'max_digits' : f"{word} You Entered Is Not Valid (It's Too Big Of A Number)"
            }
    