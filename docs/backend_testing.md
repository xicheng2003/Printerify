# Backend Testing Guide

## Running Tests

To run all backend tests:

```bash
python manage.py test api.tests
```

To run a specific test file:

```bash
python manage.py test api.tests.test_models
```

To run a specific test case:

```bash
python manage.py test api.tests.test_models.OrderModelTest
```

## Test Structure

The backend tests are organized into the following files:

1. `test_models.py` - Tests for Django models
2. `test_views.py` - Tests for API views
3. `test_serializers.py` - Tests for serializers
4. `test_pricing.py` - Tests for pricing service

## Test Categories

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Fast execution

### Integration Tests
- Test interactions between components
- Test API endpoints
- Test database operations

### Functional Tests
- Test complete user workflows
- Test business logic

## Writing New Tests

1. Choose the appropriate test file based on what you're testing
2. Create a new test class that inherits from `django.test.TestCase`
3. Use descriptive method names prefixed with `test_`
4. Include both positive and negative test cases
5. Use assertions to verify expected behavior

## Test Data

- Use `setUp()` method to create common test data
- Use `SimpleUploadedFile` for testing file uploads
- Use `reverse()` to generate URLs for testing

## Best Practices

1. Keep tests independent and isolated
2. Use meaningful test names
3. Test both expected and unexpected inputs
4. Clean up test data after tests
5. Mock external services and dependencies
6. Use factories for complex test data creation