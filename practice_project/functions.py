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
            'invalid' : 'You Have To Include Valid Budget',
            'blank' : 'You Have To Include Budget',
            'min_value' : 'Budget Has To Be More Than 0',
            'max_digits' : "Budget You Entered Is Not Valid (It's Too Big Of A Number)"
            }
    