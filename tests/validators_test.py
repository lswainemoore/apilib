import decimal
import unittest

import apilib

VC = apilib.ValidationContext

class ValidatorsTest(unittest.TestCase):
    def run_validator_test(self, validator, value, *error_codes):
        self.run_validator_test_for_method(validator, value, None, *error_codes)

    def run_validator_test_for_method(self, validator, value, method, *error_codes):
        return self.run_validator_test_for_context(validator, value,  apilib.ValidationContext(method=method), *error_codes)

    def run_validator_test_for_context(self, validator, value, context, *error_codes):
        error_context = apilib.ErrorContext()
        validator.validate(value, error_context, context)
        errors = error_context.all_errors()
        if error_codes:
            self.assertTrue(errors)
            self.assertEqual(len(error_codes), len(errors))
            for error_code in error_codes:
                self.assertHasErrorCode(error_code, errors)
        else:
            self.assertFalse(errors)
        return errors

    def validate(self, validator, value, error_context):
        validator.validate(value, error_context, None)
        return error_context.all_errors()

    def assertHasErrorCode(self, error_code, errors):
        for error in errors:
            if error.code == error_code:
                return
        self.fail('Error code %s not found' % error_code)

    def test_required_validator(self):
        self.run_validator_test(apilib.Required(), None, apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(), '', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(), u'', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(), [], apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(), {}, apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(), 'abc')
        self.run_validator_test(apilib.Required(), 123)
        self.run_validator_test(apilib.Required(), 0)
        self.run_validator_test(apilib.Required(), 0.0)
        self.run_validator_test(apilib.Required(), u'abc')
        self.run_validator_test(apilib.Required(), ['abc'])
        self.run_validator_test(apilib.Required(), [1, 2, 3])
        self.run_validator_test(apilib.Required(), [None])

        self.run_validator_test(apilib.Required(True), None, apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(True), '', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(True), u'', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(True), [], apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(True), {}, apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test(apilib.Required(True), 'abc')
        self.run_validator_test(apilib.Required(True), 123)
        self.run_validator_test(apilib.Required(True), 0)
        self.run_validator_test(apilib.Required(True), 0.0)
        self.run_validator_test(apilib.Required(True), u'abc')
        self.run_validator_test(apilib.Required(True), ['abc'])
        self.run_validator_test(apilib.Required(True), [1, 2, 3])
        self.run_validator_test(apilib.Required(True), [None])

        self.run_validator_test_for_method(apilib.Required(['insert']), None, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['insert']), '', 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['insert']), [], 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['insert']), {}, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['insert']), None, 'update')
        self.run_validator_test_for_method(apilib.Required(['insert']), [], 'update')
        self.run_validator_test_for_method(apilib.Required(['insert']), {}, 'update')
        self.run_validator_test_for_method(apilib.Required(['insert']), 123, 'insert')
        self.run_validator_test_for_method(apilib.Required(['insert']), 'abc', 'insert')
        self.run_validator_test_for_method(apilib.Required(['insert']), [1], 'insert')

        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), None, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), '', 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), [], 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), {}, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), None, 'update')
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), [], 'update')
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), {}, 'update')
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), 123, 'insert')
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), 'abc', 'insert')
        self.run_validator_test_for_method(apilib.Required(['get', 'insert']), [1], 'insert')

        self.run_validator_test_for_method(apilib.Required('insert'), None, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required('insert'), '', 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required('insert'), [], 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required('insert'), {}, 'insert', apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_method(apilib.Required('insert'), None, 'update')
        self.run_validator_test_for_method(apilib.Required('insert'), [], 'update')
        self.run_validator_test_for_method(apilib.Required('insert'), {}, 'update')
        self.run_validator_test_for_method(apilib.Required('insert'), 123, 'insert')
        self.run_validator_test_for_method(apilib.Required('insert'), 'abc', 'insert')
        self.run_validator_test_for_method(apilib.Required('insert'), [1], 'insert')

        VC = apilib.ValidationContext
        self.run_validator_test_for_context(apilib.Required('insert/ADD'), None, VC(method='insert', operator='ADD'), apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_context(apilib.Required('insert/ADD'), None, VC(method='insert', operator='UPDATE'))
        self.run_validator_test_for_context(apilib.Required('insert/ADD'), None, VC(method='insert', operator=None))
        self.run_validator_test_for_context(apilib.Required('fooservice.insert/ADD'), None, VC(service='fooservice', method='insert', operator='ADD'), apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_context(apilib.Required('fooservice.insert/ADD'), None, VC(service=None, method='insert', operator='ADD'))
        self.run_validator_test_for_context(apilib.Required('fooservice.insert'), None, VC(service='fooservice', method='insert', operator='ADD'), apilib.CommonErrorCodes.REQUIRED)
        self.run_validator_test_for_context(apilib.Required('fooservice.insert'), None, VC(service='fooservice', method='insert'), apilib.CommonErrorCodes.REQUIRED)

        ec = apilib.ErrorContext().extend(field='fstring')
        apilib.Required().validate(None, ec, VC())
        self.assertEqual(1, len(ec.all_errors()))
        self.assertEqual('fstring', ec.all_errors()[0].path)

    def test_readonly_validator(self):
        Readonly = apilib.Readonly

        self.assertEqual(
            None,
            Readonly(True).validate('foo', None, VC(method='insert')))
        self.assertEqual(
            None,
            Readonly('insert').validate('foo', None, VC(method='insert')))
        self.assertEqual(
            None,
            Readonly(['insert']).validate('foo', None, VC(method='insert')))
        self.assertEqual(
            None,
            Readonly(['update', 'insert']).validate('foo', None, VC(method='insert')))
        self.assertEqual(
            None,
            Readonly(['insert']).validate('foo', None, VC(service='service', method='insert')))
        self.assertEqual(
            None,
            Readonly(['insert']).validate('foo', None, VC(service='service', method='insert', operator='ADD')))
        self.assertEqual(
            None,
            Readonly(['insert/ADD']).validate('foo', None, VC(service='service', method='insert', operator='ADD')))
        self.assertEqual(
            None,
            Readonly(['service.insert/ADD']).validate('foo', None, VC(service='service', method='insert', operator='ADD')))

        self.assertEqual(
            'foo',
            Readonly('insert').validate('foo', None, VC(method='update')))
        self.assertEqual(
            'foo',
            Readonly('insert').validate('foo', None, VC(service='service', method='update')))
        self.assertEqual(
            'foo',
            Readonly('insert').validate('foo', None, VC(service='service', method='update', operator='ADD')))
        self.assertEqual(
            'foo',
            Readonly(['service.insert/ADD']).validate('foo', None, VC(service='service', method='insert', operator='UPDATE')))
        self.assertEqual(
            'foo',
            Readonly(['service.insert/ADD']).validate('foo', None, VC(service=None, method='insert', operator='ADD')))

        ec = apilib.ErrorContext().extend(field='fstring')
        apilib.Readonly().validate('foo', ec, VC())
        self.assertFalse(ec.has_errors())

    def test_nonempty_elements_validator(self):
        NonemptyElements = apilib.NonemptyElements

        self.run_validator_test_for_context(NonemptyElements(), None, None)
        self.run_validator_test_for_context(NonemptyElements(), [], None)
        self.run_validator_test_for_context(NonemptyElements(), ['a'], None)
        self.run_validator_test_for_context(NonemptyElements(), [1, 2, 3], None)
        self.run_validator_test_for_context(NonemptyElements(), [0], None)
        self.run_validator_test_for_context(NonemptyElements(), [False], None)
        self.run_validator_test_for_context(NonemptyElements(), [[None]], None)
        self.run_validator_test_for_context(NonemptyElements(), [{'a': None}], None)

        self.run_validator_test_for_context(NonemptyElements(), [None], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)
        self.run_validator_test_for_context(NonemptyElements(), [[]], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)
        self.run_validator_test_for_context(NonemptyElements(), [{}], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)
        self.run_validator_test_for_context(NonemptyElements(), [1, 2, 3, None], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)
        self.run_validator_test_for_context(NonemptyElements(), [1, 2, 3, []], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)
        self.run_validator_test_for_context(NonemptyElements(), [1, 2, 3, {}], None, apilib.CommonErrorCodes.NONEMPTY_ITEM_REQUIRED)

        ec = apilib.ErrorContext().extend(field='lint')
        value = NonemptyElements().validate([1, None], ec, None)
        self.assertIsNone(value)
        self.assertEqual(1, len(ec.all_errors()))
        self.assertEqual('lint[1]', ec.all_errors()[0].path)

        ec = apilib.ErrorContext().extend(field='llist')
        value = NonemptyElements().validate([[1], [2], [3], []], ec, None)
        self.assertIsNone(value)
        self.assertEqual(1, len(ec.all_errors()))
        self.assertEqual('llist[3]', ec.all_errors()[0].path)

    def test_unique_validator(self):
        Unique = apilib.Unique

        self.run_validator_test_for_context(Unique(), None, None)
        self.run_validator_test_for_context(Unique(), [], None)
        self.run_validator_test_for_context(Unique(), ['a'], None)
        self.run_validator_test_for_context(Unique(), [1], None)
        self.run_validator_test_for_context(Unique(), [None], None)
        self.run_validator_test_for_context(Unique(), [False], None)
        self.run_validator_test_for_context(Unique(), [True], None)
        self.run_validator_test_for_context(Unique(), [''], None)
        self.run_validator_test_for_context(Unique(), ['a', 'b'], None)
        self.run_validator_test_for_context(Unique(), ['b', 'a', 'c'], None)
        self.run_validator_test_for_context(Unique(), [3, 2, 1], None)
        self.run_validator_test_for_context(Unique(), [False, True], None)

        errors = self.validate(Unique(), [2, 1, 2], apilib.ErrorContext().extend(field='fint'))
        self.assertEqual(1, len(errors))
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[0].code)
        self.assertEqual('fint[2]', errors[0].path)

        errors = self.validate(Unique(), [9, 8, 7, 6, 7, 8, 9], apilib.ErrorContext().extend(field='fint'))
        self.assertEqual(3, len(errors))
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[0].code)
        self.assertEqual('fint[4]', errors[0].path)
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[1].code)
        self.assertEqual('fint[5]', errors[1].path)
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[2].code)
        self.assertEqual('fint[6]', errors[2].path)

        errors = self.validate(Unique(), ['a', 'a', 'b', 'a'], apilib.ErrorContext().extend(field='fstring'))
        self.assertEqual(2, len(errors))
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[0].code)
        self.assertEqual('fstring[1]', errors[0].path)
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[1].code)
        self.assertEqual('fstring[3]', errors[1].path)

        errors = self.validate(Unique(), ['foo', 'a', '', ''], apilib.ErrorContext().extend(field='fstring'))
        self.assertEqual(1, len(errors))
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[0].code)
        self.assertEqual('fstring[3]', errors[0].path)

        errors = self.validate(Unique(), ['foo', 'a', None, None], apilib.ErrorContext().extend(field='fstring'))
        self.assertEqual(1, len(errors))
        self.assertEqual(apilib.CommonErrorCodes.DUPLICATE_VALUE, errors[0].code)
        self.assertEqual('fstring[3]', errors[0].path)


if __name__ == '__main__':
    unittest.main()
