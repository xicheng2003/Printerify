# Frontend Testing Guide

## Running Tests

To run all frontend tests:

```bash
npm run test
```

To run tests in watch mode:

```bash
npm run test:watch
```

To run tests with coverage:

```bash
npm run test:coverage
```

To run tests with UI:

```bash
npm run test:ui
```

## Test Structure

The frontend tests are organized into the following directories:

1. `src/components/` - Tests for Vue components
2. `src/stores/` - Tests for Pinia stores
3. `src/views/` - Tests for view components
4. `src/test/` - Test setup and utilities

## Test Categories

### Unit Tests
- Test individual components and functions
- Mock external dependencies
- Fast execution

### Integration Tests
- Test interactions between components
- Test store integration with components
- Test API service calls

### Component Tests
- Test Vue component rendering
- Test component events and props
- Test component state management

## Writing New Tests

1. Create a test file with the same name as the component/file but with `.test.js` extension
2. Use `describe` blocks to group related tests
3. Use `it` or `test` for individual test cases
4. Use `expect` for assertions
5. Use Vue Test Utils for component testing

## Test Utilities

- `@vue/test-utils` - For mounting and interacting with Vue components
- `vitest` - Test runner and assertion library
- `jsdom` - DOM implementation for testing
- Mocks for API calls and browser APIs

## Authentication Tests

The authentication system includes the following test files:

1. `src/components/AuthForm.test.js` - Tests for the authentication form component
2. `src/components/UserProfile.test.js` - Tests for the user profile component
3. `src/components/UserAuthStatus.test.js` - Tests for the user authentication status component
4. `src/stores/user.test.js` - Tests for the user Pinia store
5. `src/views/AuthView.test.js` - Tests for the authentication view
6. `src/views/ProfileView.test.js` - Tests for the profile view

## Best Practices

1. Keep tests focused and specific
2. Use descriptive test names
3. Test both expected and unexpected inputs
4. Mock external dependencies
5. Use factories for complex test data creation
6. Test edge cases and error conditions
7. Clean up after tests

## Running Specific Tests

To run only authentication tests:

```bash
npm run test:run -- src/components/AuthForm.test.js
npm run test:run -- src/stores/user.test.js
```

To run tests with coverage for authentication system:

```bash
npm run test:coverage -- src/components/AuthForm.test.js src/stores/user.test.js
```