from django.utils import timezone

def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_date():
    return timezone.now().date()

def validation_dictionary(field,word,min_length=None):
    match field:
        case "CharField":
            if min_length:
                return {
                    'invalid' : f'You Have To Include Valid {word}',
                    'blank' : f'You Have To Include Valid {word}',
                    'min_length' : f'{word} Has To Be More Than {min_length-1} Character',
                    'max_length' : f"{word} Can't Be More Than Fifty Characters Long"
                }
            else:
                return {
                    'invalid' : f'You Have To Include Valid {word}',
                    'blank' : f'You Have To Include Valid {word}',
                    'max_length' : f"{word} Can't Be More Than Fifty Characters Long"
                }
        case "DecimalField":
            return {
            'invalid' : f'You Have To Include Valid {word}',
            'blank' : f'You Have To Include {word}',
            'min_value' : f'{word} Has To Be More Than 0',
            'max_digits' : f"{word} You Entered Is Not Valid (It's Too Big Of A Number)"
            }

    