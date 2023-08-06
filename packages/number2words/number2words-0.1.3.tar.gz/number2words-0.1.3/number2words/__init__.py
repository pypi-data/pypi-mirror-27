# Number2Words

class Number2Words(object):

    def __init__(self, number):
        """Initialize words dictionary"""

        self.words_dict = {
            1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
            8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
            14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen',
            18: 'eighteen', 19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
            50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninty'
        }

        self.power_list = ['thousand', 'lakh', 'crore']

        self.number = number

    def convert(self):

        if not int(self.number):
            return None

        self._validate_number(int(self.number))

        return self._convert_to_words(self.number).title()

    @staticmethod
    def _validate_number(number):

        assert str(number).isdigit()

        # Only works till 999999999
        if number > 999999999 or number < 0:
            raise AssertionError('Out Of range')

    def _convert_to_words(self, number):

        msbs, hundreds, tens = self._group_numbers(number)

        words_list = self._group_to_numbers(msbs, hundreds, tens)

        return ' '.join(words_list) + ' only'

    @staticmethod
    def _group_numbers(number):

        str_number = str(number)

        hundreds, tens = str_number[-3:-2], str_number[-2:]

        msbs_temp = list(str_number[:-3])

        msbs = []

        str_temp = ''

        for num in msbs_temp[::-1]:

            str_temp = '%s%s' % (num, str_temp)

            if len(str_temp) == 2:

                msbs.insert(0, str_temp)

                str_temp = ''

        if str_temp:

            msbs.insert(0, str_temp)

        return msbs, hundreds, tens

    def _group_to_numbers(self, msbs, hundreds, tens):

        word_list = []

        if tens:

            tens = int(tens)

            tens_in_words = self._formulate_double_digit_words(tens)

            if tens_in_words:
                word_list.insert(0, tens_in_words)

        if hundreds:

            hundreds = int(hundreds)

            if not hundreds:

                # Might be zero. Ignore.
                pass
            else:

                hundreds_in_words = '%s hundred' % self.words_dict[hundreds]

                word_list.insert(0, hundreds_in_words)

        if msbs:

            msbs.reverse()

            for idx, item in enumerate(msbs):

                in_words = self._formulate_double_digit_words(int(item))

                if in_words:

                    in_words_with_power = '%s %s' % (in_words, self.power_list[idx])

                    word_list.insert(0, in_words_with_power)

        return word_list

    def _formulate_double_digit_words(self, double_digits):

        if not int(double_digits):

            # Might be zero. Ignore.
            return None

        elif (int(double_digits)) in self.words_dict:

            # Global dict has the key for this number
            tens_in_words = self.words_dict[int(double_digits)]
            return tens_in_words

        else:

            str_double_digits = str(double_digits)

            tens, units = int(str_double_digits[0]) * 10, int(str_double_digits[1])

            tens_units_in_words = '%s %s' % (self.words_dict[tens], self.words_dict[units])

            return tens_units_in_words

